FROM mozmeao/base:python-3.6

WORKDIR /app
CMD ["./update_releases.py"]

COPY requirements.txt ./
RUN pip install -r requirements.txt
