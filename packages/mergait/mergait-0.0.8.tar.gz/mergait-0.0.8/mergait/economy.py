""" Running economy related functions

These functions help footpod data with running economy data such as speed and force
"""

import pandas as pd


def append_force_and_speed_cadence(
    df,
    df_footpods_sc,
    df_phone_activity,
    timestamp_column="t",
    foot_column="foot",
    tolerance=pd.Timedelta(5.0, unit="s"),
):
    """
    Appends information about the speed cadence sensor and compute instantateous force.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the footpod data
    df_footpods_sc : pandas.Dataframe
        The DataFrame containing footpod speed-cadence information
    timestamp_column : str
        The column containing the timestamp (for sorting)
    foot_column : str
        The column containing the foot
    tolerance : pandas.Timedelta
        The optional maximum time between a step and the next step to be considered part of the same gait cycle

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended speed cadence information
    """

    df_new = pd.merge_asof(
        left=df,
        right=df_footpods_sc,
        on=[timestamp_column],
        by=[foot_column],
        direction="nearest",
        tolerance=tolerance,
    )
    df_new = pd.merge_asof(
        left=df_new,
        right=df_phone_activity[[timestamp_column, "speed", "cadence"]],
        on=[timestamp_column],
        suffixes=["_pod", "_phone"],
        direction="nearest",
        tolerance=tolerance,
    )
    df_new.index = df.index
    # df_new["force"] = df_new.power / df_new.speed_pod
    return df_new
