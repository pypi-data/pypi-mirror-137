__author__ = "Denver Lloyd"
__copyright__ = "Copyright 2021, AMS Characterization"


import numpy as np
import pandas as pd
from scipy.ndimage import convolve
import yaml
import os
import sys

def high_pass_filter(img, dim):
    """
    Computes the high pass filtering on
    an image as defined by the EMVA Standard

    Keyword Arguments:
        img (df): DataFrame of raw image data to be filtered
        dim (int): Size of the high pass filter

    Returns:
        img (np.array): hpf image
    """

    # check that kernel for convolution is odd
    if not dim % 2:
        raise ValueError('The size of the highpass filter must be odd!')

    # create the Kernel
    kernel = np.ones((dim, dim))
    sl = dim//2
    kernel *= -1
    kernel[sl, sl] = dim**2 - 1

    # convolve
    img = convolve(img, kernel)[sl:-sl, sl:-sl]

    return img


def filter_by_temporal(s2_y):
    """
    Filters data based on the maximum
    temporal noise (Taken directly from EMVA1288 Source Code)
    TODO: this may need to be more robust

    Keyword Arguments:
        noise_vals (np.array): array to find index of maximum for
    Returns:
        idx (int): index location of max value
    """

    max_ = 0
    max_i = 0

    for i in range((len(s2_y) - 1), -1, -1):
        if (s2_y[i] >= max_) or \
                (s2_y[abs(i-1)] >= max_):
            max_ = s2_y[i]
            max_i = i
        elif (s2_y[i] < max_) and \
                (s2_y[abs(i - 1)] < max_):
            break

    idx = max_i

    if idx < 5:
        idx = np.argmax(s2_y)

    return idx


def get_index(vals, perc, upper=True):
    """
    Returns the upperindex location of a specified percent (70% input as 0.7)
    Example: if I wanted 20% to 70% of array I would input perc=0.7 and upper=True
    for upper index and perc=0.2 and upper=False for lower index

    Keyword Arguments:
        vals (np.array): array of numerical values
        perc (np.array): percent of max index is to be returned for
        upper (bool): if True then index returned will be max index if
                      False then index returned will be min index

    Returns:
        idx (int): index location closest to the perc within vals
    """

    # get value based on input percentage
    val = perc * vals.max()

    # case where we want max index after filtering
    if upper:
        vals_sub = vals[vals <= val]
        idx = np.argmax(vals_sub)

    # case where we want min index after filtering
    else:
        vals_sub = vals[vals >= vals]
        idx = np.argmin(vals_sub)

    return idx


def find_closest(arr, val):
    """
    return the index of the closest value to request
    val in arr

    Keyword Arguments:
        arr (np.array): array of values
        val (float): value to find closest value in array for

    Returns:
        idx (int): index of closest value
    """

    arr = np.asarray(arr)
    idx = (np.abs(arr-val)).argmin()
    return idx


def remove_black(df, cols=[]):
    """
    remove black level from df columns, ex. mean -->
    mean - dark mean, assumes index 0 is black level
    value

    Keyword Arguments:
        df (pd.DataFrame): DataFrame of data to subtract black
                           level from
        cols (list): list of cols to create new columns for,
                     if non specified all will be done

    Returns:
        df (pd.DataFrame): DataFrame with new black level columns
                           added in the following format:
                           'col' --> '{col} - Dark {col}'
    """

    temp = pd.DataFrame()

    # get columns we should use
    if len(cols) == 0:
        cols = list(df.columns)

    # remove black level
    temp = df[cols] - df[cols].iloc[0]

    # rename columns
    for cc in temp.columns:
        temp.rename(columns={cc: f'{cc}_black_subtracted'}, inplace=True)

    # add to original df
    df = df.join(temp)

    return df


def join_frame(df, dict_):
    """
    performe a merge operation on df and dictionary always
    preserving the largest axis

    Keyword Arguments:
        df (pd.DataFrame): DataFrame to perform join operation on
        dict_ (dictionary): dictionary of values to be added to df
    Returns:
        temp: (pd.DataFrame): DataFrame of joined values with all
                              data preserved
    """

    temp = pd.DataFrame()

    dict_df = \
        pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict_.items()]))

    if df.shape[0] > dict_df.shape[0]:
        how = 'left'
    else:
        how = 'right'

    temp = df.join(dict_df, how=how)

    return temp


def rename(df,
           rename_file=r'C:\workspace\characterization\characterization_ams\utilities\default-renames.yaml',
           renames=None,
           revert=False,
           is_print=False):
    """
    Rename columns in df based on yaml rename file

    Keyword Args:
        df (pandas.DataFrame, None): data to rename (columns)
        renames (dict, None): if None reads rename key:value pairs from the `rename_file`
                                field
        revert (bool, None): if True renames back to original
        is_print (bool, False): Print rename key:value pairs and return

    Returns:
        renamed (pandas.DataFrame): renamed data columns
    """

    renames = renames or yaml.full_load(open(rename_file))

    if is_print:
        return pd.DataFrame(renames, index=['renamed']).T

    if revert:
        renames = {v: k for k, v in renames.items()}

    return df.rename(columns=renames)


def stat_engine_col_rename():
    """
    Returns dict for renaming stat engine column
    """

    return {'tot_var': 'Tot Var [DN^2]',
            'col_var': 'Col Var [DN^2]',
            'row_var': 'Row Var [DN^2]',
            'pix_var': 'Pix Var [DN^2]',
            'tot_var_temp': 'Tot Temp Var [DN^2]',
            'col_var_temp': 'Col Temp Var [DN^2]',
            'row_var_temp': 'Row Temp Var [DN^2]',
            'pix_var_temp': 'Pix Temp Var [DN^2]',
            'mean': 'Mean Signal [DN]',
            'tot_var_black_subtracted':
            'Tot Var - Tot Dark Var [DN^2]',
            'col_va_black_subtracted':
            'Col Var - Col Dark Var [DN^2]',
            'row_var_black_subtracted':
            'Row Var - Row Dark Var [DN^2]',
            'pix_var_black_subtracted':
            'Pix Var - Pix Dark Var [DN^2]',
            'tot_var_temp_black_subtracted':
            'Tot Temp Var - Tot Dark Temp Var [DN^2]',
            'col_var_temp_black_subtracted':
            'Col Temp Var - Col Dark Temp Var [DN^2]',
            'row_var_temp_black_subtracted':
            'Row Temp Var - Row Dark Temp Var [DN^2]',
            'pix_var_temp_black_subtracted':
            'Pix Temp Var - Pix Dark Temp Var [DN^2]',
            'mean_black_subtracted': 'Signal - Dark [DN]',
            }
