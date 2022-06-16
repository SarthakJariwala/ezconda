try:
    from importlib.metadata import version  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version  # type: ignore


__version__ = version(__name__)
