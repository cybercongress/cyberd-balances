FROM python:3.6

ADD ./requirements.txt .
RUN pip install -r ./requirements.txt
ADD ./extractor.py .
ADD ./google-big-query-key.json .

CMD ["python", "/extractor.py"]