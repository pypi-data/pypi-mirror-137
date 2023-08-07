"""
Functions to help load fixtures.
"""
import os
import traceback
from pathlib import Path

import pandas as pd


def get_fixture_path(fixture):
    """Given the name of a fixture file, returns path to `../fixtures/fixture`."""
    stack = traceback.extract_stack()
    # Name of file where function was called
    filename = stack[-2].filename
    # Get path to dir two levels up
    my_dir = str(Path(filename).parents[1].resolve())
    # Create absolute path to fixture file
    fixture_path = os.path.join(my_dir, "fixtures", fixture)
    return fixture_path


def load_csv(
    filepath, fixture_path=True, index_tz=None, inferred_freq=False, **kwargs
):
    if fixture_path:
        filepath = get_fixture_path(filepath)
    df = pd.read_csv(filepath, **kwargs)
    try:
        if inferred_freq:
            df.index.freq = df.index.inferred_freq
        if index_tz:
            df.index.tz_convert(index_tz)
    except AttributeError:
        raise AttributeError(
            "In order to perform frequency and timezone alterations on DataFrame "
            "index, the index must be parsed as datetime. Include the `parse_dates` "
            "and `index_col` arguments."
        )
    return df
