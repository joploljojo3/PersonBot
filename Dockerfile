FROM python:3.12-slim

WORKDIR /app

ARG CONFIG=config.json
ENV CONFIG=${CONFIG}

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD ["sh", "-c", "python3 main.py $CONFIG"]