FROM eclipse-temurin:25-jre-noble

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-requests \
    python3-packaging \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt
RUN mkdir -p /srv/mc

COPY scripts/ /opt/scripts
COPY files/ /opt/files

RUN chmod +x /opt/scripts/entrypoint.sh
RUN chmod +x /opt/scripts/install.sh

ENV MC_LOADER="vanilla" \
    MC_VERSION="26.3" \
    EULA="false"

EXPOSE 25565

STOPSIGNAL SIGTERM
ENTRYPOINT ["/opt/scripts/entrypoint.sh"]