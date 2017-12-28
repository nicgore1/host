## What is this?
This is an easy way for anyone to host their own exploit for the PS4 on their LAN. It blocks PSN to stop accidental updates, it also serves the 4.05 update if you want it to. You can also generate an FTP payload. There is also a simple CLI for sending additional payloads.

So the scope of this has become like an all in one toolkit

## Why?
You won't be dependent on 3rd party websites
- They could be down
- They could be blocked
- They could be broken
- Etc, etc, etc.

## Requirements
- [Python 2](https://www.python.org/downloads/) (Tested on 2.7.14)
- The Python Directory added to your System Path Environment Variable (Windows)
    - Try running `envpython.bat` if you are having issues
- Root Privileges (Non-Windows)
- This should run on Windows, OSX, and Linux (Tested on Windows 7, Windows 10, and Ubuntu 16.04)

## How to download
- Download the zip on the [releases](https://github.com/Al-Azif/ps4-exploit-host/releases) page
- Download with Git, be sure to grab the submodules

    `git clone --recursive https://github.com/Al-Azif/ps4-exploit-host.git`

## How to run

#### Windows
0. Make sure you have Python 2.7 installed and ENV Paths set
1. Download the files (As shown in the "How to download" section above)
2. Double click start.py
    - Alteratively run it from CMD with `python start.py`
    - If it starts with no errors, note the IP given
4. On your PS4 `Settings > Network > Setup Network` when you get to DNS Settings select `Manual` set the IP address noted above as the Primary DNS and `0.0.0.0` as the Secondary DNS
5. Make sure the PS4 is on firmware version 4.05 (`Settings > System > System Information`). If it is not use the jump tp the "How to use the Updater" section before continuing
6. On the PS4, go to `Settings > User's Guide` and select it. The exploit should run and there should be output on the server window
7. When done use `Ctrl+C` to cleanly close the script

#### Linux/OSX
0. Make sure you have Python 2.7 installed correctly
1. Download the files (As shown in the "How to download" section above)
2. Open your CLI in the script directory
3. Run `sudo python start.py` from the command line
    - If it starts with no errors, note the IP given
4. On your PS4 `Settings > Network > Setup Network` when you get to DNS Settings select `Manual` set the IP address noted above as the Primary DNS and `0.0.0.0` as the Secondary DNS
5. Make sure the PS4 is on firmware version 4.05 (`Settings > System > System Information`). If it is not use the jump tp the "How to use the Updater" section before continuing
6. On the PS4, go to `Settings > User's Guide` and select it. The exploit should run and there should be output on the server window
7. When done use `Ctrl+C` to cleanly close the script

## How to use the updater
0. Follow the "How to run" section for your OS until it says to come here
1. Put the system update in the `updates` folder as `PS4UPDATE_SYSTEM.PUP`
    - Optionally put the recovery update in the `updates` folder as `PS4UPDATE_RECOVERY.PUP`

        **SYS SHA-256:** D0C46E3CAADE956CABCBD20313A8EAB48DDBF3BC3129F3144926BECCFE3D36C4

        **REC SHA-256:** B74CE16802CD7EC05158C1035E09A3131BC1D489DA2B4EF93B2C6029D9CA2BFA

2. MAKE SURE THE DNS IS SET CORRECTLY!
3. SEE #3 I'M SO SERIOUS!
4. There should be a different page on the `System Software Update > View Details` option on the PS4. It'll be obvious
    - If this page doesn't display it also means it worked... the server becomes blocking while uploading the update. This is a bug
    - The PS4 isn't using the right DNS if you get the standard Sony changelog page. STOP IMMEDIATELY AND RESTART THE ENTIRE PROCESS
5. Run a system update on your PS4 system.
6. Return to the "How to run" section

## How to generate an FTP payload
0. Make sure you have Python 2.7 installed
1. Run `python makeftp.py --ip ***.***.***.***` where the *s are the PS4's LAN IP
2. Run the exploit or use `sender.py`

## How to use Sender
0. Make sure you have Python 2.7 installed
1. To send payloads:

    - `python sender.py --ip ***.***.***.*** --all`, where the *s are the PS4's LAN IP, will send all payloads in the `payloads` directory
    - `python sender.py --ip ***.***.***.*** --payload "payloads/ftp.bin"`, where the *s are the PS4's LAN IP, will send the payload located at `payloads/ftp.bin`

## Contributing
You can check the [issue tracker](https://github.com/Al-Azif/ps4-exploit-host/issues) for my to do list and/or bugs. Feel free to send a [pull request](https://github.com/Al-Azif/ps4-exploit-host/pulls) for whatever.
Be sure to report any bugs, include as much information as possible.

## What if a new exploit is released?
You should just be able to replace the exploit files in the `exploit` folder.

## Why do you commit so many little changes, tweaks, etc?
I have no self control... it also lets people see the actual development. From barely working chicken scratch to actual code.

## Credits
- crypt0s for [FakeDns](https://github.com/Crypt0s/FakeDns)
- Specter, qwertyoruiopz, Flatz, CTurt, Anonymous for the [exploit](https://github.com/Cryptogenic/PS4-4.05-Kernel-Exploit)
