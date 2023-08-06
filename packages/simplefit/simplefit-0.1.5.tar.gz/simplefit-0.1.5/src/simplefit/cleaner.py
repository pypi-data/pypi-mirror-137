import pandas as pd
import numpy as np

def cleaner(input_dataframe,lower_case=False):
    """
        Load downloaded data, clean the dataset, remove the NA score. 
        Clean data(remove Nan rows, strip extra white spaces from column names, and data, convert all column names to lower case, etc)
        
        Parameters
        ----------
        input_dataframe: pandas.DataFrame
            Data set to clean
        drop_nans: boolean
             Drop all rows that have a NaN in any column (default: False)
        
        Returns
        --------
            (DataFrame):  A cleaned and simplified DataFrame of the relevant columns for summary and visualization,

        Examples
        --------
        >>>cleaner(example_data)
    """
    ## Handle dataframe type error (Check if dataframe is of type Pandas DataFrame)
    if not isinstance(input_dataframe, pd.DataFrame):

        raise TypeError(f"passed dataframe is of type {type(input_dataframe).__name__}, should be DataFrame")
        
    # Handle empty dataframe or dataframe with all NAN
    if (input_dataframe.empty or input_dataframe.dropna().empty):

        raise ValueError("passed dataframe is None")

    # Handle type Value error (Check if is a boolean')
    if not isinstance(lower_case, bool):

        raise TypeError("passed type should be a boolean")

    # Drop all rows that have a NaN in any column
    input_dataframe.dropna(inplace=True)
        
    # Strip extra white spaces from column names, and data
    input_dataframe = input_dataframe.rename(columns=lambda x: x.strip())
    
    # convert all column names to lower case (default: False)
    if lower_case:
        input_dataframe.columns= input_dataframe.columns.str.strip().str.lower()
        
    return input_dataframe
