#!/usr/bin/env bash
# `wait-for-it.sh` is a script that waits for a service to be up.
# It will exit once the service is ready.

TIMEOUT=60

while ! nc -z $1 $2; do
  echo "Waiting for $1:$2..."
  TIMEOUT=$((TIMEOUT-1))
  if [ $TIMEOUT -le 0 ]; then
    echo "Service $1:$2 did not become ready in time."
    exit 1
  fi
  sleep 1
done

echo "Service $1:$2 is up!"
