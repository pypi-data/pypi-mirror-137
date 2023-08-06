import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.compose import make_column_transformer
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV

def regressor(train_df, target_col, numeric_feats = None, categorical_feats=None, cv=5):
    """This function preprocess the data, fit baseline model(dummyregresor) and ridge with default setups to provide data scientists 
        easy access to the common models results(scores). 

        Parameters
        ----------
        train_df : pandas.DataFrame
            The clean train data which includes target column.
        target_col : str
            The column of the train data that has the target values.
        numeric_feats = list, optional
            The numeric features that needs to be considered in the model. If the user do not define this argument, the function will assume all the columns except the identified ones in other arguments as numeric features.
        categorical_feats : list, optional
            The categorical columns for which needs onehotencoder preprocessing.  
        cv : int, optional
            The number of folds on the data for train and validation set.

        Returns
        -------
        Data frame
            A data frame that includes test scores and train scores for each model.
        Examples
        -------
        >>> regressor(train_df, target_col = 'popularity', categorical_features='genre')
        >>> regressor(train_df, target_col = 'popularity', numeric_feats = ['danceability', 'loudness'], categorical_feats=['genre'], cv=10)
    """
    

    #Checking the type of inputs
    if not(isinstance(train_df , pd.core.frame.DataFrame)):
        raise TypeError("train_df must be a pandas dataframe. Please pass a pd.core.frame.DataFrame train_df.")
    if not(isinstance(target_col , str)):
        raise TypeError("target_col must be a str. Please pass target column in str object.")
    if not(isinstance(numeric_feats , list)) and numeric_feats is not None:
        raise TypeError("numeric_feats must be a list. Please pass a list of numeric columns.")
    if categorical_feats is None :
        categorical_feats = []
    elif not(isinstance(categorical_feats , list)):
        raise TypeError("categorical_feats must be a list. Please pass a list of categorical columns.")

    #Checking the valid value for the inputs
    if (not (train_df.isna().sum().sum() == 0)) :
        raise ValueError(
            f"Invalid train_df input. Please pass a clean pandas data frame"
        )

    valid_target_col = train_df.select_dtypes('number').columns.tolist()

    if (not (target_col in valid_target_col)):
        raise ValueError(
            f"Invalid target_col input. Please use one out of {valid_target_col} in str"
        )

    X_train = train_df.drop(columns=target_col, axis=1)
    y_train = train_df[target_col]

    valid_numeric_col = X_train.select_dtypes('number').columns.tolist()
    valid_categorical_col =  X_train.select_dtypes(exclude='number').columns.tolist()

    if numeric_feats is None:
        numeric_feats = valid_numeric_col
    elif not (set(numeric_feats).issubset(set(valid_numeric_col))):
        raise ValueError(
            f"Invalid numeric features. Please use a sublist out of {valid_numeric_col}"
        )
    if not (set(categorical_feats).issubset(set(valid_categorical_col))):
        raise ValueError(
            f"Invalid categorical features. Please use a sublist out of {valid_categorical_col}"
        )

    
    #PReprocessing and modeling
    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(), categorical_feats)
    )

    dummy = DummyRegressor()
    ridge = make_pipeline(preprocessor, Ridge())
    ridge_cv = make_pipeline(preprocessor, RidgeCV(cv = cv))
    lr = make_pipeline(preprocessor, LinearRegression())

    results = pd.Series(dtype='float64') 

    models = {"DummyRegressor": dummy, "Ridge" : ridge, "RidgeCV" : ridge_cv, "linearRegression" : lr}

    for model in models :
        scores = cross_validate(models[model], X_train, y_train, return_train_score = True,cv = cv)
        mean_scores = pd.DataFrame(scores).mean().to_frame(model)
        results = pd.concat([results, mean_scores], axis = 1)
    results = results.drop(columns = 0, axis=1)
    
    return results