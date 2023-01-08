ARG INSTALL_PYTHON_VERSION=3.10

# ================================= BASE =================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster as production
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/backend.txt
RUN pip3 install -r requirements/cli.txt
RUN pip3 install -r requirements/data.txt
RUN pip install --no-cache --user -r requirements/data.txt

COPY . /app
EXPOSE 8000