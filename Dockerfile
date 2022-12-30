FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /blackjack
WORKDIR /blackjack
COPY . /blackjack/
RUN pip install -r requirements.txt

# gunicorn -b 0.0.0.0:80 -k eventlet -w 1 --reload app:app
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--reload", "app:app"]