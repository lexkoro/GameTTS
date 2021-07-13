# GameTTS


## Installation

### Windows
#### Python
- [Python3](https://www.python.org/downloads/) installieren (getestet mit Python 3.9)

#### eSpeak
- [eSpeak](https://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/setup_espeak-1.48.04.exe/download) herunterladen und installieren
- Pfad zur **espeak.exe** der **Path-Umgebungsvariable** hinzufügen [Anleitung](https://michster.de/wie-setze-ich-die-path-umgebungsvariablen-unter-windows-10/)
- Der Standard Pfad sollte `C:\Program Files (x86)\eSpeak\command_line` sein [Beispiel](https://user-images.githubusercontent.com/6319070/125455610-8d303da3-0b4d-474c-98c6-3e93241f920c.png)
- Über die Kommandozeile eSpeak testen `C:\> espeak -v de "Das ist nur ein Test."`
- Ist die Sprachausgabe zu hören war die Installation erfolgreich.

#### Anwendung
  
- Die Anwendung über git klonen `git clone https://github.com/lexkoro/GameTTS.git` oder als ZIP herunterladen und entpacken
- Mit der Powershell Kommandozeile `PS C:\GameTTS> .\install.ps1` die notwendigen Abhängigkeiten installieren
- Mit `PS C:\GameTTS> .\run.ps1` kann die Anwendung gestartet werden.
