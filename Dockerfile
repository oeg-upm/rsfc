FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /rsfc

RUN git clone https://github.com/oeg-upm/rsfc.git .

RUN poetry install --no-root

RUN poetry run pip install .

RUN poetry run python -m nltk.downloader wordnet

RUN poetry run somef configure -a

RUN mkdir -p /rsfc/outputs

ENTRYPOINT ["poetry", "run", "rsfc"]
