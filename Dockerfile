# Use full Lizmap Web Client (includes QGIS Server and Web UI)
FROM 3liz/lizmap-web-client:3.8.10

# Copy Lizmap server plugin
COPY ./plugins /srv/plugins

# Copy QGIS projects
COPY ./projects /srv/projects

# Optional: WPS data and configuration
#COPY ./wps-data /srv/data
#COPY ./etc /srv/etc

ENTRYPOINT [ "/entrypoint.sh" ]


