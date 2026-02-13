FROM python:3.9

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        git \
        htop \
        make \
        tzdata \
        vim \
        && \
        rm -rf /var/lib/apt/lists/*

# set time zone
ENV TZ America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /api
COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app:app"]
