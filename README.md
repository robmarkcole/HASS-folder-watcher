# HASS-folder-watcher
Home-Assistant component which adds [Watchdog](https://github.com/gorakhargosh/watchdog) file watching. Events are fired on the creation/modification/deletion of files.

Place the custom_components folder in your configuration directory (or add its contents to an existing custom_components folder).

Add to your configuration.yaml:
```yaml
watchdog_file_changed:
  folder: /images
```
Note that you may need to add the folder to your `whitelist_external_dirs`

UPDATE: Merged in HA 0.67 https://www.home-assistant.io/blog/2018/04/13/release-67/
