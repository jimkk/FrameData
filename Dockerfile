FROM python:3.11-alpine

ADD ./data /data
ADD ./models /models
ADD ./wikis /wikis
ADD main.py .
ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]