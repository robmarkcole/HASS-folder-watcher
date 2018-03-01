# HASS-folder-watcher
Simple folder watcher for home-assistant, emulating [Watchdog](https://github.com/gorakhargosh/watchdog). Place the custom_components folder in your configuration directory (or add its contents to an existing custom_components folder).

Fires an event on a file addition, modification or deletion. The state is the sensor is the last event.
Add to your configuration.yaml:
```yaml
sensor:
  - platform: folder_watcher
    folder: /Users/robincole/.homeassistant/images
```
