# ServerTee.py

import sys
import datetime
from threading import Lock
from queue import Queue, Empty

class ServerTee:
    """
    A thread-safe logger that duplicates stdout to both console and file,
    timestamps all output lines, and supports real-time subscriber streaming.
    """

    def __init__(self, filename, mode='a'):
        self.file = open(filename, mode, buffering=1)  # line-buffered
        self.stdout = sys.stdout
        self.lock = Lock()
        self.subscribers = []
        self.buffer = ""  # buffer for partial lines
        sys.stdout = self  # redirect global stdout

    def write(self, message):
        with self.lock:
            self.buffer += message
            while '\n' in self.buffer:
                line, self.buffer = self.buffer.split('\n', 1)
                # Skip completely empty lines
                if not line.strip():
                    continue
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message_with_timestamp = f"{timestamp} - {line}\n"

                # Write to original stdout
                self.stdout.write(message_with_timestamp)
                self.stdout.flush()

                # Write to log file
                self.file.write(message_with_timestamp)
                self.file.flush()

                # Notify subscribers
                self.notify_subscribers(message_with_timestamp)

    def flush(self):
        with self.lock:
            if self.buffer:
                line = self.buffer.strip()
                if line:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    message_with_timestamp = f"{timestamp} - {line}\n"
                    self.stdout.write(message_with_timestamp)
                    self.file.write(message_with_timestamp)
                    self.notify_subscribers(message_with_timestamp)
                self.buffer = ""
            self.stdout.flush()
            self.file.flush()

    def close(self):
        with self.lock:
            self.flush()
            sys.stdout = self.stdout  # restore original stdout
            self.file.close()

    # -------------------
    # Subscriber methods
    # -------------------

    def notify_subscribers(self, message):
        for subscriber in list(self.subscribers):  # copy to avoid mutation during iteration
            try:
                subscriber.put_nowait(message)
            except Exception:
                pass  # subscriber queue full or closed

    def subscribe(self):
        q = Queue()
        with self.lock:
            self.subscribers.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.subscribers:
                self.subscribers.remove(q)

    def stream_to_frontend(self, stop_event=None):
        """
        Yields log lines to a frontend until stop_event is set (if provided).
        This can be used in a Flask or FastAPI streaming endpoint.
        """
        q = self.subscribe()
        try:
            while True:
                if stop_event and stop_event.is_set():
                    break
                try:
                    message = q.get(timeout=1)
                    yield message
                except Empty:
                    continue
        finally:
            self.unsubscribe(q)
