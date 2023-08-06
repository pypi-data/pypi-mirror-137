# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piku', 'piku.commands', 'piku.core', 'piku.template.project']

package_data = \
{'': ['*'], 'piku': ['template/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'pyserial>=3.5,<4.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['piku = piku.main:main']}

setup_kwargs = {
    'name': 'piku',
    'version': '0.1.3',
    'description': '',
    'long_description': "# Piku\nPiku is small command line utility for managing CircuitPython projects\n\nThe purpose of this project is to make creating a CircuitPython project, installing packages, deploying, and connecting to a CircuitPython device easy to do from the command line.\n\n\n# Warning\nThis tool is in very early development and needs testing! Please be careful when deploying and make sure you are only deploying your CircuitPython device!  Use at your own risk.\n\n\n# Getting Started\n\n### Installation\nPiku has been lightly tested on Linux and Windows it may also work on macOS.  I don't have an Apple computer so contributions welcome! After installation you can learn about Piku or any command line arguments or flags type `piku -h` or `piku <command> -h` or the documentation here.\n\n##### Windows\nTo install Piku in Windows please install Python 3.8 or greater from the windows store or the official python website.  Then install using pip:\n\n```\npip install piku\n```\n\nAfter Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.\n\n##### Linux\nTo install Piku in Linux, make sure you have Python 3.8 or greater and install using pip3.\n\n```\npip install --user piku\n```\n\nAfter Piku is installed you should be able to run Piku from the command line.  You can test this by typing `piku version`.\n\nSome linux computers do not have the default pip user bin directory included in the PATH.  You may add this directory to your PATH or install without the `--user` argument.\nhttps://unix.stackexchange.com/questions/612779/warning-not-on-path-when-i-tried-to-install-python-extensions-im-new-to-linu\n\n\nAfter installation if your user does not have permissions to use the serial port, you may need to add your user to the `dialout` group.\nhttps://askubuntu.com/questions/58119/changing-permissions-on-serial-port#answer-58122\n\n\n#### MacOS\n\nHelp wanted!  The process should be similar to Linux.\n\n\n### Preparing your Device\n\nBefore creating a project you must have CircuitPython installed on your device, and have your device serial and USB drivers installed.  Please check the CircuitPython website for instructions or the documentation of the board you have purchased.  When your done you should be able to see your drive mounted as a USB drive named `CIRCUITPY`.\n\nhttps://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython\n\n\n### Creating a Project\n\nTo create a new Piku project from the command line type:\n\n```\npiku create example\n```\n\nThis will create a new directory with the name of your project and a few folders and files inside. After you have created a project to use Piku, enter the directory of the project you just created to use Piku:\n\n```\ncd example\n```\n\n\n### Deploying your Project\nAfter you have created a project you can deploy your project to a connected CircuitPython device.  To deploy your project find the path of your `CIRCUITPY` UDB drive.  Then type:\n\n```\npiku deploy -d <path of your device>\n```\n\n***WARNING!!***  \nDeploying will remove other files from your device.  Piku attempts to check that the device is actually a CircuitPython device, and backup your old files, but you still need to be very careful.\n\nYou can also let Piku find your device by running deploy with no device argument:\n\n```\npiku deploy\n```\n\nAfter you have confirmed multiple times that you are deploying to the correct device you can also live on the wild side and skip the confirmation dialog using the `-y` command line argument.  Please be careful.\n\nIf changes have been made in your project code, the CircuitPython device should automatically detect and change files and reload.\n\n\n### Connecting to your Device\n\nYou can also connect to your CircuitPython device's serial port using Piku.  To do this just user the serial command from your Piku project directory:\n\n```\npiku serial\n```\n\nIf you are unable to connect, please confirm that you have the serial drivers for your device installed and you have permission to use the serial port (see installation instructions).  If you know the serial port, or Piku is connecting to the wront port you can also try specifying it directly via the `-s` command line flag.\n\nOnce connected you can exit by typing `ctrl-x`, enter the CircuitPython REPL by hitting `ctrl-c` and `ctrl-d` to exit the CircuitPython REPL.\n\n\n### Managing CircuitPython Modules/Libraries\n\nYou can easily download and add CircuitPython modules from the official Bundle or Community bundle using the command.  For example to download and add the `neopixel` module you would type:\n\n```\npiku add neopixel\n```\n\nThe specified module will be downloaded and added to your `lib` folder and your `project.toml` file. You can also remove this module by typing:\n\n```\npiku remove neopixel\n```\n\nYou can also install modules you can manually downloaded, please check cli help for more information `piku add -h`.\n\nCurrently Piku just works for the Bundle 7, which was the most recent bundle when the tool was built.  But hopefully a full semver module index and supporting older versions and CircuitPython is something that can be done in the future.\n",
    'author': 'Mark Raleson',
    'author_email': 'markraleson@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mraleson/rag.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
