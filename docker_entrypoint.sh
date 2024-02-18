#!/bin/bash
set -e

# check environment variables
if [ -z "${GOOGLE_USERNAME}" ]; then
    echo "Must set environment variable GOOGLE_USERNAME"
    exit 1 # failed
fi
if [ -z "${GOOGLE_TOKEN}" ]; then
    echo "Must set environment variable GOOGLE_TOKEN, see https://github.com/davidlang42/gkeep-login"
    exit 1 # failed
fi
if [ -z "${GOOGLE_KEEP_LIST_ID}" ]; then
    echo "Must set environment variable GOOGLE_KEEP_LIST_ID"
    exit 1 # failed
fi

set -u

LAST_DATE=""
while true
do
    THIS_DATE="$(date -d "00:00")"
    if [ "$THIS_DATE" != "$LAST_DATE" ]
    then
        LAST_DATE="$THIS_DATE"
        echo Running notify...
        if python3 /notify.sh "$GOOGLE_USERNAME" "$GOOGLE_TOKEN" "$GOOGLE_KEEP_LIST_ID"
        then
            echo ...notify complete.
        else
            echo ...notify failed.
        fi
    fi
    echo Running update...
    if python3 /update.sh "$GOOGLE_USERNAME" "$GOOGLE_TOKEN" "$GOOGLE_KEEP_LIST_ID"
    then
        echo ...update complete.
    else
        echo ...update failed.
    fi
    sleep 300 # 5min
done