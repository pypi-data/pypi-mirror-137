import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, check_array
from scipy.signal import convolve2d
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import statsmodels.tsa.api as tsa

# Define the Adstock Class as a custom Transformer
class ExponentialCarryover(BaseEstimator, TransformerMixin):
    def __init__(self, strength=0.5, length=1):
        self.strength = strength
        self.length = length

    def fit(self, X, y=None):
        X = check_array(X)
        self._check_n_features(X, reset=True)
        self.sliding_window_ = (
                self.strength ** np.arange(self.length + 1)
        ).reshape(-1, 1)

        return self

    def transform(self, X: np.ndarray):
        check_is_fitted(self)
        X = check_array(X)
        self._check_n_features(X, reset=False)
        convolution = convolve2d(X, self.sliding_window_)

        if self.length > 0:
            convolution = convolution[: -self.length]

        return convolution


# Define the Saturation Class as a custom Transformer
class ExponentialSaturation:
    def __init__(self, a=1.):
        self.a = a

    def transform(self, X):
        return 1 - np.exp(-self.a * X)


class ExponentialSaturation(BaseEstimator, TransformerMixin):
    def __init__(self, a=1.):
        self.a = a

    def fit(self, X, y=None):
        X = check_array(X)
        self._check_n_features(X, reset=True)  # from BaseEstimator

        return self

    def transform(self, X):
        check_is_fitted(self)
        X = check_array(X)
        self._check_n_features(X, reset=False)  # from BaseEstimator

        return 1 - np.exp(-self.a * X)

def trasformation(media, organic):
    trasf = []
    for x in media:
         trasf.append(
             (x, Pipeline([
                               ('carryover', ExponentialCarryover()),
                               ('saturation', ExponentialSaturation())
             ]), [x]),
         )
    for x in organic:
        trasf.append(
            (x, Pipeline([
                           ('inputer', SimpleImputer())
         ]), [x]),
        )
    return trasf

def create_model(medias, organic, model):
    trasf = ColumnTransformer(
        trasformation(medias, organic)
    )

    steps = [
        ('trasformation', trasf),
        ('regression', model)
    ]
    model = Pipeline(steps)

    return model

# Function to return Adstocked variables
def adstock(x, theta):
    return tsa.filters.recursive_filter(x, theta)

# Function to return Saturated variables
def saturation(x, beta):
    return x ** beta
