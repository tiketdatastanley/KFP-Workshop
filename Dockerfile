FROM asia-docker.pkg.dev/tk-test-data/kubebuild/base_image/gcloud:1.11.0

RUN apt-get update && apt-get -y install build-essential

RUN pip install --upgrade pip

WORKDIR /usr/workshop

COPY requirements.txt /usr/workshop/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . /usr/workshop

ENV PYTHONPATH=$PYTHONPATH:/usr/workshop/src