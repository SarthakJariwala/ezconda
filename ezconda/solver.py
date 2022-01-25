from enum import Enum


class Solver(str, Enum):
    conda = "conda"
    mamba = "mamba"
