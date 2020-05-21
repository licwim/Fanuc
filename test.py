from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class Handler(FileSystemEventHandler):

	def on_created(self, event):
		print (event)

	def on_deleted(self, event):
		print (event)

	def on_modified(self, event):
		print (event)

	def on_moved(self, event):
		print (event)

observer = Observer()
observer.schedule(Handler(), path='.', recursive=False)
observer.start()

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	observer.stop()
observer.join()