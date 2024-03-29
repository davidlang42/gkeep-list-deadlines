FROM ubuntu:latest

# install python
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		bash python3 pip tzdata

# install requirements
RUN pip install gkeepapi

# copy code
COPY --chmod=500 docker_entrypoint.sh /
COPY --chmod=400 update.py /
COPY --chmod=400 notify.py /

# run
ENV TZ="Australia/Sydney"
ENV UPDATE_TIMEOUT=60
ENTRYPOINT [ "/docker_entrypoint.sh" ]