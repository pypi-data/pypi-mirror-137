__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"


import numpy as np
import pandas as pd
import sys
import os
import inspect
import pytest
import pdb
# currentdir = \
#     os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
import characterization_ams.unittests.datasets as datasets
from characterization_ams.unittests import image_generator
from characterization_ams.stats_engine import stats
from characterization_ams.emva import emva
import pathlib
# load synthetic dataset
data = pd.read_csv(pathlib.Path(datasets.__file__).parents[0]/'test_emva.csv')


# generate dsnu and prnu images
ped_start = 168
peds = np.linspace(168, 3800, 30)
peds = [168, peds[peds.shape[0]//2]]
power = np.linspace(0, 10, 30)
rows = 100
cols = 100
pedestal = 168
n_images = 1000
images = []
temp = pd.DataFrame()
raw = pd.DataFrame()
for (idx, pp) in enumerate(peds):
    n_images = 1000
    rfpn = 4
    cfpn = 1
    ctn = 15
    rtn = 12
    ptn = 20 + np.sqrt(pp)
    pfpn = 5 + 0.08 * (pp - ped_start)

    tot_t = np.sqrt(ctn**2 + rtn**2 + ptn**2)
    tot_f = np.sqrt(rfpn**2 + pfpn**2 + cfpn**2)

    # fpn
    imgs = image_generator.gen_images(cfpn=cfpn,
                                      rfpn=rfpn,
                                      pfpn=pfpn,
                                      rtn=rtn,
                                      ptn=ptn,
                                      ctn=ctn,
                                      rows=rows,
                                      cols=cols,
                                      pedestal=pp,
                                      n_images=n_images)

    images.append(imgs)

# data structures
emva_summ = pd.DataFrame()
emva_data = pd.DataFrame()
emva_hist = pd.DataFrame()

# starting required metrics
wl = 550  # nm
texp = 16  # ms
power = data.Power
pixel_area = 0.95 * 0.95  # [um^2]
emva_data = data[['tot_var_temp', 'tot_var_temp - dark_tot_var_temp',
                  'mean - dark_mean']]
emva_data.rename(columns={'tot_var_temp - dark_tot_var_temp':
                          'tot_var_temp-dark_tot_var_temp',
                          'mean - dark_mean':
                          'mean-dark_mean'}, inplace=True)


# system gain
def test_system_gain():
    """
    """

    val_dict =\
        emva.system_gain(u_y=emva_data['mean-dark_mean'],
                         sig2_y=emva_data['tot_var_temp-dark_tot_var_temp'])

    sys_gain = val_dict['system_gain']
    emva_summ['system_gain'] = pd.Series(sys_gain)

    assert round(sys_gain, 1) == 1.6


# get photons
def test_get_photons():
    """
    """

    val_dict = emva.get_photons(wl=wl,
                                texp=texp,
                                power=power,
                                pixel_area=pixel_area)

    photons = val_dict['u_p']

    assert round(photons.iloc[-1], 0) == 4006


def test_dark_temporal_noise():
    """
    """

    val_dict = \
        emva.dark_temporal_noise(sig2_ydark=emva_data['tot_var_temp'].iloc[0],
                                 K=emva_summ['system_gain'].iloc[0])

    dtn = val_dict['dark_temporal_noise_e']

    assert round(dtn, 1) == 23.7


def test_dsnu1288():
    """
    """

    ttn_var = data['tot_var_temp'].iloc[0]
    dark_img = stats.avg_img_stack(images[0])
    L = n_images

    dsnu = emva.dsnu1288(dark_img=dark_img,
                         ttn_var=ttn_var,
                         L=L)

    assert round(dsnu['total_dsnu'], 0) == 6
    assert round(dsnu['row_dsnu'], 0) == 4
    assert round(dsnu['col_dsnu'], 0) == 1
    assert round(dsnu['pix_dsnu'], 0) == 5


def test_dsnu1288_stack():
    """
    """

    # required inputs
    dark_imgs = images[0]

    # calculate dsnu1288
    dsnu = emva.dsnu1288_stack(img_stack=dark_imgs)

    assert round(dsnu['total_dsnu'], 0) == 6
    assert round(dsnu['row_dsnu'], 0) == 4
    assert round(dsnu['col_dsnu'], 0) == 1
    assert round(dsnu['pix_dsnu'], 0) == 5


def test_dynamic_range():
    """
    """
    pass


def test_get_electrons():
    """
    """
    pass


def test_histogram1288():
    """
    """
    pass


def test_histogram1288_stack():
    """
    """
    pass


def test_linearity():
    """
    """
    pass


def test_prnu1288():
    """
    """
    pass


def test_prnu1288_stack():
    """
    """
    pass


def test_profiles():
    """
    """
    pass


def test_responsivity():
    """
    """
    pass


def test_saturation_capacity():
    """
    """
    pass


def test_sensitivity_threshold():
    """
    """
    pass


def test_snr():
    """
    """
    pass


def test_snr_stacK():
    """
    """
    pass


def test_snr_ideal():
    """
    """
    pass


def test_snr_photons():
    """
    """
    pass


def test_snr_theoretical():
    """
    """
    pass


def test_spatial_variance():
    """
    """
    pass


def test_spectrogram():
    """
    """
    pass


def test_spectogram_stack():
    """
    """
    pass
