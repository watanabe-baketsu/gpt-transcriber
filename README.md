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

### LocalStack test
```bash
docker-compose up -d
samlocal build
samlocal deploy --stack-name openai-test-api --capabilities CAPABILITY_NAMED_IAM --profile localstack
```

### AWS test
```bash
sam build
sam deploy --stack-name openai-test-api --capabilities CAPABILITY_NAMED_IAM --profile Your_AWS_PROFILE --guided
```

## src/.env
```.dotenv
LOCALSTACK_API_KEY=Your_LOCALSTACK_API_KEY
OPENAI_API_KEY=Your_OPENAI_API_KEY
```