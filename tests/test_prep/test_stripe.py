import cupy as cp
import numpy as np
from httomolib.prep.normalize import normalize_cupy
from httomolib.prep.stripe import (
    remove_stripe_based_sorting_cupy,
    remove_stripes_titarenko_cupy,
)
from numpy.testing import assert_allclose


@cp.testing.gpu
def test_stripe_removal_titarenko_cupy(data, flats, darks):
    # --- testing the CuPy implementation from TomoCupy ---#
    data = normalize_cupy(data, flats, darks, cutoff=10, minus_log=True)
    data_after_stripe_removal = remove_stripes_titarenko_cupy(data).get()

    data = None  #: free up GPU memory
    assert_allclose(np.mean(data_after_stripe_removal), 0.28924704, rtol=1e-05)
    assert_allclose(np.max(data_after_stripe_removal), 2.715983, rtol=1e-05)
    assert_allclose(np.min(data_after_stripe_removal), -0.15378489, rtol=1e-05)


@cp.testing.gpu
def test_stripe_removal_sorting_cupy(data, flats, darks):
    # --- testing the CuPy port of TomoPy's implementation ---#
    data = normalize_cupy(data, flats, darks, cutoff=10, minus_log=True)
    corrected_data = remove_stripe_based_sorting_cupy(data).get()

    data = None  #: free up GPU memory
    assert_allclose(np.mean(corrected_data), 0.288198, rtol=1e-06)
    assert_allclose(np.max(corrected_data), 2.5242403, rtol=1e-07)
    assert_allclose(np.min(corrected_data), -0.10906063, rtol=1e-07)
