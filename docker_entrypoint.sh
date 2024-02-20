#!/usr/bin/bash
set -e

if [ -z "${GOOGLE_USERNAME}" ]; then
    echo "Must set environment variable GOOGLE_USERNAME"
    exit 1
fi
if [ -z "${GOOGLE_TOKEN}" ]; then
    echo "Must set environment variable GOOGLE_TOKEN, see https://github.com/davidlang42/gkeep-login"
    exit 1
fi
if [ -z "${GOOGLE_KEEP_LIST_ID}" ]; then
    echo "Must set environment variable GOOGLE_KEEP_LIST_ID"
    exit 1
fi
if [ -z "${GOOGLE_APPS_SCRIPT_URL}" ]; then
    echo "Must set environment variable GOOGLE_APPS_SCRIPT_URL"
    exit 1
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
        if python3 /notify.py "$GOOGLE_USERNAME" "$GOOGLE_TOKEN" "$GOOGLE_KEEP_LIST_ID" "$GOOGLE_APPS_SCRIPT_URL"
        then
            echo ...notify complete.
        else
            echo ...notify failed.
        fi
    fi
    echo Running update...
    if python3 /update.py "$GOOGLE_USERNAME" "$GOOGLE_TOKEN" "$GOOGLE_KEEP_LIST_ID" "$GOOGLE_APPS_SCRIPT_URL"
    then
        echo ...update complete.
    else
        echo ...update failed.
    fi
    sleep "$UPDATE_TIMEOUT" # seconds
done