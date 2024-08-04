#!/bin/bash

function usage {
cat >&2 <<EOS
開発環境でアプリを起動するコマンド

[usage]
 $0
   (デフォルト)CSRFなどの脆弱性を対策していないモードで起動
 $0 --vuln-responsed
   CSRFなどの脆弱性を対策済みのモードで起動

[options]
 -h | --help:
   ヘルプを表示
 --vuln-responsed:
   フロントエンドでkeycloakのライブラリを利用し、CSRFなど脆弱性に対策したモードで起動
EOS
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

ENV_PATH="${PROJECT_ROOT}/local.env"
USER_ID=$(id -u)
GROUP_ID=$(id -g)
VULN_RESPONSED=
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    --vuln-responsed ) VULN_RESPONSED=1;;
    -* | --*         ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

export $(cat $ENV_PATH | grep -v -e "^ *#")

# Dockerイメージを複数生成するためビルド処理を関数化
build_image() {
  DOCKERFILE_PATH="$1"
  DOCKER_IMAGE_TAG="$2"

  docker build \
    --build-arg host_uid=$USER_ID \
    --build-arg host_gid=$GROUP_ID \
    --rm \
    -f $DOCKERFILE_PATH \
    -t $DOCKER_IMAGE_TAG \
    .
}

export DOCKER_BUILDKIT=1
build_image "docker/api/Dockerfile" "oidc-tutorial-api:latest"
build_image "docker/nginx/Dockerfile" "oidc-tutorial-nginx:latest"
build_image "docker/keycloak/Dockerfile" "oidc-tutorial-keycloak:latest"
build_image "docker/csrf_nginx/Dockerfile" "oidc-tutorial-csrf-nginx:latest"

if [ -n "$VULN_RESPONSED" ]; then
  FRONT_SRC_DIR="${PROJECT_ROOT}/app/front/vuln_responsed/.output/public"
else
  FRONT_SRC_DIR="${PROJECT_ROOT}/app/front/default/.output/public"
fi

LOCAL_APP_DIR="${PROJECT_ROOT}/app"

export FRONT_SRC_DIR="$FRONT_SRC_DIR"
export LOCAL_APP_DIR="$LOCAL_APP_DIR"
export ENV_PATH="$ENV_PATH"

cd "${PROJECT_ROOT}/docker"
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up