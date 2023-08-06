# File Name: plot_metric.py
# Author: Rohit Rawat

import altair as alt
from covizpy.get_data import get_data

alt.data_transformers.enable("data_server")


def plot_metric(
    location="Canada", metric="positive_rate", date_from=None, date_to=None
):
    """
    Create a line chart visualizing COVID total new
    cases and another metric for a specific time period

    Parameters
    ----------
    location  : str, optional
                The name of the location to be plotted with the new COVID cases.
                It can be any of the values present in the location column of df
    metric    : str, optional
                The name of the metric to be plotted with the new COVID cases.
                It can be one of the these: "reproduction_rate", "positive_rate",
                or any other numeric column
    date_from : str, optional
                Start date of the plot in "YYYY-MM-DD" format, by default "2022-01-01"
    date_to   : str, optional
                End date of the plot in "YYYY-MM-DD" format, by default "2022-01-13"
    Returns
    -------
    chart
        The line chart created
    """

    # Check the input format of arguments
    if not isinstance(metric, str):
        raise TypeError("Incorrect argument type: Metric 1 input should be a string")

    if (not isinstance(date_from, str)) and date_from is not None:
        raise TypeError(
            "Incorrect argument type: The starting date should be in string format"
        )

    if (not isinstance(date_to, str)) and date_to is not None:
        raise TypeError(
            "Incorrect argument type: The end date should be in string format"
        )

    # Check if func it is able to fetch the data
    try:
        df = get_data(date_from, date_to)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Data not found! There may be a problem with data URL or your date format."
        )

    # Check whether the location is in the df or not
    if not isinstance(location, str):
        raise TypeError("Invalid argument type: location must be a single string.")

    if not (location in df.location.unique()):
        raise ValueError(
            "Invalid argument value: location is not present in available locations."
        )

    # Check if the metric provided is present in the data frame or not
    if metric not in df.columns:
        raise ValueError(
            "Incorrect argument value: The metric chosen is not one of the columns in dataframe"
        )

    df = df.query("location in @location")

    metric_label = "Mean " + metric.replace("_", " ")
    title_label = "Daily COVID cases versus " + metric_label + " in " + location

    base = alt.Chart(df).encode(
        x=alt.X(
            "yearmonthdate(date):T", axis=alt.Axis(format="%e %b, %Y"), title="Date"
        )
    )

    line1 = base.mark_line(color="skyblue", interpolate="monotone").encode(
        alt.Y(
            "sum(new_cases)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(title="Daily new cases", titleColor="skyblue"),
        )
    )

    line2 = base.mark_line(color="orange", interpolate="monotone").encode(
        alt.Y(
            f"mean({metric})",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(title=metric_label, titleColor="orange"),
        )
    )

    plot = alt.layer(line1, line2, title=title_label).resolve_scale(y="independent")

    return plot
