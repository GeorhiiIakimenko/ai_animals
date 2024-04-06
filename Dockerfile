FROM nvidia/cuda:11.0.3-base

WORKDIR /opt/app

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=3000

# Install softwar
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub \
  && apt-get update \
  && apt-get install -y \
        gcc \
  python3 \
  python3-pip \
        python3-dev \
        zlib1g-dev \
        libjpeg-dev

COPY . .
RUN chmod 755 *.py \
    && pip install -r requirements.txt

EXPOSE 3000
CMD ["flask", "run", "--host=0.0.0.0"]

