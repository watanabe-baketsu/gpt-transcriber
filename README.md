# openai_test_api
For OpenAI API test.

## How to use
```bash
pipenv install -r requirements.txt
pipenv shell
docker build -t audio-summary-api . 
docker run -p 8080:8080 audio-summary-api
```