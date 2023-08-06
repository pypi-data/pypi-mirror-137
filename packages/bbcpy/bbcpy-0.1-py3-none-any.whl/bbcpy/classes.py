# importing pyriemann for their covariance methods. can be rewritten easily, would just clog this document
# !pip install pyriemann
import pyriemann as pr
import numpy as np
import sklearn
import scipy as sp
import scipy.signal
import warnings
import bbcpy.functions

class EEGmarker(np.ndarray):
    def __new__(cls, mrk_pos, mrk_class, mrk_className):
        obj = np.asarray(mrk_pos).view(cls)
        obj.y = np.array(mrk_class)
        obj.className: object = mrk_className
        return obj

    def __array_wrap__(self, out_arr, context=None):  #
        obj = super().__array_wrap__(out_arr, context)
        obj.y = self.y
        obj.className = self.className
        return obj

    def __init__(self, mrk_pos, mrk_class, mrk_className):
        return  # super().init()

    def __getitem__(self, key):
        obj = EEGmarker(super().__getitem__(key), self.y[key], self.className);
        return obj


class EEGdata(np.ndarray):
    def nT(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[0]

    def nCh(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[1]

    def __new__(cls, data, fs, mrk=[]):
        obj = np.asarray(data).view(cls)
        obj.fs = fs
        obj.mrk = mrk
        return obj

    def __init__(self, data, fs, mrk=[]):
        data = np.array(data)

    def __array_wrap__(self, out_arr, context=None, *args, **kwargs):  # used for printing etc
        obj = super().__array_wrap__(out_arr, context)
        obj.fs = self.fs
        obj.mrk = self.mrk
        return obj

    def epochs(self, ival, mrk=[]):
        if not len(mrk):
            try:
                mrk = self.mrk
            except (NameError, AttributeError):
                print('Error: Cannot make epochs: mrk not set.')
        [epo, epo_t] = bbcpy.functions.makeepochs(self.T, self.fs, mrk, ival)
        epo = EEGepo(epo, self.fs, self.mrk)
        epo.t = epo_t
        return epo

    def lfilter(self, band, order=5, filttype='*', filtfunc=sp.signal.butter):
        band = np.array(band)
        if filttype == '*':
            if band.shape == (2,):
                filttype = 'bandpass'
            else:
                filttype = 'low'
        [b, a] = filtfunc(order, band / self.fs * 2, filttype)
        return EEGdata(sp.signal.lfilter(b, a, self, axis=1), self.fs, self.mrk)

    def cov(self, estimator='scm', keep=True):
        # different covariance estimators possible
        if hasattr(self, 'C'):
            return self.C
        C = pr.utils.covariance._check_est(estimator)(self.T)
        if keep:
            self.C = C
        return C

    def pca(self, **kwargs):
        pca_fitter = sklearn.decomposition.PCA(**kwargs)
        pca_fitter = pca_fitter.fit(self)
        # data = pca_fitter.transform(self)
        data = EEGdata(pca_fitter.transform(self), self.fs, self.mrk)
        data.pcaobj = pca_fitter  # all values like W, A, d are stored in pca object of the EEGdata object
        # self.flat = data.flatten()
        return data


class EEGepo(EEGdata):

    def __new__(cls, data, fs, mrk):
        # print('hello')
        obj = np.asarray(data).view(cls)
        obj.fs = fs
        obj.y = mrk.y
        obj.className = mrk.className
        obj.mrk = mrk
        return obj

    def __init__(self, data, fs, mrk):
        data = np.array(data)
        assert len(data.shape) < 4

    def __array_wrap__(self, out_arr, context=None):  #
        obj = super().__array_wrap__(out_arr, context)
        obj.fs = self.fs
        obj.y = self.y
        obj.className = self.className
        obj.mrk = self.mrk
        return obj

    def __getitem__(self, key, /):
        if np.isscalar(key):
            allepo = True
        elif (len(key) < 3):
            allepo = True
        else:
            allepo = False
        if allepo:  # all epochs selectedno need to manipulate mrk
            obj = EEGepo(super().__getitem__(key), self.fs, self.mrk)
        else:  # select several epochs and return as EEGepo
            obj = EEGepo(super().__getitem__(key), self.fs, self.mrk[key[2]])
        return obj

    def nT(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[0]

    def nCh(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[1]

    def nEpo(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[2]

    def lfilter(self, band, order=5, filttype='*', filtfunc=sp.signal.butter):
        band = np.array(band)
        if len(band.shape):
            assert band.shape == (2,)
        warnings.warn(
            'Filtering the epoched data is not optimal due to filter artefacts. Consider filtering the continous data before segmentation.')
        band = np.array(band)
        if filttype == '*':
            if band.shape == (2,):
                filttype = 'bandpass'
            else:
                filttype = 'low'
        [b, a] = filtfunc(order, band / self.fs * 2, filttype)
        return EEGepo(sp.signal.lfilter(b, a, self, axis=0), self.fs, self.mrk)

    def cov(self, estimator='scm', keep=True):
        self.covmats = pr.estimation.Covariances(estimator).transform(self)
        return self
