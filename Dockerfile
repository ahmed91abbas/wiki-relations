FROM python:3-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY /src /src

WORKDIR /src

ENTRYPOINT ["python3"]

CMD ["main.py"]
