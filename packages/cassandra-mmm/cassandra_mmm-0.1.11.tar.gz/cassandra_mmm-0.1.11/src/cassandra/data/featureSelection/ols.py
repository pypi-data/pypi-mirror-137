import statsmodels.api as sm


def ols(X, y, constant = True):

    if constant == True:
        X = sm.add_constant(X)

    #model = create_model(medias, organic, sm.OLS(y, X))
    model = sm.OLS(y, X)

    result = model.fit()
    print(result.summary())

    return result, model