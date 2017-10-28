## What is this?
This is an easy way for anyone to host their own exploit for the PS4 on their LAN.

## Requirements
- [Python 2](https://www.python.org/downloads/) (Tested on 2.7.14)
- The Python Directory added to your System Path Environment Variable (Windows)
- Admin/Root Privileges
- This should run on Windows, OSX, and Linux (Tested on Windows 7, Windows 10, and Ubuntu 16.04)

## How to download
- Download the zip on the [releases](https://github.com/Al-Azif/ps4-exploit-host/releases) page
- Download with Git, be sure to grab the submodules

    `git clone --recursive https://github.com/Al-Azif/ps4-exploit-host.git`

## How to run
1. Run `python start.py` from the command line
    - If it starts with no errors, note the IP given to you
2. On your PS4 use the noted IP as your DNS server
3. On your PS4, go to `Settings > User Guide` and select it. Boom, the exploit page should load.
4. When you're done use `Ctrl+C` to cleanly close the script

## Contributing
You can check the [issue tracker](https://github.com/Al-Azif/ps4-exploit-host/issues) for my to do list and/or bugs. Feel free to send a [pull request](https://github.com/Al-Azif/ps4-exploit-host/pulls) for whatever.
Be sure to report any bugs, include as much information as possible.

## What if a new exploit is released?
You should just be able to replace the exploit files in the `exploit` folder.

## Credits
- crypt0s for [FakeDns](https://github.com/Crypt0s/FakeDns)
- qwertyoruiopz & AN0NY420 for the [exploit](https://github.com/AN0NY420/PS4-4.0x--4.05-Code-Execution-PoC)