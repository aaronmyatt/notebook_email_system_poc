FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
RUN pip install pipenv
WORKDIR /code
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN pipenv install
ADD . /code/