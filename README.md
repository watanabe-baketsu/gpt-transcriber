# openai_test_api
For OpenAI API test.

## How to use
```bash
pipenv install -r requirements.txt
pipenv shell
pip3 innstall aws-sam-cli, localstack
sam build
sam local start-api --warm-containers EAGER
```
### Simple test
```bash
cd ./src
uvicorn app:app --reload
```

## src/.env
```.dotenv
LOCALSTACK_API_KEY=Your_LOCALSTACK_API_KEY
OPENAI_API_KEY=Your_OPENAI_API_KEY
```