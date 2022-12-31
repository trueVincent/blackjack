FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /blackjack
WORKDIR /blackjack
COPY . /blackjack/
RUN pip install -r requirements.txt