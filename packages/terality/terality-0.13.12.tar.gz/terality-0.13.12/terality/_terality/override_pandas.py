from contextlib import contextmanager
import pandas as pd
import terality as te


_pd_functions_to_override = ["isna"]


@contextmanager
def override_pandas_in_external_libs():
    original_pd_functions = {}
    for pd_function in _pd_functions_to_override:
        original_pd_functions[pd_function] = pd.__dict__[pd_function]
        pd.__dict__[pd_function] = te.__getattr__(pd_function)
    try:
        yield
    finally:
        for pd_function_name, pd_function_value in original_pd_functions.items():
            pd.__dict__[pd_function_name] = pd_function_value
