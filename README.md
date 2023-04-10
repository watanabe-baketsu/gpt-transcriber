# openai_test_api
For OpenAI API test.

## How to use
```bash
pipenv install -r requirements.txt
pipenv shell
```
### Simple test
```bash
cd ./src
uvicorn app:app --reload
```

## src/.env
```.dotenv
OPENAI_API_KEY=Your_OPENAI_API_KEY
```

## EC2 deploy
```bash
git clone https://watanabe-baketsu/gpt-transcripter.git
cd ./gpt-transcripter/src
pipinstall -r requirements.txt
sudo nohup uvicorn app:app --host 0.0.0.0 --port 80 > output.log 2>&1 &
```