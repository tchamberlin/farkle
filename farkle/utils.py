import logging
from time import perf_counter


class Benchmark:
    def __init__(self, description=None, logger=None):
        self._initial_time = perf_counter()
        self._logger = logger if logger else print
        self.description = "Did stuff" if description is None else description

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        _end = perf_counter()
        self._logger(f"{self.description} in {_end - self._initial_time:.3f} seconds ")


def init_logging(logger, verbosity):
    """Initialize logging based on requested verbosity"""
    if verbosity > 2:
        loglevel = logging.DEBUG
    elif verbosity == 2:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)
    logger.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    # See: https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
