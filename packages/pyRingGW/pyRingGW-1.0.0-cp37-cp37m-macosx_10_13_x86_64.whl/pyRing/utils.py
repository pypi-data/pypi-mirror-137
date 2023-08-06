#Standard python imports
from __future__ import division
from optparse import OptionParser
from scipy.interpolate import interp1d, LinearNDInterpolator
from scipy.linalg import cholesky
from scipy.signal import butter, filtfilt, tukey
import numpy as np, pkg_resources, os, traceback, warnings

#LVC imports
import lal

#Package internal imports
try:
    import surfinBH
except:
    warnings.warn("Import of surfinBH failed with error {}.".format(traceback.print_exc()))



def set_prefix(warning_message=True):
    
    """
        Set pyRing
    """
    
    # Check environment
    try:
        prefix = os.path.join(os.environ['PYRING_PREFIX'], 'pyRing')
    except KeyError:
        prefix = ''
        if(warning_message):
            warnings.warn("The requested functionality requires data not included in the package. Please set a $PYRING_PREFIX variable which contains the path to such data. This can be done by setting 'export PYRING_PREFIX= yourpath' in your ~/.bashrc file. Typically, PYRING_PREFIX contains the path to the clone of the repository containing the source code.")
    return prefix


def import_datafile_path(filename):

    package_path = pkg_resources.resource_filename(__name__, filename)

    return package_path


def check_NR_dir():
    
    PYRING_PREFIX = set_prefix()
    if not(os.path.isdir(os.path.join(PYRING_PREFIX, 'data/NR_data/lvcnr-lfs'))):
        raise Exception("pyRing supports NR injections using the LVC-NR injection infrastructure. If you wish to inject NR simulations, please clone the LVC-NR injection infrastructure repository, located here: https://git.ligo.org/waveforms/lvcnr-lfs \nFor tutorials and info on how to use the LVC NR injection infrastructure see:\n - https://git.ligo.org/sebastian-khan/waveform-f2f-berlin/blob/master/notebooks/2017WaveformsF2FTutorial_NRDemo.ipynb \n - https://www.lsc-group.phys.uwm.edu/ligovirgo/cbcnote/Waveforms/NR/InjectionInfrastructure \n - https://arxiv.org/pdf/1703.01076.pdf")
    return


def m1_from_m_q(m, q): return m*q/(1+q)
def m2_from_m_q(m, q): return m/(1+q)

def review_warning():
    warnings.warn("\nYou are using a code block which is not reviewed. Non-reviewed code cannot be used for producing LVC results.")

def qnm_interpolate(s,l,m,n):
    print('\nPerforming interpolation of ringdown complex frequencies of {}{}{}{} mode.'.format(s,l,m,n))
    assert not(np.abs(m) > l), "QNM interpolation: m cannot be greater than l in modulus."
    assert (s==0 or s==1 or s==2), "QNM interpolation: supported s values are [0,1,2] ({} was passed)."
    try:
        PYRING_PREFIX = set_prefix()
        # Adapt to Berti conventions (start counting from 1): n -> n+1
        if (m<0):
            af, w_r, w_i, _, _ = np.loadtxt(os.path.join(PYRING_PREFIX,'data/NR_data/Kerr_BH/s{}l{}'.format(s, l),'n{}l{}mm{}.dat'.format(n+1, l, np.abs(m))), unpack=True)
        else:
            af, w_r, w_i, _, _ = np.loadtxt(os.path.join(PYRING_PREFIX,'data/NR_data/Kerr_BH/s{}l{}'.format(s, l),'n{}l{}m{}.dat'.format(n+1, l, m)), unpack=True)
    except:
        raise Exception("If you wish to use perturbation theory NR data not stored on the repository, please download the corresponding files from https://pages.jh.edu/~eberti2/ringdown\nQNM interpolation failed with error: {}.".format(traceback.print_exc()))
    return interp1d(af, w_r, kind='cubic'), interp1d(af, w_i, kind='cubic')

def qnm_interpolate_KN(s,l,m,n):
    print('\nPerforming interpolation of ringdown Kerr Newman complex frequencies of {}{}{}{} mode.'.format(s,l,m,n))
    assert not(np.abs(m) > l), "QNM interpolation: m cannot be greater than l in modulus."
    assert (s==0 or s==1 or s==2), "QNM interpolation: supported s values are [0,1,2] ({} was passed)."
    try:
        PYRING_PREFIX = set_prefix()
        if (m<0):
            Q, af, w_r, w_i = np.loadtxt(os.path.join(PYRING_PREFIX,'data/NR_data/KN_BH/s{}l{}'.format(s, l),'n{}l{}mm{}.dat'.format(n, l, np.abs(m))), unpack=True)
        else:
            Q, af, w_r, w_i = np.loadtxt(os.path.join(PYRING_PREFIX,'data/NR_data/KN_BH/s{}l{}'.format(s, l),'n{}l{}m{}.dat'.format(n, l, m)), unpack=True)
    except:
        raise Exception("Loading KN data failed. Exiting.".format(traceback.print_exc()))

    coords = np.column_stack((af,Q))
    interp_r = LinearNDInterpolator(coords, w_r)
    interp_i = LinearNDInterpolator(coords, w_i)

    return interp_r, interp_i

def whiten(strain, interp_psd, dt, f_min, f_max, mf, alpha_window=0.1):

    #########################################################################
    # Function to whiten the data. Transform to freq domain, divide by asd, #
    # then transform back, taking care to get normalization right.          #
    #########################################################################

    Nt       = len(strain)
    freqs    = np.fft.rfftfreq(Nt, dt)
    srate_dt = 1./dt
    
    # This cleaning is required because when we inject a given PSD, the extrapolation sets it to 0 in the region outside the interpolation range. Such a 0 would cause the whitening to crash.
    psd_cleaned = interp_psd(freqs)
    for i in range(0, len(psd_cleaned)):
        if((freqs[i]<f_min) or (freqs[i]>f_max)):
            psd_cleaned[i] = np.inf

    if not(mf==0.0):
        # Typical ringdown frequency (220 mode) for a BH with af=0.7 (Berti+ fit), only for plotting purposes.
        central_f_ringdown = ((lal.C_SI*lal.C_SI*lal.C_SI)/(2.*np.pi*lal.G_SI*mf*lal.MSUN_SI)) * (1.5251-1.1568*(1-0.7)**0.1292)

        window = tukey(Nt, alpha=alpha_window)
        strain = strain*window
        bb, ab = butter(4, [f_min/(0.5*srate_dt), (central_f_ringdown*2.)/(0.5*srate_dt)], btype='band')
        strain = filtfilt(bb, ab, strain)

    hf       = np.fft.rfft(strain)
    white_hf = hf / (np.sqrt(psd_cleaned/dt/2.))
    white_ht = np.fft.irfft(white_hf, n=Nt)

    return white_ht

def compute_SNR_TD(h1, h2, InvCov):

    #FIXME: Normalization factors are missing.
    SNR = 4.*np.dot(h1,np.dot(InvCov,h2))

    return SNR

def inner_product_FD(h1, h2, psd, df):
    return 4.0*df*np.sum(np.conj(h1)*h2/psd).real

def compute_SNR_FD(data, template, psd, df):

    SNR = inner_product_FD(data, template, psd, df)/np.sqrt(inner_product_FD(template, template, psd, df))

    return SNR

def final_state_surfinBH(Mtot, q, chi1, chi2, f_ref):

    fit = surfinBH.LoadFits('NRSur7dq4Remnant')
    #Adapt q to surrogate conventions.
    if(q < 1.): q = 1./q
    #This is the orbital frequency (hence the missing factor of 2, since f_ref is the GW frequency) in units of rad/M (seehttps://github.com/vijayvarma392/surfinBH/blob/master/examples/example_7dq4.ipynb for more info).
    omega_ref = np.pi*f_ref/Mtot

    Mf_sBH, _ = fit.mf(q, chi1, chi2, omega0=omega_ref)
    af_sBH, _ = fit.chif(q, chi1, chi2, omega0=omega_ref)
    Mf        = Mtot*Mf_sBH
    af        = np.sqrt(af_sBH[0]**2+af_sBH[1]**2+af_sBH[2]**2)

    return Mf, af

def railing_check(samples, prior_bins, tolerance):
    hist, bin_edges = np.histogram(samples, bins=prior_bins, density=True)

    highest_hist = np.amax(hist)
    lower_support = hist[0] / highest_hist * 100
    higher_support = hist[-1] / highest_hist * 100

    low_end_railing = lower_support > tolerance
    high_end_railing = higher_support > tolerance

    return low_end_railing, high_end_railing

##########################################
# From here downwards, NO REVIEW NEEDED. #
##########################################

def EsGB_corrections(name):
    
    if(name=='domega_220'):
        a0_GR =  0.373672
        a1_GR =  0.2438
        a2_GR = -1.2722
        a0_GB = -0.1874
        a1_GB = -0.6552
        a2_GB = -0.6385
        corr  = [a0_GB/a0_GR, (a0_GB*a1_GB)/a1_GR, (a0_GB*a2_GB)/a2_GR]
    elif(name=='dtau_220'):
        b0_GR =  11.240715
        b1_GR =  2.3569
        b2_GR = -5.0014
        b0_GB = 1.0/(-0.0622)
        b1_GB = 0.0
        b2_GB = 0.0
        corr  = [b0_GB/b0_GR, (b0_GB*b1_GB)/b1_GR, (b0_GB*b2_GB)/b2_GR]
        raise ValueError("Tau corrections to be filled yet.")
    else:
        raise ValueError("Currently EdsGB corrections only support the (l,m,n)=(2,2,0) mode deviation.")
    return corr

def mtot(m1,m2):         return m1+m2
def mc(m1,m2):           return (m1*m2)**(3./5.)/(m1+m2)**(1./5.)
def q(m1,m2):            return [(np.minimum(m1,m2))/(np.maximum(m1,m2)), (np.maximum(m1,m2))/(np.minimum(m1,m2))]  #Return both of the q conventions
def eta(m1,m2):          return (m1*m2)/(m1+m2)**2   #eta=q/(1+q)**2
def m1_from_mc_q(mc, q): return mc*((1+q)**(1./5.))*q**(-3./5.)
def m2_from_mc_q(mc, q): return mc*((1+q)**(1./5.))*q**(2./5.)
def chi_eff(q, a1, a2):                       #eta=0.25 -> chi_1=chi_2=0.5 -> chi_eff=aritmetic mean of (a1,a2)

    eta = q/(1+q)**2
    chi_1 = 0.5*(1.0+np.sqrt(1.0-4.0*eta))
    chi_2 = 1.0-chi_1

    return chi_1*a1 + chi_2*a2

def cholesky_logdet_C(covariance):
    R = cholesky(covariance)
    return 2.*np.sum([np.log(R[i,i]) for i in range(R.shape[0])])

def resize_time_series(inarr, N, dt, starttime, desiredtc):

    """
    Zero pad inarr and align its peak to the desired tc in the segment.
    """
    
    review_warning()

    waveLength = inarr.shape[0]

    # Find the sample at which we wish tc to be.
    tcSample = int(np.floor((desiredtc-starttime)/dt))
    # ... and the actual tc.
    injTc = starttime + tcSample*dt

    # find the sample in waveform space at which tc happens, using the square amplitude as reference
    waveTcSample = np.argmax(inarr[:,0]**2+inarr[:,1]**2)

    wavePostTc = waveLength - waveTcSample

    if tcSample >= waveTcSample:
        bufstartindex =  tcSample - waveTcSample
    else:
        bufstartindex = 0
    if (wavePostTc + tcSample <= N):
        bufendindex = wavePostTc + tcSample
    else:
        bufendindex = N

    bufWaveLength = bufendindex - bufstartindex;
    if (tcSample >= waveTcSample):
        waveStartIndex = 0
    else:
        waveStartIndex = waveTcSample - tcSample

    # Allocate the arrays of zeros which work as a buffer.
    hp = np.zeros(N,dtype = np.float64)
    hc = np.zeros(N,dtype = np.float64)

    # Copy the waveform over.
    waveEndIndex = waveStartIndex + bufWaveLength

    hp[bufstartindex:bufstartindex+bufWaveLength] = inarr[waveStartIndex:waveEndIndex,0]
    hc[bufstartindex:bufstartindex+bufWaveLength] = inarr[waveStartIndex:waveEndIndex,1]

    return hp,hc

class UNUSED_NR_waveform(object):

    # ===============================================================================================#
    # NR injection setup adapted from the inject_NR.py script used in IMR consistency test studies.  #
    # Credits to: Abhirup Ghosh, Archisman Ghosh, Ashok Choudhary, KaWa Tsang, Laura Van Der Schaaf, #
    # Nathan K Johnson-McDaniel, Peter Pang.                                                         #
    # ===============================================================================================#

    def __init__(self, **kwargs):
        review_warning()
        self.incl_inj  = kwargs['injection-parameters']['incl']
        self.phi_inj   = kwargs['injection-parameters']['phi']
        self.SXS_ID    = kwargs['injection-parameters']['SXS-ID']
        PYRING_PREFIX = set_prefix()
        self.data_file = os.path.join(PYRING_PREFIX, 'data/NR_data/SXS_data/BBH0{0}/rhOverM_Asymptotic_GeometricUnits_CoM.h5'.format(self.SXS_ID))
        self.N         = kwargs['injection-parameters']['N']
        # Load the data
        sys.stdout.write('\n\n----NR injection section----')
        sys.stdout.write('\nLoading SXS NR data from %s\n'%(os.path.realpath(self.data_file)))
        sys.stdout.write('Extrapolation order N = %d\n'%(self.N))
        ff               = h5py.File(self.data_file, 'r')
        available_modes  = ff.get('Extrapolated_N%d.dir'%(self.N)).keys()
        self.lmax        = int(kwargs['injection-parameters']['lmax'])
        self.fix_NR_mode = kwargs['injection-parameters']['fix-NR-mode']
        try:
            (l_fix, m_fix) = self.fix_NR_mode[0]
        except:
            (l_fix, m_fix) = (None, None)
        self.absmmin     = 0
        sys.stdout.write('lmax = %d\n'%(self.lmax))
        (self.t22_geom, hr_geom22, hi_geom22) = (ff.get('Extrapolated_N%d.dir/Y_l%d_m%d.dat'%(self.N, 2, 2)).value).T
        self.h_plus   = np.array([0.]*len(self.t22_geom))
        self.h_cross  = np.array([0.]*len(self.t22_geom))

        if not((l_fix, m_fix)==(None, None)):
            l = l_fix
            m = m_fix
            assert not(m==0), "m=0 modes not yet supported."
            sys.stdout.write('Including (%d,%d) mode.\n'%(l, m))
            (t_geom, hr_geom, hi_geom) = (ff.get('Extrapolated_N%d.dir/Y_l%d_m%d.dat'%(self.N, l, m)).value).T
            if abs(m) >= self.absmmin:
                Amp = np.sqrt(hr_geom**2+hi_geom**2)
                #FIXME: check the convention which enforces this minus sign (it stops the people being upside down)
                Phi = np.unwrap(np.angle(hr_geom - 1j*hi_geom))
                Y_p = wf.SWSH(2,l,m)(self.incl_inj,self.phi_inj)
                self.h_plus  =  Amp*(np.cos(Phi)*np.real(Y_p) + np.sin(Phi)*np.imag(Y_p))
                self.h_cross = -Amp*(np.cos(Phi)*np.imag(Y_p) - np.sin(Phi)*np.real(Y_p))
                self.h_dressed = self.h_plus-1j*self.h_cross

        else:
            for l in range(2, self.lmax+1):
                for m in range(-l, l+1):
                    #FIXME: This expansion is not true for m=0. m=0 expansion needs to be implemented
                    if not(m==0):
                        sys.stdout.write('Including (%d,%d) mode.\n'%(l, m))
                        (t_geom, hr_geom, hi_geom) = (ff.get('Extrapolated_N%d.dir/Y_l%d_m%d.dat'%(self.N, l, m)).value).T
                        if abs(m) >= self.absmmin:
                            Y_p = wf.SWSH(2,l,m)(self.incl_inj,self.phi_inj)
                            Y_m = wf.SWSH(2,l,-m)(self.incl_inj,self.phi_inj)
                            Amp = np.sqrt(hr_geom**2+hi_geom**2)
                            Phi = np.unwrap(np.angle(hr_geom - 1j*hi_geom))

                            self.h_plus  += Amp*(np.cos(Phi)*(np.real(Y_p)+np.real(Y_m)) - np.sin(Phi)*(-np.imag(Y_p)+np.imag(Y_m)))
                            self.h_cross -= Amp*(np.cos(Phi)*(np.imag(Y_p)+np.imag(Y_m)) - np.sin(Phi)*(np.real(Y_p)-np.real(Y_m)))
            self.h_dressed = self.h_plus-1j*self.h_cross
        sys.stdout.write('\n')

def UNUSED_inject_NR_signal(lenstrain, tstart, length, ifo, triggertime, **kwargs):

    mass      = kwargs['injection-parameters']['M']
    dist      = kwargs['injection-parameters']['dist']
    psi       = kwargs['injection-parameters']['psi']
    M_inj_sec = mass*lal.MTSUN_SI
    tM_gps    = lal.LIGOTimeGPS(float(triggertime))
    detector  = lal.cached_detector_by_prefix[ifo]
    ref_det   = lal.cached_detector_by_prefix[kwargs['ref-det']]

    if (kwargs['sky-frame']=='detector'):
        tg, ra, dec = DetFrameToEquatorial(lal.cached_detector_by_prefix[kwargs['ref-det']],
                                           lal.cached_detector_by_prefix[kwargs['nonref-det']],
                                           triggertime,
                                           np.arccos(kwargs['injection-parameters']['cos_altitude']),
                                           kwargs['injection-parameters']['azimuth'])
    elif (kwargs['sky-frame']=='equatorial'):
        ra  = kwargs['injection-parameters']['ra']
        dec = kwargs['injection-parameters']['dec']
    else:
        raise ValueError("Invalid option for sky position sampling.")

    time_delay = lal.ArrivalTimeDiff(detector.location, ref_det.location, ra, dec, tM_gps)

    # Build NR waveform.
    NR_wf_obj = NR_waveform(**kwargs)
    t_phys    = NR_wf_obj.t22_geom*M_inj_sec
    hp        = NR_wf_obj.h_plus
    hc        = NR_wf_obj.h_cross

    time = tstart+np.linspace(0, length, lenstrain)

    # Interpolate the waveform over a uniform grid, NR sampling (t_phys) is NOT uniform.
    h_p_int = np.interp(time, tstart+t_phys, hp)
    h_c_int = np.interp(time, tstart+t_phys, hc)

    # Shift the waveform to the desidered tc.
    hp,hc = resize_time_series(np.column_stack((h_p_int,h_c_int)),
                               lenstrain,
                               time[1]-time[0],
                               tstart,
                               triggertime+time_delay)


    # Project the waveform onto a given detector, switching from geometrical to physical units.
    hs, hvx, hvy = np.zeros(len(hp)), np.zeros(len(hp)), np.zeros(len(hp))
    h = project(hs, hvx, hvy, hp, hc, detector, ra, dec, psi, tM_gps)

    # timeshift the waveform to the desired merger time in the given detector tM = THanford+time_delay.
    h *= mass * lal.MSUN_SI * lal.G_SI / (dist * lal.PC_SI*10**6 * lal.C_SI**2)

    return h

def F_mrg_Nagar_v0(m1, m2, a1, a2):
    # Old version of the merger frequency, defined with respect to the 22 mode of the inspiral.

    review_warning()

    q       = m1/m2 #Husa conventions, m1>m2 [https://arxiv.org/abs/1611.00332]
    eta     = q/(1+q)**2
    M_tot   = m1+m2
    chi_1   = 0.5*(1.0+np.sqrt(1.0-4.0*eta))
    chi_2   = 1.0-chi_1
    chi_eff = chi_1*a1 + chi_2*a2

    A = -0.28562363*eta + 0.090355762
    B = -0.18527394*eta + 0.12596953
    C =  0.40527397*eta + 0.25864318

    res = (A*chi_eff**2 + B*chi_eff + C)*((2*np.pi*M_tot)*lal.G_SI*lal.C_SI**(-3))**(-1)
    return res


def F_mrg_Nagar(m1, m2, a1, a2):

    review_warning()

    q           = m1/m2
    nu          = q/(1+q)**2
    M           = m1+m2;
    X12         = (m1-m2)/M
    Shat        = (m1**2*a1 + m2**2*a2)/M**2
    # Orbital fits calibrated to the non-spinning SXS data
    omg_tp         = 0.273356     # for this one I won't give an error the TP
    # waveform was generated with the TEUKCode
    # and I think it is pretty much acurate
    omg1         = 0.84074
    omg1_err     = 0.014341
    omg2         = 1.6976
    omg2_err     = 0.075488
    orb         = omg_tp*(1+omg1*nu+omg2*nu**2);

    # Equal Mass fit calibrated to the q=1 SXS data
    b1             = -0.42311
    b1_err      = 0.088583
    b2            = -0.066699
    b2_err         = 0.042978
    b3             = -0.83053
    b3_err         = 0.084516

    # Unequal Mass corrections to the q=1 fit based on SXS, BAM and TP data
    c1            = 0.066045
    c1_err         = 0.13227
    c2            = -0.23876
    c2_err         = 0.29338
    c3          = 0.76819
    c3_err         = 0.01949
    c4          = -0.9201
    c4_err         = 0.025167
    num         = 1.+((b1+c1*X12)/(1.+c2*X12))*Shat+b2*Shat**2
    denom       = 1.+((b3+c3*X12)/(1.+c4*X12))*Shat
    res         = (orb*num/denom)*((2*np.pi*M)*lal.G_SI*lal.C_SI**(-3))**(-1)
    return res

def F_mrg_Bohe(m1,m2,a1,a2):

    review_warning()

    # Frequency fit from Bohe et al. arXiv:1611.03703
    q       = m1/m2
    M_tot   = m1+m2
    nu      = q/(1+q)**2
    delta   = np.sqrt(1.-4.*nu)
    chi_S   = 0.5*(a1+a2)
    chi_A   = 0.5*(a1-a2)
    chi     = chi_S + chi_A*delta*((1.-2.*nu)**(-1))

    p0_TPL  = + 0.562679
    p1_TPL  = - 0.087062
    p2_TPL  = + 0.001743
    p3_TPL  = + 25.850378
    p4_TPL  = + 25.819795

    p3_EQ   = 10.262073
    p4_EQ   = 7.629922

    A3      = p3_EQ + 4.*(p3_EQ - p3_TPL)*(nu-1./4.)
    A4      = p4_EQ + 4.*(p4_EQ - p4_TPL)*(nu-1./4.)

    res     = (p0_TPL + (p1_TPL + p2_TPL*chi)*np.log(A3 - A4*chi))*((2.*np.pi*M_tot)*lal.G_SI*lal.C_SI**(-3))**(-1)
    return res

def F_mrg_Healy(m1,m2,a1,a2):
    #Phys. Rev. D 97, 084002(2018)
    # Very Important!!!! This Fit uses the convention m1>m2 and thus has
    # Sign differences in the definitions of dm and Delta comparing to
    # the orignial paper!
    M_tot = m1+m2
    dm  = (m2-m1)/(m1+m2)
    Delta=(a1*m1-a2*m2)/(m1+m2)
    St  = (m1**2*a1+m2**2*a2)/(m1+m2)**2


    W0  = 0.3587
    W1  = 0.14189
    W2a = -0.01461
    W2b = 0.05505
    W2c = 0.00878
    W2d = -0.1211
    W3a = -0.16841
    W3b = 0.04874
    W3c = 0.09181
    W3d = -0.08607
    W4a = -0.02185
    W4b = 0.11183
    W4c = -0.01704
    W4d = 0.21595
    W4e = -0.12378
    W4f = 0.0432
    W4g = 0.00167
    W4h = -0.13224
    W4i = -0.09933
    o1     = W0 + W1*St + W2a*Delta*dm + W2b*St**2 + W2c*Delta**2 + W2d*dm**2
    o2     = W3a*Delta*St*dm + W3b*St*Delta**2 + W3c*St**3 + W3d*St*dm**2
    o3     = W4a*Delta*St**2*dm + W4b*Delta**3*dm + W4c*Delta**4 + W4d*St**4
    o4     = W4e*Delta**2*St**2 + W4f*dm**4 + W4g*Delta*dm**3 + W4h*Delta**2*dm**2 + W4i*St**2*dm**2
    res = (o1 + o2 + o3 + o4)*((2.*np.pi*M_tot)*lal.G_SI*lal.C_SI**(-3))**(-1)
    return res

def A_mrg_Bohe(m1,m2,a1,a2):

    review_warning()

    # Frequency fit from Bohe et al. arXiv:1611.03703
    q               = m1/m2
    nu      = q/(1+q)**2
    delta   = np.sqrt(1.-4.*nu)
    chi_S   = 0.5*(a1+a2)
    chi_A   = 0.5*(a1-a2)
    chi     = chi_S + chi_A*delta*((1.-2.*nu)**(-1))

    e00     = +1.452857
    e01     = +0.166134
    e02     = +0.027356
    e03     = -0.020073

    e10     = -0.034424
    e11     = -1.218066
    e12     = -0.568373
    e13     = +0.401114


    Amp_tp  = e00 + e01*chi + e02*chi**2 + e03*chi**3
    Amp_lin = e10 + e11*chi + e12*chi**2 + e13*chi**3

    e20     = + 16*1.577458 - 16*e00 - 4*e10
    e21     = - 16*0.007695 - 16*e01 - 4*e11
    e22     = + 16*0.021887 - 16*e02 - 4*e12
    e23     = + 16*0.023268 - 16*e03 - 4*e13

    Amp_quad= e20 + e21*chi + e22*chi**2 + e23*chi**3
    res     = nu*(Amp_tp + Amp_lin*nu + Amp_quad*nu**2)
    return res

def A_mrg_Healy(m1,m2,a1,a2):
        #Phys. Rev. D 97, 084002(2018)
        # Very Important!!!! This Fit uses the convention m1>m2 and thus has
        # Sign differences in the definitions of dm and Delta comparing to
        # the orignial paper!
        # When comparing with the fit presented in the paper in eq (20) then
        # it is important to note that the coeffieicents are referred to as
        # H.. instead of A

    review_warning()

    dm  = (m2-m1)/(m1+m2)
    Delta=(a1*m1-a2*m2)/(m1+m2)
    St  = (m1**2*a1+m2**2*a2)/(m1+m2)**2
    nu      = m1*m2*(m1+m2)**(-2)
    A0  = 0.3937
    A1  = -0.00252
    A2a = 0.00385
    A2b = 0.00495
    A2c = -0.00145
    A2d = -0.0526
    A3a = 0.00331
    A3b = 0.01775
    A3c = 0.03202
    A3d = 0.05267
    A4a = 0.11029
    A4b = -0.00552
    A4c = 0.00558
    A4d = 0.04593
    A4e = -0.04754
    A4f = 0.0179
    A4g = -0.00516
    A4h = 0.00163
    A4i = -0.02098

    h1      = A0 + A1*St + A2a*Delta*dm + A2b*St**2 + A2c*Delta**2
    h2              = A2d*dm**2 +A3a*Delta*St*dm + A3b*St*Delta**2 + A3c*St**3
    h3              = A3d*St*dm**2 + A4a*Delta*St**2*dm + A4b*Delta**3*dm
    h4              = A4c*Delta**4 + A4d*St**4 + A4e*Delta**2*St**2 + A4f*dm**4
    h5              = A4g*Delta*dm**3 + A4h*Delta**2*dm**2 + A4i*St**2*dm**2
    res     = 4*nu*(h1 + h2 + h3 + h4 + h5)
    return res

def A_mrg_Nagar(m1, m2, a1, a2):

    review_warning()

    q    = m1/m2
    nu   = q/(1+q)**2
    M    = m1+m2
    X12  = (m1-m2)/M
    Shat = (m1**2*a1 + m2**2*a2)/M**2

    # Orbital fits calibrated to the non-spinning SXS data
    omg_tp         = 0.273356     # for this one I won't give an error the TP waveform was generated with the TEUKCode and I think it is pretty much acurate
    omg1         = 0.84074
    omg1_err     = 0.014341
    omg2         = 1.6976
    omg2_err     = 0.075488
    orb         = omg_tp*(1.+omg1*nu+omg2*nu**2)

    # Equal Mass fit calibrated to the q=1 SXS data
    b1             = -0.42311
    b1_err      = 0.088583
    b2            = -0.066699
    b2_err         = 0.042978
    b3             = -0.83053
    b3_err         = 0.084516

    # Unequal Mass corrections to the q=1 fit based on SXS, BAM and TP data
    c1            = 0.066045
    c1_err         = 0.13227
    c2            = -0.23876
    c2_err         = 0.29338
    c3          = 0.76819
    c3_err         = 0.01949
    c4          = -0.9201
    c4_err         = 0.025167
    num         = 1.+((b1+c1*X12)/(1.+c2*X12))*Shat+b2*Shat**2
    denom       = 1.+((b3+c3*X12)/(1.+c4*X12))*Shat
    omgmx       = (orb*num/denom)

    scale       = 1. - Shat*omgmx
    # Orbital fits calibrated to the non-spinning SXS data
    Amax_tp     = 0.295897  # for this one I won't give an error the TP
    # waveform was generated with the TEUKCode
    # and I think it is pretty much acurate
    Amax1         = -0.041285
    Amax1_err     = 0.0078878
    Amax2         = 1.5971
    Amax2_err     = 0.041521

    orb_A        = Amax_tp*(1+Amax1*nu+Amax2*nu**2)

    # Equal Mass fit calibrated to the q=1 SXS data
    b1Amax         = -0.74124
    b1Amax_err     = 0.016178
    b2Amax        = -0.088705
    b2Amax_err     = 0.0081611
    b3Amax         = -1.0939
    b3Amax_err     = 0.015318

    # Unequal Mass corrections to the q=1 fit based on SXS, BAM and TP data
    c1Amax        = 0.44467
    c1Amax_err     = 0.037352
    c2Amax       = -0.32543
    c2Amax_err     = 0.081211
    c3Amax        = 0.45828
    c3Amax_err     = 0.066062
    c4Amax       = -0.21245
    c4Amax_err     = 0.080254

    num_A       = 1+((b1Amax+c1Amax*X12)/(1+c2Amax*X12))*Shat+b2Amax*Shat**2
    denom_A     = 1+((b3Amax+c3Amax*X12)/(1+c4Amax*X12))*Shat
    res         = nu*orb_A*scale*num_A*(denom_A**(-1))*np.sqrt(24)
    return res

#UNUSED code to interpolate NR wfs.
## Interpolate the waveform over a uniform grid, NR sampling (t_phys) is NOT uniform. Then pad it to the total strain length.
#    endtime            = tstart+length
#    dt_uniform         = length/lenstrain
#    nr_wf_len          = t_phys[-1]-t_phys[0]
#    npoints            = nr_wf_len/dt_uniform
#    t_phys_uniform     = np.linspace(t_phys[0], t_phys[-1], npoints)
#    h_p_int            = np.interp(t_phys_uniform, t_phys, hp)
#    h_c_int            = np.interp(t_phys_uniform, t_phys, hc)
#    t_peak             = t_phys_uniform[np.argmax(h_p_int**2 + h_c_int**2)]
#    dt_peak_start      = t_peak - t_phys_uniform[0]
#    dt_peak_end        = t_phys_uniform[-1] - t_peak
#    dt_buffer_start    = (triggertime+time_delay-dt_peak_start) - tstart
#    dt_buffer_end      = endtime - (triggertime+time_delay+dt_peak_end)
#    buffer_start_len   = int(dt_buffer_start/dt_uniform)
#    buffer_end_len     = int(dt_buffer_end/dt_uniform)
#    zeros_start        = np.zeros(buffer_start_len)
#    zeros_end          = np.zeros(buffer_end_len)
#    h_p_buffered_start = np.concatenate((zeros_start, np.array(h_p_int)), axis=None)
#    h_c_buffered_start = np.concatenate((zeros_start, np.array(h_c_int)), axis=None)
#    hp                 = np.concatenate((h_p_buffered_start, zeros_end), axis=None)
#    hc                 = np.concatenate((h_c_buffered_start, zeros_end), axis=None)
