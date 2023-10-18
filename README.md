# GameTTS


## Installation

### Application
  
- Download the ZIP folder from [releases](https://github.com/lexkoro/GameTTS/releases/latest/) and extract it
- Run the GameTTS.exe, it should install the required python dependencies and download the TTS model

If successful, the application should start automatically.

***The first start of the application may take a while since the TTS model has to be downloaded first (approx. 155 MB).***


![2021-07-13 20_58_34-Text-To-Speech GUI](https://user-images.githubusercontent.com/6319070/125511688-8c2aed42-d8ac-4826-bf57-fb2bfe27f0fb.png)


## for Linux

### Install and Start

```sh
# bash GameTTS/run.sh  [venvpath] [browser]
bash GameTTS/run.sh 
```

### Set Browser

Default Browser is `chrome`. If this is not found, the fallback is `edge`.

for Linux:
Override this setting on the start with:
main.py --browser firefox

(this is the default if you run the command `bash GameTTS/run.sh`)

## References

- TTS Repository: https://github.com/jaywalnut310/vits
- https://github.com/mdbootstrap


## License and Disclaimer

The released models are made available for non-commercial use only under the terms of the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license. For details, see: https://creativecommons.org/licenses/by-nc/4.0/legalcode
