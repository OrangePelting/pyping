from PyWatcher import *

load_watchers()
for k, v in get_watchers_and_states().items():
    toggle_watcher_state(v["watcher"])
