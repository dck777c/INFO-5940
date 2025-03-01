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

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /workspace

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --all-extras

EXPOSE 8501

FROM base as devcontainer

WORKDIR /workspace

COPY . .

CMD ["poetry", "run", "streamlit", "run", "chat_with_pdf.py"]
