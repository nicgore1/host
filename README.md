PS4 Exploit Host
================

## What is this?
This is an easy way for anyone to host their own exploit for the PS4 on their LAN. features include:
- Hosts your choice of exploit (Specter & IDC included in [releases](https://github.com/Al-Azif/ps4-exploit-host/releases))
- Sends your choice of payload after a successful exploit
- Blocks PSN domains from resolving (Stops accidental updates)
- Serves the 4.05 update to your PS4

## Requirements
- [Python 3](https://www.python.org/downloads/)
- The Python Directory added to your System Path Environment Variable (Windows)
    - Try running `envpython.bat` if you are having issues
- Root Privileges (Non-Windows)
- This will run on Windows, OSX, and Linux

## How to download
- Download the zip on the [releases](https://github.com/Al-Azif/ps4-exploit-host/releases) page
- Download with Git, be sure to grab the submodules

    `git clone --recursive https://github.com/Al-Azif/ps4-exploit-host.git`

## How to run
0. Make sure you have Python 3 installed
1. Download the files (As shown in the "How to download" section above)
2. Double click start.py
    - Alteratively run it from CMD with `python start.py`
    - If it starts with no errors, note the IP given
4. On your PS4 `Settings > Network > Setup Network` when you get to DNS Settings select `Manual` set the IP address noted above as the Primary DNS and Secondary DNS
5. Make sure the PS4 is on firmware version 4.05 (`Settings > System > System Information`). If it is not use the jump to the "How to use the Updater" section before continuing
6. On the PS4, go to `Settings > User's Guide` and select it. The exploit should run and there should be output on the script window.
7. If there is at least one payload in the `payloads` directory the script will prompt you to choose a payload to send
8. When done use `Ctrl+C` to cleanly close the script

## How to use the updater
0. Follow the "How to run" section for your OS until it says to come here
1. Put the system update in the `updates` folder as `PS4UPDATE_SYSTEM.PUP`
    - Optionally put the recovery update in the `updates` folder as `PS4UPDATE_RECOVERY.PUP`

        **SYS SHA-256:** D0C46E3CAADE956CABCBD20313A8EAB48DDBF3BC3129F3144926BECCFE3D36C4

        **REC SHA-256:** B74CE16802CD7EC05158C1035E09A3131BC1D489DA2B4EF93B2C6029D9CA2BFA

2. MAKE SURE THE DNS IS SET CORRECTLY!
3. **SEE #3 I'M SO SERIOUS!**
4. There should be a different page on the `System Software Update > View Details` option on the PS4. It'll be obvious!
    - The PS4 isn't using the right DNS if you get the standard Sony changelog page. **STOP IMMEDIATELY AND RESTART THE ENTIRE PROCESS**
5. Run a system update on your PS4 system.
6. Return to the "How to run" section

## Other Flags
- You can use the `--debug` flag to turn on the DNS & HTTP server output. This will make it hard to use the script normally as it'll push the payload menu off the screen
- You can use the `--autosend` flag to automatically send the like-named payload from the payloads directory

        ex. sudo python3 start.py --autosend debug_settings.bin

## Troubleshooting

#### Script Related
Before seeking help run though the following list:
- Follow the directions exactly, don't try to get fancy then come for help
- In your command prompt run `python --version` or `python3 --version` to make sure you have Python 3 installed correctly
    - You can edit the `envpython.bat` file to try and fix your environment errors (Notes in file on what to edit before running)
- Disable other networking apps that may interfere with the script (Skype, Discord, Torrent Clients, XAMPP, Firewalls, etc)
- It is normal to get errors while running the network test. This proves the PSN domains are blocked correctly.


#### Exploit/Payload Related
These are NOT related to this script in any way, but rather the exploits/payloads themselves
- Make sure your PS4's firmware is on 4.05 exactly
- Sending multiple exploits doesn't always work (Exploit may not be set up for it)
- The PS4 can get a kernel panic and just shutoff. Unplug the power for 30 seconds, then power it back on.
- "Out of Memory" errors while loading the exploit page are normal, restart your PS4 if you get a lot of them in a row.
- The FTP payload must be compiled, hex edited, or use `makeftp.py` with your PS4's IP
- The FTP payload does not have full access under Specter's exploit
- You must leave the exploit page open for FTP to work
- IDC's exploit page doesn't completely load even when it works
## Contributing
You can check the [issue tracker](https://github.com/Al-Azif/ps4-exploit-host/issues) for my to do list and/or bugs. Feel free to send a [pull request](https://github.com/Al-Azif/ps4-exploit-host/pulls) for whatever.
Be sure to report any bugs, include as much information as possible.

## What if a new exploit is released?
You should just be able to place the exploit files in the `exploit` directory. The exploit will automatically add the exploit to the menu.

        ex. exploit/new_exploit/index.html

## Why do you commit so many little changes, tweaks, etc?
I have no self control... it also lets people see the actual development. From barely working chicken scratch to actual code.

## Credits
- crypt0s for [FakeDns](https://github.com/Crypt0s/FakeDns)
- Specter, IDC, qwertyoruiopz, Flatz, CTurt, Anonymous for the exploits
