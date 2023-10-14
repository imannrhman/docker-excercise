FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY data_ingestion_script.py data_ingestion_script.py
CMD ["python", "-u", "data_ingestion_script.py"]