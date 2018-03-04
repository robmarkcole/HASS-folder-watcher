"""
Sensor for monitoring activity on a folder.
"""
#import datetime
#from datetime import timedelta
import logging
import os
import voluptuous as vol
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_PATH = 'folder'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PATH): cv.isdir,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the folder watcher."""
    path = config.get(CONF_PATH)
    if not hass.config.is_allowed_path(path):
        _LOGGER.error("folder %s is not valid or allowed", path)
    else:
        folder_watcher = Watcher(path)
        add_devices([folder_watcher], True)


class Watcher(Entity):
    """Class for watching a folder, state recorded in a dict."""

    ICON = 'mdi:folder'

    def __init__(self, path):
        self._path = os.path.join(path, '')  # Ass trailing /
        event = WatchdogEvent()  # Init the data object
        self._event = event
        self._observer = Observer()
        self._observer.schedule(MyHandler(event), self._path, recursive=True)
        self._observer.start()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "folder_watcher"

    @property
    def state(self):
        """Return the state of the sensor."""
        data = self._event.data
        event_str = data["event"] + " : " + data["file"]
        return event_str

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        attr = {
            'path': self._path
            }
        return attr


class WatchdogEvent():
    """Class representing the last event."""
    def __init__(self):
        data = {
            "time": "no_data",
            "event": "no_data",
            "full_path": "no_data",
            "file": "no_data"
            }
        self._data = data

    def update(self, data):
        """Update with recent data."""
        self._data = data

    @property
    def data(self):
        """Return the last event."""
        return self._data


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.txt", "*.py", "*.md", "*.jpg", "*.png"]

    def __init__(self, event_data):
        super().__init__()
        self._event_data = event_data

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        data = {
            "time": time.strftime("%Y-%m-%d %H:%M"),
            "event": event.event_type,
            "full_path": event.src_path,
            "file": os.path.split(event.src_path)[-1]
        }
        # print(json.dumps(data))
        _LOGGER.warning("WATCHDOG_CALLED with {} {}".format(
            data["event"], data["file"]))
        self._event_data.update(data)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)
