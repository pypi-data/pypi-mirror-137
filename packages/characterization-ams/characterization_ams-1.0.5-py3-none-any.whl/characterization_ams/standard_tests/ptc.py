__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"

import numpy as np
import pandas as pd
import pdb

from sympy import Q, utilities
from characterization_ams.stats_engine import stats
from characterization_ams.emva import emva
from characterization_ams.utilities import utilities as ut


def get_stats(images,
              df=pd.DataFrame(),
              rmv_ttn=False,
              hpf=True,
              rmv_black=True,
              temp_imgs=None,
              L=None):
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
        rmv_black (bool): if True creates black level subtracted columns + originals
        temp_images (list|None): If 'images' is a list of frame averages then total
                                 temporal variance images must be passed here
        L (int|None): If average frames are passed to 'images' original stack size
                      must be passed.  
    Returns:
        data (pd.DataFrame): DataFrame of all statistics with updated
                             column names and a column with black level
                             subtracted for each metric
    """

    data = pd.DataFrame()
    stack = True

    # check if we have an image stack, or avg and temp frame
    if not isinstance(temp_imgs, type(None)):
        stack = False

    # calculate all noise metrics using stats engine
    for idx, im in enumerate(images):

        # case when we have stack of images (all information)
        if stack:
            ttn_var = stats.tot_var_img_stack(im)
            ttn_var = stats.frame_avg(ttn_var)
            stat_vals = stats.noise_metrics_all(im,
                                                rmv_ttn=rmv_ttn,
                                                hpf=hpf)
            mean = stats.frame_avg_from_stack(im)
            tot_var_temp = stat_vals['tot_var_temp']

        # case where we just have an average frame and
        # temporal variance frame
        else:
            ttn_var = stats.frame_avg(temp_imgs[idx])
            stat_vals = stats.noise_metrics(im, L=L,
                                            ttn_var=ttn_var,
                                            rmv_ttn=rmv_ttn,
                                            hpf=hpf)
            mean = stats.frame_avg(images[idx])
            tot_var_temp = stats.frame_avg(temp_imgs[idx])
            stat_vals['tot_var_temp'] = tot_var_temp

        # convert to df
        stat_vals['mean'] = mean
        temp = \
            pd.DataFrame(dict([(k, pd.Series(v)) for
                         k, v in stat_vals.items()]))

        # add noise ratios
        ratios = stats.noise_ratios(stat_vals)
        ratio_cols = ratios.columns.tolist()

        temp = temp.join(ratios)
        data = pd.concat([data, temp]).reset_index(drop=True)

    # get data columns
    data_cols = data.columns.tolist()
    data_cols = [c for c in data_cols if c not in ratio_cols]

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
    if rmv_black:
        data = ut.remove_black(data, data_cols)

    # get rid of inf values
    data = data.replace(np.inf, 0)

    # rename stats columns
    data = ut.rename(data)

    return data


def ptc(images,
        df,
        exp_col='Exposure [uW/cm^2*s]',
        exp_col_units='uW/cm^2',
        rmv_ttn=False,
        hpf=False,
        image_idx_col='Image Index',
        interp_exp=False,
        temp_imgs=None,
        dark_imgs=None,
        L=None):
    """
    calculate all PTC metrics using emva functions, but does
    not require QE, pixel pitch, or wl, assumes that first image
    in list of images is dark image. This function will handle 3 cases:

    1.) all images in 'images' list are a stack of images
        - for this case temp_imgs=None, dark_imgs=None, L=None

    2.) all images in 'images' keyword are an average frame
        - L (size of original stack) must be passed
        - temp_imgs (total temporal noise images) must be passed

    3.) all images in 'images' keyword are an average frame AND a stack of
        dark images were passed with keyword 'dark_imgs' for dark temporal 
        noise metrics
        - L (size of original stack) must be passed
        - temp_imgs (total temporal noise images) must be passed (do not pass)
          total temporal noise image for 'dark_img', it will be added in source

    Keyword Arguments:
        images (list): list of images where each element is array
                       with dim (num_images, width, height)
                       OR
                       list of images where each element is average array
                       with dim (width, height)
        df (pd.DataFrame): DataFrame of parameters associated with each image
                           in image stack, right now it is assumed DataFrame
                           index corresponds to indx of images
        exp_col (str): column within df to be used for exposure
                       calculations
        exp_col_units (str): exposure column units to be used
                             for responsivity label
        rmv_ttn (bool): if True subtract off residual temporal noise
        hpf (bool): if true high pass filter image prior to
                    spatial variance calc
        image_idx_col (str): column in df associated with
                             image index in list, if this does not exist in df,
                             it will be created as the frame index
        interp_exp (bool): Case where average images are passed
                           and 50% exposure point needs to be
                           calculated (charmware .h5 file output format)
        temp_imgs (list|None): If 'images' are average of image
                               stack then this variable must be used to
                               pass total temporal variance frames, indexes
                               of both lists must align
        dark_imgs (np.array|None): if temp_imgs is used and dark_imgs
                                   are passed then component wise temporal
                                   noise components will be calculated in addition
                                   to normal calc

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
    calc_vals = {}
    stack = True

    # check if we have an image stack, or avg and temp frame
    if not isinstance(temp_imgs, type(None)):
        stack = False

    # get statistics and join image data with params
    data = get_stats(images,
                     df,
                     rmv_ttn=rmv_ttn,
                     hpf=hpf,
                     temp_imgs=temp_imgs,
                     L=L)

    if not isinstance(dark_imgs, type(None)) and not stack:
        dark_stats = get_stats([dark_imgs],
                               df.iloc[[0]],
                               rmv_ttn=rmv_ttn,
                               hpf=hpf,
                               temp_imgs=None,
                               L=None)

        # force exposure point of dark frame to zero
        dark_stats[exp_col] = 0

        # join with lighted frames
        data = pd.concat([data, dark_stats]).reset_index(drop=True)

        # sort by mean signal
        data = data.sort_values(by=['Mean Signal [DN]'])

        # calculate avg and ttn_var frame from stack
        ttn_var = stats.tot_var_img_stack(dark_imgs)
        avg = stats.avg_img_stack(dark_imgs)

        # insert into image lists for remaining processing
        images.insert(0, avg)
        temp_imgs.insert(0, ttn_var)

    # get values needed for all emva funtions
    calc_vals['u_y'] = data['Signal - Dark [DN]']
    calc_vals['sig2_y'] = data['Tot Var - Tot Dark Var [DN^2]']
    calc_vals['sig2_ydark'] = data['Tot Temp Var [DN^2]'].iloc[0]
    calc_vals['exp'] = data[exp_col]

    # case where we have data from pxi
    if stack and interp_exp:
        exp = ut.halfsat_interp(exp_arr=calc_vals['exp'],
                                sig_arr=calc_vals['u_y'])
        data[exp_col] = exp

    # create image index col if it wasn't passed
    if image_idx_col not in data.columns:
        data[image_idx_col] = data.index

    # if we have a stack of images convert to avg and pix var
    if stack:
        temp_imgs = []
        avg_imgs = []
        for img in images:
            ttn_var = stats.tot_var_img_stack(img)
            avg = stats.avg_img_stack(img)
            temp_imgs.append(ttn_var)
            avg_imgs.append(avg)
    else:
        avg_imgs = images.copy()

    # get required images and averages
    dark_avg_img, \
        half_sat_avg_img, \
        half_sat_idx = ut.get_half_sat(avg_imgs,
                                       data,
                                       calc_vals['u_y'],
                                       image_idx_col)

    prnu_img = half_sat_avg_img - dark_avg_img
    calc_vals['dark_ttn_var'] = stats.frame_avg(temp_imgs[0])
    calc_vals['half_sat_ttn_var'] = stats.frame_avg(temp_imgs[half_sat_idx])
    calc_vals['L'] = images[0].shape[0] if stack else L

    # get system gain
    sys_gain = emva.system_gain(u_y=calc_vals['u_y'],
                                sig2_y=calc_vals['sig2_y'])

    data['System Gain Fit [DN^2]'] = sys_gain['fit']
    summ['System Gain [DN/e]'] = pd.Series(sys_gain['system_gain'])
    summ['Conversion Factor [e/DN]'] = 1 / sys_gain['system_gain']
    calc_vals['K'] = sys_gain['system_gain']

    # get all noise metrics in e
    keysd = ut.stat_engine_col_rename()

    for kk in keysd:
        val = keysd[kk]
        if val not in data.columns:
            continue
        if 'DN^2' in val:
            val2 = val.replace('[DN^2]', '[e^2]')
            data[val2] = data[val] / calc_vals['K']**2
        else:
            val2 = val.replace('[DN]', '[e]')
            data[val2] = data[val] / calc_vals['K']

    # get dark temporal Noise
    dtn = emva.dark_temporal_noise(sig2_ydark=calc_vals['sig2_ydark'],
                                   K=calc_vals['K'])
    summ = ut.join_frame(summ, dtn)
    calc_vals['dark_noise_e'] = dtn['dark_temporal_noise_e']

    # get column wise temporal noise if we have the infomration available
    if 'Pix Temp Var [DN^2]' in data.columns:
        sub = data[(data['Mean Signal [DN]'] ==
                   data['Mean Signal [DN]'].min())].reset_index(drop=True)
        sub = sub[['Pix Temp Var [DN^2]',
                   'Col Temp Var [DN^2]',
                   'Row Temp Var [DN^2]']]
        summ['col_temp_noise_e'] = \
            np.sqrt(sub['Col Temp Var [DN^2]']) / calc_vals['K']
        summ['row_temp_noise_e'] = \
            np.sqrt(sub['Row Temp Var [DN^2]']) / calc_vals['K']
        summ['pix_temp_noise_e'] = \
            np.sqrt(sub['Pix Temp Var [DN^2]']) / calc_vals['K']

    # get DSNU1288 (pix, row, col, total)
    dsnu = emva.dsnu1288(dark_img=dark_avg_img,
                         ttn_var=calc_vals['dark_ttn_var'],
                         hpf=hpf,
                         L=calc_vals['L'])
    # add units to columns and calculate in e
    summ = ut.join_frame(summ, dsnu, replace_DN=True, K=calc_vals['K'])

    # get electrons
    ele = emva.get_electrons(u_y=calc_vals['u_y'],
                             K=calc_vals['K'])
    calc_vals['u_e'] = ele['u_e']
    data['Mean Signal [e]'] = ele['u_e']

    # add prnu1288 histogram
    prnu_hist = emva.histogram1288(img=prnu_img,
                                   Qmax=256,
                                   L=calc_vals['L'],
                                   black_level=False)
    hist = ut.join_frame(hist, prnu_hist)

    # add dsnu1288 histogram
    dsnu_hist = emva.histogram1288(img=dark_avg_img,
                                   Qmax=256,
                                   L=calc_vals['L'],
                                   black_level=True)
    hist = ut.join_frame(hist, dsnu_hist)

    # add linearity error TODO: Clean this up
    lin = emva.linearity(mean_arr=calc_vals['u_y'],
                         exp_arr=calc_vals['exp'],
                         ttn_arr=calc_vals['sig2_y'])

    data['linearity_fit_DN'] = lin['linearity_fit_DN']
    data['linearity_error_%'] = lin['linearity_error_%']
    data['linearity_error_DN'] = lin['linearity_error_DN']
    summ['linearity_error_max_%'] = lin['linearity_error_max_%']
    summ['linearity_error_max_DN'] = lin['linearity_error_max_DN']
    summ['linearity_error_min_%'] = lin['linearity_error_min_%']
    summ['linearity_error_min_DN'] = lin['linearity_error_min_DN']

    # add PRNU1288
    prnu = emva.prnu1288(dark_img=dark_avg_img,
                         light_img=half_sat_avg_img,
                         dark_ttn_var=calc_vals['dark_ttn_var'],
                         light_ttn_var=calc_vals['half_sat_ttn_var'],
                         L=calc_vals['L'])
    summ = ut.join_frame(summ, prnu)

    # add DSNU profiles
    prof = emva.profiles(dark_avg_img, dsnu=True)
    hist = ut.join_frame(hist, prof)

    # add PRNU profiles
    prof = emva.profiles(half_sat_avg_img, dsnu=False)
    hist = ut.join_frame(hist, prof)

    # calculate responsivity using exp_col
    resp = emva.responsivity(u_p=data[exp_col],
                             u_y=calc_vals['u_y'],
                             sig2_y=calc_vals['sig2_y'])

    data['responsivity_fit'] = resp['responsivity_fit']
    summ[f'Responsivity [DN/({exp_col_units})]'] = resp['responsivity']

    # calulcate saturation capacity
    sat = emva.saturation_capacity(u_p=data['Mean Signal [e]'],
                                   sig2_y=calc_vals['sig2_y'],
                                   qe=1)
    summ['sat_capacity_e'] = sat['sat_capacity_p']
    summ['sat_capacity_DN'] = summ['sat_capacity_e'] * calc_vals['K']

    # calculate sensitivity threshold
    sen = emva.sensitivity_threshold(sig2_ydark=calc_vals['sig2_ydark'],
                                     qe=1,
                                     K=calc_vals['K'])
    summ['sensitivity_threshold_e'] = sen['sensitivity_threshold_e']
    summ['sensitivity_threshold_DN'] = summ['sensitivity_threshold_e'] * calc_vals['K']

    # quick dynamic range calculation
    dr = emva.dynamic_range(u_p=calc_vals['u_e'],
                            sig2_y=calc_vals['sig2_y'],
                            sig2_ydark=calc_vals['sig2_ydark'],
                            qe=1,
                            K=calc_vals['K'])
    summ = ut.join_frame(summ, dr)

    # calculate snr (temp + fpn), once again hack of emva func
    snr = emva.snr(dark_img=dark_avg_img,
                   light_img=half_sat_avg_img,
                   dark_ttn_var=calc_vals['dark_ttn_var'],
                   light_ttn_var=calc_vals['half_sat_ttn_var'],
                   L=calc_vals['L'],
                   u_p=data['Mean Signal [e]'].values,
                   s2_d=calc_vals['dark_noise_e'],
                   K=calc_vals['K'],
                   qe=1)

    data = ut.join_frame(data, snr)

    # calculate snr ideal (sqrt(photons)), or in this case
    # sqrt(electrons)
    snr_ideal = emva.snr_ideal(u_p=data['Mean Signal [e]'])
    data = ut.join_frame(data, snr_ideal)

    # calculate snr theoretical
    snr_t = emva.snr_theoretical(u_p=data['Mean Signal [e]'].values,
                                 s2_d=calc_vals['dark_noise_e'],
                                 K=calc_vals['K'],
                                 qe=1)
    data = ut.join_frame(data, snr_t)

    # calculate DSNU spectrogram
    spect = emva.spectrogram(img=dark_avg_img,
                             prnu_spect=False)
    hist = ut.join_frame(hist, spect)

    # calculate PRNU spectrogram
    spect = emva.spectrogram(prnu_img,
                             prnu_spect=True)
    hist = ut.join_frame(hist, spect)

    # update column names for plotting
    summ = ut.rename(summ)
    data = ut.rename(data)
    hist = ut.rename(hist)

    return data, hist, summ


def ptc_mem_optimized(dark_imgs,
                      light_avg_imgs,
                      light_ttn_vars,
                      data,
                      exp_col='Exposure [uW/cm^2*s]',
                      exp_col_units=['uW/cm^2'],
                      rmv_ttn=False,
                      hpf=False):
    """
    This is a memory optimized version of the PTC above. 
    It does not need the whole image stack as an input.
    calculate all PTC metrics using emva functions, but does
    not require QE, pixel pitch, or wl, assumes that first image
    in list of images is dark image

    Keyword Arguments:
        dark_imgs (np.array): stack of black level images
        light_avg_imgs (list): list of 2D images of per pixel averages from image stack
        light_ttn_vars (list): list of total temporal variances of image stack
        data (pd.DataFrame): DataFrame of all statistics associated with each image
                             in image stack, right now it is assumed DataFrame
                             index corresponds to indx of images
        exp_col (str): column within data to be used for exposure calculations
        exp_col_units (str): exposure column units to be used for responsivity label
        rmv_ttn (bool): if True subtract off residual temporal noise
        hpf (bool): if true high pass filter image prior to spatial variance calc

    Returns:
        data (pd.DataFrame): DataFrame of all EMVA response metrics + noise metrics
        hist (dict): Histograms of PRNU and DSNU
        profiles (dict): Profiles of PRNU and DSNU
        spect (dict): Spectograms of PRNU and DSNU
        summ (pd.DataFrame): DataFrame of all EMVA summary metrics
        prnu_img (np.array): Image at 50% sat - dark image

    TODO: need another dynamic range function that doesn't require photons
    TOOD: Add support for saving average frame
    """

    summ = pd.DataFrame()
    temp = pd.DataFrame()

    # get values needed for all emva funtions
    u_y = data['Signal - Dark [DN]']
    sig2_y = data['Tot Temp Var - Tot Dark Temp Var [DN^2]']
    sig2_ydark = data['Tot Temp Var [DN^2]'].iloc[0]
    exp = data[exp_col]

    # get required images and averages
    dark_avg_img = stats.avg_img_stack(dark_imgs)
    dark_ttn_var = stats.total_var_temp(dark_imgs)
    half_sat_avg_img = light_avg_imgs[ut.find_closest(u_y, u_y.max() / 2)]
    half_sat_ttn_var = light_ttn_vars[ut.find_closest(u_y, u_y.max() / 2)]
    prnu_img = half_sat_avg_img - dark_avg_img
    L = dark_imgs.shape[0]

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
        if 'DN^2' in val:
            val2 = val.replace('[DN^2]', '[e^2]')
            data[val2] = data[val] / K**2
        else:
            val2 = val.replace('[DN]', '[e]')
            data[val2] = data[val] / K

    # get dark temporal Noise
    dtn = emva.dark_temporal_noise(sig2_ydark=sig2_ydark,
                                   K=K)

    summ['Dark Noise [DN]'] = dtn['dark_temporal_noise_DN']
    summ['Dark Noise [e]'] = dtn['dark_temporal_noise_e']

    # get column wise temporal noise
    tn = stats.noise_metrics_temp(dark_imgs)

    summ['Col Temp Noise [e]'] = np.sqrt(tn['col_var_temp']) / K
    summ['Row Temp Noise [e]'] = np.sqrt(tn['row_var_temp']) / K
    summ['Pix Temp Noise [e]'] = np.sqrt(tn['pix_var_temp']) / K

    # get DSNU1288 (pix, row, col, total)
    dsnu = emva.dsnu1288_stack(img_stack=dark_imgs)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dsnu.items()]))
    for cc in temp.columns:
        col_name = cc + '_DN'
        temp.rename(columns={cc: col_name}, inplace=True)
        col_name_e = cc + '_e'
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

    # add dsnu1288 histogram
    dsnu_hist = emva.histogram1288_stack(img_stack=dark_imgs,
                                         Qmax=256,
                                         black_level=True)
    hist = {"PRNU1288" : prnu_hist,  "DSNU1288" : dsnu_hist}

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
    prnu = emva.prnu1288(dark_img=dark_avg_img,
                         light_img=half_sat_avg_img,
                         dark_ttn_var=dark_ttn_var,
                         light_ttn_var=half_sat_ttn_var,
                         L=L)

    # add units to columns and calculate in e
    temp = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in prnu.items()]))

    # add prnu info to summ
    summ = summ.join(temp)

    # add DSNU profiles
    dsnu_prof = emva.profiles(dark_avg_img)

    # add PRNU profiles
    prnu_prof = emva.profiles(half_sat_avg_img)
    profiles = {"PRNU1288": prnu_prof,  "DSNU1288": dsnu_prof}

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
    summ['Saturation Capacity [e]'] = sat['Saturation Capacity [p]']
    summ['Saturation Capacity [DN]'] = summ['Saturation Capacity [e]'] * K

    # calculate sensitivity threshold
    sen = emva.sensitivity_threshold(sig2_ydark=sig2_ydark,
                                     qe=1,
                                     K=K)

    summ['sensitivity_threshold_e'] = sen['sensitivity_threshold_e']
    summ['sensitivity_threshold_DN'] = summ['sensitivity_threshold_e'] * K

    # quick dynamic range calculation
    dr = summ['Saturation Capacity [e]'] / summ['sensitivity_threshold_e']
    summ['Dynamic Range [ratio]'] = dr
    summ['Dynamic Range [dB]'] = 20 * np.log10(dr)

    # calculate snr (temp + fpn), once again hack of emva func
    snr = emva.snr(dark_img=dark_avg_img,
                   light_img=half_sat_avg_img,
                   dark_ttn_var=dark_ttn_var,
                   light_ttn_var=half_sat_ttn_var,
                   L=L,
                   u_p=data['Mean Signal [e]'].values,
                   s2_d=summ['Dark Noise [e]'].unique()[0],
                   K=K,
                   qe=1)

    data['snr_dB'] = snr['snr_dB']
    data['snr_ratio'] = snr['snr_ratio']

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
    dsnu_spect = emva.spectrogram_stack(dark_imgs, prnu_spect=False)

    # calculate PRNU spectrogram
    prnu_spect = emva.spectrogram(prnu_img, prnu_spect=True)

    spect = {"PRNU1288": prnu_spect,  "DSNU1288": dsnu_spect}

    summ = ut.rename(summ)

    return data, hist, profiles, spect, summ, prnu_img
