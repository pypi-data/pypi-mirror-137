from __future__ import annotations

import asyncio
import errno
import os
import signal
import socket
import sys
import types
import typing

from .channel import SignalChannel

__all__ = ('SignalNotifier', 'create_notifier')

WIN32 = sys.platform == 'win32'
if WIN32:
    WSAENOTSOCK: int = getattr(errno, 'WSAENOTSOCK')


class SignalNotifier:
    def __init__(self, *, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self._channels: typing.List[SignalChannel] = []

        self._task: typing.Optional[asyncio.Task[None]] = None

        self._csock, self._ssock = socket.socketpair()
        self._csock.setblocking(False)
        self._ssock.setblocking(False)

        self._wakeup_fd = -1
        self._wakeup_sock: typing.Optional[socket.socket] = None

    def open_channel(self) -> SignalChannel:
        channel = SignalChannel()
        self._channels.append(channel)
        return channel

    def notify(self, signum: signal.Signals) -> None:
        if signum not in signal.valid_signals():
            raise TypeError(f'Invalid signal: {signum}')

        for channel in self._channels:
            channel.send(signum)

    def signal_handler(self, signum: int, fame: typing.Optional[types.FrameType]) -> None:
        return None

    def _wakeup_write(self, data: bytes) -> None:
        try:
            os.write(self._wakeup_fd, data)
        except OSError as exc:
            if (
                exc.errno != errno.EWOULDBLOCK
                and exc.errno != errno.EAGAIN
            ):
                message = 'Exception ignored when trying to write to the signal wakeup fd'
                self.loop.call_exception_handler({'message': message, 'exception': exc})

    def _wakeup_send(self, data: bytes) -> None:
        assert self._wakeup_sock is not None

        try:
            self._wakeup_sock.send(data)
        except OSError as exc:
            if (
                exc.errno != errno.EWOULDBLOCK
                and exc.errno != errno.EAGAIN
            ):
                message = 'Exception ignored when trying to send to the signal wakeup fd'
                self.loop.call_exception_handler({'message': message, 'exception': exc})

    async def _read_loop(self) -> None:
        while True:
            signums = await self.loop.sock_recv(self._csock, 4096)

            if self._wakeup_fd != -1:
                self._wakeup_write(signums)
            elif self._wakeup_sock is not None:
                self._wakeup_send(signums)

            for signum in signums:
                try:
                    self.notify(signal.Signals(signum))
                except ValueError as exc:
                    message = 'Notifier received invalid signal in read loop'
                    self.loop.call_exception_handler({'message': message, 'exception': exc})

    def _set_wakeup_fd(self, wakeup_fd: int) -> None:
        try:
            self._wakeup_sock = socket.socket(fileno=wakeup_fd)
            self._wakeup_sock.setblocking(False)
        except OSError as exc:
            if exc.errno != WSAENOTSOCK:
                raise

            self._wakeup_fd = wakeup_fd

    def start_notifying(self) -> None:
        for signum in signal.valid_signals():
            try:
                signal.signal(signum, self.signal_handler)
            except OSError as exc:
                if exc.errno != errno.EINVAL:
                    raise

        wakeup_fd = signal.set_wakeup_fd(self._ssock.fileno())
        if wakeup_fd != -1:
            if WIN32:
                self._set_wakeup_fd(wakeup_fd)
            else:
                self._wakeup_fd = wakeup_fd

        self._task = self.loop.create_task(self._read_loop())

    def stop_notifying(self) -> None:
        for signum in signal.valid_signals():
            if signum == signal.SIGINT:
                default = signal.default_int_handler
            else:
                default = signal.SIG_DFL

            try:
                signal.signal(signum, default)
            except OSError as exc:
                if exc.errno != errno.EINVAL:
                    raise

        if self._wakeup_sock is not None:
            signal.set_wakeup_fd(self._wakeup_sock.detach())
        else:
            signal.set_wakeup_fd(self._wakeup_fd)

        self._wakeup_fd = -1
        self._wakeup_sock = None

        if self._task is not None:
            self._task.cancel()


def create_notifier() -> SignalNotifier:
    return SignalNotifier(loop=asyncio.get_running_loop())
