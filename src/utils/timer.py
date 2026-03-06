import pygame
from typing import Callable, Any


class Timer:
    def __init__(
        self,
        duration: int,
        callback: Callable[[], Any] | None = None,
        loop: bool = False,
        autostart: bool = True,
    ):
        self.duration = duration
        self.callback = callback
        self.loop = loop

        self._elapsed = 0
        self._running = autostart

    def update(self, dt: int) -> None:
        if not self._running:
            return

        self._elapsed += dt

        if self._elapsed >= self.duration:
            if self.callback:
                self.callback()

            if self.loop:
                self._elapsed = self._elapsed % self.duration
            else:
                self._running = False
                self._elapsed = self.duration

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def reset(self) -> None:
        self._elapsed = 0
        self._running = True

    @property
    def running(self) -> bool:
        return self._running

    @property
    def progress(self) -> float:
        if self.duration == 0:
            return 1.0
        return min(1.0, self._elapsed / self.duration)

    @property
    def remaining(self) -> int:
        return max(0, self.duration - self._elapsed)


class TimerManager:
    def __init__(self):
        self._timers: list[Timer] = []

    def add(self, timer: Timer) -> Timer:
        self._timers.append(timer)
        return timer

    def create(
        self,
        duration: int,
        callback: Callable[[], Any] | None = None,
        loop: bool = False,
        autostart: bool = True,
    ) -> Timer:
        timer = Timer(duration, callback, loop, autostart)
        self._timers.append(timer)
        return timer

    def update(self, dt: int) -> None:
        for timer in self._timers:
            timer.update(dt)

    def clear(self) -> None:
        self._timers.clear()

    def remove(self, timer: Timer) -> None:
        if timer in self._timers:
            self._timers.remove(timer)
