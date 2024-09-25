import pyefsw
import signal
import os
import sys
from time import sleep
from PIL import Image, UnidentifiedImageError
import pillow_avif

STOP = False
# Directories to monitor for webp files
WEBP_DIRS = ("/home/laptop/Downloads", "/home/laptop/Pictures")


class ImageFileListener(pyefsw.FileWatchListener):
	def handleFileAction(self, watchID, directory, filename, action, oldFilename):
		fpath = os.path.join(directory, filename)
		def saveToPng():
			pngpath = os.path.join(directory, os.path.splitext(filename)[0] + ".png")
			try:
				img = Image.open(fpath)
				img = img.convert("RGBA")
				img.save(pngpath, "png")
			except FileNotFoundError:
				print("Could not find file: " + fpath, file=sys.stderr)
			except UnidentifiedImageError:
				print("PIL failed to read file: " + fpath, file=sys.stderr)
			except OSError:
				print("Could not save PNG image at: " + pngpath, file=sys.stderr)

		if action == pyefsw.Action.Add or action == pyefsw.Action.Modified or action == pyefsw.Action.Moved:
			# check if the file is webp or avif
			if filename.endswith(".webp") or filename.endswith("avif"):

				## Check the size of the file to avoid processing empty files (e.g. when the file has just started downloading)
				if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
					print(f"Found image: {filename} | Directory: {directory} | Action {action.name}")
					saveToPng()


fileWatcher = pyefsw.FileWatcher(useGenericFileWatcher=False) # Use platform-specific way to monitor file changes
listener = ImageFileListener()
# Store all watch ids
watch_ids = [None]*len(WEBP_DIRS)

for i in range(len(WEBP_DIRS)):
	dir = WEBP_DIRS[i]
	watchID = fileWatcher.addWatch(dir, listener, recursive=False) # Track only changes to top-level domain of each dir.
	watch_ids[i] = watchID

fileWatcher.watch() # Watch for changes
print(f"Watching for webp, avif files in directories: {str(WEBP_DIRS)}")

def exit_gracefully():
	global STOP, watch_ids, fileWatcher, listener #global watch_ids shouldn't be needed but it doesn't work otherwise lol
	for watchID in watch_ids:
		if watchID is not None:
			fileWatcher.removeWatch(watchID)
	del listener, fileWatcher # explicitly delete C++ objects
	STOP = True

def sigterm_handler(signum, frame):
	print("called sigterm_handler")
	exit_gracefully()

# Handle `kill -SIGTERM` gracefully
signal.signal(signal.SIGTERM, sigterm_handler)

try:
	while(not STOP):
		sleep(3) # sleep for 3 seconds
except KeyboardInterrupt: # Handle `kill -SIGINT` and `CTRL+C` gracefully
	exit_gracefully()
finally:
	print("Stopped watching.")
