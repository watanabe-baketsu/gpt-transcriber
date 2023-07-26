from argparse import ArgumentParser
import subprocess
import soundfile as sf
import torch
from transformers import pipeline


args = ArgumentParser()
args.add_argument("--input", type=str, default="../audios/input.mp4")

args = args.parse_args()

# 動画から音声を抽出
command = f"ffmpeg -i {args.input} -ab 160k -ac 1 -ar 16000 -vn audio.wav"
subprocess.call(command, shell=True)

# 音声データのロード
audio_input, sample_rate = sf.read("audio.wav")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v2",
    chunk_length_s=30,
    device=device,
)
prediction = pipe(audio_input, batch_size=8)["text"]
print(prediction)
with open("result.txt", mode="w") as f:
    f.write(prediction)