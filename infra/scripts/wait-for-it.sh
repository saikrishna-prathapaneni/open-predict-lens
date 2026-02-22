#!/usr/bin/env sh
host="$1"
shift
until nc -z "$host" "$1"; do
  sleep 1
done
shift
exec "$@"
