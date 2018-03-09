"""
Component for monitoring activity on a folder.
"""
import os
import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.const import EVENT_HOMEASSISTANT_START
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['watchdog==0.8.3']
_LOGGER = logging.getLogger(__name__)

CONF_FOLDERS = 'folders'
CONF_FILTERS = 'filters'
DEFAULT_FILTER = '*'
DOMAIN = "folder_watcher"
EVENT_TYPE = "event_type"
FILE = 'file'
FOLDER = 'folder'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_FOLDERS):
            vol.All(cv.ensure_list, [cv.isdir]),
        vol.Optional(CONF_FILTERS, default=[DEFAULT_FILTER]):
            vol.All(cv.ensure_list, [cv.string]),
        }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the folder watcher."""
    conf = config[DOMAIN]
    paths = conf[CONF_FOLDERS]
    patterns = conf[CONF_FILTERS]

    def run_setup(event):
        for path in paths:
            if not hass.config.is_allowed_path(path):
                _LOGGER.error("folder %s is not valid or allowed", path)
                return False
            else:
                Watcher(path, patterns, hass)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, run_setup)
    return True


def create_event_handler(patterns, hass):
    from watchdog.events import PatternMatchingEventHandler

    class EventHandler(PatternMatchingEventHandler):
        """Class for handling Watcher events."""

        def __init__(self, patterns, hass):
            super().__init__(patterns)
            self.hass = hass

        def process(self, event):
            """On Watcher event, fire HA event."""
            if not event.is_directory:
                file_name = os.path.split(event.src_path)[1]
                folder_name = os.path.split(event.src_path)[0]
                self.hass.bus.fire(
                    DOMAIN, {
                        EVENT_TYPE: event.event_type,
                        FILE: file_name,
                        FOLDER: folder_name
                        })

        def on_modified(self, event):
            self.process(event)

        def on_moved(self, event):
            self.process(event)

        def on_created(self, event):
            self.process(event)

        def on_deleted(self, event):
            self.process(event)

    return EventHandler(patterns, hass)


class Watcher(Entity):
    """Class for starting Watchdog."""
    def __init__(self, path, patterns, hass):
        from watchdog.observers import Observer
        self._observer = Observer()
        self._observer.schedule(
            create_event_handler(patterns, hass),
            path,
            recursive=True)
        self._observer.start()