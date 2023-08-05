__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"

import numpy as np
import pandas as pd
import pdb
from characterization_ams.stats_engine import stats
from characterization_ams.emva import emva
from characterization_ams.utilities import utilities as ut


def get_stats(images, temp_imgs, L, df=pd.DataFrame(), rmv_ttn=False, hpf=True):
    """
    calculate all statistics per EMVA 4.0 definition

    Keyword Arguments:
        images (list): list of images where each element is array
                       with dim (num_images, width, height)
        df (pd.DataFrame): DataFrame of parameters associated with each image
                           in image stack, right now it is assumed DataFrame
                           index corresponds to indx of images
        rmv_ttn (bool): if True subtract off residual temporal noise
        hpf (bool): if true high pass filter image prior to spatial variance calc
    Returns:
        data (pd.DataFrame): DataFrame of all statistics with updated
                             column names and a column with black level
                             subtracted for each metric
    """

    data = pd.DataFrame()

    # calculate all noise metrics using stats engine
    for idx, im in enumerate(images):
        ttn_var = stats.frame_avg(temp_imgs[idx])
        stat_vals = stats.noise_metrics(im, L=L,
                                        ttn_var=ttn_var,
                                        rmv_ttn=rmv_ttn,
                                        hpf=hpf)

        temp = \
            pd.DataFrame(dict([(k, pd.Series(v)) for
                         k, v in stat_vals.items()]))
        temp['tot_var_temp'] = stats.frame_avg(temp_imgs[idx])
        temp['mean'] = stats.frame_avg(images[idx])
        data = pd.concat([data, temp]).reset_index(drop=True)

    # get data columns
    data_cols = data.columns.tolist()

    # if df of conditions was passed join with data
    if not df.empty:
        overlap_cols = [c for c in data.columns if c in df.columns]
        if any(overlap_cols):
            print(f'overlapping column names exist: {overlap_cols}')
            print('passed overlapping columns will be renamed as:"<col>_pcol"')
            data = data.join(df.reset_index(drop=True),
                             rsuffix='_pcol')
        else:
            data = data.join(df.reset_index(drop=True))

    data = data.sort_values(by='mean').reset_index(drop=True)

    # get black level subtracted columns
    data = ut.remove_black(data, data_cols)

    # rename noise metric columns
    data.rename(columns=ut.stat_engine_col_rename(), inplace=True)

    # add noise ratios, no row/col temp due to avg ims
    data['CFPN Ratio'] = \
        np.sqrt(data['Tot Temp Var [DN^2]']) /\
        np.sqrt(data['Col Var [DN^2]'])
    data['RFPN Ratio'] = \
        np.sqrt(data['Tot Temp Var [DN^2]']) /\
        np.sqrt(data['Row Var [DN^2]'])
    data['STN Ratio'] = \
        np.sqrt(data['Tot Var [DN^2]']) /\
        np.sqrt(data['Tot Temp Var [DN^2]'])
    
    # add fpn as % signal
    data['Pix FPN [%]'] = \
        np.sqrt(data['Pix Var [DN^2]']) /\
        data['Signal - Dark [DN]'] * 100
    data['Tot FPN [%]'] = \
        np.sqrt(data['Tot Var [DN^2]']) /\
        data['Signal - Dark [DN]'] * 100
    data['Col FPN [%]'] = \
        np.sqrt(data['Col Var [DN^2]']) /\
        data['Signal - Dark [DN]'] * 100
    data['Row FPN [%]'] = \
        np.sqrt(data['Row Var [DN^2]']) /\
        data['Signal - Dark [DN]'] * 100

    # get rid of inf values
    data = data.replace(np.inf, 0)

    return data

def ptc(images,
        temp_imgs,
        L,
        df,
        exp_col='Exposure [uW/cm^2*s]',
        exp_col_units='[uW/cm^2]',
        interp_exp=True,
        image_idx_col='Image Index',
        rmv_ttn=False,
        hpf=False):
    """
    calculate all PTC metrics using emva functions, but does
    not require QE, pixel pitch, or wl, assumes that first image
    in list of images is dark image

    Keyword Arguments:
        images (list): list of images where each element is array
                       with dim (num_images, width, height)
        df (pd.DataFrame): DataFrame of parameters associated with each image
                           in image stack, right now it is assumed DataFrame
                           index corresponds to indx of images
        exp_col (str): column within df to be used for exposure calculations
        exp_col_units (str): exposure column units to be used for responsivity label
        image_idx_col (str): column denoting image index within images list
        rmv_ttn (bool): if True subtract off residual temporal noise
        hpf (bool): if true high pass filter image prior to spatial variance calc

    Returns:
    Returns:
        data (pd.DataFrame): DataFrame of all EMVA response metrics + noise metrics
        hist (pd.DataFrame): DataFrame of all EMVA spatial metrics
        summ (pd.DataFrame): DataFrame of all EMVA summary metrics

    TODO: need another dynamic range function that doesn't require photons
    TOOD: Add support for saving average frame
    """

    data = pd.DataFrame()
    hist = pd.DataFrame()
    summ = pd.DataFrame()
    temp = pd.DataFrame()

    # get statistics and join image data with params
    data = get_stats(images, temp_imgs, L, df, rmv_ttn=rmv_ttn, hpf=hpf)

    # get values needed for all emva funtions
    u_y = data['Signal - Dark [DN]']
    sig2_y = data['Tot Temp Var - Tot Dark Temp Var [DN^2]']
    sig2_ydark = data['Tot Temp Var [DN^2]'].iloc[0]
    exp = data[exp_col]

    # get halfsat interp
    m = np.argmax(exp)
    m_ = m - 1
    ma_ = m + 2
    if interp_exp:
        u_ys = [u_y.values[m_], u_y.values[ma_]]
        exps = [exp[m_], exp[ma_]]
        val = np.interp(u_y[m], u_ys, exps)
        exp.replace(exp[m], val, inplace=True)
        data[exp_col] = exp

    # get required images and averages
    idx = data[image_idx_col].iloc[np.argmin(u_y)]
    idx -= data[image_idx_col].min()
    dark_avg_img = images[np.argmin(u_y)]
    half_sat = u_y.max() / 2
    idx = data[image_idx_col].iloc[ut.find_closest(u_y, half_sat)]
    idx -= data[image_idx_col].min()
    try:
        half_sat_avg_img = images[idx-1]
    except:
        pdb.set_trace()
    prnu_img = half_sat_avg_img - dark_avg_img
    dark_ttn_var = temp_imgs[0].mean()
    light_ttn_var = temp_imgs[idx-1].mean()

    # get system gain
    sys_gain = emva.system_gain(u_y=u_y,
                                sig2_y=sig2_y)

    data['System Gain Fit [DN^2]'] = sys_gain['fit']
    summ['System Gain [DN/e]'] = pd.Series(sys_gain['system_gain'])
    summ['Conversion Factor [e/DN]'] = 1 / sys_gain['system_gain']
    K = sys_gain['system_gain']

    # get all noise metrics in e
    keysd = ut.stat_engine_col_rename()
    for kk in keysd:
        val = keysd[kk]
        if val not in data.columns.tolist():
            continue
        if 'DN^2' in val:
            val2 = val.replace('[DN^2]', '[e^2]')
            data[val2] = data[val] / K**2
        else:
            val2 = val.replace('[DN]', '[e]')
            data[val2] = data[val] / K
    # get dark temporal Noise
    dtn = emva.dark_temporal_noise(sig2_ydark=sig2_ydark,
                                   K=K)

    summ['Dark Noise [e]'] = dtn['dark_temporal_noise_e']
    summ['Dark Noise [DN]'] = dtn['dark_temporal_noise_DN']

    # get DSNU1288 (pix, row, col, total)
    dsnu = emva.dsnu1288(dark_avg_img,dark_ttn_var, L)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dsnu.items()]))
    for cc in temp.columns:
        col_name = cc + ' [DN]'
        temp.rename(columns={cc: col_name}, inplace=True)
        col_name_e = cc + ' [e]'
        temp[col_name_e] = temp[col_name] / K

    # add dsnu info to summ
    summ = summ.join(temp)

    # get electrons
    ele = emva.get_electrons(u_y=u_y,
                             K=K)

    data['Mean Signal [e]'] = ele['u_e']

    # add prnu1288 histogram
    prnu_hist = emva.histogram1288(img=prnu_img,
                                   Qmax=256,
                                   L=L,
                                   black_level=False)

    hist['PRNU1288 Number of Pixels/Bin'] = pd.Series(prnu_hist['bins'])
    hist['PRNU1288 Deviation from Mean [DN]'] = pd.Series(prnu_hist['values'])
    hist['PRNU1288 Model'] = pd.Series(prnu_hist['model'])
    hist['PRNU1288 Percentage of Pixels/Bin'] = \
        pd.Series(prnu_hist['accumulated bins'])
    hist['PRNU1288 Accumulated Deviation from Mean [DN]'] = \
        pd.Series(prnu_hist['accumulated values'])

    # add dsnu1288 histogram
    dsnu_hist = emva.histogram1288(img=dark_avg_img,
                                         Qmax=256,
                                         L=10,
                                         black_level=True)

    hist['DSNU1288 Number of Pixels/Bin'] = pd.Series(dsnu_hist['bins'])
    hist['DSNU1288 Deviation from Mean [DN]'] = pd.Series(dsnu_hist['values'])
    hist['DSNU1288 Model'] = pd.Series(dsnu_hist['model'])
    hist['DSNU1288 Percentage of Pixels/Bin'] = \
        pd.Series(dsnu_hist['accumulated bins'])
    hist['DSNU1288 Accumulated Deviation from Mean [DN]'] = \
        pd.Series(dsnu_hist['accumulated values'])

    # add linearity error
    lin = emva.linearity(mean_arr=u_y,
                         exp_arr=exp,
                         ttn_arr=sig2_y)

    data[exp_col] = data[exp_col]
    data['linearity_fit_DN'] = lin['linearity_fit_DN']
    data['linearity_error_%'] = lin['linearity_error_%']
    data['linearity_error_DN'] = lin['linearity_error_DN']
    summ['linearity_error_max_%'] = lin['linearity_error_max_%']
    summ['linearity_error_max_DN'] = lin['linearity_error_max_DN']
    summ['linearity_error_min_%'] = lin['linearity_error_min_%']
    summ['linearity_error_min_DN'] = lin['linearity_error_min_DN']

    # add PRNU1288
    prnu = emva.prnu1288(dark_avg_img, half_sat_avg_img, dark_ttn_var, light_ttn_var, L)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prnu.items()]))

    # add prnu info to summ
    summ = summ.join(temp)

    # add DSNU profiles
    prof = emva.profiles(dark_avg_img)
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prof.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'DSNU1288 ' + cc + ' [DN]'}, inplace=True)

    # add profiles to hist
    hist = hist.join(temp, how='right')

    # add PRNU profiles
    prof = emva.profiles(half_sat_avg_img)
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prof.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'PRNU1288 ' + cc + ' [DN]'}, inplace=True)

    # add profiles to hist
    hist = hist.join(temp, how='right')

    # calculate responsivity using exp_col
    resp = emva.responsivity(u_p=data[exp_col],
                             u_y=u_y,
                             sig2_y=sig2_y)

    data['Responsivity Fit [DN]'] = resp['responsivity_fit']
    summ[f'Responsivity [DN/({exp_col_units})]'] = resp['responsivity']

    # calulcate saturation capacity
    sat = emva.saturation_capacity(u_p=data['Mean Signal [e]'],
                                   sig2_y=sig2_y,
                                   qe=1)

    # not a mistake here..hacking emva sat capacity function
    # for sat capacity in without use of photons column
    summ['sat_capacity_e'] = sat['sat_capacity_p']
    summ['sat_capacity_DN'] = summ['sat_capacity_e'] * K

    # calculate sensitivity threshold
    sen = emva.sensitivity_threshold(sig2_ydark=sig2_ydark,
                                     qe=1,
                                     K=K)

    summ['sensitivity_threshold_e'] = sen['sensitivity_threshold_e']
    summ['sensitivity_threshold_DN'] = summ['sensitivity_threshold_e'] * K

    # quick dynamic range calculation
    dr = summ['sat_capacity_e'] / summ['sensitivity_threshold_e']
    summ['dynamic_range_ratio'] = dr
    summ['dynamic_range_db'] = 20 * np.log10(dr)

    # calculate snr (temp + fpn), once again hack of emva func
    snr = emva.snr(dark_img=dark_avg_img,
                   light_img=half_sat_avg_img,
                   dark_ttn_var=dark_ttn_var,
                   light_ttn_var=light_ttn_var,
                   L=L,
                   u_p=data['Mean Signal [e]'].values,
                   s2_d=summ['Dark Noise [e]'].unique()[0],
                   K=K,
                   qe=1)

    data['snr_dB'] = snr['snr_dB']
    data['SNR [ratio]'] = snr['SNR [ratio]']

    # calculate snr ideal (sqrt(photons)), or in this case
    # sqrt(electrons)
    snr_ideal = emva.snr_ideal(u_p=data['Mean Signal [e]'])

    data['snr_ideal_dB'] = snr_ideal['snr_ideal_dB']
    data['snr_ideal_ratio'] = snr_ideal['snr_ideal_ratio']

    # calculate snr theoretical
    snr_t = emva.snr_theoretical(u_p=data['Mean Signal [e]'].values,
                                 s2_d=summ['Dark Noise [e]'].unique()[0],
                                 K=K,
                                 qe=1)

    data['snr_theoretical_dB'] = snr_t['snr_theoretical_dB']
    data['snr_theoretical_ratio'] = snr_t['snr_theoretical_ratio']

    # calculate DSNU spectrogram
    spect = emva.spectrogram(dark_avg_img,
                             prnu_spect=False)

    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in spect.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'DSNU1288 ' + cc}, inplace=True)

    hist = hist.join(temp)

    # calculate PRNU spectrogram
    spect = emva.spectrogram(half_sat_avg_img,
                             prnu_spect=True)

    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in spect.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'PRNU1288 ' + cc}, inplace=True)

    hist = hist.join(temp)

    return data, hist, summ

def ptc_black(images,
              temp_imgs,
              L,
              df,
              exp_col='Exposure [uW/cm^2*s]',
              interp_exp=True,
              image_idx_col='Image Index',
              rmv_ttn=False,
              K=np.nan):
    """
    calculate all PTC metrics using emva functions, but does
    not require QE, pixel pitch, or wl, assumes that first image
    in list of images is dark image

    Keyword Arguments:
        images (list): list of images where each element is array
                       with dim (num_images, width, height)
        df (pd.DataFrame): DataFrame of parameters associated with each image
                           in image stack, right now it is assumed DataFrame
                           index corresponds to indx of images
        exp_col (str): column within df to be used for exposure calculations

    Returns:
        data (pd.DataFrame): DataFrame of all statistics with updated
                             column names and a column with black level
                             subtracted for each metric
    TODO: need another dynamic range function that doesn't require photons
    TOOD: Add support for saving average frame
    """

    data = pd.DataFrame()
    hist = pd.DataFrame()
    summ = pd.DataFrame()
    temp = pd.DataFrame()

    # get statistics and join image data with params
    data = get_stats(images, temp_imgs, L, df, rmv_ttn=rmv_ttn)

    # get values needed for all emva funtions
    u_y = data['Signal - Dark [DN]']
    sig2_y = data['Tot Temp Var - Tot Dark Temp Var [DN^2]']
    sig2_ydark = data['Tot Temp Var [DN^2]'].iloc[0]
    exp = data[exp_col]

    # get halfsat interp
    m = np.argmax(exp)
    m_ = m - 1
    ma_ = m + 2
    if interp_exp:
        u_ys = [u_y.values[m_], u_y.values[ma_]]
        exps = [exp[m_], exp[ma_]]
        val = np.interp(u_y[m], u_ys, exps)
        exp.replace(exp[m], val, inplace=True)
        data[exp_col] = exp

    # get required images and averages
    idx = data[image_idx_col].iloc[np.argmin(u_y)]
    idx -= data[image_idx_col].min()
    dark_avg_img = images[np.argmin(u_y)]
    half_sat = u_y.max() / 2
    idx = data[image_idx_col].iloc[ut.find_closest(u_y, half_sat)]
    idx -= data[image_idx_col].min()
    half_sat_avg_img = images[idx-1]
    prnu_img = half_sat_avg_img - dark_avg_img
    dark_ttn_var = temp_imgs[0].mean()
    light_ttn_var = temp_imgs[idx-1].mean()

    summ['System Gain [DN/e]'] = pd.Series(K)
    summ['Conversion Factor [e/DN]'] = 1/K

    # get all noise metrics in e
    keysd = ut.stat_engine_col_rename()
    for kk in keysd:
        val = keysd[kk]
        if val not in data.columns.tolist():
            continue
        if 'DN^2' in val:
            val2 = val.replace('[DN^2]', '[e^2]')
            data[val2] = data[val] / K**2
        else:
            val2 = val.replace('[DN]', '[e]')
            data[val2] = data[val] / K
    # get dark temporal Noise
    dtn = emva.dark_temporal_noise(sig2_ydark=sig2_ydark,
                                   K=K)

    summ['Dark Noise [e]'] = dtn['dark_temporal_noise_e']
    summ['Dark Noise [DN]'] = dtn['dark_temporal_noise_DN']

    # get DSNU1288 (pix, row, col, total)
    dsnu = emva.dsnu1288(dark_avg_img, dark_ttn_var, 10)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dsnu.items()]))
    for cc in temp.columns:
        col_name = cc + ' [DN]'
        temp.rename(columns={cc: col_name}, inplace=True)
        col_name_e = cc + ' [e]'
        temp[col_name_e] = temp[col_name] / K

    # add dsnu info to summ
    summ = summ.join(temp)

    # get electrons
    ele = emva.get_electrons(u_y=u_y,
                             K=K)

    data['Mean Signal [e]'] = ele['u_e']

    # add prnu1288 histogram
    prnu_hist = emva.histogram1288(img=prnu_img,
                                   Qmax=256,
                                   L=L,
                                   black_level=False)

    hist['PRNU1288 Number of Pixels/Bin'] = pd.Series(prnu_hist['bins'])
    hist['PRNU1288 Deviation from Mean [DN]'] = pd.Series(prnu_hist['values'])
    hist['PRNU1288 Model'] = pd.Series(prnu_hist['model'])
    hist['PRNU1288 Percentage of Pixels/Bin'] = \
        pd.Series(prnu_hist['accumulated bins'])
    hist['PRNU1288 Accumulated Deviation from Mean [DN]'] = \
        pd.Series(prnu_hist['accumulated values'])

    # add dsnu1288 histogram
    dsnu_hist = emva.histogram1288(img=dark_avg_img,
                                         Qmax=256,
                                         L=L,
                                         black_level=True)

    hist['DSNU1288 Number of Pixels/Bin'] = pd.Series(dsnu_hist['bins'])
    hist['DSNU1288 Deviation from Mean [DN]'] = pd.Series(dsnu_hist['values'])
    hist['DSNU1288 Model'] = pd.Series(dsnu_hist['model'])
    hist['DSNU1288 Percentage of Pixels/Bin'] = \
        pd.Series(dsnu_hist['accumulated bins'])
    hist['DSNU1288 Accumulated Deviation from Mean [DN]'] = \
        pd.Series(dsnu_hist['accumulated values'])


    # add PRNU1288
    prnu = emva.prnu1288(dark_avg_img, half_sat_avg_img, dark_ttn_var, light_ttn_var, L)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prnu.items()]))

    # add prnu info to summ
    summ = summ.join(temp)

    # add DSNU profiles
    prof = emva.profiles(dark_avg_img)
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prof.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'DSNU1288 ' + cc + ' [DN]'}, inplace=True)

    # add profiles to hist
    hist = hist.join(temp, how='right')

    # add PRNU profiles
    prof = emva.profiles(half_sat_avg_img)
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prof.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'PRNU1288 ' + cc + ' [DN]'}, inplace=True)

    # add profiles to hist
    hist = hist.join(temp, how='right')

    # calulcate saturation capacity
    sat = emva.saturation_capacity(u_p=data['Mean Signal [e]'],
                                   sig2_y=sig2_y,
                                   qe=1)

    # not a mistake here..hacking emva sat capacity function
    # for sat capacity in without use of photons column
    summ['sat_capacity_e'] = sat['sat_capacity_p']
    summ['sat_capacity_DN'] = summ['sat_capacity_e'] * K

    # calculate sensitivity threshold
    sen = emva.sensitivity_threshold(sig2_ydark=sig2_ydark,
                                     qe=1,
                                     K=K)

    summ['sensitivity_threshold_e'] = sen['sensitivity_threshold_e']
    summ['sensitivity_threshold_DN'] = summ['sensitivity_threshold_e'] * K

    # quick dynamic range calculation
    dr = summ['sat_capacity_e'] / summ['sensitivity_threshold_e']
    summ['Dynamic Range [ratio]'] = dr
    summ['Dynamic Range [dB]'] = 20 * np.log10(dr)

    # calculate snr (temp + fpn), once again hack of emva func
    snr = emva.snr(dark_img=dark_avg_img,
                         light_img=half_sat_avg_img,
                         dark_ttn_var=dark_ttn_var,
                         light_ttn_var=light_ttn_var,
                         L=L,
                         u_p=data['Mean Signal [e]'].values,
                         s2_d=summ['Dark Noise [e]'].unique()[0],
                         K=K,
                         qe=1)

    data['snr_dB'] = snr['snr_dB']
    data['SNR [ratio]'] = snr['SNR [ratio]']

    # calculate snr ideal (sqrt(photons)), or in this case
    # sqrt(electrons)
    snr_ideal = emva.snr_ideal(u_p=data['Mean Signal [e]'])

    data['snr_ideal_dB'] = snr_ideal['snr_ideal_dB']
    data['snr_ideal_ratio'] = snr_ideal['snr_ideal_ratio']

    # calculate snr theoretical
    snr_t = emva.snr_theoretical(u_p=data['Mean Signal [e]'].values,
                                 s2_d=summ['Dark Noise [e]'].unique()[0],
                                 K=K,
                                 qe=1)

    data['snr_theoretical_dB'] = snr_t['snr_theoretical_dB']
    data['SNR Theoretical[ratio]'] = snr_t['snr_theoretical_ratio']

    # calculate DSNU spectrogram
    spect = emva.spectrogram(dark_avg_img,
                             prnu_spect=False)

    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in spect.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'DSNU1288 ' + cc}, inplace=True)

    hist = hist.join(temp)

    # calculate PRNU spectrogram
    spect = emva.spectrogram(half_sat_avg_img,
                             prnu_spect=True)

    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in spect.items()]))
    for cc in temp.columns:
        temp.rename(columns={cc: 'PRNU1288 ' + cc}, inplace=True)

    hist = hist.join(temp)

    summ.rename(columns=emva.ut.summ_col_rename(), inplace=True)

    return data, hist, summ
