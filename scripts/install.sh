#!/bin/bash

cd /srv/mc

if [ "$MC_LOADER" == "folia" ]; then
    file_name=$(python3 /opt/scripts/mcfetch.py --use-folia paper ${MC_VERSION} | awk -F'|' '{print $NF}')
else
    file_name=$(python3 /opt/scripts/mcfetch.py ${MC_LOADER} ${MC_VERSION} | awk -F'|' '{print $NF}')
fi

if [ "$MC_LOADER" == "folia" ]; then
    python3 /opt/scripts/mcfetch.py --download --use-folia paper ${MC_VERSION}
else
    python3 /opt/scripts/mcfetch.py --download ${MC_LOADER} ${MC_VERSION}
fi


if [ "$MC_LOADER" == "forge" ]; then
    java -jar ${file_name} --installServer
elif [ "$MC_LOADER" == "fabric" ]; then
    java -jar ${file_name} server -mcversion ${MC_VERSION} -downloadMinecraft nogui
    ln -s fabric-server-launcher.jar launch.jar
elif [ "$MC_LOADER" == "neoforge" ]; then
    java -jar ${file_name} --install-server
else
    ln -s ${file_name} launch.jar
fi


if [ ! -f run.sh ]; then
    cp /opt/scripts/run.sh .
fi

sed -i "s/java @user_jvm_args.txt/exec java @user_jvm_args.txt/" run.sh
chmod +x run.sh