import pandas as pd
import altair as alt


import os
alt.renderers.enable('html')
# alt.renderers.enable('mimetype')


def plot_distributions(data, bins = 40, dist_cols=None, class_label=None):
    """This function creates numerical distribution plots on either all the numeric columns or the ones provided to it
        
        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe for which distribution plot has to be created
        bins : int
            The number of bins for histogram plot
        dist_cols : list, optional
            The subset of numeric columns for which the histogram plots have to be generated
        class_label : str, optional
            The name of the target column only in case of classification dataset. For regression dataset, it is not required
        Returns
        -------
        chart_numeric
            The Altair object for the plot
        Examples
        -------
        >>> plot_distributions(data)
        >>> plot_distributions(data, dist_cols=['loudness', 'acousticness'], class_label='target')
    """
    if data is None:
        raise ValueError("Required arg 'data' cannot be empty")
    
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Please enter data of type pd.DataFrame")

    if not isinstance(bins, int):
        raise TypeError("bins should be of type int")

    if dist_cols is not None:
        if not isinstance(dist_cols, list):
            raise TypeError("The entered dist_cols should be of 'list' type")
        else:
            numeric_features = dist_cols
    else:
        numeric_features = list(data.select_dtypes('number').columns)

    if class_label is None:

        chart_numeric = alt.Chart(data).mark_bar().encode(
        alt.X(alt.repeat(), type='quantitative', bin=alt.Bin(maxbins=bins)),
                y=alt.Y('count()')
                ).properties(
                    width=300,
                    height=200
                ).repeat(
                    numeric_features, columns = 4
                ) 
        
    else:
        if not type(class_label) == str:
            raise TypeError("`class_label` should be of string type")
        else:

            chart_numeric = alt.Chart(data).mark_bar(opacity=0.6).encode(
            alt.X(alt.repeat(), type='quantitative', bin=alt.Bin(maxbins=bins)),
                    y=alt.Y('count()', stack=False),
                    color=class_label+':N'
                    ).properties(
                        width=300,
                        height=200
                    ).repeat(
                        numeric_features, columns = 2
                    ) 
    return chart_numeric


def plot_corr(data, corr='spearman'):
    """This function creates correlation plot for all the columns in the dataframe
        
        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe for which distribution plot has to be created
        corr : str
            The correlation method, which can be among 'spearman', 'kendall' or 'pearson'
            The default value is spearman
        Returns
        -------
        corr_plot
            The Altair object for the plot
        Examples
        -------
        >>> plot_corr(data)
        >>> plot_corr(data, corr='kendall')
    """    
    if data is None :
        raise ValueError("Required arg 'data' cannot be empty")
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Please enter data of type pd.DataFrame")
    if corr == '':
        raise ValueError("'corr' cannot be empty")
    if corr not in ['spearman', 'pearson', 'kendall']:
        raise ValueError("corr should be one of these: 'spearman', 'pearson', 'kendall'")

    corr_df= data.corr(corr).stack().reset_index(name='corr')
    corr_plot = alt.Chart(corr_df, title='Correlation Plot among all features and target').mark_rect().encode(
        x=alt.X('level_0', title='All features'),
        y=alt.Y('level_1', title='All features'),
        tooltip='corr',
        color=alt.Color('corr', scale=alt.Scale(domain=(-1, 1), scheme='purpleorange')))
    return corr_plot
  

def plot_splom(data, pair_cols=None):
    """This function creates SPLOM plot for all the numeric columns in the dataframe or the ones passed by the user
        
        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe for which distribution plot has to be created
        pair_cols : list
            The list of dataframe columns, for which correlation plot is to be generated
        Returns
        -------
        splom_chart
            The Altair object for the plot
        Examples
        -------
        >>> plot_splom(data)
        >>> plot_splom(data, pair_cols=['loudness', 'acousticness', 'energy'])
    """    
    if data is None :
        raise ValueError("Required arg 'data' cannot be empty")
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Please enter data of type pd.DataFrame")
    if pair_cols==[]:
        raise ValueError("pair_cols should not be empty list")
    if pair_cols is None:
        pair_cols = list(data.select_dtypes('number').columns)
    else:
        if not isinstance(pair_cols, list):
            raise TypeError("The entered pair_cols should be of 'list' type")
    splom_chart = alt.Chart(data).mark_point(opacity=0.3, size=10).encode(
    alt.X(alt.repeat('row'), type='quantitative'),
    alt.Y(alt.repeat('column'), type='quantitative')
    ).properties(
        width=200,
        height=200
    ).repeat(
        column=pair_cols,
        row=pair_cols
    )
    return splom_chart
    
