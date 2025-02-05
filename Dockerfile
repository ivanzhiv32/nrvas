FROM python:3.12.8

COPY . .

RUN pip install .

CMD python -m app
