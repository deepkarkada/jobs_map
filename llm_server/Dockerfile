FROM python:3.8
COPY requirements.txt /
RUN pip3 install pika && \
    pip install -r /requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5005
CMD [ "python", "-u", "app.py" ]