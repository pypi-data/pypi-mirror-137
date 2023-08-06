from sklearn.linear_model import LinearRegression
from model.modelClasses import Model
from src.cassandra.data import create_model


class Linear(Model):
    def __init__(self, X, y, medias, organic, settings):
        # inheritance and start timer
        super().__init__(X, y, medias, organic, settings, "Linear")

        # fit the model
        self.model = self.fit()



    # fit the model
    def fit(self):
        return create_model(self.medias, self.organic, LinearRegression()).fit(self.X_train, self.y_train)
