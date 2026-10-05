#!/bin/bash

cd /srv/mc

if [ -f run.sh ]; then
    exec /srv/mc/run.sh
else
    /opt/scripts/install.sh

    cp -rf /opt/files/. .
    echo "eula=${EULA:-false}" >> eula.txt

    if [ -n "${MEM_MAX:-}" ]; then
        echo "-Xmx${MEM_MAX}" >> user_jvm_args.txt
    fi
    if [ -n "${MEM_MIN:-}" ]; then
        echo "-Xms${MEM_MIN}" >> user_jvm_args.txt
    fi
    exit 0
fi