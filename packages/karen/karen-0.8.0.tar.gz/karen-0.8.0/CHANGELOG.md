# Changelog

All notable changes to this project will be documented in this file.

## [0.8.0] - TBD

### Modified

- Corrected bug in startup for "restart" routine to separate brain/container
- Added support for additional per-image headers in TCPStreamingClient for motion JPEG images
- Collapsed devices into primary repository
  - karen.devices - For all generic input/output devices
  - karen.panels - For all Qt forms as "panels"
- Redesigned configuration file for startup
- Failsafe startup for invalid modules

## [0.7.1] - 2021-09-19

### Added

- Build method shell scripts
- PyPi build method shell scripts
- UPNP server and client libraries for brain auto-detection
- API key-based authentication for communication between devices/brain
- User/Password authentication for web portal
- Remote upgrade capability for containers and devices
- Ability to execute karen as a module with "python -m karen.run"

### Modified

- Documentation on setting up virtual environment for installation
- Documentation on Raspberry Pi issues with FANN2 library and Python bindings
- Download Modules function within karen base for easier calling
- Fix for missing self.thread object in container class

## [0.7.0] - 2021-08-08 

This is a major change and is not backwards compatible in our quest to reach 1.0 status.

### Added

- Generic class for containers (Devices/Brain)
- Base class for Device inheritance (DeviceTemplate)
- getIPAddress() for identifying IP of network interfaces
- Base support for PyQt5 forms via karen-panel

### Modified

- Separated features into separate packages
- Rewritten brain/container communications using "accepts"
- Moved Streaming Client into karen.shared
- Defaulting containers to interface IP rather than just localhost
- Documentation updated to reflect new patterns

### Removed

- Separated features into separate packages
- See karen-brain, karen-device, karen-watcher, karen-listener, karen-speaker

## [0.6.0] - 2021-07-02

### Added

- Added Watcher device
- Trainer for watcher device using haarcascade classifiers
- Basic Configuration for Video + Audio (basic_config_video.json)
- Handlers for capturing IMAGE_INPUT
- Context object for handlers and devices

### Modified

- karen.start() method to support "video" option
- Fixed eval issues in startup
- Updated Raspberry Pi documentation
- Improved device management via control panel

## [0.5.5] - 2021-06-19

### Added

- Download_model support to auto-detect deepspeech version and location
- Simplified startup logic with default configuration

### Modified 

- Install process for pypi (validated on Raspberry Pi)
- Docs now reflect simplified startup and relocated library paths
- Minimized dependencies/requirements list


## [0.5.4] - 2021-06-16

### Added

- Callback handlers for brain for extensible support
- Callback support for data capture and output devices for extensible support
- Listener daemon supports user-supplied callbacks for STT delivery
- Dynamic device loader allow for expansion of new input/output devices
- Python module setup and egg generation
- Unit Tests for listener
- Added mobile support for web gui
- Added configuration-based startup

### Changed

- Devices are now containerized in one TCP daemon
- Device and TCP daemon interactions now operate through callbacks
- Internal libraries have all changed and are not backwards compatible
- Moved location of webgui files
- Updated look-and-feel of web gui

### Removed

- Unnecessary setup tasks


## [0.4.1] - 2020-12-26

### Added

- Multiple daemons 
- Basic support for microphone devices (via mozilla.deepspeech)
- Basic support for camera devices (via opencv2)
- Web console

### Changed

- Startup routines

### Removed

- Unnecessary setup tasks
