FROM python:3.11-slim

# Install system packages for SDL and GUI
RUN apt-get update && \
    apt-get install -y \
    python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    xvfb \
    x11-xserver-utils \
    && pip install pygame \
    && apt-get clean
RUN apt-get -y install make
RUN mkdir -p /tmp/runtime

WORKDIR /app
COPY . /app
RUN make install

CMD [ "sh", "./docker/entrypoint.sh" ]