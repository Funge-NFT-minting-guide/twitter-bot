FROM python:3

WORKDIR /app

COPY requirements.txt /app
COPY stream.py /app

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["python", "stream.py"]
