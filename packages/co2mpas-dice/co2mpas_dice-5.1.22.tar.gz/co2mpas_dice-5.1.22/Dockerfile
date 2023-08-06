FROM debian:buster-slim as base

FROM base as builder

LABEL maintainer="DICE <vinci1it2000@gmail.com>"

# Add library to compile C-code.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev python3-pip gcc libyaml-dev && \
    pip3 install -U pip wheel setuptools --no-cache-dir

# Install DICE requirements.
COPY ./requirements /tmp/dice/requirements
RUN cd /tmp/dice/requirements && pip3 install -r server.pin --no-cache-dir

# Install DICE.
COPY ./co2mpas_dice /tmp/dice/co2mpas_dice
ENV DICE_SERVER='True'
COPY ./setup.py /tmp/dice/setup.py

RUN cd /tmp/dice && \
    python3 setup.py bdist_wheel && \
    WHEEL=$(find /tmp/dice/dist/co2mpas_dice*.whl) && \
    pip3 install $WHEEL --no-dependencies --no-cache-dir

FROM base

COPY --from=builder /usr/local /usr/local

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 libyaml-0-2 && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.7 /usr/bin/python

ENV APP_HOST='0.0.0.0'
ENV APP_PORT='8080'
ENV DICE_BUILD_DIR=/build/dice

USER www-data
EXPOSE 8080

CMD co2mpas_dice server --flask /build/app.ini
