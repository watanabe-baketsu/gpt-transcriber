import json
import os

import boto3
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from pydantic import BaseModel
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory="templates")

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
# For AWS or LocalStack Environment.
# client = boto3.client(region_name="ap-northeast-1", service_name="secretsmanager")
# secret = client.get_secret_value(SecretId=os.environ['OPENAI_API_KEY'])
# secret_json = json.loads(secret["SecretString"])
# openai.api_key = secret_json['apikey']


class SummaryItem(BaseModel):
    text: str


async def transcribe_audio(audio_file: str) -> str:
    with open(audio_file, "rb") as audio_data:
        model = "whisper-1"
        language = "ja"
        print(audio_data.name)
        response = openai.Audio.transcribe(
            file=audio_data,
            model=model,
            language=language
        )
    transcribe_text = response.text
    return transcribe_text


async def save_audio(audio_file: UploadFile) -> str:
    file_location = f"/tmp/{audio_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(audio_file.file.read())
    return file_location


async def summarize_text(text: str) -> List[str]:
    prompt = f"あなたはとても優秀なassistantです。" \
             f"以下のテキストを箇条書きにして、内容を要約してください。箇条書きの数は多くても5つまでとします。" \
             f":\n\n{text}\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
    )

    summary = response.choices[0].message.content.strip()
    bullet_points = summary.split('\n')

    return bullet_points


@app.get('/')
async def index(request: Request):
    # For audio upload, render the index.html template.
    context = {"request": request}
    return templates.TemplateResponse('index.html', context)


@app.post('/process_audio')
async def process_audio(request: Request, audio: UploadFile = File(...)):
    audio_location = await save_audio(audio)
    transcribed_text = await transcribe_audio(audio_location)
    print(transcribed_text)
    summary_points = await summarize_text(transcribed_text)

    summary = [point for point in summary_points]
    context = {"request": request, "summary": summary}
    return templates.TemplateResponse('summary.html', context)


lambda_handler = Mangum(app)
