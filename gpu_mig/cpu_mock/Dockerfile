FROM python:3
WORKDIR /import_data/api
COPY . /import_data/api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "compute_engine_poll.py"]