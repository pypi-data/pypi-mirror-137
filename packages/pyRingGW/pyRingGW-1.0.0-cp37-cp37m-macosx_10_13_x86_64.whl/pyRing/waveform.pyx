#Standard python imports
#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: cdivision=True
#cython: language_level=3
#cython: embedsignature=True
from __future__        import division
import numpy as np, os, scipy
cimport numpy as np, cython
from math              import factorial as fact
from libc.math cimport cos, pow, sin, sqrt, ceil, fabs, tanh, cosh, exp, log

#LVC imports
import lalsimulation as lalsim
import lal

#Package internal imports
from pyRing     cimport eob_utils as eu
from pyRing      import NR_amp
from pyRing.utils import resize_time_series, import_datafile_path

import pykerr

#cdef extern from "complex.h":
#    double complex exp(double complex)
cdef double MPC_SI = lal.PC_SI*1e6
cdef double mass_dist_units_conversion = lal.MSUN_SI* lal.G_SI / ( MPC_SI * lal.C_SI**2)
cdef double MTSUN_SI = lal.MTSUN_SI

# Fit of the complex ringdown frequencies for l = (2,3,4) and n = (0,1,2) from table VIII in http://arxiv.org/abs/gr-qc/0512160
cdef dict F_fit_coeff = {}
cdef dict q_fit_coeff = {}
Kerr_Berti_coeffs = np.genfromtxt(import_datafile_path('data/NR_data/berti_qnm_fits.txt'), names=True)
for i in xrange(Kerr_Berti_coeffs.shape[0]):
    F_fit_coeff[(int(Kerr_Berti_coeffs['l'][i]),int(Kerr_Berti_coeffs['m'][i]),int(Kerr_Berti_coeffs['n'][i]))] = [Kerr_Berti_coeffs['f1'][i],Kerr_Berti_coeffs['f2'][i],Kerr_Berti_coeffs['f3'][i]]
    q_fit_coeff[(int(Kerr_Berti_coeffs['l'][i]),int(Kerr_Berti_coeffs['m'][i]),int(Kerr_Berti_coeffs['n'][i]))] = [Kerr_Berti_coeffs['q1'][i],Kerr_Berti_coeffs['q2'][i],Kerr_Berti_coeffs['q3'][i]]

#FIXME temporary placeholder file
# Fit of the complex ringdown frequencies for l = (?) and n = (?) from ?
cdef dict F_KN_fit_coeff = {}
cdef dict q_KN_fit_coeff = {}
KN_coeffs = np.genfromtxt(import_datafile_path('data/NR_data/berti_qnm_fits.txt'), names=True)
for i in xrange(KN_coeffs.shape[0]):
    F_KN_fit_coeff[(int(KN_coeffs['l'][i]),int(KN_coeffs['m'][i]),int(KN_coeffs['n'][i]))] = [KN_coeffs['f1'][i],KN_coeffs['f2'][i],KN_coeffs['f3'][i]]
    q_KN_fit_coeff[(int(KN_coeffs['l'][i]),int(KN_coeffs['m'][i]),int(KN_coeffs['n'][i]))] = [KN_coeffs['q1'][i],KN_coeffs['q2'][i],KN_coeffs['q3'][i]]

# Fit of the QNM spin expansion coefficients for (l,m) = [(2,2), (2,1), (3,3)] and n = (0) from table I in arXiv:1910.12893v2
cdef dict f_ParSpec_coeff = {}
cdef dict tau_ParSpec_coeff = {}

ParSpec_coeffs = np.genfromtxt(import_datafile_path('data/NR_data/ParSpec_coefficients.txt'), names=True)
ParSpec_coeffs_f_order   = 4
ParSpec_coeffs_tau_order = 4
for i in xrange(ParSpec_coeffs.shape[0]):
    f_ParSpec_coeff[(int(ParSpec_coeffs['l'][i]),int(ParSpec_coeffs['m'][i]),int(ParSpec_coeffs['n'][i]))]   = [ParSpec_coeffs['w{}'.format(j)][i] for j in range(ParSpec_coeffs_f_order+1)]
    tau_ParSpec_coeff[(int(ParSpec_coeffs['l'][i]),int(ParSpec_coeffs['m'][i]),int(ParSpec_coeffs['n'][i]))] = [ParSpec_coeffs['t{}'.format(j)][i] for j in range(ParSpec_coeffs_tau_order+1)]

# Fit of the QNM spin expansion coefficients for (l,m,n) = [(2,2,0), (2,2,1)] modes, valid up to high spin.
cdef dict f_ParSpec_coeff_high_spin   = {}
cdef dict tau_ParSpec_coeff_high_spin = {}
ParSpec_coeffs_high_spin = np.genfromtxt(import_datafile_path('data/NR_data/ParSpec_coefficients_high_spin.txt'), names=True)
ParSpec_coeffs_f_order_high_spin   = 5
ParSpec_coeffs_tau_order_high_spin = 9
for i in xrange(ParSpec_coeffs_high_spin.shape[0]):
    f_ParSpec_coeff_high_spin[(int(ParSpec_coeffs_high_spin['l'][i]),int(ParSpec_coeffs_high_spin['m'][i]),int(ParSpec_coeffs_high_spin['n'][i]))]   = [ParSpec_coeffs_high_spin['w{}'.format(j)][i] for j in range(ParSpec_coeffs_f_order_high_spin+1)]
    tau_ParSpec_coeff_high_spin[(int(ParSpec_coeffs_high_spin['l'][i]),int(ParSpec_coeffs_high_spin['m'][i]),int(ParSpec_coeffs_high_spin['n'][i]))] = [ParSpec_coeffs_high_spin['t{}'.format(j)][i] for j in range(ParSpec_coeffs_tau_order_high_spin+1)]


cdef class QNM:

    def __cinit__(self,unsigned int s, unsigned int l, int m, unsigned int n, dict interpolants):
        self.s = s
        self.l = l
        self.m = m
        self.n = n

        self.omegar_interp = interpolants[(self.s,self.l,self.m,self.n)]['freq']
        self.omegai_interp = interpolants[(self.s,self.l,self.m,self.n)]['tau']

    cpdef double f(self, double M, double a):
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        return prefactor_freq*self.omegar_interp(a)

    cpdef double tau(self, double M, double a):
        cdef double prefactor_tau = (lal.C_SI*lal.C_SI*lal.C_SI/(lal.G_SI*M*lal.MSUN_SI))
        return -1.0/(self.omegai_interp(a)*prefactor_tau)

    cpdef double f_KN(self, double M, double a, double Q):
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        return prefactor_freq*self.omegar_interp(a, Q)

    cpdef double tau_KN(self, double M, double a, double Q):
        cdef double prefactor_tau = (lal.C_SI*lal.C_SI*lal.C_SI/(lal.G_SI*M*lal.MSUN_SI))
        return -1.0/(self.omegai_interp(a, Q)*prefactor_tau)

cdef class QNM_fit:

    def __cinit__(self,unsigned int l, int m, unsigned int n, unsigned int charge = 0):

        assert not(np.abs(m) > l), "QNM: m cannot be greater than l in modulus."
        assert not(np.abs(n) > 2), "Berti fits are not available for n>2. Please unselect the 'qnm-fit' option in order to obtain a direct interpolation from NR data."
        assert not(charge == 1),    "KN QNMs still do not support fits. Please set the qnm-fit=0"

        self.l       = l
        self.m       = m
        self.n       = n
        self.charge  = charge

        if(self.charge):
            self.f_coeff = F_KN_fit_coeff[(self.l,self.m,self.n)]
            self.q_coeff = q_KN_fit_coeff[(self.l,self.m,self.n)]
        else:
            self.f_coeff = F_fit_coeff[(self.l,self.m,self.n)]
            self.q_coeff = q_fit_coeff[(self.l,self.m,self.n)]

    cpdef double f(self, double M, double a):
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        return prefactor_freq*(self.f_coeff[0]+self.f_coeff[1]*(1-a)**self.f_coeff[2])

    cpdef double q(self, double a):
        return (self.q_coeff[0]+self.q_coeff[1]*(1-a)**self.q_coeff[2])

    cpdef double tau(self, double M, double a):
        return self.q(a)/(np.pi*self.f(M,a))

    cpdef double f_KN(self, double M, double a, double Q):
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        return prefactor_freq*(self.f_coeff[0]+self.f_coeff[1]*(1-a)**self.f_coeff[2])

    cpdef double q_KN(self, double a, double Q):
        return (self.q_coeff[0]+self.q_coeff[1]*(1-a)**self.q_coeff[2])

    cpdef double tau_KN(self, double M, double a, double Q):
        return self.q_KN(a, Q)/(np.pi*self.f_KN(M, a, Q))

#NO-REVIEW-NEEDED
cdef class QNM_ParSpec:

    def __cinit__(self,unsigned int l, int m, unsigned int n, fit='high_spin'):

        assert not(np.abs(m) > l), "QNM: m cannot be greater than l in modulus."
        
        self.l         = l
        self.m         = m
        self.n         = n
        if(fit=='high_spin'):
            self.f_coeff   = f_ParSpec_coeff_high_spin[(self.l,self.m,self.n)]
            self.tau_coeff = tau_ParSpec_coeff_high_spin[(self.l,self.m,self.n)]
        else:
            self.f_coeff   = f_ParSpec_coeff[(self.l,self.m,self.n)]
            self.tau_coeff = tau_ParSpec_coeff[(self.l,self.m,self.n)]     

    cpdef double f(self, double M, double a, double gamma, np.ndarray[double, ndim=1] dw_vec):
        cdef int D_max = len(self.f_coeff)
        cdef int D_dw  = len(dw_vec)
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        ParSpec_fit_freq = 0.0
        for i in range(D_max):
            # Apply the deviations up to a given order, while the expansion has to stay valid up to the maximum order to avoid fake GR deviations.
            if(i < D_dw): ParSpec_fit_freq += a**i * self.f_coeff[i] * (1 + gamma * dw_vec[i])
            else:         ParSpec_fit_freq += a**i * self.f_coeff[i]
        
        return prefactor_freq*ParSpec_fit_freq

    cpdef double tau(self, double M, double a, double gamma, np.ndarray[double, ndim=1] dt_vec):
        cdef int D_max = len(self.tau_coeff)
        cdef int D_dt  = len(dt_vec)
        cdef double prefactor_tau = 1.0/(lal.C_SI*lal.C_SI*lal.C_SI/(lal.G_SI*M*lal.MSUN_SI))
        ParSpec_fit_tau = 0.0
        for i in range(D_max):
            # Apply the deviations up to a given order, while the expansion has to stay valid up to the maximum order to avoid fake GR deviations. 
            if(i < D_dt): ParSpec_fit_tau += a**i * self.tau_coeff[i] * (1 + gamma * dt_vec[i])
            else:         ParSpec_fit_tau += a**i * self.tau_coeff[i]
        return prefactor_tau*ParSpec_fit_tau

#NO-REVIEW-NEEDED
cdef class QNM_220_area_quantized:

    # Reference: arXiv:1611.07009v3
    # Since I couldn't find a quantum-inspired formula for tau, I am assuming GR in decay time
    def __cinit__(self,unsigned int l_QA, int m_QA, unsigned int n_QA):
        self.l_QA       = l_QA
        self.m_QA       = m_QA
        self.n_QA       = n_QA
        self.q_coeff_GR = q_fit_coeff[(self.l_QA,self.m_QA,self.n_QA)]

        assert ((self.l_QA == 2) and (self.m_QA == 2) and (self.n_QA == 0)), "The QNM coming from quantized are valid only for the 220 mode."

    cpdef double f_QA(self, double M, double a, double alpha):
        cdef double prefactor_freq = (lal.C_SI*lal.C_SI*lal.C_SI/(2.*np.pi*lal.G_SI*M*lal.MSUN_SI))
        cdef double n_tra     = 1 # Order of quantum transition, see pg.3
        cdef double m_grav    = 2 # Graviton, see pg.3
        return prefactor_freq*(n_tra*alpha*np.sqrt(1-a*a)+8*np.pi*a*m_grav)/(16*np.pi*(1+np.sqrt(1-a*a)))

    cpdef double q_GR(self, double a):
        return (self.q_coeff_GR[0]+self.q_coeff_GR[1]*(1-a)**self.q_coeff_GR[2])

    cpdef double tau_QA(self, double M, double a, double alpha):
        cdef double f_QA = self.f_QA(M, a, alpha)
        cdef double q_GR = self.q_GR(a)
        return q_GR/(np.pi*f_QA)

@cython.boundscheck(False) # turn off bounds-checking for entire function, increases the speed of the code.
cdef np.ndarray[complex,ndim=1] damped_sinusoid(double A,                     # Amplitude
                                                double f,                     # Frequency
                                                double tau,                   # Damping time
                                                double phi,                   # Phase
                                                double t0,                    # Start time
                                                np.ndarray[double, ndim=1] t  # Time array
                                               ):

    cdef unsigned int n                = t.shape[0]
    cdef np.ndarray[complex, ndim=1] h = np.zeros(n,dtype='complex')
    cdef double omega                  = 2.0*np.pi*f
    cdef complex om_cplx               = omega+1j/tau
    cdef int t_start_idx               = int(ceil((t0-t[0])/(t[1]-t[0])))

    h[t_start_idx:] = A*np.exp(1j*om_cplx*(t[t_start_idx:]-t0)+1j*phi)

    return h

cdef np.ndarray[complex,ndim=1] morlet_gabor_wavelet(double A,                     # Amplitude
                                                     double f,                     # Frequency
                                                     double tau,                   # Damping time
                                                     double phi,                   # Phase
                                                     double t0,                    # Start time
                                                     np.ndarray[double, ndim=1] t  # Time array
                                                    ):

    cdef unsigned int n                = t.shape[0]
    cdef np.ndarray[complex, ndim=1] h = np.zeros(n,dtype='complex')
    cdef double omega                  = 2.0*np.pi*f
    cdef int t_start_idx               = int(ceil((t0-t[0])/(t[1]-t[0])))

    #FIXME: this is real, while it should be a complex quantity.
    h[t_start_idx:] = A*np.cos(omega*(t[t_start_idx:]-t0)+phi)*np.exp(-((t[t_start_idx:]-t0)/(tau))**2)

    return h

cdef class Damped_sinusoids:

    """
    Class implementing a superposition of Damped Sinusoids of arbitrary polarisation.

    """
    def __cinit__(self,
                  dict A,
                  dict f,
                  dict tau,
                  dict phi,
                  dict t0):

        self.A   = A
        """
        :param A: Amplitudes
        """
        self.f   = f
        self.tau = tau
        self.phi = phi
        self.t0  = t0
        self.N   = {}
        for key in self.A.keys():
            self.N[key] = len(self.A[key])

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] t):

        """
            | Returns five polarisations (the ones independent in a L-shaped GW detector, see https://arxiv.org/abs/1710.03794) allowed for a metric theory of gravity: hs (scalar mode), {hvx, hvy} (vector modes), {hp, hc} (tensor modes).
            | We employ the conventions:
            | h_s           = sum_{i} A_i * cos(omega*t+phi)  * e^(-(t-t^{start}_i/tau)
            | h_vx - i h_vy = sum_{i} A_i * e^(i*omega*t+phi) * e^(-(t-t^{start}_i/tau)
            | h_+  - i h_x  = sum_{i} A_i * e^(i*omega*t+phi) * e^(-(t-t^{start}_i/tau)
        """

        cdef unsigned int i,j, K = t.shape[0]
        cdef np.ndarray[complex, ndim=1] h_tmp = np.zeros(K,dtype=complex)
        cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
        h_s  = np.zeros(K, dtype='double')
        h_vx = np.zeros(K, dtype='double')
        h_vy = np.zeros(K, dtype='double')
        h_p  = np.zeros(K, dtype='double')
        h_c  = np.zeros(K, dtype='double')

        for pol in self.N.keys():
            for i in range(self.N[pol]):
                h_tmp += damped_sinusoid(self.A[pol][i]  ,
                                         self.f[pol][i]  ,
                                         self.tau[pol][i],
                                         self.phi[pol][i],
                                         self.t0[pol][i] ,
                                         t)
            if(pol=='s'):
                h_s  +=  np.real(h_tmp)
            elif(pol=='v'):
                h_vx +=  np.real(h_tmp)
                h_vy += -np.imag(h_tmp)
            elif(pol=='t'):
                h_p  +=  np.real(h_tmp)
                h_c  += -np.imag(h_tmp)
            h_tmp = np.zeros(K, dtype='complex')

        return np.array([h_s, h_vx, h_vy, h_p, h_c])

cdef class Morlet_Gabor_wavelets:

    def __cinit__(self,
                  dict A,
                  dict f,
                  dict tau,
                  dict phi,
                  dict t0):

        self.A   = A
        self.f   = f
        self.tau = tau
        self.phi = phi
        self.t0  = t0
        self.N   = {}
        for key in self.A.keys():
            self.N[key] = len(self.A[key])

    cpdef np.ndarray[double, ndim=5] waveform(self,np.ndarray[double, ndim=1] t):

        """
            Returns five polarisations (the ones independent in a L-shaped GW detector) allowed for a metric theory of gravity: hs (scalar mode), {hvx, hvy} (vector modes), {hp, hc} (tensor modes).
            We employ the conventions: h_s           = sum_{i} A_i * cos(omega*t+phi)  * e^(-(t-t^{start}_i/tau)
                                       h_vx - i h_vy = sum_{i} A_i * e^(i*omega*t+phi) * e^(-(t-t^{start}_i/tau)
                                       h_+  - i h_x  = sum_{i} A_i * e^(i*omega*t+phi) * e^(-(t-t^{start}_i/tau)
        """

        cdef unsigned int i,j, K = t.shape[0]
        cdef np.ndarray[complex, ndim=1] h_tmp = np.zeros(K,dtype=complex)
        cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
        h_s  = np.zeros(K, dtype='double')
        h_vx = np.zeros(K, dtype='double')
        h_vy = np.zeros(K, dtype='double')
        h_p  = np.zeros(K, dtype='double')
        h_c  = np.zeros(K, dtype='double')

        for pol in self.N.keys():
            for i in range(self.N[pol]):
                h_tmp += morlet_gabor_wavelet(self.A[pol][i]  ,
                                              self.f[pol][i]  ,
                                              self.tau[pol][i],
                                              self.phi[pol][i],
                                              self.t0[pol][i] ,
                                              t)
            if(pol=='s'):
                h_s  +=  np.real(h_tmp)
            elif(pol=='v'):
                h_vx +=  np.real(h_tmp)
                h_vy += -np.imag(h_tmp)
            elif(pol=='t'):
                h_p  +=  np.real(h_tmp)
                h_c  += -np.imag(h_tmp)
            h_tmp = np.zeros(K, dtype='complex')

        return np.array([h_s, h_vx, h_vy, h_p, h_c])

cdef class SWSH:

  """
    Spin weighted spherical harmonics
    -s_Y_{lm}
    Defined in Kidder (https://arxiv.org/pdf/0710.0614.pdf) Eq.s (4, 5).
    Note that this function returns -s_Y_{l,m} as defined by Kidder.
    Thus, for gravitational perturbation s=2 must be passed.
  """

  def __init__(self, int s, int l, int m):

    self.s = s
    self.l = l
    self.m = m
    self.swsh_prefactor = (-1)**(self.s) \
                        * sqrt((2*self.l+1)/(4.0*np.pi)) \
                        * sqrt(fact(self.l+self.m)*fact(self.l-self.m)*fact(self.l+self.s)*fact(self.l-self.s))

  def __call__(self, double theta, double phi):
    return self.evaluate(theta, phi)
  
  cpdef complex evaluate(self, double theta, double phi):

    """
        SWSH for angles theta [0,pi] and phi [0,2pi]
    """

    cdef complex result = 0

    ki = max(0,self.m-self.s)
    kf = min(self.l+self.m,self.l-self.s)
    for k in range(ki,kf+1):
      result += (-1)**k * sin(theta/2)**(2*k+self.s-self.m) * cos(theta/2)**(2*self.l+self.m-self.s-2*k) \
              * 1/(fact(k)*fact(self.l+self.m-k)*fact(self.l-self.s-k)*fact(self.s-self.m+k))
    
    result *= np.exp(1j*self.m*phi)*self.swsh_prefactor

    return result

cdef class KerrBH:

  """
    | Multi mode ringdown model for a Kerr black hole using predictions of the frequencies and damping times as function of mass and spin, as predicted by perturbation theory.
    |
    | Input parameters:
    | t0    : Start time of the ringdown, currently common for all modes. #IMPROVEME: allow for a different start time for each mode.
    | Mf    : Final mass in solar masses.
    | af    : Dimensionless final spin.
    | amps  : Amplitudes of the modes.
    | r     : Distance in Mpc.
    | iota  : Inclination in radians.
    | phi   : Azimuthal angle in radians.
    |
    | Optional parameters:
    | TGR_params          : Additional non-GR parameters to be sampled.
    | reference_amplitude : Value with which to replace the Mf/r prefactor.
    | geom                : Flag to compute only the h_{l,m} modes, without spherical harmonics.
    | qnm_fit             : Flag to request the use of an interpolation for QNM complex frequency, instead of analytical fits (not available for n>2)
    | interpolants        : QNM complex frequencies interpolants.
    | Spheroidal          : Flag to activate the use of spheroidal harmonics instead of spherical. Relies on the pykerr package.
    | AreaQuantization    : Flag to use a prescription to impose QNM frequencies derived from the area quantisation proposal.
    | ParSpec             : Flag to use the ParSpec parametrisation of beyond-GR modifications to QNMs.
    | charge              : Flag to include the effect of charge.

  """

  def __cinit__(self,
                double       t0,
                double       Mf,
                double       af,
                dict         amps,
                double       r,
                double       iota,
                double       phi,
                dict         TGR_params,
                double       reference_amplitude = 0.0,
                unsigned int geom                = 0,
                unsigned int qnm_fit             = 1,
                dict         interpolants        = None,
                unsigned int Spheroidal          = 0,
                unsigned int amp_non_prec_sym    = 0,
                unsigned int AreaQuantization    = 0,
                unsigned int ParSpec             = 0,
                unsigned int charge              = 0):

    self.t0                  = t0
    self.Mf                  = Mf
    self.af                  = af
    self.amps                = amps
    self.r                   = r
    self.iota                = iota
    self.phi                 = phi
    self.TGR_params          = TGR_params
    self.reference_amplitude = reference_amplitude
    self.geom                = geom
    self.qnm_fit             = qnm_fit
    self.interpolants        = interpolants
    self.Spheroidal          = Spheroidal
    self.amp_non_prec_sym    = amp_non_prec_sym
    self.AreaQuantization    = AreaQuantization
    self.ParSpec             = ParSpec
    self.charge              = charge

    cdef int s,l,m,n
    self.qnms         = {}
    self.qnms_ParSpec = {}
    self.swshs        = {}

    for (s,l,m,n) in self.amps.keys():

        assert not(not(s==2) and (self.AreaQuantization or self.Spheroidal or self.qnm_fit)), "Extra polarisations (s={} was selected) are incompatible with using either a fit for QNM or the area quantization proposal or spheroidal harmonics.".format(s)
        if(self.AreaQuantization and l==2 and m==2 and n==0):
            qnm = QNM_220_area_quantized(l,m,n)
        else:
            if not(self.ParSpec):
                if(self.qnm_fit):
                    if(self.charge): raise ValueError('KN QNMs still do not support fits. Please set qnm-fit=0 inside the config file.')
                    else: qnm = QNM_fit(l,m,n)
                else:
                    assert not(self.interpolants==None), "You deselected qnm-fit without providing any interpolant."
                    qnm = QNM(s,l,m,n,self.interpolants)
            else:
                # For the parameters which are not being perturbed beyond GR, we want to retain the full spin expansion.
                qnm = QNM_fit(l,m,n)
                self.qnms_ParSpec[(s,l,m,n)] = QNM_ParSpec(l,m,n)
                
        self.qnms[(s,l,m,n)] = qnm

        if (self.Spheroidal):
            swsh_p = pykerr.spheroidal(self.iota, self.af, l,  m, n, phi=self.phi)
            swsh_m = np.conj(pykerr.spheroidal(np.pi-self.iota, self.af, l,  m, n, phi=self.phi))*(-1)**l
        else:
            swsh_p = SWSH(s,l, m)(self.iota, self.phi)
            swsh_m = SWSH(s,l,-m)(self.iota, self.phi)
        self.swshs[(s,l, m,n)] = swsh_p
        self.swshs[(s,l,-m,n)] = swsh_m

  cpdef np.ndarray[double, ndim=5] waveform(self, np.ndarray[double,ndim=1] times):

    """
        | We employ the conventions of arXiv:gr-qc/0512160 (Eq. 2.9):
        |                            h_s           = Re(sum_{lmn} S_{lmn} h_{lmn})
        |                            h_vx + i h_vy = sum_{lmn} S_{lmn} h_{lmn}
        |                            h_+  + i h_x  = sum_{lmn} S_{lmn} h_{lmn}
        | Non-precessing symmetry implies the property: h_{l,-m} = (-1)**l h^*_{l,m}
        | (see: Blanchet, “Gravitational Radiation from Post-Newtonian Sources and Inspiralling Compact Binaries”).
    """

    cdef int s,l,m,n
    cdef double prefactor
    cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
    cdef np.ndarray[complex,ndim=1] h_tmp
    h_s   = np.zeros(times.shape[0], dtype='double')
    h_vx  = np.zeros(times.shape[0], dtype='double')
    h_vy  = np.zeros(times.shape[0], dtype='double')
    h_p   = np.zeros(times.shape[0], dtype='double')
    h_c   = np.zeros(times.shape[0], dtype='double')
    h_tmp = np.zeros(times.shape[0], dtype='complex')

    for (s,l,m,n),a in self.amps.items():

        # This first block computes the complex frequency, with whatever modification the user has selected.
        # GR deviations in the spectrum for non-tensorial modes are not supported.
        if(s==2):
            try:    dfreq = self.TGR_params['domega_{}{}{}'.format(l,m,n)]
            except: dfreq = 0.0
            try:    dtau  = self.TGR_params['dtau_{}{}{}'.format(l,m,n)]
            except: dtau  = 0.0
        else:
            dfreq = 0.0
            dtau  = 0.0
        if(self.AreaQuantization and l==2 and m==2 and n==0 and s==2):
            try:    alpha = self.TGR_params['alpha']
            except: raise KeyError('If quantization of the horizon area is invoked, the alpha parameter must be passed.')
            freq = self.qnms[(s,l,m,n)].f_QA(self.Mf, self.af, alpha)
            try:    tau = self.TGR_params['tau_AQ']
            except: tau = self.qnms[(s,l,m,n)].tau_QA(self.Mf, self.af, alpha)
            corr_dfreq = 1.0
            corr_dtau  = 1.0
        elif(self.ParSpec):
            # In this case dfreq and dtau are arrays.
            gamma    = self.TGR_params['gamma']
            if not('domega_{}{}{}'.format(l,m,n) in self.TGR_params.keys()): freq = self.qnms[(s,l,m,n)].f(self.Mf, self.af)
            else:                                                            freq = self.qnms_ParSpec[(s,l,m,n)].f(self.Mf, self.af, gamma, dfreq)
            if not('dtau_{}{}{}'.format(l,m,n) in self.TGR_params.keys()):   tau  = self.qnms[(s,l,m,n)].tau(self.Mf, self.af)
            else:                                                            tau  = self.qnms_ParSpec[(s,l,m,n)].tau(self.Mf, self.af, gamma, dtau)
            corr_dfreq = 1.0
            corr_dtau  = 1.0
        elif(self.charge):
            Q          = self.TGR_params['Q']
            freq       = self.qnms[(s,l,m,n)].f_KN(self.Mf, self.af, Q)
            tau        = self.qnms[(s,l,m,n)].tau_KN(self.Mf, self.af, Q)
            corr_dfreq = 1.0+dfreq
            corr_dtau  = 1.0+dtau
        else:
            freq       = self.qnms[(s,l,m,n)].f(self.Mf, self.af)
            tau        = self.qnms[(s,l,m,n)].tau(self.Mf, self.af)
            corr_dfreq = 1.0+dfreq
            corr_dtau  = 1.0+dtau

        # This block computes the waveform.
        if(self.amp_non_prec_sym):
            if(self.geom):
                h_tmp = damped_sinusoid(1.0,  freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * a + \
                        damped_sinusoid(1.0, -freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * np.conj(a)*(-1)**l
            else:
                h_tmp = damped_sinusoid(1.0,  freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * self.swshs[(s,l, m,n)] * a + \
                        damped_sinusoid(1.0, -freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * self.swshs[(s,l,-m,n)] * np.conj(a)*(-1)**l
        else:
            (amp_1, amp_2) = a
            if(self.geom):
                h_tmp = damped_sinusoid(1.0,  freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * amp_1 + \
                        damped_sinusoid(1.0, -freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * amp_2
            else:
                h_tmp = damped_sinusoid(1.0,  freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * self.swshs[(s,l, m,n)] * amp_1 + \
                        damped_sinusoid(1.0, -freq*corr_dfreq, tau*corr_dtau, 0.0, self.t0, times) * self.swshs[(s,l,-m,n)] * amp_2

        if(s==0):
            h_s  += np.real(h_tmp)
        elif(s==1):
            h_vx += np.real(h_tmp)
            h_vy += np.imag(h_tmp)
        elif(s==2):
            h_p  += np.real(h_tmp)
            h_c  += np.imag(h_tmp)
        h_tmp = np.zeros(times.shape[0],dtype='complex')

    if(self.geom):                   prefactor = 1.0
    else:
        if self.reference_amplitude: prefactor = self.reference_amplitude
        else:                        prefactor = (self.Mf/self.r) * mass_dist_units_conversion

    return np.array([h_s*prefactor, h_vx*prefactor, h_vy*prefactor, h_p*prefactor, h_c*prefactor])

#NO-REVIEW-NEEDED
cdef class MMRDNS:

  """
    | Multi mode ringdown model from non-spinning progenitors.
    | Reference: https://arxiv.org/pdf/1404.3197.pdf
    |
    | Input parameters:
    | t0    : Start time of the ringdown.
    | Mf    : Final mass in solar masses.
    | af    : Dimensionless final spin.
    | eta   : Symmetric mass ratio of the progenitors.
    | r     : Distance in Mpc.
    | iota  : Inclination in radians.
    | phi   : Azimuthal angle in radians.
    |
    | Optional parameters:
    | TGR_params                   : Additional non-GR parameters to be sampled.
    | single_mode                  : Flag to request a single specific mode.
    | single_l, single_m, single_n : Indices of the specific mode to be selected. Requires single_mode = True in order to be read.
    | Spheroidal                   : Flag to activate the use of spheroidal harmonics instead of spherical. Relies on the pykerr package.
    | qnm_fit                      : Flag to request the use of an interpolation for QNM complex frequency, instead of analytical fits (not available for n>2)
    | interpolants                 : QNM complex frequencies interpolants.

  """

  def __cinit__(self,
                double       t0                  ,
                double       Mf                  ,
                double       af                  ,
                double       eta                 ,
                double       r                   ,
                double       iota                ,
                double       phi                 ,
                dict         TGR_params          ,
                int          single_l     = 2    ,
                int          single_m     = 2    ,
                int          single_n     = 0    ,
                unsigned int single_mode  = 0    ,
                unsigned int Spheroidal   = 0    ,
                dict         interpolants = None ,
                unsigned int qnm_fit      = 1    ):

    self.Mf           = Mf
    self.af           = af
    self.eta          = eta
    self.r            = r
    self.iota         = np.pi-iota #BAM convention
    self.phi          = phi
    self.t0           = t0
    self.TGR_params   = TGR_params
    self.single_l     = single_l
    self.single_m     = single_m
    self.single_n     = single_n
    self.single_mode  = single_mode
    self.Spheroidal   = Spheroidal
    self.interpolants = interpolants
    self.qnm_fit      = qnm_fit

    assert not(self.Mf <= 0), "MMRDNS: Mass cannot be negative or 0. No tachyons around here, not yet al least."
    assert not(np.abs(self.af) >= 1), "MMRDNS: |Spin| cannot be grater than 1. You shall not break causality, not on my watch."
    assert not(self.eta > 0.25 or self.eta <= 0), "MMRDNS: Eta cannot be smaller than 0 or greater than 0.25."
    assert not(self.r <= 0), "MMRDNS: Distance be negative or 0."

    if (self.qnm_fit):
        self.multipoles = [(2,2,0), (2,2,1), (2,1,0), (3,3,0), (3,3,1), (3,2,0), (4,4,0), (4,3,0)]
    else:
        self.multipoles = [(2,2,0), (2,2,1), (2,1,0), (3,3,0), (3,3,1), (3,2,0), (4,4,0), (4,3,0), (5,5,0)]


  cpdef np.ndarray[double, ndim=5] waveform(self, np.ndarray[double,ndim=1] times):

    """
        | We employ the convention h_+ - i h_x = sum_{lmn} S_{lmn} h_{lmn}
        | Non-precessing symmetry implies the property: h_{l,-m} = (-1)**l h^*_{l,m}
        | (see: Blanchet, “Gravitational Radiation from Post-Newtonian Sources and Inspiralling Compact Binaries”).
        | This model does not support extra scalar/vector polarisations, which are set to zero.
    """

    cdef np.ndarray[complex,ndim=1] result
    cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
    h_s    = np.zeros(times.shape[0], dtype='double')
    h_vx   = np.zeros(times.shape[0], dtype='double')
    h_vy   = np.zeros(times.shape[0], dtype='double')
    h_p    = np.zeros(times.shape[0], dtype='double')
    h_c    = np.zeros(times.shape[0], dtype='double')
    result = np.zeros(len(times), dtype=complex)

    # FIXME: The amplitude is too big by a factor of roughly 4, do we need to multiply by the unitless omega^2?
    # See Eq. 2 of https://arxiv.org/pdf/1404.3197.pdf

    Amp_cmplx = NR_amp.Amp_MMRDNS(self.eta)
    cdef dict swshs = {}
    if (self.single_mode):

        if(self.qnm_fit):
            qnm = QNM_fit(self.single_l,self.single_m,self.single_n)
        else:
            assert not(self.interpolants==None), "You deselected qnm-fit without providing any interpolant."
            qnm = QNM(2, self.single_l, self.single_m, self.single_n, self.interpolants)

        try:    dfreq = self.TGR_params['domega_{0}{1}{2}'.format(self.single_l, self.single_m, self.single_n)]
        except: dfreq = 0.0
        try:    dtau  = self.TGR_params['dtau_{0}{1}{2}'.format(self.single_l, self.single_m, self.single_n)]
        except: dtau  = 0.0
        freq = qnm.f(self.Mf, self.af)
        tau  = qnm.tau(self.Mf, self.af)

        if (self.Spheroidal): swsh = pykerr.spheroidal(self.iota, self.af, self.single_l,  self.single_m, self.single_n, phi=self.phi)
        else:                 swsh = SWSH(2,self.single_l,self.single_m)(self.iota, self.phi)
        swshs[(self.single_l,self.single_m,self.single_n)] = swsh

        result += swshs[(self.single_l, self.single_m,self.single_n)] * Amp_cmplx.amps[(self.single_l,self.single_m,self.single_n)] * damped_sinusoid(1.0,  freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times) + \
                  swshs[(self.single_l,-self.single_m,self.single_n)] * np.conj(Amp_cmplx.amps[(self.single_l,self.single_m,self.single_n)])*(-1)**self.single_l * damped_sinusoid(1.0, -freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times)
    else:
        for (l,m,n) in self.multipoles:

            if(self.qnm_fit):
                qnm = QNM_fit(l,m,n)
            else:
                assert not(self.interpolants==None), "You deselected qnm-fit without providing any interpolant."
                qnm = QNM(2,l,m,n,self.interpolants)

            try:    dfreq = self.TGR_params['domega_{0}{1}{2}'.format(l, m, n)]
            except: dfreq = 0.0
            try:    dtau  = self.TGR_params['dtau_{0}{1}{2}'.format(l, m, n)]
            except: dtau  = 0.0
            freq = qnm.f(self.Mf, self.af)
            tau  = qnm.tau(self.Mf, self.af)

            if (self.Spheroidal):
                swsh_p = pykerr.spheroidal(self.iota, self.af, l,  m, n, phi=self.phi)
                swsh_m = pykerr.spheroidal(self.iota, self.af, l, -m, n, phi=self.phi)
            else:
                swsh_p = SWSH(2,l, m)(self.iota, self.phi)
                swsh_m = SWSH(2,l,-m)(self.iota, self.phi)

            swshs[(l, m,n)] = swsh_p
            swshs[(l,-m,n)] = swsh_m

            result += swshs[(l, m,n)] * Amp_cmplx.amps[(l,m,n)]                  * damped_sinusoid(1.0,  freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times) + \
                      swshs[(l,-m,n)] * np.conj(Amp_cmplx.amps[(l,m,n)])*(-1)**l * damped_sinusoid(1.0, -freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times)

    # FIXME: Why this minus sign? NR comparison? TOBECHECKED, Lionel has e^(+i*omega*t) for m>0 (omega>0)
    result = -np.conj(result)
    result*=self.Mf * lal.MSUN_SI* lal.G_SI / (self.r * MPC_SI * lal.C_SI**2)
    #FIXME The prefactor should be the initial M_tot, not Mf, use NR fits to switch between the two of them.

    h_p +=  np.real(result)
    h_c += -np.imag(result)

    return np.array([h_s, h_vx, h_vy, h_p, h_c])

cdef class MMRDNP:

  """
    | Multi mode ringdown non-precessing model.
    | Reference: https://arxiv.org/pdf/1801.08208.pdf
    | Technical notes: https://github.com/llondon6/kerr_public/blob/master/notes/ns/mmrd.pdf
    | Mi is the initial total mass of the binary, m_i the single masses, chi_i the single spins.
    | The model was calibrated such that t=0 corresponds to 20M after |\dot{h}_22| peak.
    |
    | Input parameters:
    | t0    : Start time of the ringdown.
    | Mf    : Final mass in solar masses.
    | af    : Dimensionless final spin.
    | Mi    : Initial mass in solar masses.
    | eta   : Symmetric mass ratio of the progenitors.
    | chi_s : (m_1*chi_1 + m_2*chi_2)/M_tot
    | chi_a : (m_1*chi_1 - m_2*chi_2)/M_tot
    | r     : Distance in Mpc.
    | iota  : Inclination in radians.
    | phi   : Azimuthal angle in radians.
    |
    | Optional parameters:
    | TGR_params         : Additional non-GR parameters to be sampled.
    | single_mode        : Flag requesting a single specific mode.
    | single_l, single_m : Indices of the specific mode to be used. Requires single_mode=True in order to be used.
    | geom               : Flag to compute only the h_{l,m} modes, without spherical harmonics.


  """

  def __cinit__(self,
                double       t0,
                double       Mf,
                double       af,
                double       Mi,
                double       eta,
                double       chi_s,
                double       chi_a,
                double       r,
                double       iota,
                double       phi,
                dict         TGR_params,
                int          single_l     = 2,
                int          single_m     = 2,
                unsigned int single_mode  = 0,
                unsigned int geom         = 0,
                unsigned int qnm_fit      = 1,
                dict         interpolants = None):

    cdef int l, m, l_prime, m_prime, n
    self.Mf           = Mf
    self.af           = af
    self.r            = r
    self.iota         = np.pi-iota # This is related to BAM m conventions.
    self.phi          = phi
    self.Mi           = Mi
    self.eta          = eta
    self.chi_s        = chi_s
    self.chi_a        = chi_a
    self.delta        = np.sqrt(1-4*self.eta)
    self.t0           = t0
    self.TGR_params   = TGR_params
    self.single_l     = single_l
    self.single_m     = single_m
    self.single_mode  = single_mode
    self.geom         = geom
    self.qnm_fit      = qnm_fit
    self.interpolants = interpolants


    assert not(self.Mf <= 0), "MMRDNP: Mass cannot be negative or 0. No tachyons around here, not yet at least."
    assert not(np.abs(self.af) >= 1), "MMRDNP: |Spin| cannot be grater than 1. You shall not break CCC, not on my watch."
    assert not(self.eta > 0.25 or self.eta <= 0), "MMRDNP: Eta cannot be smaller than 0 or greater than 0.25."
    assert not(self.r <= 0), "MMRDNP: Distance cannot be negative or 0."
    #IMPROVEME: Implement similar checks for chi_s, chi_a.

    self.multipoles = {
                        (2,2): [(2,2,0)         ],
                        (2,1): [(2,1,0)         ],
                        (3,3): [(3,3,0)         ],
                        (3,2): [(2,2,0), (3,2,0)],
                        (4,4): [(4,4,0)         ],
                        (4,3): [(3,3,0), (4,3,0)]
                      }

  cpdef np.ndarray[double, ndim=5] waveform(self, np.ndarray[double,ndim=1] times):

    """
        We employ the convention: h_+  - i h_x  = sum_{lm} Y_{lm} h_{lm}
        Non-precessing symmetry implies the property: h_{l,-m} = (-1)**l h^*_{l,m}
        (see: Blanchet, “Gravitational Radiation from Post-Newtonian Sources and Inspiralling Compact Binaries”).
        This model does not support extra scalar/vector polarisations, which are set to zero.
    """

    cdef dict h_multipoles = {}

    Amp_cmplx = NR_amp.Amp_MMRDNP(self.eta, self.chi_s, self.chi_a, self.delta)

    for (l,m) in self.multipoles.keys():
        h_multipoles[(l,m)] = np.zeros(len(times), dtype=complex)
        for (l_prime, m_prime, n) in self.multipoles[(l,m)]:

            # The model includes counter-rotating (wrt to the original binary total angular momentum) modes, excited for negative final spins. For consistency with Berti NR data, invert the sign of the spin and call the negative-m mode.
            if(self.af < 0.0):
                m_prime = - m_prime
                self.af = -self.af
            if(self.qnm_fit):
                freq = QNM_fit(l_prime, m_prime, n).f(  self.Mf, self.af)
                tau  = QNM_fit(l_prime, m_prime, n).tau(self.Mf, self.af)
            else:
                assert not(self.interpolants==None), "You deselected qnm-fit without providing any interpolant."
                freq = QNM(2,l_prime, m_prime, n, self.interpolants).f(  self.Mf, self.af)
                tau  = QNM(2,l_prime, m_prime, n, self.interpolants).tau(self.Mf, self.af)
            try:    dfreq = self.TGR_params['domega_{0}{1}{2}'.format(l_prime, m_prime, n)]
            except: dfreq = 0.0
            try:    dtau  = self.TGR_params['dtau_{0}{1}{2}'.format(  l_prime, m_prime, n)]
            except: dtau  = 0.0

            if(self.geom):
                h_multipoles[(l,m)] += \
                    Amp_cmplx.amps[(l,m)][l_prime, np.abs(m_prime), n]                  * \
                    damped_sinusoid(1.0,  freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times) + \
                    np.conj(Amp_cmplx.amps[(l,m)][l_prime, np.abs(m_prime), n])*(-1)**l * \
                    damped_sinusoid(1.0, -freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times)
            else:
                h_multipoles[(l,m)] += \
                    SWSH(2, l, m)(self.iota,self.phi)  * Amp_cmplx.amps[(l,m)][l_prime, np.abs(m_prime), n]                  * \
                    damped_sinusoid(1.0,  freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times) + \
                    SWSH(2, l, -m)(self.iota,self.phi) * np.conj(Amp_cmplx.amps[(l,m)][l_prime, np.abs(m_prime), n])*(-1)**l * \
                    damped_sinusoid(1.0, -freq*(1.0+dfreq), tau*(1.0+dtau), 0, self.t0, times)

    cdef np.ndarray[complex,ndim=1] result
    cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
    h_s    = np.zeros(times.shape[0], dtype='double')
    h_vx   = np.zeros(times.shape[0], dtype='double')
    h_vy   = np.zeros(times.shape[0], dtype='double')
    h_p    = np.zeros(times.shape[0], dtype='double')
    h_c    = np.zeros(times.shape[0], dtype='double')
    result = np.zeros(len(times), dtype=complex)
    if (self.single_mode):
        result = h_multipoles[(self.single_l, self.single_m)]
    else:
        for (l,m) in self.multipoles.keys():
            result += h_multipoles[(l,m)]

    if not(self.geom):
        result*=self.Mi * lal.MSUN_SI* lal.G_SI / (self.r * MPC_SI * lal.C_SI**2)

    h_p +=  np.real(result)
    h_c += -np.imag(result)

    return np.array([h_s, h_vx, h_vy, h_p, h_c])

#NO-REVIEW-NEEDED
cdef class KHS_2012:

  """
    | Multi mode ringdown non-precessing model.
    | References: https://arxiv.org/abs/1207.0399, https://arxiv.org/abs/1406.3201
    | M_tot is the initial total mass of the binary, m_i the single mass, chi_i the single spin.
    | In this model t=0 corresponds to 20M after the merger.
    |
    | Input parameters:
    | t0      : start time of the ringdown
    | Mf      : final mass in solar masses
    | af      : dimensionless final spin
    | eta     : symmetric mass ratio of the progenitors
    | chi_eff : symmetric spin of the progenitors (defined as: 1/2*(sqrt(1-4*nu) chi1 + (m1*chi1 - m2*chi2)/(m1+m2)))
    | r       : distance in Mpc
    | iota    : inclination in radians
    | phi     : azimuthal angle in radians
    |
    | Optional parameters:
    | single_l, single_n : select a specific mode
    | single_mode        : flag to request only a specific mode
  """

  def __cinit__(self,
                double       t0,
                double       Mf,
                double       af,
                double       eta,
                double       chi_eff,
                double       r,
                double       iota,
                double       phi,
                dict         TGR_params,
                int          single_l    = 2,
                int          single_m    = 2,
                unsigned int single_mode = 0):

    cdef int l, m
    self.Mf          = Mf
    self.af          = af
    self.r           = r
    self.iota        = iota # FIXME check NR conventions, if BAM ones, need np.pi-iota
    self.phi         = phi
    self.eta         = eta
    self.chi_eff     = chi_eff
    self.t0          = t0
    self.TGR_params  = TGR_params
    self.single_l    = single_l
    self.single_m    = single_m
    self.single_mode = single_mode


    assert not(self.Mf <= 0), "KHS_2012: Mass cannot be negative or 0. No tachyons around here, not yet at least."
    assert not(np.abs(self.af) >= 1), "KHS_2012: |Spin| cannot be grater than 1. You shall not break CCC, not on my watch."
    assert not(self.eta > 0.25 or self.eta <= 0), "KHS_2012: Eta cannot be smaller than 0 or greater than 0.25."
    assert not(self.r <= 0), "KHS_2012: Distance be negative or 0."

    self.multipoles = [(2,2), (2,1), (3,3), (4,4)]


  cpdef np.ndarray[double, ndim=5] waveform(self, np.ndarray[double,ndim=1] times):

    """
    Returns h_+ - i* h_x
    """

    cdef dict h_multipoles = {}
    cdef complex Yplus, Ycross

    Amps = NR_amp.Amp_KHS(self.eta, self.chi_eff)

    for (l,m) in self.multipoles:
        h_multipoles[(l,m)] = np.zeros(len(times), dtype=complex)
        freq = QNM_fit(l,m,0).f(self.Mf, self.af)
        tau  = QNM_fit(l,m,0).tau(self.Mf, self.af)
        try:
            dfreq = self.TGR_params['domega_{0}{1}{2}'.format(l,m,0)]
        except:
            dfreq = 0.0
        try:
            dtau = self.TGR_params['dtau_{0}{1}{2}'.format(l,m,0)]
        except:
            dtau = 0.0

        Yplus  = SWSH(2, l, m)(self.iota, 0.0) + (-1)**l * SWSH(2, l, -m)(self.iota, 0.0)
        Ycross = SWSH(2, l, m)(self.iota, 0.0) - (-1)**l * SWSH(2, l, -m)(self.iota, 0.0)
        A      = Amps.amps[(l,m)]

        h_multipoles[(l,m)] += \
            Yplus  * np.real(damped_sinusoid(A, freq*(1.0+dfreq), tau*(1.0+dtau), -m*self.phi, self.t0, times))                + \
            Ycross * np.imag(damped_sinusoid(A, freq*(1.0+dfreq), tau*(1.0+dtau), -m*self.phi, self.t0, times)) * 1j

    cdef np.ndarray[complex,ndim=1] result
    result = np.zeros(len(times), dtype=complex)
    cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
    h_s    = np.zeros(times.shape[0], dtype='double')
    h_vx   = np.zeros(times.shape[0], dtype='double')
    h_vy   = np.zeros(times.shape[0], dtype='double')
    h_p    = np.zeros(times.shape[0], dtype='double')
    h_c    = np.zeros(times.shape[0], dtype='double')

    if (self.single_mode):
        result = h_multipoles[(self.single_l, self.single_m)]
    else:
        for (l,m) in self.multipoles:
            result += h_multipoles[(l,m)]
    result*=self.Mf * lal.MSUN_SI* lal.G_SI / (self.r * MPC_SI * lal.C_SI**2)

    #FIXME: check signs conventions
    h_p +=  np.real(result)
    h_c += -np.imag(result)

    return np.array([h_s, h_vx, h_vy, h_p, h_c])

#NO-REVIEW-NEEDED
cdef class TEOBPM:

    """
    | Post-merger EOB model
    | References: arxiv.1406.0401, arXiv:1606.03952, arXiv:2001.09082.
    | C implementation available here: https://bitbucket.org/eob_ihes/teobresums/src/master/C/src/
    |
    | Input parameters:
    | t0     : start time of the waveform (s)
    | m1     : heavier BH mass (solar masses)
    | m2     : lighter BH mass (solar masses)
    | chi1   : heavier BH spin (adimensional)
    | chi2   : lighter BH spin (adimensional)
    | phases : phases of modes at peak (rad)
    | r      : distance (Mpc)
    | iota   : inclination (rad)
    | phi    : azimuthal angle (rad)
    |
    | Optional parameters:
    | TGR_params         : Additional non-GR parameters to be sampled.
    | single_l, single_m : select a specific mode
    | single_mode        : flag to request only a specific mode
    | geom               : Flag to compute only the h_{l,m} modes, without spherical harmonics.

    """

    def __cinit__(self,
                 double       t0,
                 double       m1,
                 double       m2,
                 double       chi1,
                 double       chi2,
                 dict         phases,
                 double       r,
                 double       iota,
                 double       phi,
                 dict         TGR_params,
                 unsigned int single_l    = 2,
                 int          single_m    = 2,
                 unsigned int single_mode = 0,
                 unsigned int geom        = 0):

        cdef double tmp

        self.t0          = t0
        self.m1          = m1
        self.m2          = m2
        self.s1z         = chi1
        self.s2z         = chi2
        self.phases      = phases
        self.M           = m1+m2
        self.r           = r
        self.iota        = iota
        self.phi         = phi
        self.TGR_params  = TGR_params
        self.single_l    = single_l
        self.single_m    = single_m
        self.single_mode = single_mode
        self.geom        = geom

        if not(single_mode and (single_l==2) and (single_m==2)):
            raise ValueError("Only l=m=2 mode is currently supported. HMs need to be checked against the C code and the relative start times of the modes are broken.")

        if (self.m1 < self.m2):
            # Impose that the conventions of TEOBResumSPM are respected, first BH is the heaviest.
            tmp      = self.m1
            self.m1  = self.m2
            self.m2  = tmp
            tmp      = self.s1z
            self.s1z = self.s2z
            self.s2z = tmp

        self.nu   = eu._sym_mass_ratio(self.m1,self.m2)
        self.X12  = eu._X_12(self.m1,self.m2)
        self.Shat = eu._S_hat(self.m1, self.m2, self.s1z, self.s2z)
        self.a12  = eu._a_12(self.m1, self.m2, self.s1z, self.s2z)
        self.Sbar = eu._S_bar(self.m1, self.m2, self.s1z, self.s2z)
        self.aK   = eu._a_K(self.m1, self.m2, self.s1z, self.s2z)
        self.Mf   = eu._JimenezFortezaRemnantMass(self.m1, self.m2, self.s1z, self.s2z)
        self.af   = eu._JimenezFortezaRemnantSpin(self.nu, self.s1z, self.s2z)
        
        # Sanity checks
        assert not(self.single_mode and (np.abs(self.single_m) > self.single_l)), "m cannot be greater than l in modulus."
        assert not(self.r <= 0), "TEOBPM: Distance cannot be negative or 0."
        assert not((self.m1 <= 0) or (self.m2 <= 0)), "TEOBPM: Masses cannot be negative."
        assert not((np.abs(self.s1z) > 1) or (np.abs(self.s2z) > 1)), "TEOBPM: Please do not invoke a naked singularity."

        if(self.single_mode):
            self.multipoles = [(self.single_l,self.single_m)]
        else:
            # These are the multipoles we can trust for sure (also sprache Rossella)
            self.multipoles = [(2,2), (3,3), (4,4), (5,5)]
            # These are the multipoles that are present, but must be tested with care, especially for negative high spins
            #self.multipoles = [(2,2), (2,1), (3,3), (3,2), (3,1), (4,4), (4,3), (4,2), (4,1), (5,5)]

        self.fit_coefficients = {}
        for (l,m) in self.multipoles:
            self.fit_coefficients[(l,m)] = self._EOBPM_SetupFitCoefficients(l, m)

    ###########################
    # Core waveform functions #
    ###########################

    def EOBPM_SetupFitCoefficients(self, int l, int m):
        return self._EOBPM_SetupFitCoefficients(l, m)

    cdef dict _EOBPM_SetupFitCoefficients(self, int l, int m):

        cdef double omg1   = eu._omega1(self.af,  l, m)
        cdef double alph1  = eu._alpha1(self.af,  l, m)
        cdef double alph21 = eu._alpha21(self.af, l, m)

        try:
            dfreq1 = self.TGR_params['domega_220']
            omg1   = omg1*(1.0+dfreq1)
        except: pass
        try:
            dtau1  = self.TGR_params['dtau_220']
            alph1  = alph1*(1.0/(1.0+dtau1))
        except: pass

        #FIXME: Needs to be tested, namely to check the sign conventions.
        if(0):
            try:
                dtau2  = self.TGR_params['dtau_221']
                alph2  = alph21+alph1
                alph2  = alph2*(1.0/(1.0+dtau2))
                alph21 = alph2-alph1
            except: pass

        cdef double omg_peak   = eu._omega_peak(    self.nu, self.X12, self.Shat,                      self.aK,           l, m)
        cdef double A_peak     = eu._amplitude_peak(self.nu, self.X12, self.Shat, self.a12, self.Sbar, self.aK, omg_peak, l, m)
        cdef double Domg       = eu._dOmega(omg1, self.Mf/self.M, omg_peak)

        cdef double c1A,c2A,c3A,c4A
        cdef double c1p,c2p,c3p,c4p

        c2A = 0.5*alph21
        c3A = eu._c3_A(self.nu, self.X12, self.Shat, self.a12, l, m)
        cdef double coshc3A = cosh(c3A)
        c1A = A_peak*alph1*(coshc3A*coshc3A)/c2A
        c4A = A_peak-c1A*tanh(c3A)

        c2p = alph21
        c3p = eu._c3_phi(self.nu, self.X12, self.Shat, l, m)
        c4p = eu._c4_phi(self.nu, self.X12, self.Shat, l, m)
        c1p = Domg*(1.0+c3p+c4p)/(c2p*(c3p+2.0*c4p))

        cdef dict single_mode_fit_coefficients = {}

        single_mode_fit_coefficients['a1']     = c1A
        single_mode_fit_coefficients['a2']     = c2A
        single_mode_fit_coefficients['a3']     = c3A
        single_mode_fit_coefficients['a4']     = c4A
        single_mode_fit_coefficients['p1']     = c1p
        single_mode_fit_coefficients['p2']     = c2p
        single_mode_fit_coefficients['p3']     = c3p
        single_mode_fit_coefficients['p4']     = c4p
        single_mode_fit_coefficients['omega1'] = omg1
        single_mode_fit_coefficients['alpha1'] = alph1

        return single_mode_fit_coefficients

    def TEOBPM_Amplitude(self, double tau, double sigma_real, double a1, double a2, double a3, double a4):
        return self._TEOBPM_Amplitude(tau, sigma_real, a1, a2, a3, a4)

    cdef inline double _TEOBPM_Amplitude(self, double tau, double sigma_real, double a1, double a2, double a3, double a4):
        return (a1*tanh(a2*tau +a3) + a4)*exp(-sigma_real*tau)

    def TEOBPM_Phase(self, double tau, double sigma_imag, double phi_fundamental, double p1, double p2, double p3, double p4):
        return self._TEOBPM_Phase(tau, sigma_imag, phi_fundamental, p1, p2, p3, p4)

    cdef inline double _TEOBPM_Phase(self, double tau, double sigma_imag, double phi_fundamental, double p1, double p2, double p3, double p4):
        return -p1*log((1.0+p3*exp(-p2*tau) + p4*exp(-2.0*p2*tau))/(1.0+p3+p4))-phi_fundamental-sigma_imag*tau
    
    def TEOBPM_single_multipole(self,
        np.ndarray[double,ndim=1] time,  # time array on which to compute the waveform (s)
        double tlm,                      # starting time of the lm mode (s)
        double philm,                    # phase at the peak of the lm mode (rad)
        int l,                           # orbital index
        int m,                           # magnetic index
        int N                            # number of points in the time array
        ):
        return self._TEOBPM_single_multipole(time, tlm, philm, l, m, N)
    
    cdef np.ndarray[complex,ndim=1] _TEOBPM_single_multipole(self, double[::1] time, double tlm, double philm, int l, int m, int N):

        cdef double                     tau
        cdef int                        i      = 0
        cdef np.ndarray[complex,ndim=1] h      = np.zeros(N, dtype=complex)
        cdef complex[::1]               h_view = h
        cdef double                     A      = 0
        cdef double                     phase  = 0

        cdef dict fc           = self.fit_coefficients[(l, m)]
        cdef double a1         = fc['a1']
        cdef double a2         = fc['a2']
        cdef double a3         = fc['a3']
        cdef double a4         = fc['a4']
        cdef double p1         = fc['p1']
        cdef double p2         = fc['p2']
        cdef double p3         = fc['p3']
        cdef double p4         = fc['p4']
        cdef double sigma_real = fc['alpha1']
        cdef double sigma_imag = fc['omega1']
        cdef double tM         = (self.Mf*MTSUN_SI)

        for i in range(N):
            tau  = (time[i]-tlm)/tM
            if (time[i] >= tlm):
                A          = self._TEOBPM_Amplitude(tau, sigma_real,        a1, a2, a3, a4)
                phase      = self._TEOBPM_Phase(    tau, sigma_imag, philm, p1, p2, p3, p4)
                h_view[i]  = self.nu*A*(cos(phase)+1j*sin(phase))
            else:
                h_view[i] = 0.0+1j*0.0
        return h

    def waveform(self, np.ndarray[double, ndim=1, mode="c"] times):
        return self._waveform(times)

    cdef np.ndarray[double, ndim=5] _waveform(self, double[::1] times):

        # Returns h_+ - i* h_x

        #Non-precessing symmetry implies the property
        #(see L. Blanchet, “Gravitational Radiation from Post-Newtonian Sources and Inspiralling Compact Binaries,”):
        # h_{l,-m} = (-1)**l h^*_{l,m}
        # FIXME: BAM wfs have a different convention with respect to SXS wfs, namely m_BAM = -m_SXS.
        # Plot the template on top of an SXS wf to verify this and if needed cure it simply by incl --> pi - incl.
        
        cdef int l,m
        cdef int N                       = times.shape[0]
        cdef double multipole_start_time = 0.0

        cdef np.ndarray[complex,ndim=1] multipole_pm = np.zeros(N, dtype=complex)
        cdef np.ndarray[complex,ndim=1] multipole_mm = np.zeros(N, dtype=complex)
        cdef np.ndarray[complex,ndim=1] result
        cdef np.ndarray[double,ndim=1] h_s, h_vx, h_vy, h_p, h_c
        h_s    = np.zeros(N, dtype='double')
        h_vx   = np.zeros(N, dtype='double')
        h_vy   = np.zeros(N, dtype='double')
        h_p    = np.zeros(N, dtype='double')
        h_c    = np.zeros(N, dtype='double')
        result = np.zeros(N, dtype=complex)

        for (l,m) in self.multipoles:

            multipole_start_time = self.t0 + eu._DeltaT(self.m1, self.m2, self.s1z, self.s2z, l, m)
            multipole_pm = self._TEOBPM_single_multipole(times, multipole_start_time, self.phases[(l,m)], l, m, N)
            multipole_mm = (-1)**(l)*np.conj(multipole_pm)

            if not(self.geom):
                result += SWSH(2, l,  m)(self.iota,self.phi) * multipole_pm + \
                          SWSH(2, l, -m)(self.iota,self.phi) * multipole_mm
            else:
                result += multipole_pm
        
        cdef double prefactor = mass_dist_units_conversion*self.M/self.r

        if not(self.geom):
            result *= prefactor

        h_p += np.real(result)
        h_c += np.imag(result)

        return np.array([h_s, h_vx, h_vy, h_p, h_c])

    ##################################################################
    # Utils Section 1: Useful combinations of progenitors parameters #
    ##################################################################
    
    def sym_mass_ratio(self):
        return eu._sym_mass_ratio(self.m1, self.m2)

    def X_12(self):
        return eu._X_12(self.m1, self.m2)

    def S_hat(self):
        return eu._S_hat(self.m1, self.m2, self.s1z, self.s2z)

    def S_bar(self):
        return eu._S_bar(self.m1, self.m2, self.s1z, self.s2z)

    def a_12(self):
        return eu._a_12(self.m1, self.m2, self.s1z, self.s2z)

    def a_K(self):
        return eu._a_K(self.m1, self.m2, self.s1z, self.s2z)

    #############################################################
    # Utils Section 2: Ringdown frequency and damping time fits #
    #############################################################

    def alpha1(self, int l, int m):
        return eu._alpha1(self.af, l, m)

    def alpha21(self, int l, int m):
        return eu._alpha21(self.af, l, m)
    
    def omega1(self, int l, int m):
        return eu._omega1(self.af, l, m)

    #############################################################
    # Utils Section 3: Amplitude and phase fitting coefficients #
    #############################################################

    def c3_A(self, int l, int m):
        return eu._c3_A(self.nu, self.X12, self.Shat, self.a12, l, m)
    
    def c3_phi(self, int l, int m):
        return eu._c3_phi(self.nu, self.X12, self.Shat, l, m)
    
    def c4_phi(self, int l, int m):
        return eu._c4_phi(self.nu, self.X12, self.Shat, l, m)

    #############################################
    # Utils Section 4: Fits for peak quantities #
    #############################################
    
    def dOmega(self, double omega1, double omega_peak):
        return eu._dOmega(omega1, self.Mf, omega_peak)
    
    def amplitude_peak(self, double omega_peak, int l, int m):
        return eu._amplitude_peak(self.nu, self.X12, self.Shat, self.a12, self.S_bar, self.aK, omega_peak, l, m)
    
    def omega_peak(self, int l, int m):
        return eu._omega_peak(self.nu, self.X12, self.Shat, self.aK, l, m)

    ###################################################
    # Utils Section 5: Fits for remnant mass and spin #
    ###################################################

    def JimenezFortezaRemnantMass(self):
        return eu._JimenezFortezaRemnantMass(self.m1, self.m2, self.s1z, self.s2z)
    
    def JimenezFortezaRemnantSpin(self):
        return eu._JimenezFortezaRemnantSpin(self.nu, self.s1z, self.s2z)


# From this point on, it's work in progress.
"""
    read https://cython.readthedocs.io/en/latest/src/userguide/extension_types.html#instantiation-from-existing-c-c-pointers
    ctypedef struct lal_series:
        lal.REAL8TimeSeries hp
        lal.REAL8TimeSeries hp
"""



#NO-REVIEW-NEEDED
cdef class IMR_WF:

  """
    Call an IMR waveform from LAL
  """

  def __cinit__(self, double m1, double m2, double s1z, double s2z, double dist, double cosiota, double phi, double t0, double dt, double starttime, double signal_seglen):

    self.m1            = m1
    self.m2            = m2
    self.s1z           = s1z
    self.s2z           = s2z
    self.dist          = dist
    self.cosiota       = cosiota
    self.phi           = phi
    self.dt            = dt
    self.starttime     = starttime
    self.signal_seglen = signal_seglen
    self.t0            = t0

  cpdef np.ndarray[double, ndim=5] waveform(self, np.ndarray[double,ndim=1] times):

    cdef int result
    result=0
    """
        cdef np.ndarray[complex,ndim=1] result, hp, hc
        Need to learn how to call a lal.REAL8TimeSeries in cython
        hp, hc = lalsim.SimInspiralChooseTDWaveform(
             self.m1*lalsim.lal.MSUN_SI,
             self.m2*lalsim.lal.MSUN_SI,
             0.0, 0.0, self.s1z,
             0.0, 0.0, self.s2z,
             self.dist*1e6*lalsim.lal.PC_SI,
             np.arccos(self.cosiota),
             self.phi,
             0, #longAscNodes
             0, #eccentricity
             0, #meanPerAno
             self.dt,
             15.,
             100., #fref
             None, #lalpars
             lalsim.SEOBNRv3
             )
        #hp, hc = resize_time_series(np.column_stack((hp.data.data, hc.data.data)),
                                      self.signal_seglen, self.dt, self.starttime, self.t0)

        result = hp.data.data-1j*hc.data.data
    """

    return result
