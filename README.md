# ambientmixer - a graphical Python player with pygame to play and edit ambient-mixer.com mixes locally
This script is based on Philooz's script found here

https://github.com/Philooz/pyambientmixer

This little hacked script is here to allow people to download and play ambient mixes stored on ambient-mixer.com. It's not really "out for all users", but it works enough to be public.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need python3 installed on your system, with the python packages untangle, pygame, requests and docopt.

I recommend pip to install the required modules. Install them with

```sudo pip3 install requests pygame untangle docopt requests```

You'll also need an OGG encoder, as I went with pygame (and because it's a free format).
I recommend the easy-to-use tool fre:ac utility, which encodes a whole directory into ogg.
The encoding can be started with the graphical interface or via batch commands (my choice
since startable from pyhton).
If you're a windows user, you can download the installer from

[www.freac.org](https://www.freac.org/)

## Authors

* **Philooz** - *Initial work* - [Philooz](https://github.com/Philooz)
* **Alasterer** - *Addition of GUI and more features* - [Alasterer]((https://github.com/Alasterer)

## License

This project is licensed under the GPL License.

## Acknowledgments

* Thanks to ambient-mixer.com website
* Thanks to Philooz for the great downloading and sound playback scripts
* Huge thanks to the makers of the awesome python modules
* You for downloading this!
