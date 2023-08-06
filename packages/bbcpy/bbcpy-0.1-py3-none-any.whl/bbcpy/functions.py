import numpy as np
def makeepochs(X: object, fs: object, mrk_pos: object, ival: object) -> object:
    '''
    Usage:
        makeepochs(X, fs, mrk_pos, ival)
    Parameters:
        X: 2D array of multi-channel timeseries (channels x samples)
        fs: sampling frequency [Hz]
        mrk_pos: marker positions [sa]
        ival: a two element vector giving the time interval relative to markers (in ms)
    Returns:
        epo: a 3D array of segmented signals (samples x channels x epochs)
        epo_t: a 1D array of time points of epochs relative to marker (in ms)
    '''
    time = np.arange(int(np.floor(ival[0] * fs / 1000)),
                     int(np.ceil(ival[1] * fs / 1000)) + 1)[np.newaxis, :]
    T = time.shape[1]
    nEvents = len(mrk_pos)
    nChans = X.shape[0]
    idx = (time.T + np.array([mrk_pos])).reshape(T * nEvents)
    epo = np.array(X)[:, idx].T.reshape(T, nEvents, nChans)
    epo = np.transpose(epo, (0, 2, 1))
    epo_t = np.linspace(ival[0], ival[1], T)
    return epo, epo_t