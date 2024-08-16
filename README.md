# アプリ概要
Chainlit 上の簡易的な RAG チャットアプリ
AWS Bedrock の KnowledgeBase　を RAG の 本体として使用

#　Get Started
## デプロイ

### 前提条件
デプロイには以下のソフトウェアがインストールされている必要があります．  
以下のソフトウェアがインストールされている必要があります．
* Python 3.12
* pipenv
* Docker
* AWS Copilot

### 概要
1. ECRにDockerイメージをpush
2. ECSでタスクとサービスを定義
3. ECSでタスクをrun
これをAWS Copilotで簡易的にIaC化

### 具体的な順序
1. アプリケーションの初期化
```sh
$ copilot init app
Application name: 【好きなアプリ名を入力】
Workload type: 【Load Balanced Web Serviceを選択】
Service name: 【好きなサービス名を入力】
Dockerfile: 【./Dockerfileを選択】
Environment: 【devとかお好きに】
```
2. 提供されたURLにアクセス
3. 再デプロイ
```sh
$ copilot deploy
$ copilot deploy --env ssl-dev #user_domain.comにデプロイしたいときはこっち！
$ copilot svc status #デプロイの進行状況の確認
$ copilot svc log #新しくデプロイされたサービスのログの確認
```

## ローカルで開発
1. Dockerfile作成
```sh
$ touch Dockerfile
```
Dockerfile.exampleを参考にAWSCredentials（AWSの認証情報）は自分の情報を入力
2. Dockerイメージをbuild
```sh
$ docker build -t ragchat-chainlit:latest . 
```
3. Dockerアプリをrun
```sh
$ docker run -p 8080:8080 ragchat-chainlit:latest
```

## ユーザ名とパスワード
実はまだハードコーディングしてる（いつかOAuth実装する）  

## リソースのクリーンアップ
```sh
copilot app delete
```
