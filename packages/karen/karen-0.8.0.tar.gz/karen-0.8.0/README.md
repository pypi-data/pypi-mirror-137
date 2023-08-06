# Project Karen &middot; [![GitHub license](https://img.shields.io/github/license/lnxusr1/karen)](https://github.com/lnxusr1/karen/blob/master/LICENSE) ![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg) ![Read the Docs](https://img.shields.io/readthedocs/project-karen) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/lnxusr1/karen)

This project is dedicated to building a "Synthetic Human" which is called Karen (for now) for which we have assigned the female gender pronoun of "she". She has visual face recognition ([opencv/opencv](https://github.com/opencv/opencv)), speech transcription ([mozilla/deepspeech](https://github.com/mozilla/DeepSpeech)), and speech synthesis ([festival](http://www.cstr.ed.ac.uk/projects/festival/)).  Karen is written in Python and is targeted primarily at the single board computer (SBC) platforms like the [Raspberry Pi](https://www.raspberrypi.org/).

Visit our main site: [https://projectkaren.ai/](https://projectkaren.ai/)

Read the docs: [https://docs.projectkaren.ai/](https://docs.projectkaren.ai/)

## Karen's Architecture

Karen's architecture is divided into two main components:  Containers and Devices.  The containers focus on communication between other containers and devices are designed to control input and output operations.  The most important container is the Brain which is a special type of container as it collects data and provides the skill engine for reacting to inputs.  While a Brain does support all the methods of a normal container it is recommended to create a separate container to store all your devices.

__Python Module Overview__

| Class/Object                      | Description                      | TCP Port |
| :-------------------------------- | :------------------------------- | :------: |
| karen.containers.Brain            | Main service for processing I/O. | 8080     |
| karen.containers.DeviceContainer  | Secondary service for devices.   | 8081     |

__Python Device Module Overview__

| Class/Object            | Description                                                 |
| :---------------------- | :---------------------------------------------------------- |
| karen.devices.Speaker   | Audio output device for text-to-speech conversion           |
| karen.devices.Listener  | Microphone device for speech-to-text conversion             |
| karen.devices.Watcher   | Video/Camera device for object recognition                  |
| karen.panels.RaspiPanel | Panel device designed for Raspberry Pi 7" screen @ 1024x600 |


In version 0.8.0 and later you are no longer required to install the brain, device, and the built-in plugins separately.

## Installation

Karen is available through pip, but to use the built-in devices there are a few extra libraries you may require.  Please visit the [Basic Install](https://docs.projectkaren.ai/en/latest/installation.basic/) page for more details.  

```
# Install the required system packages
sudo apt-get -y install \
  libfann2 \
  python3-fann2 \
  python3-pyaudio \
  python3-pyqt5 \
  python3-dev \
  festival \
  festvox-us-slt-hts  \
  libportaudio2 \
  libasound2-dev \
  libatlas-base-dev \
  cmake

# Optionally create your local environment and then activate it
python3 -m venv /path/to/virtual/env --system-site-packages
/path/to/virtual/env/bin/activate

# Install the required build libraries
python3 -m pip install scikit-build 

# Install required runtime libraries
python3 -m pip install urllib3 \
  requests \
  netifaces \
  numpy \
  deepspeech \
  pyaudio \
  webrtcvad \
  opencv-contrib-python \
  Pillow \
  padatious \
  fann2

# Install the karen module
python3 -m pip install karen
```

To start execute as follows:
```
python3 -m karen
```

## Troubleshooting: "Cannot find FANN libs"
If you encounter an error trying to install the karen module on the Raspberry Pi then you may need to add a symlink to the library FANN library. This is due to a bug/miss in the "find_fann" function within the Python FANN2 library as it doesn't look for the ARM architecture out-of-the-box.  To fix it run the following:

```
ln -s /usr/lib/arm-linux-gnueabihf/libdoublefann.so.2 /usr/local/bin/libdoublefann.so
```

## Web Control Panel

If everything is working properly you should be able to point your device to the web control panel running on the __Brain__ engine to test it out.  The default URL is:

__&raquo; [http://localhost:8080/](http://localhost:8080/)__

![Control Panel](https://projectkaren.ai/wp-content/uploads/2022/02/karen_model_0_8_0_control_panel.png)

## Demo running on Raspberry Pi

[![Project Karen](https://projectkaren.ai/wp-content/uploads/2021/06/karen_model_0_1_0_demo3.jpg)](https://projectkaren.ai/static/karen_model_0_1.mp4)

-----

## Help &amp; Support
Help and additional details is available at [https://projectkaren.ai](https://projectkaren.ai)
