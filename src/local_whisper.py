from argparse import ArgumentParser
import subprocess
import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


args = ArgumentParser()
args.add_argument("--input", type=str, default="input.mp4")

args = args.parse_args()

# 動画から音声を抽出
command = f"ffmpeg -i {args.input} -ab 160k -ac 2 -ar 16000 -vn audio.wav"
subprocess.call(command, shell=True)

# 音声データのロード
audio_input, sample_rate = sf.read("audio.wav")

# プロセッサとモデルのロード
processor = Wav2Vec2Processor.from_pretrained("openai/whisper-large-v2")
model = Wav2Vec2ForCTC.from_pretrained("openai/whisper-large-v2").to("cuda")

# 入力音声データの前処理
input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

# モデルでの予測
logits = model(input_values).logits

# 予測値から文字列への変換
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.decode(predicted_ids[0])

# 文字起こし結果の表示
print(transcription)
with open("result.txt", mode="w") as f:
    f.write(transcription)

