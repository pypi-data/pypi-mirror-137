import altair as alt
import pandas as pd
import re


def boxplot(df, x, y, facet_col=""):
    """Plot a boxplot with the magma color scheme and an option to facet.

    Parameters
    ----------
    df : dataframe
        Dataframe containing the variables for plotting
    x : string
        Column name of the numerical variable to view the distribution of
    y : list
        Column name containing the categorical variables to assign boxes to
    facet_col : column to use for faceting
        Determines whether separate graphs will be created for each category

    Returns
    -------
    altair.vegalite.v4.api.Chart
        Boxplot displaying distribution of categorical variables with/without faceting

    Examples
    --------
    >>> from magmaviz.magmaviz import boxplot
    >>> from vega_datasets import data
    >>> boxplot(data.cars(), "Miles_per_Gallon", "Origin", facet_col="Cylinders")
    """

    # checking that the dataframe is a pandas dataframe type
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError(
            "'df' should be of type 'pandas.core.frame.DataFrame', a pandas dataframe."
        )
    # checking that type of column name for x is a string
    if not isinstance(x, str):
        raise TypeError("'x' should be of type 'str'.")
    # checking that type of column name for y is a string
    if not isinstance(y, str):
        raise TypeError("'y' should be of type 'str'.")
    # checking that type for facet is a boolean
    if not isinstance(facet_col, str):
        raise TypeError("'facet_col' should be of type 'string'.")

    # checking if x is a column name in the dataframe
    assert x in list(
        df.columns
    ), "This column specified for 'x' does not exist in the dataframe."
    # checking if y is a column name in the dataframe
    assert y in list(
        df.columns
    ), "This column specified for 'y' does not exist in the dataframe."
    # checking if facet_col is a column name in the dataframe

    if len(facet_col) > 0:
        assert facet_col in list(
            df.columns
        ), "This column specified for 'facet_col' does not exist in the dataframe."

    # creating titles
    x_title = re.sub(r"[_.,-]", " ", x)

    y_title = re.sub(r"[_.,-]", " ", y)

    # creating plot object
    plot = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X(x, title=x_title),
            y=alt.Y(y, title=y_title),
            color=alt.Color(y, scale=alt.Scale(scheme="magma"), legend=None),
        )
    )

    # facet if required
    if len(facet_col) > 0:
        return plot.facet(row=facet_col)

    else:
        return plot
