from __future__ import annotations

import random
import threading
import time


class ReadersWritersMonitor:

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

        self.active_readers = 0
        self.active_writers = 0
        self.waiting_writers = 0

    def start_read(self, reader_id: int) -> None:
        with self.condition:
            print(f"Reader {reader_id} is waiting to read")
            while self.active_writers > 0:
                self.condition.wait()
            self.active_readers += 1
            print(f"Reader {reader_id} starts reading. Active readers = {self.active_readers}")

    def end_read(self, reader_id: int) -> None:
        with self.condition:
            self.active_readers -= 1
            print(f"Reader {reader_id} stops reading. Active readers = {self.active_readers}")
            if self.active_readers == 0:
                self.condition.notify_all()

    def start_write(self, writer_id: int) -> None:
        with self.condition:
           print(f"Writer {writer_id} is waiting to write")
           self.waiting_writers += 1
           while self.active_readers > 0 or self.active_writers > 0:
                self.condition.wait()

    def end_write(self, writer_id: int) -> None:
        with self.condition:
            self.active_writers -= 1
            print(f"Writer {writer_id} stops writing")
            self.condition.notify_all()

# Donot Change this
class Reader(threading.Thread):
    def __init__(self, reader_id: int, monitor: ReadersWritersMonitor, rounds: int = 3) -> None:
        super().__init__()
        self.reader_id = reader_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.1, 0.7))  # stagger thread arrival

            print(f"Reader {self.reader_id} wants to read")
            self.monitor.start_read(self.reader_id)

            print(f"Reader {self.reader_id} is READING")
            time.sleep(random.uniform(0.3, 0.8))  # simulate reading

            self.monitor.end_read(self.reader_id)
            print(f"Reader {self.reader_id} finished reading")

# Donot Change this
class Writer(threading.Thread):
    def __init__(self, writer_id: int, monitor: ReadersWritersMonitor, rounds: int = 2) -> None:
        super().__init__()
        self.writer_id = writer_id
        self.monitor = monitor
        self.rounds = rounds

    def run(self) -> None:
        for _ in range(self.rounds):
            time.sleep(random.uniform(0.2, 0.9))  # stagger thread arrival

            print(f"Writer {self.writer_id} wants to write")
            self.monitor.start_write(self.writer_id)

            print(f"Writer {self.writer_id} is WRITING")
            time.sleep(random.uniform(0.4, 0.9))  # simulate writing

            self.monitor.end_write(self.writer_id)
            print(f"Writer {self.writer_id} finished writing")


def main() -> None:
   
    random.seed(42)

    monitor = ReadersWritersMonitor()
    readers = [Reader(reader_id=i, monitor=monitor) for i in range(1, 4)]
    writers = [Writer(writer_id=i, monitor=monitor) for i in range(1, 3)]

    readers = [
        Reader(reader_id=1, monitor=monitor)
    ]
    
    #TODO: Create at least 2 writer threads.
    writers = [
        Writer(writer_id=1, monitor=monitor)
    ]

    all_threads = readers + writers
    
    print("-----Starting Simulation-----")
    for t in all_threats:
        t.start（）
    for t in all_threats:
        t.join（）


if __name__ == "__main__":
    main()
