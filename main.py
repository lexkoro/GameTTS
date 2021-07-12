import eel
import sys
import json
from datetime import datetime
from pathlib import Path
from vits.inference import Synthesizer
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog
import traceback
import platform


plt = platform.system()

if plt == "Windows":
    import winsound
elif plt == "Linux" or plt == "Darwin":
    from pydub import AudioSegment
    from pydub.playback import play
else:
    print("Unidentified system")

# init paths
APP_FOLDER = Path(Path(__file__).parent.resolve())
APP_CONFIG_PATH = Path(APP_FOLDER, "static_web/resource/", "app-config.json")
SPEAKER_CONFIG = Path(
    APP_FOLDER, "static_web/resource/json-mapping/", "speaker_map.json"
)
TTS_CONFIG_PATH = Path(APP_FOLDER, "vits/model", "config.json")
TTS_MODEL_PATH = Path(APP_FOLDER, "vits/model", "G_630000.pth")

try:
    from vits.inference import Synthesizer

    synthesizer = Synthesizer()
    synthesizer.load_config(TTS_CONFIG_PATH)
    synthesizer.load_model(TTS_MODEL_PATH)
    synthesizer.init_speaker_map(SPEAKER_CONFIG)

except ImportError as err:
    print(err)
    eel.call_torch_modal()  # call javascript modal if torch not available


def create_samples():
    sentence = "So hört sich meine Stimme an."
    for name, idx in synthesizer.speaker_map.items():
        audio_data = synthesizer.synthesize(
            str(sentence),
            idx,
            {"speech_speed": 1.0, "speech_var_a": 0.56, "speech_var_b": 0.7},
        )
        print(name)
        tmp_file_path = Path("static_web", "resource", "audio-samples", idx + ".wav")
        write(tmp_file_path, 22050, audio_data)


def synthesize(text, speaker_id, speaker_name, params):
    audio_data = synthesizer.synthesize(text, speaker_id, params)
    cur_timestamp = datetime.now().strftime("%m%d%f")
    file_name = Path(
        "tmp",
        "_".join([str(speaker_id), speaker_name, str(cur_timestamp), "tmp_file.wav"]),
    )
    tmp_file_path = Path("static_web", file_name)
    write(tmp_file_path, 22050, audio_data)

    if params["out_path"]:
        save_file_name = "_".join(
            [cur_timestamp, speaker_id, speaker_name, text[:15] + ".wav"]
        )
        save_file_path = Path(params["out_path"], save_file_name)
        write(save_file_path, 22050, audio_data)

    eel.addTableRow(speaker_name, text, str(file_name))


@eel.expose
def load_config():
    with open(APP_CONFIG_PATH) as json_file:
        config_data = json.load(json_file)
    return config_data


@eel.expose
def save_config(data):
    with open(APP_CONFIG_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)


@eel.expose
def play_sample(speaker_idx):
    file_path = Path("static_web", "resource", "audio-samples", speaker_idx + ".wav")

    if plt == "Windows":
        winsound.PlaySound(str(file_path), winsound.SND_ASYNC)
    elif plt == "Linux" or plt == "Darwin":
        audio = AudioSegment.from_wav(str(file_path))
        play(audio)


@eel.expose
def process_input(params=None):
    try:
        if params["text"]:
            audio = synthesize(
                params["text"], params["speaker_id"], params["speaker_name"], params
            )

        if params["file_content"]:
            for line in params["file_content"]:
                if len(line.split("|")) > 1:
                    text, sp_id = line.split("|")
                    sp_name = synthesizer.get_speaker_by_id(sp_id)
                    synthesize(text, sp_id, sp_name, params)
                else:
                    synthesize(
                        line, params["speaker_id"], params["speaker_name"], params
                    )
        eel.finishSynthesize()
    except Exception as err:
        print(err)
        traceback.print_tb(err.__traceback__)
        eel.launchErrorModal()(err)
        eel.finishSynthesize()


@eel.expose
def select_out_dir():
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        folder_path = filedialog.askdirectory()
        return folder_path
    except:
        return None


@eel.expose
def exit_clean_up():
    tmp_files = Path("static_web", "tmp").glob("*.wav")
    for f in tmp_files:
        f.unlink()
    sys.exit(0)


# start EEL App
if __name__ == "__main__":

    # create_samples()

    directory = "static_web"
    app = "chrome"
    page = "index.html"

    eel_kwargs = dict(
        host="localhost",
        port=8080,
        size=(1050, 750),
    )

    eel.init(directory)

    try:
        try:
            eel.start(page, mode=app, **eel_kwargs)
        except EnvironmentError:
            # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
            if plt == "Windows" and int(platform.release()) >= 10:
                eel.start(page, mode="edge", **eel_kwargs)
            else:
                exit_clean_up()
    except (SystemExit, MemoryError, KeyboardInterrupt):
        exit_clean_up()
