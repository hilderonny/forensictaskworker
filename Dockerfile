FROM python:3.12.4-slim-bookworm

WORKDIR /app

COPY . /app

RUN mkdir -p /app/argosmodels/packages

RUN pip install -r requirements.txt

RUN python argosupdate.py --argospath /app/argosmodels

ENV APIURL http://127.0.0.1/api/

CMD [ "python", "texttranslator.py", "--apiurl", ${APIURL}, "--argospath", "/app/argosmodels" ]