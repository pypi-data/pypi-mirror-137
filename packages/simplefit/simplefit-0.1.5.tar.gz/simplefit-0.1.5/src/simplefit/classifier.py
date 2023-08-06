import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline


def classifier(train_df, target_col, numeric_feats = None, categorical_feats = None, cv = 5):
    """This function preprocess the data, fit baseline model(dummyclassifier) and logistic regression with default setups to provide data scientists 
        easy access to the common models results(scores). 
        
        Parameters
        ----------
        train_df : pandas.DataFrame
            The clean train data which includes target column.
        target_col : str
            The column of the train data that has the target values.
        numeric_feats = list
            The numeric features that needs to be considered in the model. If the user enters an empty list, the function will use all numeric columns.
        categorical_feats : list
            The categorical features that needs to be considered in the model. 
        cv : int, optional
            The number of folds on the data for train and validation set.
        Returns
        -------
        Data frame
            A data frame that includes test scores and train scores for each model.
        Examples
        -------
        >>> classifier(train_df, target_col = 'target', numerical_feats = [], categorical_features = [])
        >>> classifier(train_df, target_col = 'target', numeric_feats = ['danceability', 'loudness'], categorical_feats=['genre'], cv=10)
    """


    if (not(isinstance(train_df , pd.core.frame.DataFrame))):
        raise TypeError("Invalid function input. Please enter a data frame")
    if (not (train_df.isna().sum().sum() == 0)):
        raise ValueError("Invalid function input. Please pass a clean pandas data frame")
    if not(isinstance(numeric_feats , list)):
        raise TypeError("Numeric Features should be passed as a list")
    if not(isinstance(categorical_feats , list)):
        raise TypeError("Categorical Features should be passed as a list")
    if not(isinstance(target_col , str)):
        raise TypeError("Target column must be passed as a string")

    
    X_train = train_df.drop(columns=target_col, axis=1)
    y_train = train_df[target_col]


    if not isinstance(numeric_feats, list):
        raise TypeError("The numeric features have to be entered as a list")
    if not isinstance(categorical_feats , list):
        raise TypeError("The categorical features have to be entered as a list")
    
    if numeric_feats == None or numeric_feats==[]:
        numeric_feats = train_df.select_dtypes(include='number').columns.tolist()
    if categorical_feats == None or categorical_feats ==[]:
        categorical_feats = train_df.select_dtypes(exclude='number').columns.tolist()


    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(), categorical_feats))

    dummy = DummyClassifier()
    lr = make_pipeline(preprocessor, LogisticRegression())

    results = pd.Series(dtype='float64') 

    models = {"DummyClassifier": dummy, "LogisticRegression" : lr}

    for model in models :
        scores = cross_validate(models[model], X_train, y_train, return_train_score = True,cv = cv)
        mean_scores = pd.DataFrame(scores).mean().to_frame(model)
        results = pd.concat([results, mean_scores], axis = 1)
    results = results.drop(columns = 0, axis=1)
    
    return results




