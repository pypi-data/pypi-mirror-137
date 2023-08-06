# -*- coding: utf-8 -*-
#Standard python imports
from __future__ import division
import h5py, matplotlib.pyplot as plt, numpy as np, os, sys

#LVC imports
from lalinference import DetFrameToEquatorial, EquatorialToDetFrame
from lalinference.imrtgr.nrutils import bbh_final_mass_projected_spins, bbh_final_spin_projected_spins, bbh_Kerr_trunc_opts

import lal, lalsimulation as lalsim

#Package internal imports
from pyRing.likelihood import project
from pyRing.utils      import check_NR_dir, qnm_interpolate, qnm_interpolate_KN, resize_time_series, review_warning
from pyRing            import waveform as wf



def inject_ringdown_signal(lenstrain, tstart, length, ifo, triggertime, **kwargs):

    """
        Main function to set an injection using one of the analytical ringdown templates available.
        Handles parameters common to all templates.
    """

    time_wf = np.linspace(0,length,lenstrain)

    if (kwargs['injection-approximant']=='Damped-sinusoids'):
        wf_model = damped_sinusoids_injection(**kwargs)
    elif (kwargs['injection-approximant']=='Morlet-Gabor-wavelets'):
        wf_model = morlet_gabor_wavelets_injection(**kwargs)
    elif (kwargs['injection-approximant']=='Kerr'):
        wf_model = kerr_injection(**kwargs)
    elif (kwargs['injection-approximant']=='MMRDNS'):
        wf_model = mmrdns_injection(**kwargs)
    elif (kwargs['injection-approximant']=='MMRDNP'):
        wf_model = mmrdnp_injection(**kwargs)
    elif (kwargs['injection-approximant']=='TEOBResumSPM'):
        wf_model = TEOBPM_injection(**kwargs)
    elif (kwargs['injection-approximant']=='KHS_2012'):
        wf_model = khs_injection(**kwargs)
    hs, hvx, hvy, hp, hc = wf_model.waveform(time_wf)[0], wf_model.waveform(time_wf)[1], wf_model.waveform(time_wf)[2], wf_model.waveform(time_wf)[3], wf_model.waveform(time_wf)[4]

    sys.stdout.write('\nInjecting waveform in {}.\n'.format(ifo))

    h        = np.zeros(len(hs))
    srate    = kwargs['sampling-rate']
    detector = lal.cached_detector_by_prefix[ifo]
    ref_det  = lal.cached_detector_by_prefix[kwargs['ref-det']]
    psi      = kwargs['injection-parameters']['psi']
    tM_gps   = lal.LIGOTimeGPS(float(triggertime))
    scaling  = kwargs['injection-scaling']
    if not(scaling==1.0):
        sys.stdout.write('\nApplying a scaling factor {} to the injection.'.format(scaling))

    if (kwargs['sky-frame']=='detector'):
        tg, ra, dec = DetFrameToEquatorial(lal.cached_detector_by_prefix[kwargs['ref-det']],
                                           lal.cached_detector_by_prefix[kwargs['nonref-det']],
                                           triggertime,
                                           np.arccos(kwargs['injection-parameters']['cos_altitude']),
                                           kwargs['injection-parameters']['azimuth'])
    elif (kwargs['sky-frame']=='equatorial'):
        ra         = kwargs['injection-parameters']['ra']
        dec        = kwargs['injection-parameters']['dec']
    else:
        raise ValueError("Invalid option for sky position sampling.")

    hs, hvx, hvy, hp, hc = hs*scaling, hvx*scaling, hvy*scaling, hp*scaling, hc*scaling
    wave       = project(hs, hvx, hvy, hp, hc, detector, ra, dec, psi, tM_gps)
    time_delay = lal.ArrivalTimeDiff(detector.location, ref_det.location, ra, dec, tM_gps)
    trig_idx   = int((triggertime+time_delay-tstart)*srate)

    for i in range(0, len(wave)-trig_idx):
        h[trig_idx+i] = wave[i]

    return h

def damped_sinusoids_injection(**kwargs):

    sys.stdout.write('Injecting Damped Sinusoids model.')

    wf_model = wf.Damped_sinusoids(kwargs['injection-parameters']['A']  ,
                                   kwargs['injection-parameters']['f']  ,
                                   kwargs['injection-parameters']['tau'],
                                   kwargs['injection-parameters']['phi'],
                                   kwargs['injection-parameters']['t']  )
    return wf_model

def morlet_gabor_wavelets_injection(**kwargs):

    sys.stdout.write('Injecting Morlet-Gabor wavelets model.')

    wf_model = wf.Morlet_Gabor_wavelets(kwargs['injection-parameters']['A']  ,
                                        kwargs['injection-parameters']['f']  ,
                                        kwargs['injection-parameters']['tau'],
                                        kwargs['injection-parameters']['phi'],
                                        kwargs['injection-parameters']['t']  )
    return wf_model

def kerr_injection(**kwargs):

    sys.stdout.write('Injecting Kerr model.')

    t0               = kwargs['injection-parameters']['t0']
    Mf               = kwargs['injection-parameters']['Mf']
    af               = kwargs['injection-parameters']['af']
    Q                = kwargs['injection-parameters']['Q']
    r                = np.exp(kwargs['injection-parameters']['logdistance'])
    phi              = kwargs['injection-parameters']['phi']
    cosiota          = kwargs['injection-parameters']['cosiota']
    iota             = np.arccos(cosiota)
    amps             = kwargs['injection-parameters']['kerr-amplitudes']
    domegas          = kwargs['injection-parameters']['kerr-domegas']
    dtaus            = kwargs['injection-parameters']['kerr-dtaus']
    area_flag        = kwargs['inject-area-quantization']
    charge_flag      = kwargs['inject-charge']
    spheroidal       = kwargs['spheroidal']
    Amp_non_prec_sym = kwargs['amp-non-prec-sym']
    qnm_fit          = kwargs['qnm-fit']
    ref_amplitude    = kwargs['reference-amplitude']

    TGR_parameters   = {}
    qnm_interpolants = {}

    if(kwargs['qnm-fit'] == 0):
        #FIXME: when including 2 amps for each mode, this line will need to be changed
        for (s,l,m,n) in amps.keys():
            if(charge_flag):
                interpolate_freq, interpolate_tau = qnm_interpolate_KN(s,l,m,n)
            else:
                interpolate_freq, interpolate_tau = qnm_interpolate(s,l,m,n)
            qnm_interpolants[(s,l,m,n)] = {'freq': interpolate_freq, 'tau': interpolate_tau}

    try:
        for (s,l,m,n) in domegas.keys():
            TGR_parameters['domega_{}{}{}'.format(l,m,n)] = domegas[(s,l,m,n)]
    except:
        pass
    try:
        for (s,l,m,n) in dtaus.keys():
            TGR_parameters['dtau_{}{}{}'.format(l,m,n)] = dtaus[(s,l,m,n)]
    except:
        pass

    if(area_flag):
        TGR_parameters['alpha'] = kwargs['injection-parameters']['alpha']
        sys.stdout.write('Injecting a modified Kerr waveform according to the area quantization prescription. alpha: {}'.format(TGR_parameters['alpha']))
    elif(charge_flag):
        TGR_parameters['Q'] = Q
        sys.stdout.write('Injecting a KN waveform. Q: {}'.format(TGR_parameters['Q']))
    if not(af**2 + Q**2 < 1):
        raise ValueError("The selected values of charge and spin break the extremality limit (spin = {spin}, charge = {charge} : af^2 + Q^2 = {tot}).".format(spin=af, charge=Q, tot = af**2 + Q**2))

    wf_model = wf.KerrBH(t0                                 ,
                         Mf                                 ,
                         af                                 ,
                         amps                               ,
                         r                                  ,
                         iota                               ,
                         phi                                ,
                         TGR_parameters                     ,
                         ref_amplitude                      ,
                         qnm_fit          = qnm_fit         ,
                         interpolants     = qnm_interpolants,
                         Spheroidal       = spheroidal      ,
                         amp_non_prec_sym = Amp_non_prec_sym,
                         AreaQuantization = area_flag       ,
                         charge           = charge_flag     )

    return wf_model

def mmrdns_injection(**kwargs):

    sys.stdout.write('Injecting MMRDNS model.')

    t0      = kwargs['injection-parameters']['t0']
    Mf      = kwargs['injection-parameters']['Mf']
    af      = kwargs['injection-parameters']['af']
    eta     = kwargs['injection-parameters']['eta']
    r       = np.exp(kwargs['injection-parameters']['logdistance'])
    cosiota = kwargs['injection-parameters']['cosiota']
    iota    = np.arccos(cosiota)
    phi     = kwargs['injection-parameters']['phi']
    qnm_fit = kwargs['qnm-fit']

    TGR_par          = {}
    qnm_interpolants = {}
    modes =  [(2,2,2,0), (2,2,2,1), (2,2,1,0), (2,3,3,0), (2,3,3,1), (2,3,2,0), (2,4,4,0), (2,4,3,0), (2,5,5,0)]
    if(kwargs['qnm-fit'] == 0):
        for (s,l,m,n) in modes:
            interpolate_freq, interpolate_tau = qnm_interpolate(s,l,m,n)
            qnm_interpolants[(s,l,m,n)] = {'freq': interpolate_freq, 'tau': interpolate_tau}

    wf_model = wf.MMRDNS(t0                             ,
                         Mf                             ,
                         af                             ,
                         eta                            ,
                         r                              ,
                         iota                           ,
                         phi                            ,
                         TGR_par                        ,
                         interpolants = qnm_interpolants,
                         qnm_fit      = qnm_fit         )

    return wf_model

def mmrdnp_injection(**kwargs):

    sys.stdout.write('Injecting MMRDNP model.')

    t0      = kwargs['injection-parameters']['t0']
    m1      = kwargs['injection-parameters']['m1']
    m2      = kwargs['injection-parameters']['m2']
    chi1    = kwargs['injection-parameters']['chi1']
    chi2    = kwargs['injection-parameters']['chi2']
    r       = np.exp(kwargs['injection-parameters']['logdistance'])
    cosiota = kwargs['injection-parameters']['cosiota']
    iota    = np.arccos(cosiota)
    phi     = kwargs['injection-parameters']['phi']
    TGR_par = {}

    # Adapt to final state fits conventions
    if(chi1 < 0): tilt1 = np.pi
    else:         tilt1 = 0.0
    if(chi2 < 0): tilt2 = np.pi
    else:         tilt2 = 0.0
    chi1_abs = np.abs(chi1)
    chi2_abs = np.abs(chi2)
    
    Mf   = bbh_final_mass_projected_spins(m1, m2, chi1_abs, chi2_abs, tilt1, tilt2, 'UIB2016')
    af   = bbh_final_spin_projected_spins(m1, m2, chi1_abs, chi2_abs, tilt1, tilt2, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)
    Mi   = m1 + m2
    eta  = (m1*m2)/(Mi)**2
    chis = (m1*chi1 + m2*chi2)/(Mi)
    chia = (m1*chi1 - m2*chi2)/(Mi)

    wf_model = wf.MMRDNP(t0     ,
                         Mf     ,
                         af     ,
                         Mi     ,
                         eta    ,
                         chis   ,
                         chia   ,
                         r      ,
                         iota   ,
                         phi    ,
                         TGR_par)

    return wf_model

def TEOBPM_injection(**kwargs):

    sys.stdout.write('Injecting TEOBResumSPM model.')
    
    multipoles = [(2,2), (3,3), (4,4), (5,5)]
    
    t0      = kwargs['injection-parameters']['t0']
    m1      = kwargs['injection-parameters']['m1']
    m2      = kwargs['injection-parameters']['m2']
    chi1    = kwargs['injection-parameters']['chi1']
    chi2    = kwargs['injection-parameters']['chi2']
    r       = np.exp(kwargs['injection-parameters']['logdistance'])
    cosiota = kwargs['injection-parameters']['cosiota']
    iota    = np.arccos(cosiota)
    phi     = kwargs['injection-parameters']['phi']
    TGR_par = {}
    phases  = {}

    for multipole in multipoles:
        (l,m) = multipole
        phases[(l,m)] = kwargs['injection-parameters']['phi{}{}'.format(l,m)]

    wf_model = wf.TEOBPM(t0     ,
                         m1     ,
                         m2     ,
                         chi1   ,
                         chi2   ,
                         phases ,
                         r      ,
                         iota   ,
                         phi    ,
                         TGR_par)

    return wf_model

def khs_injection(**kwargs):

    sys.stdout.write('Injecting KHS_2012 model.')

    t0      = kwargs['injection-parameters']['t0']
    Mf      = kwargs['injection-parameters']['Mf']
    af      = kwargs['injection-parameters']['af']
    chi_eff = kwargs['injection-parameters']['chi_eff']
    eta     = kwargs['injection-parameters']['eta']
    r       = np.exp(kwargs['injection-parameters']['logdistance'])
    cosiota = kwargs['injection-parameters']['cosiota']
    iota    = np.arccos(cosiota)
    phi     = kwargs['injection-parameters']['phi']
    TGR_par = {}

    wf_model = wf.KHS_2012(t0     ,
                           Mf     ,
                           af     ,
                           eta    ,
                           chi_eff,
                           r      ,
                           iota   ,
                           phi    ,
                           TGR_par)

    return wf_model

def inject_IMR_signal(lenstrain, tstart, length, ifo, triggertime, **kwargs):

    review_warning()

    params  = lal.CreateDict()
    deltaT  = 1.0/kwargs['sampling-rate']
    f_ref   = kwargs['injection-parameters']['f-ref']
    f_start = kwargs['injection-parameters']['f-start']
    scaling = kwargs['injection-scaling']

    if(kwargs['injection-approximant']=='NR'):
        #=======================================================================================================================#
        # For tutorials and info on how to use the LVC NR injection infrastructure see:                                         #
        # - https://git.ligo.org/sebastian-khan/waveform-f2f-berlin/blob/master/notebooks/2017WaveformsF2FTutorial_NRDemo.ipynb #
        # - https://www.lsc-group.phys.uwm.edu/ligovirgo/cbcnote/Waveforms/NR/InjectionInfrastructure                           #
        # - https://arxiv.org/pdf/1703.01076.pdf                                                                                #
        #=======================================================================================================================#

        check_NR_dir()
        data_file = kwargs['injection-parameters']['NR-datafile']
        approx    = lalsim.NR_hdf5
        lalsim.SimInspiralWaveformParamsInsertNumRelData(params, data_file)
    else:
        approx = lalsim.SimInspiralGetApproximantFromString(kwargs['injection-approximant'].strip('LAL-'))
        lalsim.SimInspiralWaveformParamsInsertPNAmplitudeOrder(params,int(kwargs['injection-parameters']['amp-order']))
        lalsim.SimInspiralWaveformParamsInsertPNPhaseOrder(params,int(kwargs['injection-parameters']['phase-order']))

    detector  = lal.cached_detector_by_prefix[ifo]
    ref_det   = lal.cached_detector_by_prefix[kwargs['ref-det']]
    tM_gps    = lal.LIGOTimeGPS(float(triggertime))

    m1       = kwargs['injection-parameters']['m1']
    m2       = kwargs['injection-parameters']['m2']
    s1x      = kwargs['injection-parameters']['s1x_LALSim']
    s1y      = kwargs['injection-parameters']['s1y_LALSim']
    s1z      = kwargs['injection-parameters']['s1z_LALSim']
    s2x      = kwargs['injection-parameters']['s2x_LALSim']
    s2y      = kwargs['injection-parameters']['s2y_LALSim']
    s2z      = kwargs['injection-parameters']['s2z_LALSim']
    theta_LN = kwargs['injection-parameters']['theta_LN']
    phi      = kwargs['injection-parameters']['phi']
    dist     = kwargs['injection-parameters']['dist']
    psi      = kwargs['injection-parameters']['psi']

    if not (scaling == 1.0):
        dist = dist/scaling
        sys.stdout.write('\nApplying a scaling factor {} to the injection.'.format(scaling))

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

    if (kwargs['injection-parameters']['inject-modes'] is not None):
        ModeArray = lalsim.SimInspiralCreateModeArray()
        sys.stdout.write('\nInjecting a subset of modes: ')
        for mode in kwargs['injection-parameters']['inject-modes']:
            sys.stdout.write('l={}, m={}; \n'.format(mode[0], mode[1]))
            lalsim.SimInspiralModeArrayActivateMode(ModeArray, mode[0], mode[1])
        lalsim.SimInspiralWaveformParamsInsertModeArray(params, ModeArray)
    elif (kwargs['injection-parameters']['inject-l-modes'] is not None):
        ModeArray = lalsim.SimInspiralCreateModeArray()
        sys.stdout.write('\nInjecting a subset of l modes (all |m|<l modes are being injected): ')
        for mode in kwargs['injection-parameters']['inject-l-modes']:
            sys.stdout.write('l={}; '.format(mode))
            lalsim.SimInspiralModeArrayActivateAllModesAtL(ModeArray, mode)
        lalsim.SimInspiralWaveformParamsInsertModeArray(params, ModeArray)
    sys.stdout.write('\n')

    h_p, h_c = lalsim.SimInspiralChooseTDWaveform(m1*lal.MSUN_SI,
                                                  m2*lal.MSUN_SI,
                                                  s1x, s1y, s1z,
                                                  s2x, s2y, s2z,
                                                  dist*lal.PC_SI*10**6, theta_LN, phi,
                                                  0.0, 0.0, 0.0,
                                                  deltaT, f_start, f_ref,
                                                  params, approx)

    h_p = h_p.data.data
    h_c = h_c.data.data

    # Shift the peak of the amplitude to the desidered triggertime.
    hp,hc = resize_time_series(np.column_stack((h_p,h_c)),
                               lenstrain,
                               deltaT,
                               tstart,
                               triggertime+time_delay)

    # Project the waveform onto a given detector.
    hs, hvx, hvy = np.zeros(len(hp)), np.zeros(len(hp)), np.zeros(len(hp))
    h = project(hs, hvx, hvy, hp, hc, detector, ra, dec, psi, tM_gps)

    return h
