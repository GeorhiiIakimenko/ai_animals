FROM python:3.12-slim

WORKDIR /opt/app

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=3000

# Install software
RUN apt-get update \
  && apt-get install -y \
        gcc \
        python3-dev \
        zlib1g-dev \
        libjpeg-dev

COPY . .
RUN chmod 755 *.py \
    && pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

EXPOSE 3000
CMD ["flask", "run", "--host=0.0.0.0"]
