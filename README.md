# GameTTS


## Installation

### Windows
#### Python
- Install [Python3](https://www.python.org/downloads/) (tested with Python 3.9)

#### eSpeak
- download and install [eSpeak](https://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/setup_espeak-1.48.04.exe/download)
- Add **espeak.exe** to **PATH- system variable** [Instruction](https://java.com/en/download/help/path.html)
- Default path should be `C:\Program Files (x86)\eSpeak\command_line` [Example](https://user-images.githubusercontent.com/6319070/125455610-8d303da3-0b4d-474c-98c6-3e93241f920c.png)
- Test eSpeak via the command line `C:\> espeak -v de "Das ist nur ein Test."`
- If you hear the speech output the setup was successful

#### Application
  
- Clone the application via git `git clone https://github.com/lexkoro/GameTTS.git` or download and extract it
- Install the necessary dependencies using Powershell `PS C:\GameTTS> .\install.ps1`
- The application can be run with `PS C:\GameTTS> .\run.ps1`


***The first start of the application may take a while since the TTS model has to be downloaded first (approx. 466 MB).***


![2021-07-13 20_58_34-Text-To-Speech GUI](https://user-images.githubusercontent.com/6319070/125511688-8c2aed42-d8ac-4826-bf57-fb2bfe27f0fb.png)


## References

- TTS Repository: https://github.com/jaywalnut310/vits
- https://github.com/mdbootstrap


## License and Disclaimer

The released models are made available for non-commercial use only under the terms of the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license. For details, see: https://creativecommons.org/licenses/by-nc/4.0/legalcode
