# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 6969

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Install libraries
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y default-jre
RUN apt-get install -y default-jdk
RUN apt-get install -y zip unzip

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "6969"]

# To test locally, run `docker build -t api .` and then `docker run -p 6969:6969 --env-file=<PATH_TO_YOUR_ENVIRONMENT_FILE> api`