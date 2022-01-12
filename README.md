# EZconda

![EZconda](https://github.com/SarthakJariwala/ezconda/blob/2945291bc9ef123cb52e9c6436906ac0728b0451/docs/logo.png)

<p align="center">
    <a href="https://github.com/SarthakJariwala/ezconda/actions?workflow=Tests">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Tests/badge.svg">
    </a>
    <a href="https://codecov.io/gh/SarthakJariwala/ezconda">
        <img src="https://codecov.io/gh/SarthakJariwala/ezconda/branch/main/graph/badge.svg">
    </a>
    <a href="https://pypi.org/project/ezconda/">
        <img src="https://img.shields.io/pypi/v/ezconda.svg">
    </a>
    <a href="https://ezconda.sarthakjariwala.com">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Docs/badge.svg">
    </a>
</p>

<p align="center">
    <em><b>Create, Manage, Re-create</b> conda environments & specifications with ease.</em>
</p>

---

**EZconda** is a command line interface application that helps practitioners to create and manage `conda` environment and related specifications with ease.

## Key Features

- **Environment specifications** : Add & remove packages from the <abbr title="commonly known as environment.yml file">specifications file</abbr> as you install & remove packages. _**No manual file edits!**_

- **Environment management** : Create & manage `conda` environments with ease.

- **Reproducible environments** : Lock current environment state and re-create it when necessary.

- **Easy to use & intuitive** : It very closely mimics `conda` API, so there is no new API to learn for users. Autocomplete for all shells.

- **Best practices built-in** : Enforces the user to follow best `conda` practices.

## Requirements

- Python 3.6+
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installation

## Installation

The recommended way to install **EZconda** is using `conda` and in the `base` environment : 

```console
$ conda install ezconda -c conda-forge
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