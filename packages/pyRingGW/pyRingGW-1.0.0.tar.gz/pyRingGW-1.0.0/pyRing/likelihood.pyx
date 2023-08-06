#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: cdivision=True
#cython: language_level=3
#cython: embedsignature=True

#Standard python imports
from __future__ import division
from scipy.linalg import toeplitz, solve_toeplitz, inv
from libc.math cimport log, M_PI
import  numpy as np, scipy
cimport numpy as np
cimport cython

#LVC imports
import lal
from   lal import ComputeDetAMResponseExtraModes, GreenwichMeanSiderealTime, LIGOTimeGPS

#Package internal imports
from pyRing      import noise

cdef double log2pi = log(2.0*M_PI)

cpdef tuple toeplitz_slogdet(np.ndarray[double, ndim=1] r):

    """
        Method from Marano et al. "Fitting Earthquake Spectra: Colored Noise and Incomplete Data", Bulletin of the Seismological Society of America, Vol. 107, No. 1, pp. –, February 2017, doi: 10.1785/0120160030
        Code available here: http://mercalli.ethz.ch/~marra/publications/2017_fitting_earthquake_spectra_colored_noise_and_incomplete_data/
        All credits go to the original authors.

        Compute the log determinant of a positive-definite symmetric toeplitz matrix.
        The determinant is computed recursively. The intermediate solutions of the
        Levinson recursion are exploited.

        parameters:
            r      : first row of the Toeplitz matrix

        returns:
            sign   : sign of the determinant
            logdet : natural log of the determinant
    """

    cdef int k, n
    cdef double r_0, logdet, sign, alpha, beta, d, mu
    cdef np.ndarray[double, ndim=1] x, y, b

    n      = len(r)
    r_0    = r[0]
    r      = np.concatenate((r, np.array([r_0])))
    r     /= r_0 # normalize the system so that the T matrix has diagonal of ones
    logdet = n*np.log(np.abs(r_0))
    sign   = np.sign(r_0)**n

    if(n == 1):
        return (sign, logdet)

    # From this point onwards, is a modification of Levinson algorithm.
    y       = np.zeros((n,))
    x       = np.zeros((n,))
    b       = -r[1:n+1]
    r       = r[:n]
    y[0]    = -r[1]
    x[0]    = b[0]
    beta    = 1
    alpha   = -r[1]
    d       = 1 + np.dot(-b[0], x[0])
    sign   *= np.sign(d)
    logdet += np.log(np.abs(d))

    for k in range(0, n-2):

        beta     = (1 - alpha*alpha)*beta
        mu       = (b[k+1] - np.dot(r[1:k+2], x[k::-1])) /beta
        x[0:k+1] = x[0:k+1] + mu*y[k::-1]
        x[k+1]   = mu

        d        = 1 + np.dot(-b[0:k+2], x[0:k+2])
        sign    *= np.sign(d)
        logdet  += np.log(np.abs(d))

        if(k < n-2):
            alpha    = -(r[k+2] + np.dot(r[1:k+2], y[k::-1]))/beta
            y[0:k+1] = y[0:k+1] + alpha * y[k::-1]
            y[k+1]   = alpha

    return (sign, logdet)

cdef class detector:

    def __cinit__(self, str ifo_name, str datafile, **kwargs):

        self.lal_detector                      = lal.cached_detector_by_prefix[ifo_name]
        self.location                          = self.lal_detector.location
        self.time_series, covariance, self.psd = noise.load_data(ifo_name, datafile, **kwargs)
        self.time                              = kwargs['trigtime']+np.linspace(-kwargs['signal-chunksize']/2, kwargs['signal-chunksize']/2, len(self.time_series))
        # Save the times and data that will be actually used in the likelihood.
        np.savetxt(kwargs['output']+'/Noise/times_data_{det}.txt'.format(det=ifo_name), np.column_stack((self.time, self.time_series)))

        self.inverse_covariance = inv(covariance)
        if kwargs['no-lognorm']:
            self.log_normalisation = 0.
        else:
            self.log_normalisation = -0.5*toeplitz_slogdet(covariance[0])[1] - 0.5*(covariance.shape[0])*log2pi

cpdef double inner_product(np.ndarray[double, ndim=2] C,
                           np.ndarray[double, ndim=1] X):
    return np.dot(X,np.dot(C,X))

cpdef double loglikelihood_core(np.ndarray[double, ndim=1] residuals,
                                np.ndarray[double, ndim=2] inverse_covariance,
                                double log_normalisation):
    return -0.5*inner_product(inverse_covariance, residuals) + log_normalisation

cpdef double loglikelihood_core_onsource(np.ndarray[double, ndim=1] residuals):

    # solve_toeplitz returns np.dot(inv(toeplitz(acf)), residuals)

    cdef np.ndarray[double, ndim=1] onsource_ACF = noise.acf(residuals)
    cdef double onsource_log_normalisation       = -0.5*toeplitz_slogdet(onsource_ACF)[1] - 0.5*(len(onsource_ACF))*log2pi
    cdef np.ndarray[double, ndim=1] rwt          = solve_toeplitz(onsource_ACF, residuals)

    return -0.5*np.dot(residuals, rwt) + onsource_log_normalisation

cpdef np.ndarray[double,ndim=1] project(np.ndarray[double,ndim=1] hs,
                                        np.ndarray[double,ndim=1] hvx,
                                        np.ndarray[double,ndim=1] hvy,
                                        np.ndarray[double,ndim=1] hp,
                                        np.ndarray[double,ndim=1] hc,
                                        detector,
                                        double ra,
                                        double dec,
                                        double psi,
                                        object tgps):

    #==============================================================================#
    # Project complex time series onto the given detector (laldetector structure). #
    # Signal is shifted in time relative to the geocenter.                         #
    # ra   - right ascension                                                       #
    # dec  - declination                                                           #
    # psi  - polarisation angle                                                    #
    # tgps - time (GPS seconds)                                                    #
    #==============================================================================#

    cdef double gmst, fs, fvx, fvy, fp, fc
    gmst   = GreenwichMeanSiderealTime(tgps)
    #The breathing and longitudinal modes act on a L-shaped detector in the same way up to a constant amplitude, thus we just use one. See Isi-Weinstein, arxiv 1710.03794
    fp, fc, fb, fs, fvx, fvy = ComputeDetAMResponseExtraModes(detector.response, ra, dec, psi, gmst)
    cdef np.ndarray[double, ndim=1] waveform = fs*hs + fvx*hvx + fvy*hvy + fp*hp + fc*hc

    return waveform

cpdef double loglikelihood(object model,
                           object x,
                           object waveform_model,
                           double ra,
                           double dec,
                           double psi,
                           double t_start,
                           dict time_delay,
                           str ref_det,
                           int truncate,
                           int duration_n,
                           unsigned int OnsourceACF  = 0,
                           unsigned int Dirac_comb   = 0,
                           unsigned int Zeroing_data = 0):

    cdef double dt
    cdef double logL = 0.0
    cdef np.ndarray[double, ndim=1] residuals, time_array, time_array_raw, data, prediction, zeros_array, zerod_data, hs, hvx, hvy, hp, hc
    cdef object tref

    for d in model.detectors.keys():

        # Waveform starts at time 0, so we need the 0 to be at model.tevent+dt
        # Sample times for each detector are: d.time-(model.tevent + dt)
        dt   = time_delay['{0}_'.format(ref_det)+d]
        tref = LIGOTimeGPS(t_start+dt+model.tevent)

        if not truncate:
            time_array     = model.detectors[d].time - (model.tevent+dt)
            data           = model.detectors[d].time_series
        else:
            # crop data
            time_array_raw = model.detectors[d].time - (model.tevent+dt)
            time_array     = time_array_raw[time_array_raw >= t_start][:duration_n]
            data           = model.detectors[d].time_series[time_array_raw >= t_start][:duration_n]

        if waveform_model is not None:

            wf_model             = waveform_model.waveform(time_array)
            hs, hvx, hvy, hp, hc = wf_model[0], wf_model[1], wf_model[2], wf_model[3], wf_model[4]

            if(Dirac_comb):
                #NO-REVIEW-NEEDED
                prediction  = np.concatenate((data[time_array < t_start], project(hs, hvx, hvy, hp, hc, model.detectors[d].lal_detector, ra, dec, psi, tref)[time_array >= t_start]), axis=None)
                residuals   = data - prediction
            elif(Zeroing_data):
                #NO-REVIEW-NEEDED
                zeros_array = np.zeros(time_array.shape[0], dtype='double')
                zerod_data  = np.concatenate((zeros_array[time_array < t_start], data[time_array >= t_start]), axis=None)
                residuals   = zerod_data - project(hs, hvx, hvy, hp, hc, model.detectors[d].lal_detector, ra, dec, psi, tref)
            else:
                residuals   = data - project(hs, hvx, hvy, hp, hc, model.detectors[d].lal_detector, ra, dec, psi, tref)
        else:
            residuals = data

        if(OnsourceACF):
            logL += loglikelihood_core_onsource(residuals)
        else:
            logL += loglikelihood_core(residuals, model.detectors[d].inverse_covariance, model.detectors[d].log_normalisation)

    return logL
