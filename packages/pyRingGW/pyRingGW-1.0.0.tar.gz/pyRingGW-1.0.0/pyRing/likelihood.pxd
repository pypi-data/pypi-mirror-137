cimport numpy as np

cdef class detector:
    cdef public str name
    cdef public np.ndarray location
    cdef public np.ndarray time
    cdef public np.ndarray time_series
    cdef public np.ndarray normed_acf
    cdef public np.ndarray covariance
    cdef public np.ndarray inverse_covariance
    cdef public double     log_normalisation
    cdef public object     psd
    cdef public object     lal_detector
