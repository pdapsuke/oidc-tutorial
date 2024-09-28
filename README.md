# OIDCチュートリアル
OIDCの概要、具体的な実装、関連するセキュリティの脅威とその対応方法を理解するためのチュートリアルです。

## コンテンツ
1. [OIDCの概要・利用シーン](./doc/oidc_overview.md)
2. [OIDCのフローと具体的な実装](./doc/major_flow_and_example_impl.md)
3. [OIDCに関連するセキュリティの脅威](./doc/security_threats_related_to_OIDC.md)

## 参考文献
- [OpenID Connect入門: 概念からセキュリティまで体系的に押さえる Kindle版](https://amzn.asia/d/3yIRDiC)

## 開発Tips
カレントディレクトリはプロジェクトルートとする
### Keycloak設定変更
1. Keycloakをメンテナンスモードで起動  
`./bin/setting-keycloak.sh --mode maintainance`
2. Keycloakにアクセスし、GUIから設定変更  
ログインURL: `http://localhost:8888`  
adminユーザーID: `admin`, pass: `admin`  
設定対象のrealm: `oidc-tutorial`  
3. `ctrl+c`でKeycloakを停止
4. 2.で実施した設定をエクスポート  
`./bin/setting-keycloak.sh --mode export`

### フロントエンド開発
0. (前提)`./bin/run.sh`でDB, APIを起動させておく
1. `./app/front/default`または`./app/front/vuln_responsed`に移動
2. nuxtサーバを起動 `MODE=dev npm run dev`  
`http://localhost:3000`にアクセスして開発
3. nginxで公開する静的ファイルをビルド `npm run generate`

### OIDCチュートリアルアプリのテーブル設計
`doc/tables.pu`（PlantUML）を参照