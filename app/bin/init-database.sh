#!/bin/bash
set -ex

APP_ROOT=$(cd $(dirname $0)/..; pwd)
ALEMBIC_DIR="${APP_ROOT}/alembic"

# データベース削除
MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h $DB_HOST -P $DB_PORT -e "DROP DATABASE IF EXISTS $DB_NAME"

# データベース作成
MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h $DB_HOST -P $DB_PORT -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"

cd $ALEMBIC_DIR

# マイグレーション
alembic upgrade head