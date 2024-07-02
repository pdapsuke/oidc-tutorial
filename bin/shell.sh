#!/bin/bash

function usage {
cat >&2 <<EOS
開発環境でシェルを起動するコマンド

[usage]
 $0
  開発用シェルを起動（default）

[options]
 -h | --help:
   ヘルプを表示
EOS
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

ENV_PATH="${PROJECT_ROOT}/local.env"
USER_ID=$(id -u)
GROUP_ID=$(id -g)
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help   ) usage;;
    -* | --*      ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

export DOCKER_BUILDKIT=1
docker build \
  --build-arg host_uid=$USER_ID \
  --build-arg host_gid=$GROUP_ID \
  --rm \
  -f docker/shell/Dockerfile \
  -t oidc-tutorial:latest \
  .

LOCAL_APP_DIR="${PROJECT_ROOT}/app"

docker run \
	--rm \
	-ti \
	--network host \
  --env-file $ENV_PATH \
  -v $LOCAL_APP_DIR:/opt/app \
	-w /opt/app \
	--user="$USER_ID:$GROUP_ID" \
	oidc-tutorial:latest \
	"/bin/bash"