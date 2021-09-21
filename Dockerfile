FROM continuumio/miniconda3

COPY . /ezconda
WORKDIR /ezconda

RUN conda install pip typer PyYaml pytest pytest-cov
RUN pip install .

CMD ["pytest", "--cov=ezconda"]