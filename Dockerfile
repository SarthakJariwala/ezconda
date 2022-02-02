FROM continuumio/miniconda3

RUN conda install -c conda-forge mamba pip typer PyYaml pytest pytest-cov rich tomlkit

COPY . /ezconda

WORKDIR /ezconda

RUN pip install . --no-deps

CMD ["pytest", "--cov=ezconda"]