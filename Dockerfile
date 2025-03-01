FROM public.ecr.aws/docker/library/python:3.11-slim-bookworm as base

RUN apt-get update && apt-get install -y \
   curl \
   git \
   unzip \
   vim \
   wget \
   gcc \
   g++ \
   make \
   python3-dev \
   libffi-dev \
   libssl-dev \
   poppler-utils \
   && rm -rf /var/lib/apt/lists/* \
   && apt-get clean

RUN pip install --no-cache "poetry>1.7,<1.8"
RUN poetry config virtualenvs.create false

WORKDIR /workspace

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --all-extras

RUN pip install --no-cache PyMuPDF==1.24.11 chromadb==0.5.13 streamlit

COPY . .

CMD ["tail", "-f", "/dev/null"]
