FROM --platform=linux/amd64 python:3.12.2-slim-bullseye

ENV PYTHONBUFFERED=1
ENV PORT 8080

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${PORT}

CMD [ "python", "manage.py", "runserver", "0.0.0.0:${PORT}"]