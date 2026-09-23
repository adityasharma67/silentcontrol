


<p align="center">
  <img src="https://i.discord.fr/PSS.png">
</p>

<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  </a>
  <a href="https://paypal.me/davidecose">
    <img src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white">
  </a>
    <a href="https://instagram.com/davide.cose">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white">
  </a>
    <a href="https://github.com/callmenoway">
    <img src="https://img.shields.io/github/repo-size/callmenoway/SilentScreenshare">
  </a>
    <a href="https://github.com/callmenoway/IP-Logger/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-important">
  </a>
</p>

# Silent Screenshare
Silent Screenshare is a python tool that shows the screen of pc in local ip. When you open the script it will desapear from the taskbar and you can only view in task manager.

## Disclaimer

|SilentScreenshare was made for Educational purposes|
|-------------------------------------------------|
This project was created only for good purposes and personal use.
By using SilentScreenshare, you agree that you hold responsibility and accountability of any consequences caused by your actions.

## Installation (Windows)

Requirements:

- Windows 10/11
- Python 3.10 or newer from [python.org](https://www.python.org/downloads/windows/)
- Git, if cloning from GitHub

Clone the repository and run the setup script from the project folder:

```bat
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
setup.bat
```

`setup.bat` creates a project-local `.venv` folder and installs every package
from `requirements.txt`. It does not modify the global Python installation.

## Usage

```bash
python main.py
```

For a detached Windows launch, double-click `start_screenshare.bat` after setup.
The app keeps running after that terminal closes. To stop the instance, run
`stop_screenshare.bat`.
The launcher stores the process ID in `screenshare.pid` so it only targets the
instance it started.

This cannot prevent a Windows administrator, antivirus, or system shutdown from
terminating the process. The server also has no authentication, so do not expose
port 5000 to untrusted networks.

## Security
The tool is full undetected, i relase the [virustotal](https://www.virustotal.com/gui/file/e3ee155535832fdd6c5f2c95a990012acb159bf3441de060c4fa2545a0bab699?nocache=1) scan.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
