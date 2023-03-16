import os
import PySimpleGUI as sg
from pytube import YouTube
from PySimpleGUI.PySimpleGUI import popup_error, popup


def download_video(url, quality):
    save_path = os.path.expanduser("~/Desktop")

    try:
        yt = YouTube(url)
    except Exception as e:
        popup_error(f"Error: {e}")
        return

    if quality == "highest":
        stream = yt.streams.get_highest_resolution()
    elif quality == "lowest":
        stream = yt.streams.get_lowest_resolution()
    else:
        stream = yt.streams.get_by_resolution(quality)

    if stream is None:
        popup_error("No available stream found")
        return

    try:
        stream.download(output_path=save_path)
        popup("Success", f"Video downloaded to {save_path}")
    except Exception as e:
        popup_error(f"Error: {e}")


layout = [
    [sg.Text("YouTube URL:"), sg.InputText(key="url")],
    [sg.Text("Quality:"), sg.Combo(["highest", "lowest", "720p", "480p", "360p", "240p"], key="quality", default_value="highest")],
    [sg.Button("Download"), sg.Button("Exit")]
]

window = sg.Window("YouTube Video Downloader", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Download":
        download_video(values["url"], values["quality"])

window.close()
