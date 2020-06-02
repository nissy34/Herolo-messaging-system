FROM python:3.7.3

WORKDIR /usr/src/app

RUN mkdir logs

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-c","gunicorn.conf.py" ,"app:app"]



