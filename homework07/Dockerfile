FROM python:3.9

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY src /api
WORKDIR /api

ENTRYPOINT ["python"]
CMD ["worker.py"]
