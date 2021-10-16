import eel
import sys
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import traceback
import platform
from app.utils import *

try:
    from vits.synthesizer import Synthesizer

    synthesizer = Synthesizer(TTS_CONFIG_PATH)

    if TTS_MODEL_PATH.exists():
        synthesizer.load_model(TTS_MODEL_PATH)
    else:
        download_model("G_600000.pth")
        synthesizer.load_model(TTS_MODEL_PATH)

    synthesizer.init_speaker_map(SPEAKER_CONFIG)

except ImportError as err:
    print(err)
    eel.call_torch_modal()  # call javascript modal if torch not available


def synthesize(text, speaker_id, speaker_name, params):
    audio_data = synthesizer.synthesize(text, speaker_id, params)
    cur_timestamp = datetime.now().strftime("%m%d%f")
    tmp_path = Path("static_web", "tmp")

    if not tmp_path.exists():
        tmp_path.mkdir()

    file_name = "_".join(
        [str(speaker_id), speaker_name, str(cur_timestamp), "tmp_file"]
    )
    save_audio(tmp_path, file_name, audio_data)

    if params["out_path"]:
        save_file_name = "_".join([cur_timestamp, speaker_id, speaker_name, text[:15]])
        save_file_path = Path(params["out_path"])
        save_audio(
            save_file_path, save_file_name, audio_data, params["file_export_ext"]
        )

    eel.addTableRow(speaker_name, text, str(Path("tmp", ".".join([file_name, "wav"]))))


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

    if PLATFORM == "Windows":
        winsound.PlaySound(str(file_path), winsound.SND_ASYNC)
    elif PLATFORM == "Linux" or PLATFORM == "Darwin":
        audio = AudioSegment.from_wav(str(file_path))
        play(audio)


@eel.expose
def process_input(params=None):
    try:
        if params["text"]:
            synthesize(
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
    tmp_files = Path("static_web", "tmp").glob("*.*")
    for f in tmp_files:
        f.unlink()
    sys.exit(0)


# start EEL App
if __name__ == "__main__":

    directory = "static_web"
    app = "chrome"
    page = "index.html"

    eel_kwargs = dict(
        host="localhost",
        port=8080,
        size=(1050, 750),
    )

    # create_samples(synthesizer)

    eel.init(directory)

    try:
        try:
            eel.start(page, mode=app, **eel_kwargs)

        except EnvironmentError:
            # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
            if PLATFORM == "Windows" and int(platform.release()) >= 10:
                eel.start(page, mode="edge", **eel_kwargs)
            else:
                exit_clean_up()
    except (SystemExit, MemoryError, KeyboardInterrupt):
        exit_clean_up()
