from sklearn.model_selection import train_test_split

class Model():
    def __init__(self, X, y, medias, organic, settings, model):

        self.settings = settings
        self.model = model
        self.media_labels = medias
        self.media_labels = organic

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        self.X_actual = X
        self.y_actual = y
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def fit(self, y, X):
        return None

    # def results(self):
    #     results_df = pd.DataFrame(self.contribution().sum(), columns=['contribution'])
    #     results_df['share'] = results_df['contribution'] / results_df['contribution'].sum() * 100
    #     results_df['coefficient'] = self.coefficients
    #     results_df['pvalue'] = self._pvalues()
    #     results_df = pd.concat([results_df, self._confidence_intervals()], axis=1)
    #
    #     return np.around(results_df, 3)
    #
    # def contribution(self, X=None):
    #     if (X) is None:
    #         X = self.X_actual
    #
    #     coef_df = pd.DataFrame({'coefficient': self.coefficients}, index=X.columns)
    #
    #     data = []
    #     for x in list(X.columns):
    #         contrib = coef_df['coefficient'].loc[x] * X[x]
    #         data.append(contrib)
    #
    #     contrib_df = pd.DataFrame(data).T
    #
    #     return contrib_df
    #
    # def predict(self, X=None):
    #     contribution = self.contribution(X)
    #     y_pred = contribution.sum(axis=1)
    #     return y_pred
    #
    # def metrics(self, metric_labels):
    #     metrics = []
    #     for metric in metric_labels:
    #         value = check_metric(metric, self)
    #         metrics.append((metric, value))
    #     for label, output in metrics:
    #         print(f"{output[1]} {label}: {output[0]}")
    #
    # def metric(self, metric_label):
    #     value = check_metric(metric_label, self)
    #     return value[0]

    # def _save(self):
    #     file = self.settings['file']
    #     file_paths = file.split('/')
    #     filename = file_paths.pop()
    #     file_paths.append("models-" + filename)
    #     file_loc = '/'.join(file_paths)
    #     models_output = pd.DataFrame.from_dict([{
    #         'file': self.settings['file'],
    #         'model': self.model,
    #         'metric': self.settings['metric'],
    #         'error': self.metric(self.settings['metric']),
    #         'timestamp': dt.datetime.today().strftime('%Y-%m-%d %H:%M'),
    #         'runtime': self.runtime,
    #         'y_label': self.y_train.name,
    #         'X_labels': ', '.join(list(self.X_train.columns)),
    #     }])
    #     if os.path.isfile(file_loc):
    #         # save to existing file
    #         loaded_models = pd.read_csv(file_loc)
    #         all_models = loaded_models.append(models_output)
    #         all_models.to_csv(file_loc, index=False)
    #         print("added model to existing file")
    #     else:
    #         # save new model file
    #         models_output.to_csv(file_loc, index=False)
    #         print("added new model file locally")

    # def show(self, charts=True, metrics=True, results=True):
    #     accuracy(self.y_actual, self.predict()) if charts else False
    #     self.metrics(["rsquared", "nrmse", "mape", "decomp-rssd", "cond-no"]) if metrics else False
    #     display(self.results()) if results else False








