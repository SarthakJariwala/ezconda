FROM continuumio/miniconda3

RUN conda install pip typer PyYaml pytest pytest-cov

COPY . /ezconda

WORKDIR /ezconda

RUN pip install . --no-deps

CMD ["pytest", "--cov=ezconda"]