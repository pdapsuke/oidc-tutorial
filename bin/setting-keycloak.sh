#!/bin/bash

function usage {
cat >&2 <<EOS
keycloakのrealm, user, clientなど各種設定
設定をエクスポートするコマンド

[usage]
 $0 [options]

[options]
 -m | --mode <MODE>
  モードを指定
   MODE:
    maintainance (default)
     設定変更のためにkeycloakコンテナを起動
    export
     設定をエクスポート
 -h | --help:
   ヘルプを表示

[example]
 メンテナンスモードでkeycloakコンテナを起動
  $0 --mode maintainance
 設定をエクスポート
  $0 --mode export
EOS
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

MODE="maintainance"

while [ "$#" != 0 ]; do
  case $1 in
    -h | --help ) usage;;
    -m | --mode ) shift; MODE="$1";;
    *           ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

if [ "$MODE" != "maintainance" -a "$MODE" != "export" ]; then
  echo "--mode には maintainance, exportのいずれかを指定してください" >&2
  exit 1
fi

export DOCKER_BUILDKIT=1

docker build \
	--rm \
	-f docker/keycloak/Dockerfile \
	-t oidc-tutorial-keycloak:latest \
	.

if [ "$MODE" = "maintainance" ]; then
  CMD="start-dev --http-port=8888"
elif [ "$MODE" = "export" ]; then
  CMD="export --dir /opt/keycloak/data/export --users realm_file --realm oidc-tutorial"
fi

docker run \
	--rm \
  -p 8888:8888 \
	-v $PWD/keycloak-dist:/opt/keycloak/data \
	oidc-tutorial-keycloak:latest \
	$CMD