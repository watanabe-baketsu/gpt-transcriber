from argparse import ArgumentParser
import subprocess
import soundfile as sf
from transformers import WhisperProcessor, WhisperForConditionalGeneration


args = ArgumentParser()
args.add_argument("--input", type=str, default="../audios/input.mp4")

args = args.parse_args()

# 動画から音声を抽出
command = f"ffmpeg -i {args.input} -ab 160k -ac 1 -ar 16000 -vn audio.wav"
subprocess.call(command, shell=True)

# 音声データのロード
audio_input, sample_rate = sf.read("audio.wav")

# プロセッサとモデルのロード
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny").to("cuda")
forced_decoder_ids = processor.get_decoder_prompt_ids(language="japanese", task="transcribe")

chunk_length = 30 * sample_rate  # 30 seconds
min_length = 5 * sample_rate  # 1 second
audio_chunks = [audio_input[i:i + chunk_length] for i in range(0, len(audio_input), chunk_length)]

transcriptions = []

for audio_chunk in audio_chunks:
    # If the audio chunk is too short, skip it
    if len(audio_chunk) < min_length:
        continue

    input_features = processor(audio_chunk, sampling_rate=sample_rate, return_tensors="pt").input_features.to("cuda")

    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)

    # 予測値から文字列への変換
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print(transcription)

    transcriptions.append(transcription)
results = ""
for transcription in transcriptions:
    results += transcription[0]
with open("result.txt", mode="w") as f:
    f.write(results)

