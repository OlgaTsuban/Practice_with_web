FROM python:3.11-slim

# Встановимо змінну середовища
#ENV DISPLAY=host.docker.internal:0
ENV APP_HOME /app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Встановлюємо залежності в середовищі pipenv
COPY Pipfile .
#RUN python -m pip install --upgrade pip && pip install pipenv
RUN python -m pip install --upgrade pip
# Встановлюємо бібліотеки Tkinter
#RUN apt-get update && apt-get install -y python3-tk
#RUN apt-get update && apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libtk8.6 x11-apps xvfb

ENV DISPLAY=:99

# Копіюємо весь вміст нашого проекту у контейнер
COPY ./crutching_botdan ./crutching_botdan


CMD Xvfb :99 -ac -screen 0 1024x768x16 & python crutching_botdan/main.py