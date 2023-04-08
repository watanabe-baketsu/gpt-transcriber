from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import os
import whisper
import openai
import torch

# NVIDIA GPUが利用可能かどうかを確認
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Whisperモデルをロードする
model = whisper.load_model("medium", device=DEVICE)

# OpenAPI APIキーを設定する
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to my Blog Post about ChatGPT and Whisper!"


@app.route('/summary', methods=['POST'])
def handler():
    if not request.files:
        # ユーザーがファイルを渡さなかった場合は、400 (Bad Request) エラーを返す
        abort(400)

    results = []

    # ユーザーが渡したすべてのファイルに対してループする
    for filename, handle in request.files.items():
        # 一時ファイルを作成する.
        temp = NamedTemporaryFile()
        # ユーザーがアップロードしたファイルを一時ファイルに書きこむ
        handle.save(temp)
        # Whisperモデルで音声の一時ファイルからテキストを取得する
        result = model.transcribe(temp.name)

        # Sテキストを要約する
        summary_result = summary_text(result['text'])
        # 結果オブジェクトを作成する
        results.append({
            'transcript': result['text'],
            'language': result['language'],
            'summary': summary_result,
        })

    # JSON形式で結果を返却する
    return {'results': results}


def summary_text(transcribed_text):
    if len(transcribed_text) == 0:
        return ""
    print(generate_prompt(transcribed_text))

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=1024,
            stop=None,
            prompt=generate_prompt(transcribed_text),
            temperature=0.7,
        )
        print(response)

        return response.choices[0].text
    except Exception as e:
        print(e)
        return ""


def generate_prompt(transcribed_text):
    return f"以下の文章において、日本語で不自然なところを修正してください。" \
           f"修正した文章を箇条書き文章にして簡潔に要約してください。:{transcribed_text}"
