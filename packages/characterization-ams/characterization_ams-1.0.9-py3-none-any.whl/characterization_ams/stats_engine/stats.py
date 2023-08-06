__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"


import numpy as np
import pandas as pd
import pdb
from characterization_ams.utilities import utilities as ut

def agg_results(img_stack, ddof=0, units='DN'):
    """
    get standard deviation for all fpn and temporal noise components

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0) degree of freedom for variance calc
        units (str, 'DN') units of pixel values used for column names

    Returns:
        stats (df) dataframe of summary stats
    """

    df = pd.DataFrame()
    ratios = pd.DataFrame()

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # get mean row, col, pix, and total standard deviation
    var_noise = noise_metrics_all(img_stack, ddof=ddof)

    # add result to df and compute std
    df[f'Mean [{units}]'] = pd.Series(var_noise['mean'])
    df[f'Total FPN [{units}]'] = var_noise['tot_var']**0.5
    df[f'Pix FPN [{units}]'] = var_noise['pix_var']**0.5
    df[f'Col FPN [{units}]'] = var_noise['col_var']**0.5
    df[f'Row FPN [{units}]'] = var_noise['row_var']**0.5
    df[f'Total Temp Noise [{units}]'] = var_noise['tot_var_temp']**0.5
    df[f'Pix Temp Noise [{units}]'] = var_noise['pix_var_temp']**0.5
    df[f'Col Temp Noise [{units}]'] = var_noise['col_var_temp']**0.5
    df[f'Row Temp Noise [{units}]'] = var_noise['row_var_temp']**0.5

    # calculate noise ratios
    ratios = noise_ratios(var_noise)

    # join with noise metrics
    df = df.join(ratios)

    # rename columns for plotting
    df = ut.rename(df)

    return round(df, 3)


def noise_ratios(var_noise):
    """
    calculate noise ratios
    'var_noise' is what stats.noise_metrics_all returns
    keyword arguments:
        noise_var (dict): dictionary with the following keys and values:
                          mean
                          tot_var
                          pix_var
                          col_var
                          row_var
                          tot_var_temp
                          pix_var_temp
                          col_var_temp
                          row_var_temp
    Returns:
        ratios(pd.DataFrame): DataFrame of the following noise ratios:
                              CFPN Ratio
                              CTN Ratio
                              RFPN Ratio
                              RTN Ratio
                              STN Ratio
                              Pix FPN [%]
                              Tot FPN [%]
                              Col FPN [%]
                              Row FPN [%]
    """

    ratios = pd.DataFrame()

    # add noise ratios
    ratios['cfpn_ratio'] = \
        pd.Series(var_noise['tot_var_temp']**0.5 /
                  var_noise['col_var']**0.5)
    ratios['rfpn_ratio'] = \
        var_noise['tot_var_temp']**0.5 /\
        var_noise['row_var']**0.5
    ratios['stn_ratio'] = \
        var_noise['tot_var']**0.5 /\
        var_noise['tot_var_temp']**0.5
    if 'col_var_temp' in var_noise.keys():
        ratios['ctn_ratio'] = \
            var_noise['tot_var_temp']**0.5 /\
            var_noise['col_var_temp']**0.5
    if 'row_var_temp' in var_noise.keys():
        ratios['rtn_ratio'] = \
            var_noise['tot_var_temp']**0.5 /\
            var_noise['row_var_temp']**0.5

    # add fpn as % of signal
    ratios['tot_fpn_%'] = \
        var_noise['tot_var']**0.5 /\
        var_noise['mean'] * 100
    ratios['pix_fpn_%'] = \
        var_noise['pix_var']**0.5 /\
        var_noise['mean'] * 100
    ratios['col_fpn_%'] = \
        var_noise['col_var']**0.5 /\
        var_noise['mean'] * 100
    ratios['row_fpn_%'] = \
        var_noise['row_var']**0.5 /\
        var_noise['mean'] * 100

    return ratios


def avg_img_stack(img_stack):
    """
    take a stack of images and compute the per pixel average

    Keyword Arguments:
        img_stack (np.array): stack of images

    Returns:
        avg_img (np.array): 2D image of per pixel averages from img_stack
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute the average
    avg_im = np.mean(img_stack, axis=0)

    return avg_im


def col_avg(img):
    """
    get column average

    Keyword Arguments:
        img (np.array): img to calcuate column average on

    Returns:
        avg (np.array): 1D array of column average values
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    return np.mean(img, axis=0)


def col_var(img, L, ttn_var, ddof=0):
    """
    compute exact solution of column variance from
    image with residual temporal noise removed,
    EMVA 4.0 definition

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from average
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        col_var (float): column variance of img
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    var = noise_metrics(img=img,
                        L=L,
                        ttn_var=ttn_var,
                        ddof=ddof)

    return var['col_var']


def col_var_cav(img, L, ttn_var, ddof=0, rmv_ttn=True, hpf=False):
    """
    compute column variance from image with residual temporal noise removed,
    not exact solution

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from image stack used to get img
        ddof (int, 0): degree of freedom for variance calc
        rmv_ttn (bool, True): if True remove residual temporal noise
        hpf (bool, False): if hpf was applied we correct for noise
                           reduction from hpf (factor of 0.96)

    Returns:
        var (float): column variance of img
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    M = img.shape[0]

    # compute column variance
    var = np.var(np.mean(img, axis=0), ddof=ddof)

    # if hpf was applied correct variance
    if hpf:
        var = (np.sqrt(var) / 0.96)**2

    # remove residual temporal noisec
    if rmv_ttn:
        var -= ttn_var / (L * M)

    return var


def col_var_temp(img_stack, ddof=1):
    """
    compute exact solution for column temporal
    variance from image stack

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): column temporal noise variance of img_stack
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute column variance
    var = noise_metrics_temp(img_stack=img_stack,
                             ddof=ddof)

    return var['col_var_temp']


def frame_avg(img):
    """
    compute the average of a frame, returns a scalar

    keyword arguments:
        img (np.array): average image to compute mean on

    Returns:
        temp (float): mean of average grame
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    temp = img.mean()

    return temp


def frame_avg_from_stack(img_stack):
    """
    compute the average of a stack of frames, returns a scalar

    Keyword Arguments:
        img_stack (np.array): stack of images

    Returns:
        mean (float): mean of image stack
    """

    temp = {}

    # get average frame from stack of frames
    avg_img = avg_img_stack(img_stack)

    # get average of average frame
    temp = frame_avg(avg_img)

    return temp


def noise_calc(rav_var, cav_var, tot_var, M, N, key='_var'):
    """
    calculate row, col, pix, tot variance using exact solution,
    EMVA 4.0 definition

    Keyword Arguments:
        rav_var (float): row variance, not exact solution
        cav_var (float): column variance, not exact solution
        tot_var (float): total variance
        M (int): # rows of image used for row, col, tot variance calc
        N (int): # cols of image used for row, col, tot variance calc
        key (str, '_var'): key to denote if result is temporal or spatial noise

    Returns:
        var (dict): row_var|row_temp_var
                    col_var|col_temp_var
                    pix_var|pix_temp_var
                    tot_var|tot_temp_var
    """

    var = {}

    # get exact values
    # col
    col_var = ((M * N - M) / (M * N - M - N)) * cav_var - \
        (N / (M * N - M - N)) * (tot_var - rav_var)

    # row
    row_var = ((M * N - N) / (M * N - M - N)) * rav_var - \
        (M / (M * N - M - N)) * (tot_var - cav_var)

    # pix
    pix_var = ((M * N) / (M * N - M - N)) * \
        (tot_var - cav_var - row_var)

    # add all metrics to dict
    var = {f'tot{key}': tot_var,
           f'col{key}': col_var,
           f'row{key}': row_var,
           f'pix{key}': pix_var}

    return var


def noise_metrics(img, L, ttn_var, ddof=0, rmv_ttn=True, hpf=False):
    """
    compute spatial noise metrics from an average
    image with residual temporal noise removed

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from image stack used to get img
        ddof (int, 0): degree of freedom for variance calc
        rmv_ttn (bool, True): if True remove residual temporal noise
        hpf (bool, False): if hpf was applied we correct for noise
                           reduction from hpf (factor of 0.96)

    Returns:
        var (dict): row_var
                    col_var
                    pix_var
                    tot_var
    """

    var = {}

    # make sure we have a numpy array
    img = to_numpy(img)

    # compute row variance
    M = img.shape[0]
    N = img.shape[1]

    # get row/col/total
    rav_var = np.mean(row_var_cav(img, L, ttn_var, ddof, rmv_ttn, hpf))
    cav_var = np.mean(col_var_cav(img, L, ttn_var, ddof, rmv_ttn, hpf))
    tot_var = np.mean(total_var(img, L, ttn_var, ddof, rmv_ttn, hpf))

    # get exact noise values
    var = noise_calc(rav_var=rav_var,
                     cav_var=cav_var,
                     tot_var=tot_var,
                     M=M,
                     N=N)

    return var


def noise_metrics_all(img_stack, ddof=0, ddof_temp=1, rmv_ttn=True, hpf=False):
    """
    compute spatial and temporal noise metrics from a stack
    of images

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc
        ddof_temp (int, 0): degree of freedom for temporal variance calc
        rmv_ttn (bool, True): if True remove residual temporal noise
        hpf (bool, False): if hpf was applied we correct for noise
                           reduction from hpf (factor of 0.96)

    Returns:
        all_var (dict): row_var
                        col_var
                        pix_var
                        tot_var
                        row_temp_var
                        col_temp_var
                        pix_temp_var
                        tot_temp_var
                        mean
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # get average frame
    avg_img = avg_img_stack(img_stack)

    # get total temp noise
    ttn_var = total_var_temp(img_stack, ddof=ddof)

    # get shape
    L = img_stack.shape[0]
    M = img_stack.shape[1]
    N = img_stack.shape[2]

    # get row/col/total for avg img
    rav_var = np.mean(row_var_cav(avg_img, L, ttn_var, ddof, rmv_ttn, hpf))
    cav_var = np.mean(col_var_cav(avg_img, L, ttn_var, ddof, rmv_ttn, hpf))
    tot_var = np.mean(total_var(avg_img, L, ttn_var, ddof, rmv_ttn, hpf))

    # get row/col/total for temp_img
    cav_var_temp = \
        np.mean(img_stack, axis=1).var(ddof=ddof_temp, axis=0).mean()
    rav_var_temp = \
        np.mean(img_stack, axis=2).var(ddof=ddof_temp, axis=0).mean()
    tot_var_tempn = np.var(img_stack, axis=0, ddof=ddof_temp).mean()

    # get exact noise values
    var = noise_calc(rav_var=rav_var,
                     cav_var=cav_var,
                     tot_var=tot_var,
                     M=M,
                     N=N,
                     key='_var')

    # get exact temp noise values
    var_temp = noise_calc(rav_var=rav_var_temp,
                          cav_var=cav_var_temp,
                          tot_var=tot_var_tempn,
                          M=M,
                          N=N,
                          key='_var_temp')

    # combine fpn and temp noise components
    all_var = {**var, **var_temp}

    # add the mean to be complete
    mean = frame_avg(avg_img)
    all_var['mean'] = mean

    return all_var


def noise_metrics_temp(img_stack, ddof=1):
    """
    compute temporal noise metrics from a stack of images

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (dict): row_var_temp
                    col_var_temp
                    pix_var_temp
                    tot_var_temp
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute row variance
    M = img_stack.shape[1]
    N = img_stack.shape[2]

    # get col/row/tot
    col_var_temp = \
        np.mean(img_stack, axis=1).var(ddof=ddof, axis=0).mean()
    row_var_temp = \
        np.mean(img_stack, axis=2).var(ddof=ddof, axis=0).mean()
    tot_var_temp = np.var(img_stack, axis=0, ddof=ddof).mean()

    var = noise_calc(rav_var=row_var_temp,
                     cav_var=col_var_temp,
                     tot_var=tot_var_temp,
                     M=M,
                     N=N,
                     key='_var_temp')

    return var


def tot_var_img_stack(img_stack, ddof=1):
    """
    take a stack of images and compute
    the per pixel variance (total temporal noise)

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var_im -- 2D image of pix temporal noise values
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute per pixel variance
    var_im = np.var(img_stack, axis=0, ddof=ddof)

    return var_im


def pix_var(img, L, ttn_var, ddof=0):
    """
    compute exact solution of pixel variance from
    image with residual temporal noise removed,
    EMVA 4.0 definition

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from average
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): pix variance of img
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    var = noise_metrics(img=img,
                        L=L,
                        ttn_var=ttn_var,
                        ddof=ddof)

    return var['pix_var']


def pix_var_temp(img_stack, ddof=1):
    """
    compute exact solution for pixel temporal
    variance from image stack

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): pixel temporal noise variance
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute column variance
    var = noise_metrics_temp(img_stack=img_stack,
                             ddof=ddof)

    return var['pix_var_temp']


def profile(img, horizontal=True):
    """
    calculate profiles for an image

    Keyword Arguments:
        img (np.array): image to calculate profiles from
        horizontal (bool): if True horizontal profile is takem, else vertical

    Returns:
        temp (dict): index: index of columns
                     middle: center value of columns
                     mean: mean value of columns
                     max: max value of columns
                     min: min value of columns
    """

    temp = {}

    # make sure we have a numpy array
    img = to_numpy(img)

    # if vertical data then transpose image
    if not horizontal:
        img = img.T
        key = 'vertical'
    else:
        key = 'horizontal'

    # calculate profiles
    temp = {f'index_{key}': pd.DataFrame(img).columns,
            f'middle_{key}': img[np.shape(img)[0] // 2, :],
            f'mean_{key}': np.mean(img, axis=0),
            f'max_{key}': np.max(img, axis=0),
            f'min_{key}': np.min(img, axis=0)}

    return temp


def row_avg(img):
    """
    get row average

    Keyword Arguments:
        img (np.array): img to calcuate row average on

    Returns:
        avg (np.array): 1D array of row average values
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    return np.mean(img, axis=1)


def row_var(img, L, ttn_var, ddof=0):
    """
    compute exact solution of row variance from
    image with residual temporal noise removed,
    EMVA 4.0 definition

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from average
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): row variance of img
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    var = noise_metrics(img=img,
                        L=L,
                        ttn_var=ttn_var,
                        ddof=ddof)

    return var['row_var']


def row_var_temp(img_stack, ddof=1):
    """
    compute exact solution for row temporal
    variance from image stack

    Keyword Arguments:
        img_stack (np.array): stack of images
        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): row temporal noise variance
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute column variance
    var = noise_metrics_temp(img_stack=img_stack,
                             ddof=ddof)

    return var['row_var_temp']


def row_var_cav(img, L, ttn_var, ddof=0, rmv_ttn=True, hpf=False):
    """
    compute row variance from image with residual temporal noise removed,
    not exact solution

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from image stack used to get img
        ddof (int, 0): degree of freedom for variance calc
        rmv_ttn (bool, True): if True remove residual temporal noise
        hpf (bool, False): if hpf was applied we correct for noise
                           reduction from hpf (factor of 0.96)

    Returns:
        var (float): row variance of image
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    N = img.shape[1]

    # compute row variance
    var = np.var(np.mean(img, axis=1), ddof=ddof)

    # if hpf was applied correct variance
    if hpf:
        var = (np.sqrt(var) / 0.96)**2

    # remove residual temporal noise
    if rmv_ttn:
        var -= ttn_var / (L * N)

    return var


def total_var(img, L, ttn_var, ddof=0, rmv_ttn=True, hpf=False):
    """
    compute total variance from image with
    residual temporal noise removed

    Keyword Arguments:
        img (np.array): input image (tyically average)
        L (int): number of images used for average
        ttn_var (float): temporal noise from image stack used to get img
        ddof (int, 0): degree of freedom for variance calc
        rmv_ttn (bool, True): if True remove residual temporal noise
        hpf (bool, False): if hpf was applied we correct for noise
                           reduction from hpf (factor of 0.96)

    Returns:
        var (float): total variance of img
    """

    # make sure we have a numpy array
    img = to_numpy(img)

    # compute total variance
    var = np.var(img.flatten(), ddof=ddof)

    # if hpf
    if hpf:
        var = (np.sqrt(var) / 0.96)**2

    # remove residual temporal noise
    if rmv_ttn:
        var -= ttn_var / L

    return var


def total_var_temp(img_stack, ddof=1):
    """
    compute total temporal variance from a stack of images

    Keyword Arguments:
        img_stack (np.array): stack of images

        ddof (int, 0): degree of freedom for variance calc

    Returns:
        var (float): total temporal variance of img
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute column variance
    var = noise_metrics_temp(img_stack=img_stack,
                             ddof=ddof)

    return var['tot_var_temp']


def to_numpy(img_stack):
    """
    convert list to numpy array and rshape (1,m,n) to (m,n)

    Keyword Arguments:
        img_stack (list|np.array): input image data structure

    Returns:
        img_stack(np.array): list converted to np.array or reshaped array
    """

    # if input is a list of images convert to 3D numpy array
    if isinstance(img_stack, list):
        img_stack = np.dstack(img_stack)
        img_stack = np.rollaxis(img_stack, -1)

    # if we only have 1 image then re-shape
    if img_stack.shape[0] == 1:
        img_stack = img_stack.reshape((img_stack.shape[1], img_stack.shape[2]))

    return img_stack


def noise_profile(img_stack, axis):
    """
    take a stack of images and compute the row/column noise profile

    Keyword Arguments:
        img_stack (np.array): stack of images
        axis (str): row or column

    Returns:
        noise_profile (np.array): 1D array of row/column noise values
    """

    # make sure we have a numpy array
    img_stack = to_numpy(img_stack)

    # compute the row/column noise profile
    if axis == 'row':
        noise_profile = np.std(np.mean(img_stack, axis=2), axis=0, ddof=1)
    elif axis == 'column':
        noise_profile = np.std(np.mean(img_stack, axis=1), axis=0, ddof=1)

    return noise_profile


def fpn_profile(img_stack, axis):
    """
    take a stack of images and compute the row/column fpn profile

    Keyword Arguments:
        img_stack (np.array): stack of images
        axis (str): row or column

    Returns:
        fpn_profile (np.array): 1D array of row/column fpn values
    """

    # compute the row/column fpn profile
    if axis == 'row':
        fpn_profile = np.std(avg_img_stack(img_stack), axis=1, ddof=1)
    elif axis == 'column':
        fpn_profile = np.std(avg_img_stack(img_stack), axis=0, ddof=1)

    return fpn_profile