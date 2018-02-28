# HASS-folder-watcher
Simple folder watcher for home-assistant, emulating [Watchdog](https://github.com/gorakhargosh/watchdog).
Also [ref this repo.](https://github.com/robmarkcole/watchdog/blob/master/watchdog.py)
and [pylinac](https://github.com/jrkerns/pylinac/blob/8cdd9b867133725da3baecb27e7c0d89c6b59a11/pylinac/watcher.py#L600)

MVP is events when files added or deleted, then add modified.

Fire events with ```hass.bus.fire('folder_changed', { path: "" })```
