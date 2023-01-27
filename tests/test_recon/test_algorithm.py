import numpy as np
import pytest
from numpy.testing import assert_allclose

from httomolib.recon.algorithm import reconstruct_tomobar, reconstruct_tomopy

from tomopy.prep.normalize import normalize

in_file = 'tests/test_data/tomo_standard.npz'
datafile = np.load(in_file)
host_data = datafile['data']
host_flats = datafile['flats']
host_darks = datafile['darks']


def test_reconstruct_methods():
    cor = 79.5 #: center of rotation for tomo_standard
    data = normalize(host_data, host_flats, host_darks, cutoff=15.0)
    angles = np.linspace(0. * np.pi / 180., 180. * np.pi / 180., data.shape[0])

    #--- reconstructing the data ---#
    recon_data = reconstruct_tomobar(data, angles, cor, algorithm="FBP3D_host")
    recon_data_tomopy = reconstruct_tomopy(data, angles, cor, algorithm="FBP_CUDA")
    assert recon_data.shape == (128, 160, 160)

    for _ in range(3):
        assert_allclose(np.mean(recon_data), -0.00047175083, rtol=1e-07)
        assert_allclose(np.std(recon_data), 0.0034436132, rtol=1e-07)

    for _ in range(3):              
        assert_allclose(np.mean(recon_data_tomopy), 0.008697214, rtol=1e-07)
        assert_allclose(np.std(recon_data_tomopy), 0.009089365, rtol=1e-07)
