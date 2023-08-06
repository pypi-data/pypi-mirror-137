import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
class ModificationEventHandler(PatternMatchingEventHandler):
    def __init__(self,path,handler):
        super(ModificationEventHandler, self).__init__(patterns=[path])
        self.handler=handler
    def on_modified(self, event):
        self.handler()
def watch_file_change(path,handler):
    event_handler = ModificationEventHandler(path,handler)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(path), recursive=True)
    observer.start()
