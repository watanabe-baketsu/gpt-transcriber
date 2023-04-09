import openai
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from pydantic import BaseModel
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory="templates")
openai.api_key = "Your API Key"


class SummaryItem(BaseModel):
    text: str


async def transcribe_audio(audio_file: bytes) -> str:
    file = audio_file
    model = "whisper-1"
    language = "ja-JP"
    response = openai.Audio.transcribe(
        file=file,
        model=model,
        language=language
    )
    print(response)
    transcribe_text = response.transcript
    return transcribe_text


async def summarize_text(text: str) -> List[str]:
    prompt = f"Summarize the following text in bullet points and in Japanese:\n\n{text}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    bullet_points = summary.split('\n')

    return bullet_points


@app.get('/')
async def index(request: Request):
    # For audio upload, render the index.html template.
    context = {"request": request}
    return templates.TemplateResponse('index.html', context)


@app.post('/process_audio', response_model=List[SummaryItem])
async def process_audio(audio: UploadFile = File(...)):
    audio_data = await audio.read()
    transcribed_text = await transcribe_audio(audio_data)
    summary_points = await summarize_text(transcribed_text)

    return [{"text": point} for point in summary_points]


lambda_handler = Mangum(app)
