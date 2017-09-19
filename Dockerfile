FROM python:3.6-slim

# Set Python-related environment variables to reduce annoying-ness
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV LANG C.UTF-8

WORKDIR /app
CMD ["./update_releases.py"]

COPY requirements.txt ./
RUN pip install -r requirements.txt
