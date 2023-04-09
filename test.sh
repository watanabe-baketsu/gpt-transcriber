samlocal build -t template.yaml

# localstackの設定と起動
apikey=$(cat .env | grep LOCALSTACK_API_KEY | cut -d '=' -f 2)
export LOCALSTACK_API_KEY=$apikey
docker-compose up -d

sleep 20
# イメージアップロード用のレポジトリの作成
awslocal ecr create-repository --repository-name lambda-image-repo --profile localstack

# localstackへデプロイ
samlocal deploy --guided --capabilities CAPABILITY_NAMED_IAM --profile localstack