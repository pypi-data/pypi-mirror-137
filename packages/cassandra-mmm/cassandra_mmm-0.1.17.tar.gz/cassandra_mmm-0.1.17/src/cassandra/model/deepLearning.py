from dataProcessing.cleanFormatMerge import guess_categorical_variables, guess_numerical_variables
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer, Normalizer
from cassandra.model.modelEvaluation.evaluation import show_nrmse, show_mape


def deepLearning(df, X, y, target, name_model, metric = ['accuracy', 'nrmse', 'mape'], return_metric = False, cv=5, verbose=2):

    metrics_values = {}

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    all_features = list(X_train.columns)
    categorical = guess_categorical_variables(X_train)
    numerical = guess_numerical_variables(X_train.drop(categorical, axis=1))

    transformers = [
        ('one hot', OneHotEncoder(handle_unknown='ignore'), categorical),
        ('scaler', QuantileTransformer(), numerical),
        ('normalizer', Normalizer(), all_features)
    ]
    ct = ColumnTransformer(transformers)

    if len(df.index) < 1000:
        solver_value = 'lbfgs'
    else:
        solver_value = 'adam'

    steps = [
        ('column_transformer', ct),
        ('model', MLPRegressor(solver=solver_value))
        # solver 'lbfgs' is used for dataset with less than 1000 rows, if more than 1000 use solver 'adam'
    ]
    pipeline = Pipeline(steps)
    param_space = {
        'column_transformer__scaler__n_quantiles': [80, 100, 120],
        'column_transformer__normalizer': [Normalizer(), 'passthrough'],
        'model__hidden_layer_sizes': [(35, 35), (50, 50), (75, 75)],
        'model__alpha': [0.005, 0.001]
    }

    # input the param space into "param_grid", define what pipeline it needs to run, in our case is named "pipeline", and the you can decide how many cross validation can do "cv=" and the verbosity.
    model = GridSearchCV(pipeline, param_grid=param_space, cv=cv, verbose=verbose)
    model.fit(X_train, y_train)

    #model.best_estimator_

    # Ask the model to predict on X_test without having Y_test
    # This will give you exact predicted values

    # Score returns the accuracy of the above prediction or R^2
    if 'accuracy' in metric:
        accuracy = model.score(X_test, y_test)
        if return_metric:
            metrics_values[name_model + '_accuracy'] = accuracy
        print(name_model, 'Accuracy: ', accuracy)

    # We can use our NRMSE and MAPE functions as well

    # Create new DF not to edit the original one
    result = df

    # Create a new column with predicted values
    result['prediction'] = model.predict(result)

    # Get the NRMSE & MAPE values
    if 'nrmse' in metric:
        nrmse_val = show_nrmse(result[target], result['prediction'])
        if return_metric:
            metrics_values[name_model + '_nrmse'] = nrmse_val
        print(name_model, 'NRMSE: ', nrmse_val)

    if 'mape' in metric:
        mape_val = show_mape(result[target], result['prediction'])
        if return_metric:
            metrics_values[name_model + '_mape'] = mape_val
        print(name_model, 'MAPE: ', mape_val)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model