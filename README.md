# ambientmixer - a graphical Python player with pygame to play and edit ambient-mixer.com mixes locally
This script is based on Philooz's great script found here

https://github.com/Philooz/pyambientmixer

If you just want to play presets and don't need a graphical user interface and editing features you should check out his script!

This little hacked script is here to allow people to download and play ambient mixes stored on ambient-mixer.com. It's not really "out for all users", but it works enough to be public.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need python3 installed on your system, with the python packages untangle, pygame, requests and docopt.

I recommend pip to install the required modules. Install them with

```sudo pip3 install requests pygame untangle docopt requests```

You'll also need an OGG encoder, as I went with pygame (and because it's a free format).
I recommend the easy-to-use tool **fre:ac** utility, which encodes a whole directory into ogg.
The encoding can be started with the graphical interface or via batch commands (my choice
since startable from pyhton).
If you're a windows user, you can download the installer from

[https://www.freac.org/](https://www.freac.org/)

### Installing

Just store ```ambient_mixer.py``` and ```ambient_downloader.py``` anywhere on your system.

## Downloading a mix

Easy. Get to the mix you'd like to keep. In this example, I went with "**Night in a Medieval Monastery**".

Just run ```ambient_downloader.py``` with the url.

In our example :

```python3 ambient_downloader.py http://religion.ambient-mixer.com/night-in-a-medieval-monastery```

which will give us

```Saved http://xml.ambient-mixer.com/audio-template?player=html5&id_template=48152 as presets/night-in-a-medieval-monastery.xml.
Saved http://xml.ambient-mixer.com/audio/9/5/7/957298df7abb5d7e94e6323c45d94063.mp3 as sounds/3677.mp3.
Saved http://xml.ambient-mixer.com/audio/d/3/3/d33c249dc7497e59091fab0ef08ee283.mp3 as sounds/529.mp3.
Saved http://xml.ambient-mixer.com/audio/a/0/1/a015edfc739fd3c7d942823511ba869d.mp3 as sounds/329.mp3.
Saved http://xml.ambient-mixer.com/audio/4/9/a/49a0e9aef698b60cf2c43312225778b9.mp3 as sounds/5745.mp3.
Saved http://xml.ambient-mixer.com/audio/3/b/6/3b64e0b6dffd39bd239e8071c25a4f37.mp3 as sounds/4583.mp3.
Saved http://xml.ambient-mixer.com/audio/7/8/e/78ece9cbea4fe23031c07ce15278f84a.mp3 as sounds/3354.mp3.
Saved http://xml.ambient-mixer.com/audio/7/5/e/75e7d0a3c6c6ef6ed69b26e7098b208c.mp3 as sounds/6432.mp3.
Saved http://xml.ambient-mixer.com/audio/1/6/8/168498dfdf8743eefb46dfebfd09c9eb.mp3 as sounds/6773.mp3.
```

Once the downloads are complete, you'll get two folders inside the current directory : ```sounds_named```, which contains all the sounds files you've downloaded (already converted from .mp3 to .ogg); and ```presets``` which holds all the .xml files corresponding to the presets.


### TODOS and possible bugs

* Crossfade needs to be implemented with fade switching between 2 identical tracks
* Download of presets via GUI with support for multiple links (large textbox)
* ...

## Authors

* **Philooz** - *Initial work* - [Philooz](https://github.com/Philooz)
* **Alasterer** - *Addition of GUI and more features* - [Alasterer](https://github.com/Alasterer)

## License

This project is licensed under the GPL License.

## Acknowledgments

* Thanks to ambient-mixer.com website
* Thanks to Philooz for the great downloading and sound playback scripts
* Huge thanks to the makers of the awesome python modules
* You for downloading this!
