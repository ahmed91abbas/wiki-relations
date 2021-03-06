FROM python:3.8-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY /src /src

WORKDIR /src

ENTRYPOINT ["python3"]

CMD ["main.py"]
