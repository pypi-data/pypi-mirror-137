import sklearn
class MakeEpochs(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    def __init__(self, fs, ival):
        self.fs = fs
        self.ival = ival

    def fit(self, X, y=None):
        '''Nothing. for compatibility purposes'''
        return self

    # this is a deviation from sklearn standards, as the y-values are transformed as well.
    # I (gabriel) wrote a custom pipeline for this, I'll try to get it into the official sklearn build
    def transform(self, X, y):
        """Make Epochs.

        Parameters
        ----------
        X : ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        y : ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        Returns
        -------
        covmats : ndarray, shape (n_matrices, n_channels, n_channels)
            Covariance matrices.
        """
        epo, epo_t = makeepochs(X, self.fs, y[0], self.ival)
        self.epo_t = epo_t
        return epo, y[1]


