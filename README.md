# EZconda

> Manage conda environments, write environment files and create conda lock files

## Create new conda environment
```bash
ezconda create -n new-env
```

## Install packages into environment

```bash
ezconda install -n new-env python=3.9 numpy scipy matplotlib
```

## Developing EZconda

### Run tests

```bash
docker-compose up --build test
```

### Local iterative development

```bash
docker-compose build dev && docker-compose run dev bash
```