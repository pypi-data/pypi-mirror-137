from cpython cimport array
cimport numpy as np

cdef public dict interpolate_freqs
cdef public dict interpolate_taus
cdef public list Interpolated_ls
cdef public list Interpolated_ms
cdef public list Interpolated_ns

cdef class QNM:

    cdef public unsigned int s
    cdef public unsigned int l
    cdef public int          m
    cdef public unsigned int n
    cdef public object omegar_interp
    cdef public object omegai_interp

    cpdef double f(self, double M, double a)
    cpdef double tau(self, double M, double a)
    cpdef double f_KN(self, double M, double a, double Q)
    cpdef double tau_KN(self, double M, double a, double Q)

cdef class QNM_fit:

    cdef public unsigned int l
    cdef public int          m
    cdef public unsigned int n
    cdef public unsigned int charge
    cdef public object f_coeff
    cdef public object q_coeff

    cpdef double f(self, double M, double a)
    cpdef double q(self, double a)
    cpdef double tau(self, double M, double a)

    cpdef double f_KN(self, double M, double a, double Q)
    cpdef double q_KN(self, double a, double Q)
    cpdef double tau_KN(self, double M, double a, double Q)


cdef class QNM_ParSpec:

    cdef public unsigned int l
    cdef public int          m
    cdef public unsigned int n
    cdef public object f_coeff
    cdef public object tau_coeff

    cpdef double f(self, double M, double a, double gamma, np.ndarray[double, ndim=1] dw_vec)
    cpdef double tau(self, double M, double a, double gamma, np.ndarray[double, ndim=1] dw_vec)

cdef class QNM_220_area_quantized:

    cdef public unsigned int l_QA
    cdef public int          m_QA
    cdef public unsigned int n_QA
    cdef public object q_coeff_GR

    cpdef double f_QA(self, double M, double a, double alpha)
    cpdef double q_GR(self, double a)
    cpdef double tau_QA(self, double M, double a, double alpha)

cdef class Damped_sinusoids:

    cdef public dict A
    cdef public dict f
    cdef public dict tau
    cdef public dict phi
    cdef public dict t0

    cdef public dict N

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] t)

cdef class Morlet_Gabor_wavelets:

    cdef public dict A
    cdef public dict f
    cdef public dict tau
    cdef public dict phi
    cdef public dict t0

    cdef public dict N

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] t)

cdef class SWSH:

    cdef public int    l
    cdef public int    m
    cdef public int    s
    cdef public double swsh_prefactor

    cpdef complex evaluate(self, double theta, double phi)

cdef class KerrBH:

    cdef public double       t0
    cdef public double       Mf
    cdef public double       af
    cdef public dict         amps
    cdef public double       r
    cdef public double       iota
    cdef public double       phi
    cdef public dict         TGR_params
    cdef public double       reference_amplitude
    cdef public unsigned int geom
    cdef public unsigned int qnm_fit
    cdef public dict         interpolants
    cdef public unsigned int Spheroidal
    cdef public unsigned int amp_non_prec_sym
    cdef public unsigned int AreaQuantization
    cdef public unsigned int ParSpec
    cdef public unsigned int charge


    cdef public dict         qnms
    cdef public dict         qnms_ParSpec
    cdef public dict         swshs

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] times)

cdef class MMRDNS:

    cdef public double       t0
    cdef public double       Mf
    cdef public double       af
    cdef public double       eta
    cdef public double       r
    cdef public double       iota
    cdef public double       phi
    cdef public dict         TGR_params
    cdef public int          single_l
    cdef public int          single_m
    cdef public int          single_n
    cdef public unsigned int single_mode
    cdef public unsigned int Spheroidal
    cdef public dict         interpolants
    cdef public unsigned int qnm_fit

    cdef public list         multipoles

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] times)


cdef class MMRDNP:

    cdef public double       t0
    cdef public double       Mf
    cdef public double       af
    cdef public double       Mi
    cdef public double       eta
    cdef public double       chi_s
    cdef public double       chi_a
    cdef public double       r
    cdef public double       iota
    cdef public double       phi
    cdef public dict         TGR_params
    cdef public int          single_l
    cdef public int          single_m
    cdef public unsigned int single_mode
    cdef public unsigned int geom
    cdef public unsigned int qnm_fit     
    cdef public dict         interpolants

    cdef public double       delta
    cdef public dict         multipoles

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] times)

cdef class KHS_2012:

    cdef public double       t0
    cdef public double       Mf
    cdef public double       af
    cdef public double       eta
    cdef public double       chi_eff
    cdef public double       r
    cdef public double       iota
    cdef public double       phi
    cdef public dict         TGR_params
    cdef public int          single_l
    cdef public int          single_m
    cdef public unsigned int single_mode

    cdef public list         multipoles

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] times)

cdef class TEOBPM:

    cdef public double t0
    cdef public double m1
    cdef public double m2
    cdef public double s1z
    cdef public double s2z
    cdef public dict   phases
    cdef public double M
    cdef public double r
    cdef public double iota
    cdef public double phi
    cdef public dict TGR_params
    cdef public int single_l
    cdef public int single_m
    cdef public unsigned int single_mode
    cdef public unsigned int geom

    cdef public list multipoles
    cdef public dict fit_coefficients

    cdef public double nu
    cdef public double X12
    cdef public double Shat
    cdef public double a12
    cdef public double Sbar
    cdef public double aK
    cdef public double Mf
    cdef public double af

    cdef dict _EOBPM_SetupFitCoefficients(self, int l, int m)
    cdef double _TEOBPM_Amplitude(self, double tau, double sigma_real, double a1, double a2, double a3, double a4)
    cdef double _TEOBPM_Phase(self, double tau, double sigma_imag, double phi_fundamental, double p1, double p2, double p3, double p4)
    cdef np.ndarray[complex,ndim=1] _TEOBPM_single_multipole(self, double[::1] time, double tlm, double philm, int l, int m, int N)
    cdef np.ndarray[double, ndim=5] _waveform(self, double[::1] times)

cdef class IMR_WF:

    cdef public double m1
    cdef public double m2
    cdef public double s1z
    cdef public double s2z
    cdef public double dist
    cdef public double cosiota
    cdef public double phi
    cdef public double t0
    cdef public double dt
    cdef public double starttime
    cdef public double signal_seglen

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] times)
