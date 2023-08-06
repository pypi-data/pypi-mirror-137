#!/usr/bin/env python
#Standard python imports
import ast, itertools as it, json, h5py, matplotlib, numpy as np, os, subprocess, sys, time, traceback, warnings
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
from optparse import OptionParser

#LVC imports
from lalinference import DetFrameToEquatorial
from lalinference.imrtgr.nrutils import *
import lal, lalsimulation as lalsim

#Package internal imports
import cpnest.model
from pyRing            import plots, utils, waveform as wf
from pyRing.likelihood import loglikelihood, loglikelihood_core, detector



ell_units_factor = (lal.C_SI**2 * 10**3)/(lal.MSUN_SI*lal.G_SI)
matplotlib.rc('text', usetex=False)

def get_param_override(fixed_params,x,name):
    """
        Function returning either a sample or the fixed value for the parameter considered.
        ---------------
        
        Returns x[name], unless it is over-ridden by
        value in the fixed_params dictionary.
        
    """
    if name in fixed_params:
        return fixed_params[name]
    else:
        return x[name]

def read_parameter_bounds(Config, configparser, kwargs, name, default_bounds, approx_name, extra_polarisation=None):
    
    single_bounds = [0.0,0.0]
    
    if(extra_polarisation==None):
        composite_name = name
    else:
        pol, i = extra_polarisation
        composite_name = '{}_{}_{}'.format(name, pol,i)
        
    try:
        single_bounds[0] = Config.getfloat("Priors", composite_name+'-min')
    except (KeyError, configparser.NoOptionError, configparser.NoSectionError, configparser.NoSectionError):
        single_bounds[0] = default_bounds[name][0]
    try:
        single_bounds[1] = Config.getfloat("Priors", composite_name+'-max')
    except (KeyError, configparser.NoOptionError, configparser.NoSectionError, configparser.NoSectionError):
        single_bounds[1] = default_bounds[name][1]

    # This try-except is needed because we might inject and recover a different set of parameters
    try:
        if (kwargs['injection-approximant']==approx_name):
            if(extra_polarisation==None):
                if (not(single_bounds[0] <= kwargs['injection-parameters']['{}'.format(name)] <= single_bounds[1])):
                    print('\n\n######################### WARNING ############################')
                    print(('# The {} injected value lies outside prior bounds. #'.format(name)))
                    print('##############################################################\n\n')
            else:
                if (name=='logA'):
                    if (not(10**(single_bounds[0]) <= kwargs['injection-parameters']['A'][pol][i] <= 10**(single_bounds[1]))):
                        print('\n\n######################### WARNING ############################')
                        print(('# The {} injected values are outside the prior bounds. #'.format(name)))
                        print('##############################################################\n\n')
                else:
                    if (not(single_bounds[0] <= kwargs['injection-parameters'][name][pol][i] <= single_bounds[1])):
                        print('\n\n######################### WARNING ############################')
                        print(('# The {} injected values are outside the prior bounds. #'.format(name)))
                        print('##############################################################\n\n')
    except(IndexError, KeyError):
        pass

    print(('{} : [{}, {}]'.format(composite_name.ljust(len('cos_altitude')), single_bounds[0], single_bounds[1])))

    return single_bounds



class LIGOVirgoModel(cpnest.model.Model):

    """
    Parent class for all the models used in the package.
    Reads the data and sets sky position parameters common to all waveform models.
    """
        
    def __init__(self, **kwargs):

        super(LIGOVirgoModel,self).__init__()
        self.gr_time_prior    = kwargs['gr-time-prior']
        self.srate            = kwargs['sampling-rate']
        self.dt               = 1./self.srate
        self.noise_chunksize  = kwargs['noise-chunksize']
        self.signal_chunksize = kwargs['signal-chunksize']
        self.OnsourceACF      = kwargs['onsource-ACF']
        self.Dirac_comb       = kwargs['Dirac-comb']
        self.Zeroing_data     = kwargs['Zeroing-data']
        self.truncate         = kwargs['truncate']
        self.duration_n       = kwargs['analysis-duration-n']

        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])

        # Estimate of peak time in reference detector.
        self.tevent = kwargs['trigtime']
        self.tgps   = lal.LIGOTimeGPS(float(self.tevent))
        print(('\nTrigtime in {}: {:f}\n'.format(kwargs['ref-det'], self.tevent)))

        # Set up the datafiles and the detectors.
        # Analyze a stretch T of data centered around the t_merger (default trigtime in H1).
        # T must be bigger than light travel time between detectors + lenght of ringdown
        # (light travel time across Earth diameter: 0.042s)
        self.datafiles = {det:kwargs['data-{}'.format(det)] if(not(kwargs['data-{}'.format(det)]=='')) else None for det in kwargs['detectors']}
        self.detectors = {'{}'.format(ifo): detector(ifo, fname, **kwargs) for ifo,fname in list(self.datafiles.items())}
        
        if(kwargs['run-type']=='psd-only'): exit()
        
        self.len_det       = len(kwargs['detectors'])
        self.ref_det       = kwargs['ref-det']
        self.sky_frame     = kwargs['sky-frame']
        self.signal_seglen = np.int(self.srate*self.signal_chunksize)
        if(self.len_det > 1): self.non_ref_det = kwargs['nonref-det']

        # Set common parameters structures.
        self.names         = []
        self.bounds        = []
        self.fixed_params  = {}

        # Set sky position parameters.
        if (self.sky_frame == 'detector'):
            print('\nUsing detectors network-based sky coordinates.\n')
            self.default_angles_bounds = {'azimuth'      : [0.0,2.0*np.pi],
                                          'cos_altitude' : [-1.0,1.0]     ,
                                          'psi'          : [0.0,np.pi]    }
            print('\nUsing azimuth and cos_altitude to sample sky position.\n')
        elif(self.sky_frame == 'equatorial'):
            print('\nUsing equatorial sky coordinates.\n')
            self.default_angles_bounds = {'ra'  : [0.0,2.0*np.pi]     ,
                                          'dec' : [-np.pi/2.,np.pi/2.],
                                          'psi' : [0.0,np.pi]         }
        else:
            raise ValueError("Invalid option for sky position coordinates.")

        print('\n----Prior section - General----\nI\'ll be running with the following prior bounds:\n')

        for name in self.default_angles_bounds.keys():
            try:
                self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                assert not((name=='dec') and ((self.fixed_params['dec'] > (self.default_angles_bounds['dec'][1])) or (self.fixed_params['dec'] < (self.default_angles_bounds['dec'][0])))), "Injected value of declination out of definition interval."
                assert not((name=='ra') and ((self.fixed_params['ra'] > (self.default_angles_bounds['ra'][1])) or (self.fixed_params['ra'] < (self.default_angles_bounds['ra'][0])))), "Injected value of right ascension out of definition interval."
                assert not((name=='psi') and ((self.fixed_params['psi'] > (self.default_angles_bounds['psi'][1])) or (self.fixed_params['psi'] < (self.default_angles_bounds['psi'][0])))), "Injected value of polarization out of definition interval."
            except(configparser.NoOptionError, configparser.NoSectionError):
                try:
                    single_bounds = [self.Config.getfloat("Priors",name+'-min'),self.Config.getfloat("Priors",name+'-max')]
                except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    single_bounds = self.default_angles_bounds[name]
                print(('{} : [{}, {}]'.format(name.ljust(len('cos_altitude')), single_bounds[0], single_bounds[1])))
                if ( not(kwargs['injection-approximant']=='') and (self.len_det == 1) ):
                    if (not(single_bounds[0] <= kwargs['injection-parameters']['{}'.format(name)] <= single_bounds[1])):
                        print('\n\n######################### WARNING ############################')
                        print(('# The {} injected values are outside the prior bounds. #'.format(name)))
                        print('##############################################################\n\n')
                self.names.append('{}'.format(name))
                self.bounds.append(single_bounds)
        if not self.truncate:
            # Compute the probability that the whole chunk is explained by gaussian noise.
            self.logZnoise = np.sum([loglikelihood_core(d.time_series, d.inverse_covariance, d.log_normalisation) for d in list(self.detectors.values())])
        else:
            # FIXME: In the case the data analyzed varies with t0 and sky location (not currently used), we need to compute a distribution of logBs for each (t0, skypos) sample. To be done in post-processing.
            time_delay = {'{}_'.format(self.ref_det)+d2: 0.0 for d2 in list(self.detectors.keys())}
            self.logZnoise = loglikelihood(self,
                                           None,
                                           None,
                                           0.0,
                                           0.0,
                                           0.0,
                                           0.0,
                                           time_delay,
                                           self.ref_det,
                                           self.truncate,
                                           self.duration_n,
                                           self.OnsourceACF,
                                           self.Dirac_comb,
                                           self.Zeroing_data)
        print("\nNoise evidence: {}".format(self.logZnoise))

class RingDownModel(LIGOVirgoModel):

    """
    Parent class for all ringdown models.
    Sets common time prior and likelihood.
    """
    
    def __init__(self,**kwargs):

        super(RingDownModel,self).__init__(**kwargs)
        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])
        self.qnm_interpolants = {}
        try:
            self.fixed_params['t'] = self.Config.getfloat("Priors",'fix-t')
        except (configparser.NoOptionError, configparser.NoSectionError):
            if (self.gr_time_prior):
                try:
                    if not(kwargs['injection-approximant']==''): mf_time_prior = kwargs['injection-parameters']['Mf']
                    else:                                        mf_time_prior = kwargs['mf-time-prior']
                    assert (-100 <= self.Config.getfloat("Priors",'t-min') <= 100), "GR prior is currently only compatible with start times of [-100,100]M after the merger. If you know what you are doing, tweak the code to change these hardcoded values."
                    Tmerger = np.array([self.Config.getfloat("Priors",'t-min'),self.Config.getfloat("Priors",'t-max')])*mf_time_prior*lal.MTSUN_SI
                    self.time_prior = [Tmerger[0], Tmerger[1]]
                    print('An estimate of the final mass is being used to select a GR prior on time ([{:.6f}, {:.6f}] Mf after peak): {:.2f}'.format(Tmerger[0], Tmerger[1], mf_time_prior))
                except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    raise Exception("\nIf a GR prior on time is selected, an estimate of the final mass, together with start and end times must be passed.")
            else:
                try:
                    self.time_prior = [self.Config.getfloat("Priors",'t-min'),self.Config.getfloat("Priors",'t-max')]
                except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    self.time_prior = [0.0,0.01]
                    warnings.warn("\nNo time prior given, setting prior to default: [{},{}]".format(self.time_prior[0], self.time_prior[1]))
                if((self.time_prior[0] > 1) or (self.time_prior[1] > 1)):
                    warnings.warn("\nIf no time prior option is passed the time prior is set in units of seconds. You passed a time prior with a value greater than 1s, are you sure you didn't mean to pass it in units of mass?")

        if not('t' in self.fixed_params.keys()):
            assert not((self.time_prior[1]+kwargs['analysis-duration']) > (kwargs['signal-chunksize']/2.) ), "The selected analysis duration plus the upper bound of the time prior, exceeds half of the signal seglen. This will raise an 'index out of bound' error. Please decrease the analysis duration or increase the signal seglen."
            assert not((self.time_prior[1]-self.time_prior[0]) > (kwargs['signal-chunksize'])), "The selected time prior range exceeds the signal seglen. This will raise an 'index out of bound' error. Please decrease the time prior ranges or increase the signal seglen."
            if (self.gr_time_prior):
                if(((self.time_prior[0])/(mf_time_prior*lal.MTSUN_SI) < 20) and (kwargs['template']=='MMRDNP')):
                    warnings.warn("\nYou are using the MMRDNP model outside its calibration domain.")
                elif(((self.time_prior[0])/(mf_time_prior*lal.MTSUN_SI) < 10) and (kwargs['template']=='MMRDNS')):
                    warnings.warn("\nYou are using the MMRDNS model outside its calibration domain.")
        else:
            assert not((self.fixed_params['t']+kwargs['analysis-duration']) > (kwargs['signal-chunksize']/2.)), "The selected analysis duration plus the fixed time, exceeds half of the signal seglen. This will raise an 'index out of bound' error. Please decrease the analysis duration or increase the signal seglen."

    def log_likelihood(self,x):

        if (self.sky_frame == 'detector'):
            
            # ===================================================================================================================#
            # DetFrameToEquatorial makes the sampling on sky position parameters much easier                                     #
            # by parametrizing in a convenient way the ring in the sky in the case of two detectors.                             #
            # In the one detector case there is no advantage in using it, thus we will rely on ra and dec directly,              #
            # while in the three detector case we will use as detectors H1 and L1 because they break the degeneracy more easily. #
            # We need to pass the trigtime of the first detector as input.                                                       #
            # The returned tg is the time at geocenter.                                                                          #
            # ===================================================================================================================#
            
            cos_altitude = get_param_override(self.fixed_params,x,'cos_altitude')
            azimuth      = get_param_override(self.fixed_params,x,'azimuth')

            tg, ra, dec = DetFrameToEquatorial(self.detectors[self.ref_det].lal_detector,
                                               self.detectors[self.non_ref_det].lal_detector,
                                               self.tevent,
                                               np.arccos(cos_altitude),
                                               azimuth)
        elif (self.sky_frame == 'equatorial'):
            ra  = get_param_override(self.fixed_params,x,'ra')
            dec = get_param_override(self.fixed_params,x,'dec')
        else:
            raise ValueError("Invalid option for sky position sampling.")

        psi = get_param_override(self.fixed_params,x,'psi')

        if ('t' in self.fixed_params): t_start = self.fixed_params['t']
        else:                          t_start = x['t0']

        self.time_delay = {'{}_'.format(self.ref_det)+d2: lal.ArrivalTimeDiff(self.detectors[d2].location,lal.cached_detector_by_prefix[self.ref_det].location, ra, dec, self.tgps) for d2 in list(self.detectors.keys())}
        wf_model        = self.get_waveform(x)
        logL            = loglikelihood(self,
                                        x,
                                        wf_model,
                                        ra,
                                        dec,
                                        psi,
                                        t_start,
                                        self.time_delay,
                                        self.ref_det,
                                        self.truncate,
                                        self.duration_n,
                                        self.OnsourceACF,
                                        self.Dirac_comb,
                                        self.Zeroing_data)
        return logL

class IMR_Ringdown_Model(RingDownModel):
    
    """
    Class implementing a non-precessing ringdown model extracted from LAL IMR waveforms.
    """

    def __init__(self, **kwargs):
        super(IMR_Ringdown_Model,self).__init__(**kwargs)

        utils.review_warning()

        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])

        #FIXME: read it from config
        IMR_approx_name = 'LAL-X'

        # ==================================#
        # Initialise model names and bounds #
        # for mandatory parameters.         #
        # ==================================#
        
        print('\n----Prior section - Inspiral Model----\nI\'ll be running with the following prior bounds:\n')

        self.default_bounds = {'m1'     : [20.,100.]     ,
                               'm2'     : [20.,100.]     ,
                               's1z'    : [-0.99,0.99]   ,
                               's2z'    : [-0.99,0.99]   ,
                               'dist'   : [10.,1000.]    ,
                               'cosiota': [-1.0,1.0]     ,
                               'phi'    : [0.0, 2*np.pi] }

        if not('t' in self.fixed_params):
            self.names.append('t0')
            self.bounds.append(self.time_prior)
            print(('{}: [{},{}]'.format('t0'.ljust(len('cosiota')), self.time_prior[0], self.time_prior[1])))

        for name in self.default_bounds.keys():
            try:
                self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
            except(configparser.NoOptionError):
                single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, IMR_approx_name)
                self.names.append('{}'.format(name))
                self.bounds.append(single_bounds)

    def log_prior(self,x):
        
        #Order the masses: m1>m2, same convention as in LAL.
        try:
            if x['m1']<x['m2']: return -np.inf
        except(KeyError):
            pass
        return super(RingDownModel,self).log_prior(x)

    def get_waveform(self,x):

        insp_params = {}
        for name in self.names:
            insp_params[name] = get_param_override(self.fixed_params,x,name)

        return wf.IMR_WF(insp_params['m1'],
                         insp_params['m2'],
                         insp_params['s1z'],
                         insp_params['s2z'],
                         insp_params['dist'],
                         insp_params['cosiota'],
                         insp_params['phi'],
                         insp_params['t0'],
                         self.dt,
                         float(0.0),#FIXME needs to read the start-time
                         float(self.signal_seglen))

class DampedSinusoids(RingDownModel):

    """
    Class implementing a superposition of damped sinusoids as ringdown model.
    Frequency, damping time, amplitude and phase are sampled over for each mode.
    """

    def __init__(self,**kwargs):
        super(DampedSinusoids,self).__init__(**kwargs)

        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])

        # ==================================#
        # Initialise model names and bounds #
        # for mandatory parameters.         #
        # ==================================#
        print('\n----Prior section - Damped Sinusoids Model----\nI\'ll be running with the following prior bounds:\n')

        self.default_bounds = {'logA': [-22.,-20.]     ,
                               'f'   : [20., 1000.]    ,
                               'tau' : [0.0005,0.0500] ,
                               'phi' : [0.0,2.0*np.pi] }

        self.n_modes         = kwargs['n-ds-modes']
        self.mode_ordering   = kwargs['ds-ordering']
        self.amp_flat_prior  = kwargs['ds-amp-flat-prior']

        self.multiple_modes = False
        for pol in self.n_modes.keys():
            if(self.n_modes[pol] > 1): self.multiple_modes = True
        
        #To avoid incompatibilities, all polarisations start at the same time, since t0 is used in likelihood. If needed, change this to allow for different start times.
        if not('t' in self.fixed_params):
            for pol in self.n_modes.keys():
                for i in (list(range(self.n_modes[pol]))):
                    self.names.append('t{}'.format(i))
                    self.bounds.append(self.time_prior)
                    print(('{}{}: [{}, {}]'.format('t', str(i), self.time_prior[0], self.time_prior[1])))
                break

        # Since we are agnostic, all the modes are given the same prior bounds.
        for pol in self.n_modes.keys():
            for i,name in it.product(list(range(self.n_modes[pol])),self.default_bounds.keys()):
                try:
                    self.fixed_params[name+'_{}_{}'.format(pol,i)] = self.Config.getfloat("Priors",'fix-'+name+'_{}_{}'.format(pol,i))
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'Damped-sinusoids', extra_polarisation=[pol,i])
                    if((name=='f') and (single_bounds[0]<kwargs['f-min-bp'])):
                        warnings.warn("The prior upper bound on the frequency is smaller than the smallest frequency allowed by bandpassing. Setting the lower bound of the frequency to the smallest bandpassing frequency={} for consistency.".format(kwargs['f-min-bp']))
                        single_bounds[0] = kwargs['f-min-bp']
                    if((name=='f') and (single_bounds[1]>kwargs['f-max-bp'])):
                        warnings.warn("The prior upper bound on the frequency is higher than the highest frequency allowed by bandpassing. Setting the upper bound of the frequency to the highest bandpassing frequency={} for consistency.".format(kwargs['f-max-bp']))
                        single_bounds[1] = kwargs['f-max-bp']
                    self.names.append('{}_{}_{}'.format(name, pol, i))
                    self.bounds.append(single_bounds)
        if not self.fixed_params:
            print('\nNo parameter was fixed.')
        else:
            print('I\'ll be running with the following fixed parameters:\n')
            for name in self.fixed_params.keys():
                print('{} : {}'.format(name, self.fixed_params[name]))

    def log_prior(self,x):
        
        if(self.amp_flat_prior):
            for pol in self.n_modes.keys():
                if(self.n_modes[pol]>1):
                    for i in range(1,self.n_modes[pol]):
                        logPrior += x['logA_{}_{}'.format(pol,i)]

        if(self.multiple_modes):
            # Order the modes per given polarisation (same as m1>m2 in LAL).
            for pol in self.n_modes.keys():
                if(self.n_modes[pol]>1):
                    for i in range(1,self.n_modes[pol]):
                        if((self.mode_ordering=='freq')  and (x['f_{}_{}'.format(pol,i)]    < x['f_{}_{}'.format(pol,i-1)]   )): return -np.inf
                        elif((self.mode_ordering=='tau') and (x['tau_{}_{}'.format(pol,i)]  < x['tau_{}_{}'.format(pol,i-1)] )): return -np.inf
                        elif((self.mode_ordering=='amp') and (x['logA_{}_{}'.format(pol,i)] < x['logA_{}_{}'.format(pol,i-1)])): return -np.inf

        return super(RingDownModel,self).log_prior(x)

    def get_waveform(self,x):

        params = {}
        for name in self.default_bounds.keys():
            if ('logA' not in name):
                params[name] = {}
                for pol in self.n_modes.keys():
                    params[name][pol] = []
                    for i in range(self.n_modes[pol]):
                        try:    params[name][pol].append(self.fixed_params[name+'_{}_{}'.format(pol,i)])
                        except: params[name][pol].append(x[name+'_{}_{}'.format(pol,i)])
            else:
                params['A'] = {}
                for pol in self.n_modes.keys():
                    params['A'][pol] = []
                    for i in range(self.n_modes[pol]):
                        try:    params['A'][pol].append(10**(self.fixed_params[name+'_{}_{}'.format(pol,i)]))
                        except: params['A'][pol].append(10**(x[name+'_{}_{}'.format(pol,i)]))
        params['t'] = {}
        for pol in self.n_modes.keys():
            params['t'][pol] = []
            for i in range(self.n_modes[pol]):
                try:    params['t'][pol].append(self.fixed_params['t'])
                except: params['t'][pol].append(x['t{}'.format(i)])

        return wf.Damped_sinusoids(params['A']  ,
                                   params['f']  ,
                                   params['tau'],
                                   params['phi'],
                                   params['t']  )


class MorletGaborWavelets(RingDownModel):

    """
    Class implementing a superposition of Morlet-Gabor-wavelets as waveform model.
    Frequency, damping time, amplitude and phase are sampled over for each mode.
    """

    def __init__(self,**kwargs):
        super(MorletGaborWavelets,self).__init__(**kwargs)

        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])

        # ==================================#
        # Initialise model names and bounds #
        # for mandatory parameters.         #
        # ==================================#
        print('\n----Prior section - Morlet-Gabor wavelets Model----\nI\'ll be running with the following prior bounds:\n')

        self.default_bounds = {'logA': [-22., -20.]    ,
                               'f'   : [20., 1000.]    ,
                               'tau' : [0.0005, 0.0500],
                               'phi' : [0.0, 2.0*np.pi]}

        self.n_modes = kwargs['n-ds-modes']

        #To avoid incompatibilities, all polarisations start at the same time, since t0 is used in likelihood. If needed, change this to allow for different start times.

        if not('t' in self.fixed_params):
            for pol in self.n_modes.keys():
                for i in (list(range(self.n_modes[pol]))):
                    self.names.append('t{}'.format(i))
                    self.bounds.append(self.time_prior)
                    print(('{}{}: [{}, {}]'.format('t', str(i), self.time_prior[0], self.time_prior[1])))
                break

        # Since we are agnostic, all the modes are given the same prior bounds.
        for pol in self.n_modes.keys():
            for i,name in it.product(list(range(self.n_modes[pol])),self.default_bounds.keys()):
                try:
                    self.fixed_params[name+'_{}_{}'.format(pol,i)] = self.Config.getfloat("Priors",'fix-'+name+'_{}_{}'.format(pol,i))
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'Morlet-Gabor-wavelets', extra_polarisation=[pol,i])
                    if((name=='f') and (single_bounds[0]<kwargs['f-min-bp'])):
                        warnings.warn("The prior upper bound on the frequency is smaller than the smallest frequency allowed by bandpassing. Setting the lower bound of the frequency to the smallest bandpassing frequency={} for consistency.".format(kwargs['f-min-bp']))
                        single_bounds[0] = kwargs['f-min-bp']
                    if((name=='f') and (single_bounds[1]>kwargs['f-max-bp'])):
                        warnings.warn("The prior upper bound on the frequency is higher than the highest frequency allowed by bandpassing. Setting the upper bound of the frequency to the highest bandpassing frequency={} for consistency.".format(kwargs['f-max-bp']))
                        single_bounds[1] = kwargs['f-max-bp']
                    self.names.append('{}_{}_{}'.format(name, pol, i))
                    self.bounds.append(single_bounds)
        if not self.fixed_params:
            print('\nNo parameter was fixed.')
        else:
            print('I\'ll be running with the following fixed parameters:\n')
            for name in self.fixed_params.keys():
                print('{} : {}'.format(name, self.fixed_params[name]))

    def log_prior(self,x):
        # Order the frequencies per given polarisation (same as m1>m2 in LAL).
        for pol in self.n_modes.keys():
            for i in range(1,self.n_modes[pol]):
                try:
                    if (x['f_{}_{}'.format(pol,i)] < x['f_{}_{}'.format(pol,i-1)]):
                        return -np.inf
                except(KeyError):
                    pass
        return super(RingDownModel,self).log_prior(x)

    def get_waveform(self,x):

        params = {}
        for name in self.default_bounds.keys():
            if ('logA' not in name):
                params[name] = {}
                for pol in self.n_modes.keys():
                    params[name][pol] = []
                    for i in range(self.n_modes[pol]):
                        try:    params[name][pol].append(self.fixed_params[name+'_{}_{}'.format(pol,i)])
                        except: params[name][pol].append(x[name+'_{}_{}'.format(pol,i)])
            else:
                params['A'] = {}
                for pol in self.n_modes.keys():
                    params['A'][pol] = []
                    for i in range(self.n_modes[pol]):
                        try:    params['A'][pol].append(10**(self.fixed_params[name+'_{}_{}'.format(pol,i)]))
                        except: params['A'][pol].append(10**(x[name+'_{}_{}'.format(pol,i)]))
        params['t'] = {}
        for pol in self.n_modes.keys():
            params['t'][pol] = []
            for i in range(self.n_modes[pol]):
                try:    params['t'][pol].append(self.fixed_params['t'])
                except: params['t'][pol].append(x['t{}'.format(i)])

        return wf.Morlet_Gabor_wavelets(params['A']  ,
                                        params['f']  ,
                                        params['tau'],
                                        params['phi'],
                                        params['t']  )

class KerrModel(RingDownModel):

    """
    Class implementing a Kerr waveform as ringdown model.
    Frequencies and damping times of the specified (s,l,m,n) modes are fixed as a function of the mass and spin of the remnant BH.
    Relative amplitudes and phases of the modes are instead free to vary.
    """

    def __init__(self, modes=[(2,2,2,0)], **kwargs):
        super(KerrModel,self).__init__(**kwargs)
        
        self.modes = modes
        print('Running the Kerr model with modes: {}'.format(self.modes))

        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])

        # ==================================#
        # Initialise model names and bounds #
        # for mandatory parameters.         #
        # ==================================#

        self.default_bounds = {'Mf'         : [10.0,500.0]                  ,
                               'af'         : [0.0,0.99]                    ,
                               'logdistance': [np.log(10.0),np.log(10000.0)],
                               'cosiota'    : [-1.0,1.0]                    ,
                               'phi'        : [0.0, 2*np.pi]                }

        # Testing GR options
        self.TGR_params             = []
        self.AreaQuantization       = kwargs['area-quantization']
        self.charge                 = kwargs['charge']
        self.ParSpec                = kwargs['ParSpec']
        self.ParSpec_Dmax_TGR       = kwargs['ParSpec_Dmax_TGR']
        self.ParSpec_Dmax_charge    = kwargs['ParSpec_Dmax_charge']
        self.EsGB                   = kwargs['EsGB']
        self.default_AQ_names       = ['alpha']
        self.default_AQ_bounds      = {'alpha': [0.0,50.0]}
        self.tau_AQ                 = kwargs['tau-AQ']
        self.domega_tgr_modes       = kwargs['domega-tgr-modes']
        self.dtau_tgr_modes         = kwargs['dtau-tgr-modes']
        self.TGR_overtones_ordering = kwargs['TGR-overtones-ordering']

        if(self.EsGB):
            self.EsGB_corrections_dict = {}
            self.EsGB_corrections_dict['domega_220'] = utils.EsGB_corrections('domega_220')
            if(not(self.ParSpec_Dmax_TGR==2) or not(self.ParSpec_Dmax_charge==4)):
                warnings.warn("Einstein-scalar-Gauss-Bonnet option is currently only compatible with p=4 and M_max=2, following reference arXiv:2002.08559. Forcing those values.")
                self.ParSpec_Dmax_TGR      = 2
                self.ParSpec_Dmax_charge   = 4

        # GR options
        self.dist_flat_prior        = kwargs['dist-flat-prior']
        self.coherent_n             = kwargs['coherent-n']
        self.Spheroidal             = kwargs['spheroidal']
        self.qnm_fit                = kwargs['qnm-fit']
        self.amp_non_prec_sym       = kwargs['amp-non-prec-sym']
        self.prior_reweight         = kwargs['prior-reweight']
        self.reference_amplitude    = kwargs['reference-amplitude']
        self.max_amp_ratio          = kwargs['max-Kerr-amp-ratio']
        if(self.max_amp_ratio < 0.0): raise ValueError("The maximum Kerr amplitudes ratio is positive defined. Aborting.")
   
        print('\n----Prior section - Kerr model----\nI\'ll be running with the following prior bounds:\n')
        if not('t' in self.fixed_params):
            self.names.append('t0')
            self.bounds.append(self.time_prior)
            print(('{} : [{},{}]'.format('t0'.ljust(len('cos_altitude')), self.time_prior[0], self.time_prior[1])))

        for name in self.default_bounds.keys():
            if(name=='logdistance' and self.reference_amplitude): continue
            try:
                self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
            except(configparser.NoOptionError):
                single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'Kerr')
                self.names.append('{}'.format(name))
                self.bounds.append(single_bounds)

        print('\n----Prior section - Kerr Model - Testing-GR parameters----\nI\'ll be running with the following prior bounds:\n')
        if ((self.domega_tgr_modes is not None) or (self.dtau_tgr_modes is not None)):
            if (self.domega_tgr_modes is not None):
                for mode in self.domega_tgr_modes:
                    (l,m,n) = mode
                    if not(self.ParSpec):
                        name = 'domega_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('cos_altitude')), bound[0], bound[1])))
                    else:
                        basename = 'domega_{}{}{}'.format(l, m, n)
                        self.TGR_params.append(basename)
                        if not(self.EsGB):
                            for i in range(0,self.ParSpec_Dmax_TGR+1):
                                name  = basename+'_{}'.format(i)
                                bound = [-0.5,0.5]
                                self.names.append(name)
                                self.bounds.append(bound)
                                print(('{} : [{},{}]'.format(name.ljust(len('cos_altitude')), bound[0], bound[1])))

            if (self.dtau_tgr_modes is not None):
                for mode in self.dtau_tgr_modes:
                    (l,m,n) = mode
                    if not(self.ParSpec):
                        name = 'dtau_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('cos_altitude')), bound[0], bound[1])))
                    else:
                        basename = 'dtau_{}{}{}'.format(l, m, n)
                        self.TGR_params.append(basename)
                        if not(self.EsGB):
                            for i in range(0,self.ParSpec_Dmax_TGR+1):
                                name  = basename+'_{}'.format(i)
                                bound = [-0.5,0.5]
                                self.names.append(name)
                                self.bounds.append(bound)
                                print(('{} : [{},{}]'.format(name.ljust(len('cos_altitude')), bound[0], bound[1])))

            if((self.ParSpec) and (self.ParSpec_Dmax_charge > 0)):
                self.names.append('ell')
                self.bounds.append([0,75])#km units
                print(('{} : [{},{}]'.format('ell'.ljust(len('cos_altitude')), 0, 75)))

        elif (self.AreaQuantization):
            utils.review_warning()
            if (self.tau_AQ):
                self.default_AQ_names.append('tau_AQ')
                self.default_AQ_bounds['tau_AQ'] = [0.0005,0.0500]
            for name in self.default_AQ_names:
                try:
                    self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                    print("{} : fixed".format(name.ljust(len('cos_altitude'))))
                except(configparser.NoOptionError):
                    try:
                        single_bounds = [self.Config.getfloat("Priors",name+'-min'),self.Config.getfloat("Priors",name+'-max')]
                    except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                        single_bounds = self.default_AQ_bounds[name]
                    print(('{} : [{},{}]'.format(name.ljust(len('cos_altitude')), single_bounds[0], single_bounds[1])))
                    if (kwargs['inject-area-quantization']):
                        if (not(single_bounds[0] <= kwargs['injection-parameters']['{}'.format(name)] <= single_bounds[1])):
                            print('\n\n######################### WARNING ############################')
                            print('# The {} injected values are outside the prior bounds. #'.format(name))
                            print('##############################################################\n\n')
                    self.names.append('{}'.format(name))
                    self.bounds.append(single_bounds)
        elif (self.charge):
            utils.review_warning()
            charge_single_bounds = [0,1]
            charge_name = 'Q'
            try:
                self.fixed_params[charge_name] = self.Config.getfloat("Priors",'fix-'+charge_name)
                print("{} : {}".format(charge_name.ljust(len('cos_altitude')),self.fixed_params[charge_name]))
            except(configparser.NoOptionError):
                try:
                    single_bounds = [self.Config.getfloat("Priors",charge_name+'-min'),self.Config.getfloat("Priors",charge_name+'-max')]
                except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    single_bounds = charge_single_bounds
                print(('{} : [{},{}]'.format(charge_name.ljust(len('cos_altitude')), single_bounds[0], single_bounds[1])))
                if (kwargs['inject-charge']):
                    if (not(single_bounds[0] <= kwargs['injection-parameters']['Q'] <= single_bounds[1])):
                        print('\n\n######################### WARNING ############################')
                        print('# The {} injected value is outside the prior bounds. #'.format(charge_name))
                        print('##############################################################\n\n')
                self.names.append(charge_name)
                self.bounds.append(single_bounds)
        else:
            print("No TGR parameter was considered.")

        print('\n----Prior section - Kerr Model - Amplitudes and phases----\nI\'ll be running with the following prior bounds:\n')
        amps,phis = self.amp_phi_names()
        for name in np.concatenate((amps, phis), axis=0):
            name = str(name)
            try:
                self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
            except(configparser.NoOptionError):
                try:
                    single_bounds = [self.Config.getfloat("Priors",name+'-min'),self.Config.getfloat("Priors",name+'-max')]
                except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    if ('phi' in name): single_bounds = [0.0, 2*np.pi]
                    elif ('A' in name): single_bounds = [0.0, 50.0]
                    else:               raise ValueError("Kerr amplitudes section: you tried to fix an unknown parameter.")
                self.names.append(name)
                self.bounds.append(single_bounds)
                print(('{} : [{}, {}]'.format(name.ljust(len('cos_altitude')), single_bounds[0], single_bounds[1])))
        print('\n----Prior section - Kerr Model - Fixed parameters----')
        if not self.fixed_params:
            print('\nNo parameter was fixed.')
        else:
            print('I\'ll be running with the following fixed parameters:\n')
            for name in self.fixed_params.keys():
                print('{} : {}'.format(name.ljust(len('cos_altitude')), self.fixed_params[name]))

        #TODO: optimize/generalize the following piece of code
        if (self.prior_reweight):
        # Read in the simulated events and create spline interpolants for the Mf, af, A2220 priors
            utils.review_warning()
            from scipy.interpolate import UnivariateSpline
            print('\n----Prior section - Reweighting the priors for a random population of injections----')
            try:
                par_file = 'ringdown/random_parameters_interpolation.txt'
                if not ('Mf' in self.fixed_params.keys()):
                    print("\nReweighting the prior for Mf...")
                    PYRING_PREFIX = utils.set_prefix()
                    masses_interp = np.genfromtxt(os.path.join(PYRING_PREFIX, par_file), names=True)['Mf']
                    m = np.histogram(masses_interp, bins=32, density=True)
                    bins_m = 0.5*(m[1][1:]+m[1][:-1])
                    self.spline_interpolant_mass = UnivariateSpline(bins_m,m[0],k=1,ext=1, s=0)
                if not ('af' in self.fixed_params.keys()):
                    print("\nReweighting the prior for af...")
                    PYRING_PREFIX = utils.set_prefix()
                    spins_interp = np.genfromtxt(os.path.join(PYRING_PREFIX, par_file), names=True)['af']
                    s = np.histogram(spins_interp, bins=32, density=True)
                    bins_s = 0.5*(s[1][1:]+s[1][:-1])
                    self.spline_interpolant_spin = UnivariateSpline(bins_s,s[0],k=1,ext=1, s=0)
                if not ('A2220' in self.fixed_params.keys()):
                    print("\nReweighting the prior for A2220...")
                    PYRING_PREFIX = utils.set_prefix()
                    ampl_interp = np.genfromtxt(os.path.join(PYRING_PREFIX, par_file), names=True)['amplitude']
                    a = np.histogram(ampl_interp, bins=32, density=True)
                    bins_a = 0.5*(a[1][1:]+a[1][:-1])
                    self.spline_interpolant_ampl = UnivariateSpline(bins_a,a[0],k=1,ext=1, s=0)
            except:
                warnings.warn("\nPrior reweight failed with error: {}.\nA random_parameters_interpolation file must be passed.".format(traceback.print_exc()))

        if(kwargs['qnm-fit'] == 0):
            for (s,l,m,n) in self.modes:
                if(self.charge): interpolate_freq, interpolate_tau = utils.qnm_interpolate_KN(s,l,m,n)
                else:            interpolate_freq, interpolate_tau = utils.qnm_interpolate(s,l,m,n)
                self.qnm_interpolants[(s,l,m,n)]  = {'freq': interpolate_freq, 'tau': interpolate_tau}

    def log_prior(self,x):
        logPrior = 0

        if('logdistance' in self.names):
            if(self.dist_flat_prior): logPrior    += x['logdistance']
            else:                     logPrior    += 3.0*x['logdistance'] #Assume uniform comoving density, hence p(D|I)~D^2 --> p(log(D)|I)~D^3
        
    
        #If requested by the user, impose a hierarchy on the amplitudes. Higher modes cannot have an amplitude bigger than the one of the l=m=2, n=0. Does not apply to overtones.
        if(not(self.max_amp_ratio==0.0) and (('A2220' in self.names) or ('A2220_1' in self.names))):
            for (s,l,m,n) in self.modes:
                if(l==2 and m==2): continue
                else:
                    if(self.amp_non_prec_sym):
                        if(x['A{}{}{}{}'.format(s,l,m,n)]   > self.max_amp_ratio * x['A2220']  ): return -np.inf
                    else:
                        if(x['A{}{}{}{}_1'.format(s,l,m,n)] > self.max_amp_ratio * x['A2220_1']): return -np.inf
                        if(x['A{}{}{}{}_2'.format(s,l,m,n)] > self.max_amp_ratio * x['A2220_2']): return -np.inf
                
        if (self.prior_reweight):
            utils.review_warning()
            if not ('Mf' in self.fixed_params.keys()):      logPrior += np.log(self.spline_interpolant_mass(x['Mf']))
            if not ('af' in self.fixed_params.keys()):      logPrior += np.log(self.spline_interpolant_spin(x['af']))
            if not ('A2220_1' in self.fixed_params.keys()): logPrior += np.log(self.spline_interpolant_ampl(x['A2220_1']))
            if not ('A2220_2' in self.fixed_params.keys()): logPrior += np.log(self.spline_interpolant_ampl(x['A2220_2']))

        # You shall not break the Cosmic Censorship Conjecture.
        if(self.charge):
            af_tmp = get_param_override(self.fixed_params,x,'af')
            Q_tmp  = get_param_override(self.fixed_params,x,'Q')

            if not(af_tmp**2 + Q_tmp**2 < 0.99): return -np.inf

        # Implement an ordering of the modes when testing GR using overtones. This is not imposing the GR modes structure to the template, since all possible template values can still be reached by shifting (Mf,af), it is just preventing that a given mode in the data can be latched upon by different modes in the template.
        if((self.domega_tgr_modes is not None) and (self.dtau_tgr_modes is not None) and not(self.TGR_overtones_ordering=='Unordered')):
            # The fundamental mode is defined to be the one with the largest damping time OR largest frequency.
            if(self.TGR_overtones_ordering=='freq'):
                for mode in self.domega_tgr_modes:
                    (l,m,n)   = mode
                    next_mode = (2,l,m,n+1)
                    # If higher overtones are included, check that the mode ordering is not broken by these higher overtones.
                    if(next_mode in self.modes):
                        freq_eff              = wf.QNM_fit(l,m,  n).f(x['Mf'], x['af'])*(1.0+x['domega_{}{}{}'.format(l, m,   n)])
                        try:    freq_eff_next = wf.QNM_fit(l,m,n+1).f(x['Mf'], x['af'])*(1.0+x['domega_{}{}{}'.format(l, m, n+1)])
                        except: freq_eff_next = wf.QNM_fit(l,m,n+1).f(x['Mf'], x['af'])
                        if(freq_eff < freq_eff_next): return -np.inf
                    # Here we are supposing that all the lower overtones wrt a given n are included (except for the n=0 of course) and check for mode ordering compared to lower overtones.
                    if(n>0):
                        freq_eff              = wf.QNM_fit(l,m,  n).f(x['Mf'], x['af'])*(1.0+x['domega_{}{}{}'.format(l, m,   n)])
                        try:    freq_eff_prev = wf.QNM_fit(l,m,n-1).f(x['Mf'], x['af'])*(1.0+x['domega_{}{}{}'.format(l, m, n-1)])
                        except: freq_eff_prev = wf.QNM_fit(l,m,n-1).f(x['Mf'], x['af'])
                        if(freq_eff_prev < freq_eff): return -np.inf
            elif(self.TGR_overtones_ordering=='tau'):
                for mode in self.dtau_tgr_modes:
                    (l,m,n)   = mode
                    next_mode = (2,l,m,n+1)
                    # If higher overtones are included, check that the mode ordering is not broken by these higher overtones.
                    if(next_mode in self.modes):
                        tau_eff              = wf.QNM_fit(l,m,  n).tau(x['Mf'], x['af'])*(1.0+x['dtau_{}{}{}'.format(l, m,   n)])
                        try:    tau_eff_next = wf.QNM_fit(l,m,n+1).tau(x['Mf'], x['af'])*(1.0+x['dtau_{}{}{}'.format(l, m, n+1)])
                        except: tau_eff_next = wf.QNM_fit(l,m,n+1).tau(x['Mf'], x['af'])
                        if(tau_eff_next > tau_eff): return -np.inf
                    # Here we are supposing that all the lower overtones wrt a given n are included (except for the n=0 of course) and check for mode ordering compared to lower overtones.
                    if(n>0):
                        tau_eff              = wf.QNM_fit(l,m,  n).tau(x['Mf'], x['af'])*(1.0+x['dtau_{}{}{}'.format(l, m,   n)])
                        try:    tau_eff_prev = wf.QNM_fit(l,m,n-1).tau(x['Mf'], x['af'])*(1.0+x['dtau_{}{}{}'.format(l, m, n-1)])
                        except: tau_eff_prev = wf.QNM_fit(l,m,n-1).tau(x['Mf'], x['af'])
                        if(tau_eff_prev < tau_eff): return -np.inf
        return super(KerrModel,self).log_prior(x)+logPrior

    def amp_phi_names(self):
        amps = []
        phis = []
        for (s,l,m,n) in self.modes:
            if(self.amp_non_prec_sym):
                amps.append('A'+self.modename(s,l,m,n))
            else:
                amps.append('A'+self.modename(s,l,m,n)+'_1')
                amps.append('A'+self.modename(s,l,m,n)+'_2')
        if not self.coherent_n:
            for (s,l,m,n) in self.modes:
                if(self.amp_non_prec_sym):
                    phis.append('phi'+self.modename(s,l,m,n))
                else:
                    phis.append('phi'+self.modename(s,l,m,n)+'_1')
                    phis.append('phi'+self.modename(s,l,m,n)+'_2')
        else:
            # For coherent n modes, only set for l,m
            for (s,l,m,n) in self.modes:
                name='phi{}{}{}'.format(s,l,m)
                if name not in phis:
                    phis.append(name)
        return amps, phis

    @staticmethod
    def modename(s,l,m,n):
        """
        Returns "slmn"
        """
        return "{}{}{}{}".format(s,l,m,n)

    def get_cplx_amp(self,x,s,l,m,n):
        name = self.modename(s,l,m,n)
        if(self.amp_non_prec_sym):
            amp = get_param_override(self.fixed_params,x,'A'+name)
            if not self.coherent_n:
                phi = get_param_override(self.fixed_params,x,'phi'+name)
            else:
                phi = get_param_override(self.fixed_params,x,'phi{}{}{}'.format(s,l,m))
            amp *= np.exp(1j*phi)
            return amp
        else:
            amp_1  = get_param_override(self.fixed_params,x,'A'  +name+'_1')
            phi_1  = get_param_override(self.fixed_params,x,'phi'+name+'_1')
            amp_2  = get_param_override(self.fixed_params,x,'A'  +name+'_2')
            phi_2  = get_param_override(self.fixed_params,x,'phi'+name+'_2')
            amp_1 *= np.exp(1j*phi_1)
            amp_2 *= np.exp(1j*phi_2)
            return (amp_1, amp_2)

    def get_waveform(self,x):

        amps           = {}
        TGR_parameters = {}

        # Build the amplitude structure.
        for mode in self.modes:
            s,l,m,n    = mode
            amps[mode] = self.get_cplx_amp(x,s,l,m,n)

        if(self.AreaQuantization):
            utils.review_warning()
            alpha_tmp = get_param_override(self.fixed_params,x, 'alpha')
            TGR_parameters['alpha'] = alpha_tmp
            if(self.tau_AQ):
                tau_AQ_tmp = get_param_override(self.fixed_params,x, 'tau_AQ')
                TGR_parameters['tau_AQ'] = tau_AQ_tmp
        elif(self.charge):
            TGR_parameters['Q'] = get_param_override(self.fixed_params,x, 'Q')
        else:
            if not(self.ParSpec):
                for name in self.TGR_params:
                    TGR_parameters[name] = x[name]
            else:
                if (self.ParSpec_Dmax_charge > 0):
                    z = ((np.exp(x['logdistance'])*lal.PC_SI*1e6)/lal.C_SI)*lal.H0_SI
                    # ell is measured in km
                    TGR_parameters['gamma'] = ((ell_units_factor*x['ell']*(1+z))/x['Mf'])**(self.ParSpec_Dmax_charge)
                else:
                    TGR_parameters['gamma'] = 1.0
                # In this case, TGR_parameters[name] will be an array with all the spin expansion coefficients for a given mode.
                if not(self.EsGB):
                    for name in self.TGR_params:
                        TGR_parameters[name] = []
                        for i in range(self.ParSpec_Dmax_TGR+1):
                            TGR_parameters[name].append(x[name+'_{}'.format(i)])
                        TGR_parameters[name] = np.array(TGR_parameters[name])
                else:
                    for name in self.TGR_params:
                        TGR_parameters[name] = np.array(self.EsGB_corrections_dict[name])

        Kerr_params = {}
        for name in (self.default_bounds.keys()):
            if(name=='logdistance' and self.reference_amplitude): Kerr_params[name] = 0.0
            else:                                                 Kerr_params[name] = get_param_override(self.fixed_params,x,name)
        try:    Kerr_params['t0'] = self.fixed_params['t']
        except: Kerr_params['t0'] = x['t0']

        return wf.KerrBH(Kerr_params['t0'],
                         Kerr_params['Mf'],
                         Kerr_params['af'],
                         amps,
                         np.exp(Kerr_params['logdistance']),
                         np.arccos(Kerr_params['cosiota']),
                         Kerr_params['phi'],
                         TGR_parameters,
                         reference_amplitude = self.reference_amplitude,
                         geom                = 0,
                         qnm_fit             = self.qnm_fit,
                         interpolants        = self.qnm_interpolants,
                         Spheroidal          = self.Spheroidal,
                         amp_non_prec_sym    = self.amp_non_prec_sym,
                         AreaQuantization    = self.AreaQuantization,
                         ParSpec             = self.ParSpec,
                         charge              = self.charge)


class MMRDNSModel(RingDownModel):

        """
        Class implementing the MMRDNS waveform as ringdown model (valid for non-spinning progenitors).
        Frequencies and damping times of the specified (l,m,n) modes are fixed as a function of the mass and spin of the remnant BH.
        Relative amplitudes and phases are fixed as a function of the symmetric mass ratio.
        Reference: https://arxiv.org/pdf/1404.3197.pdf
        """

        def __init__(self, **kwargs):
            super(MMRDNSModel,self).__init__(**kwargs)

            utils.review_warning()

            self.Config = configparser.ConfigParser()
            self.Config.read(kwargs['config-file'])
            print('\n----Prior section - MMRDNS Model----\nI\'ll be running with the following prior bounds:\n')
            self.Spheroidal   = kwargs['spheroidal']
            self.qnm_fit      = kwargs['qnm-fit']
            self.single_mode  = kwargs['single-mode']
            self.tensor_index = 2
            self.TGR_params   = []
            #Syntax: [(s,l,m,n)]
            self.modes =  [(2,2,0), (2,2,1), (2,1,0), (3,3,0), (3,3,1), (3,2,0), (4,4,0), (4,3,0), (5,5,0)]
            
            print('\n----Prior section - MMRDNS Model----\nI\'ll be running with the following prior bounds:\n')
            # ==================================#
            # Initialise model names and bounds #
            # for mandatory parameters.         #
            # ==================================#

            self.default_bounds = {'Mf'         : [10,500]                      ,
                                   'af'         : [0.0,0.99]                    ,
                                   'eta'        : [0.0, 0.25]                   ,
                                   'logdistance': [np.log(10.0),np.log(10000.0)],
                                   'cosiota'    : [-1,1]                        ,
                                   'phi'        : [0.0,2*np.pi]                 }

            if not('t' in self.fixed_params):
                self.names.append('t0')
                self.bounds.append(self.time_prior)
                print(('{}: [{}, {}]'.format('t0'.ljust(len('logdistance')), self.time_prior[0], self.time_prior[1])))

            for name in self.default_bounds.keys():
                try:
                    self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'MMRDNS')
                    self.names.append('{}'.format(name))
                    self.bounds.append(single_bounds)

            print('\n----Prior section - MMRDNS Model - Fixed parameters----')
            if not self.fixed_params:
                print('\nNo parameter was fixed.')
            else:
                print('I\'ll be running with the following fixed parameters:\n')
                for name in self.fixed_params.keys():
                    print('{} : {}'.format(name.ljust(len('cos_altitude')), self.fixed_params[name]))

            print('\n----Prior section - MMRDNS Model - Testing-GR parameters----\nI\'ll be running with the following prior bounds:\n')
            if ((kwargs['domega-tgr-modes'] is not None) or (kwargs['dtau-tgr-modes'] is not None)):
                if (kwargs['domega-tgr-modes'] is not None):
                    for mode in kwargs['domega-tgr-modes']:
                        (l,m,n) = mode
                        name  = 'domega_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
                if (kwargs['dtau-tgr-modes'] is not None):
                    for mode in kwargs['dtau-tgr-modes']:
                        (l,m,n) = mode
                        name  = 'dtau_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
            else:
                print("No TGR parameter was considered.")

            if(self.qnm_fit == 0):
                for (l,m,n) in self.modes:
                    interpolate_freq, interpolate_tau = utils.qnm_interpolate(2,l,m,n)
                    self.qnm_interpolants[(2,l,m,n)]  = {'freq': interpolate_freq, 'tau': interpolate_tau}
            else:
                warnings.warn("\nNo interpolant selected, running MMRDNS without the (5,5,0) mode. If you wish to turn on this mode, please pass the option: 'qnm-fit=0'.")

        def log_prior(self,x):
            logPrior = 0
            if ('logdistance' in self.names):
                logPrior    += 3.0*x['logdistance']
            return super(MMRDNSModel,self).log_prior(x)+logPrior

        def get_waveform(self,x):

            MMRDNS_params = {}
            for name in (self.default_bounds.keys()):
                MMRDNS_params[name] = get_param_override(self.fixed_params,x,name)

            try:    MMRDNS_params['t0'] = self.fixed_params['t']
            except: MMRDNS_params['t0'] = x['t0']

            TGR_parameters = {}
            for name in self.TGR_params:
                TGR_parameters[name] = x[name]

            if (self.single_mode is not None):
                single_mode_flag = 1
                single_mode_l, single_mode_m = self.single_mode[0]

            else:
                single_mode_flag = 0
                single_mode_l, single_mode_m = (0,0)

            return wf.MMRDNS(MMRDNS_params['t0']                  ,
                             MMRDNS_params['Mf']                  ,
                             MMRDNS_params['af']                  ,
                             MMRDNS_params['eta']                 ,
                             np.exp(MMRDNS_params['logdistance']) ,
                             np.arccos(MMRDNS_params['cosiota'])  ,
                             MMRDNS_params['phi']                 ,
                             TGR_parameters                       ,
                             single_l     = single_mode_l         ,
                             single_m     = single_mode_m         ,
                             single_n     = 0                     ,
                             single_mode  = single_mode_flag      ,
                             Spheroidal   = self.Spheroidal       ,
                             interpolants = self.qnm_interpolants ,
                             qnm_fit      = self.qnm_fit          )

class MMRDNPModel(RingDownModel):

        """
        Class implementing the MMRDNP waveform as ringdown model (valid for spinning, non-precessing progenitors).
        Reference: https://arxiv.org/pdf/1801.08208.pdf
        Technical notes: https://github.com/llondon6/kerr_public/blob/master/notes/ns/mmrd.pdf
        """

        def __init__(self, **kwargs):
            super(MMRDNPModel,self).__init__(**kwargs)

            self.single_mode = kwargs['single-mode']
            self.Config = configparser.ConfigParser()
            self.Config.read(kwargs['config-file'])
            self.TGR_params = []
            self.qnm_fit = kwargs['qnm-fit']
            #Syntax: [(l,m,n)]
            self.modes = [(2,2,0),(2,1,0),(3,3,0),(3,2,0),(4,4,0),(4,3,0)] + [(2,-2,0),(2,-1,0),(3,-3,0),(3,-2,0),(4,-4,0),(4,-3,0)]

            print('\n----Prior section - MMRDNP Model----\nI\'ll be running with the following prior bounds:\n')
            # ==================================#
            # Initialise model names and bounds #
            # for mandatory parameters.         #
            # ==================================#

            self.default_bounds = {'m1'          : [10,250]                      ,
                                   'm2'          : [10,250]                      ,
                                   'chi1'        : [-0.99,0.99]                  ,
                                   'chi2'        : [-0.99,0.99]                  ,
                                   'logdistance' : [np.log(10.0),np.log(10000.0)],
                                   'cosiota'     : [-1,1]                        ,
                                   'phi'         : [0.0,2*np.pi]                 }

            if not('t' in self.fixed_params):
                self.names.append('t0')
                self.bounds.append(self.time_prior)
                print(('{}: [{}, {}]'.format('t0'.ljust(len('logdistance')), self.time_prior[0], self.time_prior[1])))

            for name in self.default_bounds.keys():
                try:
                    self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'MMRDNP')
                    self.names.append('{}'.format(name))
                    self.bounds.append(single_bounds)

            print('\n----Prior section - MMRDNP Model - Fixed parameters----')
            if not self.fixed_params:
                print('\nNo parameter was fixed.')
            else:
                print('I\'ll be running with the following fixed parameters:\n')
                for name in self.fixed_params.keys():
                    print('{} : {}'.format(name.ljust(len('cos_altitude')), self.fixed_params[name]))

            print('\n----Prior section - MMRDNP Model - Testing-GR parameters----\nI\'ll be running with the following prior bounds:\n')
            if ((kwargs['domega-tgr-modes'] is not None) or (kwargs['dtau-tgr-modes'] is not None)):
                if (kwargs['domega-tgr-modes'] is not None):
                    for mode in kwargs['domega-tgr-modes']:
                        (l,m,n) = mode
                        name = 'domega_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
                if (kwargs['dtau-tgr-modes'] is not None):
                    for mode in kwargs['dtau-tgr-modes']:
                        (l,m,n) = mode
                        name = 'dtau_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
            else:
                print("No TGR parameter was considered.")

            if(self.qnm_fit == 0):
                for (l,m,n) in self.modes:
                    interpolate_freq, interpolate_tau = utils.qnm_interpolate(2,l,m,n)
                    self.qnm_interpolants[(2,l,m,n)]  = {'freq': interpolate_freq, 'tau': interpolate_tau}
                    interpolate_freq_negm, interpolate_tau_negm = utils.qnm_interpolate(2,l,-m,n)
                    self.qnm_interpolants[(2,l,-m,n)]  = {'freq': interpolate_freq_negm, 'tau': interpolate_tau_negm}

        def log_prior(self,x):
            logPrior = 0
            if ('logdistance' in self.names):
                logPrior    += 3.0*x['logdistance']
            return super(MMRDNPModel,self).log_prior(x)+logPrior

        def get_waveform(self,x):

            MMRDNP_params = {}
            for name in (self.default_bounds.keys()):
                MMRDNP_params[name] = get_param_override(self.fixed_params,x,name)

            try:    MMRDNP_params['t0'] = self.fixed_params['t']
            except: MMRDNP_params['t0'] = x['t0']

            TGR_parameters = {}
            for name in self.TGR_params:
                TGR_parameters[name] = x[name]

            if (self.single_mode is not None):
                single_mode_flag = 1
                single_mode_l, single_mode_m = self.single_mode[0]

            else:
                single_mode_flag = 0
                single_mode_l, single_mode_m = (0,0)

            # Adapt to final state fits conventions
            if(MMRDNP_params['chi1'] < 0): tilt1_fit = np.pi
            else: tilt1_fit = 0.0
            if(MMRDNP_params['chi2'] < 0): tilt2_fit = np.pi
            else: tilt2_fit = 0.0
            chi1_fit  = np.abs(MMRDNP_params['chi1'])
            chi2_fit  = np.abs(MMRDNP_params['chi2'])
            MMRDNP_params['Mf']   = bbh_final_mass_projected_spins(MMRDNP_params['m1'], MMRDNP_params['m2'], chi1_fit, chi2_fit, tilt1_fit, tilt2_fit, 'UIB2016')
            MMRDNP_params['af']   = bbh_final_spin_projected_spins(MMRDNP_params['m1'], MMRDNP_params['m2'], chi1_fit, chi2_fit, tilt1_fit, tilt2_fit, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)

            MMRDNP_params['Mi']   = MMRDNP_params['m1'] + MMRDNP_params['m2']
            MMRDNP_params['eta']  = (MMRDNP_params['m1']*MMRDNP_params['m2'])/(MMRDNP_params['Mi'])**2
            MMRDNP_params['chis'] = (MMRDNP_params['m1']*MMRDNP_params['chi1'] + MMRDNP_params['m2']*MMRDNP_params['chi2'])/(MMRDNP_params['Mi'])
            MMRDNP_params['chia'] = (MMRDNP_params['m1']*MMRDNP_params['chi1'] - MMRDNP_params['m2']*MMRDNP_params['chi2'])/(MMRDNP_params['Mi'])

            return wf.MMRDNP(MMRDNP_params['t0']                  ,
                             MMRDNP_params['Mf']                  ,
                             MMRDNP_params['af']                  ,
                             MMRDNP_params['Mi']                  ,
                             MMRDNP_params['eta']                 ,
                             MMRDNP_params['chis']                ,
                             MMRDNP_params['chia']                ,
                             np.exp(MMRDNP_params['logdistance']) ,
                             np.arccos(MMRDNP_params['cosiota'])  ,
                             MMRDNP_params['phi']                 ,
                             TGR_parameters                       ,
                             single_l     = single_mode_l         ,
                             single_m     = single_mode_m         ,
                             single_mode  = single_mode_flag      ,
                             interpolants = self.qnm_interpolants ,
                             qnm_fit      = self.qnm_fit          )

#OPTIMISEME: parametrise KHS in terms of initial parameters
class KHS_2012Model(RingDownModel):

        """
        Class implementing the KHS_2012 waveform as ringdown model (valid for spinning, non-precessing progenitors).
        Frequencies and damping times of the specified (l,m,n) modes are fixed as a function of the mass and spin of the remnant BH.
        Relative amplitudes and phases are fixed as a function of the symmetric mass ratio and effective spin.
        References: https://arxiv.org/abs/1207.0399, https://arxiv.org/abs/1406.3201
        """

        def __init__(self, **kwargs):
            super(KHS_2012Model,self).__init__(**kwargs)

            utils.review_warning()

            self.Config = configparser.ConfigParser()
            self.Config.read(kwargs['config-file'])
            
            self.single_mode = kwargs['single-mode']
            self.TGR_params  = []

            print('\n----Prior section - KHS_2012 Model----\nI\'ll be running with the following prior bounds:\n')
            # ==================================#
            # Initialise model names and bounds #
            # for mandatory parameters.         #
            # ==================================#

            self.default_bounds = {'Mf'          : [10,500]                      ,
                                   'af'          : [0.0,0.99]                    ,
                                   'eta'         : [0.0, 0.25]                   ,
                                   'chi_eff'     : [-1.0, 1.0]                   ,
                                   'logdistance' : [np.log(10.0),np.log(10000.0)],
                                   'cosiota'     : [-1,1]                        ,
                                   'phi'         : [0.0,2*np.pi]                 }

            if not('t' in self.fixed_params):
                self.names.append('t0')
                self.bounds.append(self.time_prior)
                print(('{}: [{}, {}]'.format('t0'.ljust(len('logdistance')), self.time_prior[0], self.time_prior[1])))

            for name in self.default_bounds.keys():
                try:
                    self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'KHS_2012')
                    self.names.append('{}'.format(name))
                    self.bounds.append(single_bounds)

            print('\n----Prior section - KHS_2012 Model - Fixed parameters----')
            if not self.fixed_params:
                print('\nNo parameter was fixed.')
            else:
                print('I\'ll be running with the following fixed parameters:\n')
                for name in self.fixed_params.keys():
                    print('{} : {}'.format(name.ljust(len('cos_altitude')), self.fixed_params[name]))

            print('\n----Prior section - KHS_2012 Model - Testing-GR parameters----\nI\'ll be running with the following prior bounds:\n')
            if ((kwargs['domega-tgr-modes'] is not None) or (kwargs['dtau-tgr-modes'] is not None)):
                if (kwargs['domega-tgr-modes'] is not None):
                    for mode in kwargs['domega-tgr-modes']:
                        (l,m,n) = mode
                        name = 'domega_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
                if (kwargs['dtau-tgr-modes'] is not None):
                    for mode in kwargs['dtau-tgr-modes']:
                        (l,m,n) = mode
                        name = 'dtau_{}{}{}'.format(l, m, n)
                        bound = [-1.0,1.0]
                        self.names.append(name)
                        self.bounds.append(bound)
                        self.TGR_params.append(name)
                        print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
            else:
                print("No TGR parameter was considered.")


        def log_prior(self,x):
            logPrior = 0
            if ('logdistance' in self.names):
                logPrior    += 3.0*x['logdistance']
            return super(KHS_2012Model,self).log_prior(x)+logPrior

        def get_waveform(self,x):

            KHS_2012_params = {}
            for name in (self.default_bounds.keys()):
                KHS_2012_params[name] = get_param_override(self.fixed_params,x,name)

            try:    KHS_2012_params['t0'] = self.fixed_params['t']
            except: KHS_2012_params['t0'] = x['t0']

            TGR_parameters = {}
            for name in self.TGR_params:
                TGR_parameters[name] = x[name]

            if (self.single_mode is not None):
                single_mode_flag = 1
                single_mode_l, single_mode_m = self.single_mode[0]

            else:
                single_mode_flag = 0
                single_mode_l, single_mode_m = (0,0)

            return wf.KHS_2012(KHS_2012_params['t0']                 ,
                               KHS_2012_params['Mf']                 ,
                               KHS_2012_params['af']                 ,
                               KHS_2012_params['eta']                ,
                               KHS_2012_params['chi_eff']            ,
                               np.exp(KHS_2012_params['logdistance']),
                               np.arccos(KHS_2012_params['cosiota']) ,
                               KHS_2012_params['phi']                ,
                               TGR_parameters                        ,
                               single_l    = single_mode_l           ,
                               single_m    = single_mode_m           ,
                               single_mode = single_mode_flag        )

class TEOBPMModel(RingDownModel):

    """
    Class implementing the EOBPM waveform as post-merger model (valid for non-precessing progenitors).
    References: arXiv: 1406.0401, 1606.03952, 2001.09082.
    """

    def __init__(self, **kwargs):
        super(TEOBPMModel,self).__init__(**kwargs)

        utils.review_warning()
        self.Config = configparser.ConfigParser()
        self.Config.read(kwargs['config-file'])
        
        self.single_mode = kwargs['single-mode']
        self.TGR_params  = []

        if(self.single_mode is not None):
            self.multipoles = [self.single_mode[0]]
        else:
            # These are the multipoles we can trust for sure (also sprache Rossella)
            self.multipoles = [(2,2), (3,3), (4,4), (5,5)]
            # These are the multipoles that are present, but must be tested with care, especially for negative high spins
            #self.multipoles = [(2,2), (2,1), (3,3), (3,2), (3,1), (4,4), (4,3), (4,2), (4,1), (5,5)]
            
        print('\n----Prior section TEOBPM model----\nI\'ll be running with the following prior bounds:\n')

        # ==================================#
        # Initialise model names and bounds #
        # for mandatory parameters.         #
        # ==================================#
        
        # Spin and q ranges from https://arxiv.org/abs/2011.01958
        self.default_bounds = {'m1'          : [10,200]                      ,
                               'm2'          : [10,200]                      ,
                               'chi1'        : [-0.8,0.95]                   ,
                               'chi2'        : [-0.8,0.95]                   ,
                               'phase'       : [0,2*np.pi]                   ,
                               'logdistance' : [np.log(10.0),np.log(1000.0)] ,
                               'cosiota'     : [-1,1]                        ,
                               'phi'         : [0,2*np.pi]                   }

        if not('t' in self.fixed_params):
            self.names.append('t0')
            self.bounds.append(self.time_prior)
            print('{}: [{}, {}]'.format('t0'.ljust(len('logdistance')), self.time_prior[0], self.time_prior[1]))

        for name in self.default_bounds.keys():
            
            if(name=='phase'):
                # FIXME: Temporary solution setting the prior equal for all merger phases, phases should be fit.
                for multipole in self.multipoles:
                    (l,m) = multipole
                    phase_name = 'phase_{}{}'.format(l,m)
                    try:
                        self.fixed_params[phase_name] = self.Config.getfloat("Priors",'fix-{}'.format(phase_name))
                    except(configparser.NoOptionError):
                        single_bounds = self.default_bounds[name]
                        print('{} : [{}, {}]'.format(phase_name.ljust(len('logdistance')), single_bounds[0], single_bounds[1]))
                        self.names.append(phase_name)
                        self.bounds.append(single_bounds)
            else:
                try:
                    self.fixed_params[name] = self.Config.getfloat("Priors",'fix-'+name)
                except(configparser.NoOptionError):
                    single_bounds = read_parameter_bounds(self.Config, configparser, kwargs, name, self.default_bounds, 'TEOBResumSPM')
                    self.names.append('{}'.format(name))
                    self.bounds.append(single_bounds)
            
        print('\n----Prior section - TEOBPM Model - Fixed parameters----')
        if not self.fixed_params:
            print('\nNo parameter was fixed.')
        else:
            print('I\'ll be running with the following fixed parameters:\n')
            for name in self.fixed_params.keys():
                print('{}: {}'.format(name.ljust(len('cos_altitude')), self.fixed_params[name]))

        print('\n----Prior section - TEOBPM Model - Testing-GR parameters----\nI\'ll be running with the following prior bounds:\n')
        if ((kwargs['domega-tgr-modes'] is not None) or (kwargs['dtau-tgr-modes'] is not None)):
            if (kwargs['domega-tgr-modes'] is not None):
                for mode in kwargs['domega-tgr-modes']:
                    (l,m,n) = mode
                    name = 'domega_{}{}{}'.format(l, m, n)
                    bound = [-1.0,1.0]
                    self.names.append(name)
                    self.bounds.append(bound)
                    self.TGR_params.append(name)
                    print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
            if (kwargs['dtau-tgr-modes'] is not None):
                for mode in kwargs['dtau-tgr-modes']:
                    (l,m,n) = mode
                    name = 'dtau_{}{}{}'.format(l, m, n)
                    bound = [-1.0,1.0]
                    self.names.append(name)
                    self.bounds.append(bound)
                    self.TGR_params.append(name)
                    print(('{} : [{},{}]'.format(name.ljust(len('domega_000')), bound[0], bound[1])))
        else:
            print("No TGR parameter was considered.")

    def log_prior(self,x):
        
        logPrior = 0
        if ('logdistance' in self.names):
            logPrior    += 3.0*x['logdistance']
        # Swap masses and spins to respect model conventions (m1 is the heaviest BH)
        try:
            if (x['m1']<x['m2']):
                tmp       = x['m1']
                x['m1']   = x['m2']
                x['m2']   = x['m1']
                tmp       = x['chi1']
                x['chi1'] = x['chi2']
                x['chi2'] = x['chi1']
        except(KeyError):
            pass
        
        return super(TEOBPMModel,self).log_prior(x)+logPrior


    def get_waveform(self,x):

        TEOBPM_params, merger_phases = {}, {}
        for name in (self.default_bounds.keys()):
            if(name=='phase'):
                for multipole in self.multipoles:
                    (l,m) = multipole
                    merger_phases[(l,m)] = get_param_override(self.fixed_params,x,'phase_{}{}'.format(l,m))
            else:
                TEOBPM_params[name] = get_param_override(self.fixed_params,x,name)
        try:    TEOBPM_params['t0'] = self.fixed_params['t']
        except: TEOBPM_params['t0'] = x['t0']

        if (self.single_mode is not None):
            single_mode_flag = 1
            single_mode_l, single_mode_m = self.single_mode[0]
        else:
            single_mode_flag = 0
            single_mode_l, single_mode_m = (0,0)

        TGR_parameters = {}
        for name in self.TGR_params:
            TGR_parameters[name] = x[name]
                      
        return wf.TEOBPM(TEOBPM_params['t0']                 ,
                         TEOBPM_params['m1']                 ,
                         TEOBPM_params['m2']                 ,
                         TEOBPM_params['chi1']               ,
                         TEOBPM_params['chi2']               ,
                         merger_phases                       ,
                         np.exp(TEOBPM_params['logdistance']),
                         np.arccos(TEOBPM_params['cosiota']) ,
                         TEOBPM_params['phi']                ,
                         TGR_parameters                      ,
                         single_l    = single_mode_l         ,
                         single_m    = single_mode_m         ,
                         single_mode = single_mode_flag      )



#Description of the package. Printed on stdout if --help option is give.
usage="""\n\n %prog --config-file config.ini\n
Parameter estimation package targeting time-domain ringdown analyses.

Options syntax: type, default values and sections of the configuration
file where each parameter should be passed are declared below.
By convention, booleans are represented by the integers [0,1].
A dot is present at the end of each description line and is not
to be intended as part of the default value.



       ***************************************************
       * Parameters to be passed to the [input] section. *
       ***************************************************

               #==========================================================#
               # Data inputs.                                             #
               # Data reading from file assumes the following convention: #
               # "IFO-frame_type-segment_start_time-segment_duration"     #
               # e.g.: H-H1_GWOSC_4_V1-1126259446-32.txt                  #
               #==========================================================#

               data-H1                  Name of H1 data file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               data-L1                  Name of L1 data file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               data-V1                  Name of LV data file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               ignore-data-filename     Option to ignore naming of data file if loading from disk. Default: False.
               download-data            Option to allow for data fetching through gwpy. If true, a channel name is required for each detector. Default: 0.
               datalen-download         Length (in s) of the data to be downloaded through gwpy. Default: 4096.
               gw-data-find             Option to fetch LVC proprietary data not available through GWPY. Default: 0.
               gw-data-type-H1          Type of the H1.gwf file fetched through gw_data_find. Default: ''.
               gw-data-type-L1          Type of the L1.gwf file fetched through gw_data_find. Default: ''.
               gw-data-type-V1          Type of the V1.gwf file fetched through gw_data_find. Default: ''.
               tag                      Attribute to be used in downloading data from GWOSC. Default: 'CLN'.
               channel-H1               Name of H1 interferometric channel. Defult: 'GWOSC'.
               channel-L1               Name of L1 interferometric channel. Defult: 'GWOSC'.
               channel-V1               Name of V1 interferometric channel. Defult: 'GWOSC'.

               #===============================#
               # Run configuration parameters. #
               #===============================#

               run-type                 Type of run to be launched. Available options: ['full', 'psd-only', 'post-processing']. Default: 'full'.
               output                   Output directory of the run. Default: './default_outdir'.
               run-tag                  Label of the run in the PESummary metafile. Default: outdir.
               screen-output            Option to allow for the stdout to appear on screen. Default: 0.
               pesummary                Option to create a PESummary metafile at the end of the run containing all the needed inputs to completely reproduce the run and the run output. Default: 1.
               
               #==============================================#
               # Detectors, time and sky position parameters. #
               #==============================================#

               trigtime                 Reference time in the reference detector 'ref-det' from which the analysis will start. For ringdown-only injections will be the start of the signal, while IMR injections will be aligned in such a way that the trigtime corresponds to the peak of hp^2 + hc^2. Default: 1126259462.423.
               detectors                Detectors to be used in the run. Default: 'H1,L1'.
               ref-det                  Detector corresponding to the given trigtime. Default: 'H1'.
               sky-frame                Sky-frame reference systems. Valid options: ['equatorial', 'detector', 'default']. Default: 'default'.

               #=========================================#
               # Noise and signal processing parameters. #
               #=========================================#

               acf-H1                     Name of H1 ACF from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               acf-L1                     Name of L1 ACF from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               acf-V1                     Name of V1 ACF from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               psd-H1                     Name of H1 PSD from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               psd-L1                     Name of L1 PSD from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.
               psd-V1                     Name of V1 PSD from file (either path relative to the package data, or to a PYRING_PREFIX or absolute path). Default: ''.

               signal-chunksize           Length (in s) of the chunk that contains the signal. Default: 2.0.
               noise-chunksize            Length (in s) of the chunks used in ACF estimation. Should be equal to signal-chunksize if our standard method is employed (but Max et al. method does not require it). Default: 2.0.
               window-onsource            Option to add a window on the signal chunk. Default: 0.
               window                     Option to add a window on the noise chunk. Default: 1.
               alpha-window               Value setting the rise and decay time of the noise window. Default: 0.1 (same value as LALInference).
               sampling-rate              Inverse of the data time step. Default: 4096.0.
               f-min-bp                   Minimum frequency of the bandpass filter. Default: 20.0.
               f-max-bp                   Maximum frequency of the bandpass filter. Default: 2038.0.
               bandpassing                Option to turn on/off the bandpassing. Default: 1.

               fft-acf                    Option to compute the ACF through an FFT. Default: 1.
               acf-simple-norm            Option to FIXME Default: False.
               no-lognorm                 Option to FIXME Default: False.
               truncate                   Option to computed the likelihood only on data starting at t0. Default: 1.
               analysis-duration          Option used to set seglen (in seconds) if truncating. Default: 0.1.

               zero-noise                 Option to inject a waveform without any detector noise. Default: 0.
               gaussian-noise             Option to generate a strain from a gaussian stochastic process. Available options: ['white', 'coloured', 'None']. Default: None.
               gaussian-noise-seed        Option to fix a random seed for the noise generation. If -1, noise will be different at each iteration. Default: -1.
               gaussian-noise-white-sigma Standard deviation of white gaussian noise. Default: 1e-21.
               
               chisquare-computation      Option to output a chisquare computation on the data. Default: 0.
               non-stationarity-check     Option to perform a simple non-stationarity check on the data. Default: 0.
               onsource-ACF               Option to use the ACF computed on-source. Technically the correct thing to do, but still in testing phase. Default: 0.
               noise-averaging-method     Option to perform the noise averaging using different methods. Available options: ['mean', 'median']. Deafult: 'mean'.
               Dirac-comb                 Option to use as inspiral model the data itself. Sets to 0 all the contributions except for ringdown inside the likelihood. Default: 0.
               Zeroing-data               Option to zero-out the data before the start of the analysis. Sets to 0 all the contributions except for ringdown inside the likelihood, but inserts spurious frequencies in the data (FIXME: implement window to cure this). Default: 0.
               maxent-psd                 Option to use the maximum entropy estimation method to compute the PSD. Valid options: ['average', 'onsource-chunk', 'pre-onsource-chunk', 'post-onsource-chunk']. Default:''.
               PSD-investigation          Option to plot the PSDs from all chunks. Useful to identify localized non-stationarities. Default: 0.

               #=======================#
               # Injection parameters. #
               #=======================#

               injection-approximant    Option to select the waveform approximant to be injected.  Current available options: ['Damped-sinusoids', 'Morlet-Gabor-wavelets', 'Kerr', 'MMRDNS', 'MMRDNP', 'KHS_2012', 'NR', 'LAL-X'where X is any LAL approximant]. If 'NR', requires a PYRING_PREFIX to be set. Default: ''.
               inject-n-ds-modes        Number of scalar, vector and tensor damped sinuoids to be injected for 'Damped-sinusoids' template. Default: '{"s": 0, "v": 0, "t": 1}'.
               inject-area-quantization Option to inject a Kerr waveform with frequencies set by the area quantization proposal in the data. Default: 0.
               inject-charge            Option to inject a Kerr-Newman waveform. Default: 0.
               injection-scaling        Parameter used to scale the distance of the injection. Default: 1.0.
               injection-T              Duration of data segment when performing an injection. Default: 64.0.

               #======================#
               # Waveform parameters. #
               #======================#

               template                 Template to be used in the run. Current available options: ['Damped-sinusoids', 'Kerr', 'MMRDNS', 'MMRDNP', 'KHS_2012', 'TEOBResumSPM']. Default: 'Kerr'.
               single-mode              Option to use a single mode in multi-modal NR waveforms ('MMRDNS', 'MMRDNP', 'KHS_2012', 'TEOBResumSPM'). Example of expected syntax: [(l,m)]. For MMRDNS it fixes the (l,m,0) mode. Default: None.

               #==============================#
               # Damped sinusoids parameters. #
               #==============================#

               n-ds-modes               Number of scalar, vector and tensor damped sinuoids to be used for 'Damped-sinusoids' template. Default: '{"s": 0, "v": 0, "t": 1}'.
               ds-ordering              Sort the modes according to increasing values of this parameter, relevant for damped-sinusoid waveforms. Available options: ['freq', 'tau', 'amp']. Default: 'freq'.
               ds-amp-flat-prior        Option to select a flat prior on the damped-sinusoids amplitude. Default: 0.

               #=====================#
               # Kerr GR parameters. #
               #=====================#

               kerr-modes               Modes to be used in 'Kerr' template. Default: [(2,2,2,0)] (syntax: [(s,l,m,n)]).
               reference-amplitude      Option to set a reference amplitude (e.g. 1E-21) in place of the M_f/D_L waveform prefactor (in geometrised units) since this factor is completely degenerate with modes free amplitudes. Overwrites sampling in distance. Default: 0.0 (not active).
               spheroidal               Option to allow for spheroidal decomposition of the waveform. Default: 0.
               qnm-fit                  Option to use fits for QNM complex frequencies, instead of interpolating numerical relativity data directly. Available only up to n=2 and l=4, for s=2. If 0, requires a PYRING_PREFIX to be set. Default: 1.
               coherent-n               Option to allow for different overtones to be summed up coherently in phase. Default: False.
               amp-non-prec-sym         Option to enforce non-precessing symmetry on Kerr amplitudes. Default: 0.
               max-Kerr-amp-ratio       Option to force amplitudes of modes different than l=m=2 to be smaller than max-Kerr-amp-ratio*A_220. Does not apply to overtones. Default: 0.0

               #============================#
               # Kerr beyond GR parameters. #
               #============================#

               TGR-overtones-ordering   Sort the Kerr modes according to increasing values of this parameter, relevant for Kerr waveforms when including overtones and parametrised deviations. Available options: ['Unordered', 'freq', 'tau']. Default: 'Unordered'.
               domega-tgr-modes         Modes on which to sample on deviation from GR prediction in QNM frequency. Example of expected syntax: [(2,2,0)]. Default: None.
               dtau-tgr-modes           Modes on which to sample on deviation from GR prediction in QNM frequency. Example of expected syntax: [(2,2,0)]. Default: None.
               area-quantization        Option to allow for area-quantization test. Default: 0.
               tau-AQ                   Option to sample on tau in area-quantization test. Default: 0.
               prior-reweight           Option used in area-quantization tests to reweight the prior for injections. Default: 0.
               ParSpec                  Option to sample GR deviations using the parametrised spinning formalism. Default: 0.
               ParSpec_Dmax_TGR         Option to specify the maximum order of the testing GR deviation coefficients in the parametrised spinning expansion. Default: 5.
               ParSpec_Dmax_charge      Option to specify the dimension of the charge in the parametrised spinning expansion. Default: 0.
               EsGB                     Option to specify the Einstein-scalar-Gauss-Bonnet corrections within the ParSpec formalism. Default: 0.
               charge                   Option to allow for the inclusion of charge. Default: 0.

       ****************************************************
       * Parameters to be passed to the [Priors] section. *
       ****************************************************

               #========================#
               # Time prior parameters. #
               #========================#

               gr-time-prior            Option to select a time prior between [X,Y] in units of mf-time-prior. Default: 1.
               dist-flat-prior          Option to select a flat prior on the luminosity distance. Default: 0.
               mf-time-prior            Option to pass a value of the mass used to set the time prior. Default: 0.0.

               #==============================================#
               # Waveform parameters priors and fixed values. #
               #==============================================#

               Prior default bounds can be changed by adding 'param-min=value' or 'param-max=value' to this section.
               Currently for sky position parameters and Kerr modes specific parameters (amplitudes, phases and QNM deviations) it is not possible to change only the lower or upper bound separately, thus the above commands should both be passed (FIXME).
               All sampled parameters can be fixed adding the 'fix-name=value' option.
               The list of available waveforms, waveform parameters and default parameters priors can be accessed through FIXME MISSING.

       **************************************************************
       * Parameters to be passed to the [Sampler settings] section. *
       **************************************************************

               #========================================================#
               # Sampler parameters.                                    #
               # For more info see: https://johnveitch.github.io/cpnest #
               #========================================================#

               verbose                  Option to set the output verbosity of the sampler. Available options: FIXME MISSING. Default: 2.
               poolsize                 Option to set the number of pools in the CPNest algorithm. Default: 128.
               nthreads                 Option to set the number of parallel threads to be used by CPNest. Default: 1.
               nlive                    Option to set the number of live points (main feature controlling the accuracy of the sampling) to be used by CPNest. Default: 1024.
               maxmcmc                  Option to set the number of maximum Markov Chain Monte Carlo steps at each sample (main feature limiting the autocorrelation legth of the samples) to be used by CPNest. Default: 1024.
               seed                     Option to set the random seed to be used by CPNest. Default: 1234.
               resume                   Option to allow CPNest to resume the run after it was killed. Default: 1.

       *******************************************************
       * Parameters to be passed to the [Injection] section. *
       *******************************************************

               inject-modes             Option to select a list of modes to be injected. Example of expected syntax: [(l1,m1), (l2,m2), ...]. Default: None.
               inject-l-modes           Option to select a list of l-modes to be injected. All |m|<l modes will be injected by default. Example of expected syntax: [l1, l2, ...]. Default: None.

               FIXME: MISSING description of injection parameters for the different waveforms.
               
       **************************************************
       * Parameters to be passed to the [Plot] section. *
       **************************************************
       
                imr-samples             File containing the posterior samples from an IMR run to compare against ringdown values in plots. Needs to be either a full posterior in the GWTC-1 format or the marginalised posterior on Mf-af, with two columns and the ['Mf', 'af'] header.

"""


def main():
    execution_time = time.time()
    parser         = OptionParser(usage)
    parser.add_option('--config-file', type='string', metavar = 'config_file', default = None)

    (opts,args) = parser.parse_args()
    config_file = opts.config_file

    if not config_file:
        parser.print_help()
        parser.error('Please specify a config file.')
    if not os.path.exists(config_file):
        parser.error('Config file {} not found.'.format(config_file))
    Config = configparser.ConfigParser()
    Config.read(config_file)

    # ===================================#
    # Deviate stdout and stderr to file. #
    # ===================================#

    try:
        directory = str(Config.get("input",'output'))
    except(KeyError, configparser.NoOptionError):
        directory = 'default_directory'
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        if not(Config.getint("input",'screen-output')):
            sys.stdout = open(os.path.join(directory,'stdout_pyRing.txt'), 'w')
            sys.stderr = open(os.path.join(directory,'stderr_pyRing.txt'), 'w')
        else:
            pass
    except(configparser.NoOptionError):
        sys.stdout = open(os.path.join(directory,'stdout_pyRing.txt'), 'w')
        sys.stderr = open(os.path.join(directory,'stderr_pyRing.txt'), 'w')

    print(('\nReading config file: {}'.format(config_file)))
    print('With sections '+str(Config.sections()))
    print('\n----Input parameters----\nI\'ll be running with the following values:\n')

    # ==================================================#
    # Initialize and read from config input parameters. #
    # ==================================================#

    input_par={
               #==============#
               # Data inputs. #
               #==============#

               'data-H1'                  : '',
               'data-L1'                  : '',
               'data-V1'                  : '',
               'ignore-data-filename'     : 0,
               'download-data'            : 0,
               'datalen-download'         : 4096.,
               'gw-data-find'             : 0,
               'gw-data-type-H1'          : '',
               'gw-data-type-L1'          : '',
               'gw-data-type-V1'          : '',
               'tag'                      : 'CLN',
               'channel-H1'               : 'GWOSC',
               'channel-L1'               : 'GWOSC',
               'channel-V1'               : 'GWOSC',

               #===============================#
               # Run configuration parameters. #
               #===============================#

               'config-file'              : config_file,
               'run-type'                 : 'full', # Valid options: ['full', 'psd-only', 'post-processing']
               'output'                   : './default_outdir',
               'run-tag'                  : '',
               'screen-output'            : 0,
               'pesummary'                : 1,

               #==============================================#
               # Detectors, time and sky position parameters. #
               #==============================================#
               
               'trigtime'                 : float(1126259462.423), #Default GW150914 H1 trigtime, consistent with H1 being the ref detector (GW150914 L1 trigtime is 1126259462.416)
               'detectors'                : 'H1,L1,V1',
               'ref-det'                  : 'H1',
               'sky-frame'                : 'default', # Valid options: ['equatorial', 'detector', 'default']

               #=========================================#
               # Noise and signal processing parameters. #
               #=========================================#

               'acf-H1'                     : '',
               'acf-L1'                     : '',
               'acf-V1'                     : '',
               'psd-H1'                     : '',
               'psd-L1'                     : '',
               'psd-V1'                     : '',

               'signal-chunksize'           : 2.0,
               'noise-chunksize'            : 2.0,
               'window-onsource'            : 0,
               'window'                     : 1,
               'alpha-window'               : 0.1, # Default set to the same value as LALInference.
               'sampling-rate'              : 4096.0,
               'f-min-bp'                   : 20.,
               'f-max-bp'                   : 2038.,
               'bandpassing'                : 1,

               'fft-acf'                    : 1,
               'acf-simple-norm'            : 1,
               'no-lognorm'                 : 0,
               'truncate'                   : 1,
               'analysis-duration'          : 0.1,
               'analysis-duration-n'        : 410,

               'zero-noise'                 : 0,
               'gaussian-noise'             : '',
               'gaussian-noise-seed'        : -1,
               'gaussian-noise-white-sigma' : 1e-21,

               'chisquare-computation'      : 0,
               'non-stationarity-check'     : 0,
               'onsource-ACF'               : 0,
               'noise-averaging-method'     : 'mean',
               'Dirac-comb'                 : 0,
               'Zeroing-data'               : 0,
               'maxent-psd'                 : '', # Valid options: ['average', 'onsource-chunk', 'pre-onsource-chunk', 'post-onsource-chunk']
               'PSD-investigation'          : 0,

               #=======================#
               # Injection parameters. #
               #=======================#

               'injection-parameters'       : None,
               'injection-approximant'      : '', # Current available options: ['Damped-sinusoids', 'Kerr', 'MMRDNS', 'MMRDNP', 'KHS_2012', 'NR', 'LAL-X' where X is any LAL approximant]
               'inject-n-ds-modes'          : {"s": 0, "v": 0, "t": 1},
               'inject-area-quantization'   : 0,
               'inject-charge'              : 0,
               'injection-scaling'          : 1.0,
               'injection-T'                : 64.0,

               #======================#
               # Waveform parameters. #
               #======================#

               'template'                   : 'Kerr', # Current available options: ['Damped-sinusoids', 'Kerr', 'MMRDNS', 'MMRDNP', 'KHS_2012', 'TEOBResumSPM']
               'single-mode'                : None,

               #==============================#
               # Damped sinusoids parameters. #
               #==============================#

               'n-ds-modes'                 : {"s": 0, "v": 0, "t": 1},
               'ds-ordering'                : 'freq',

               #=====================#
               # Kerr GR parameters. #
               #=====================#

               'kerr-modes'                 : [(2,2,2,0)],
               'reference-amplitude'        : 0.0,
               'spheroidal'                 : 0,
               'qnm-fit'                    : 1,
               'coherent-n'                 : 0,
               'amp-non-prec-sym'           : 0,
               'max-Kerr-amp-ratio'         : 0.0,

               #============================#
               # Kerr beyond GR parameters. #
               #============================#

               'TGR-overtones-ordering'     : 'Unordered',
               'domega-tgr-modes'           : None,
               'dtau-tgr-modes'             : None,
               'area-quantization'          : 0,
               'tau-AQ'                     : 0,
               'prior-reweight'             : 0,
               'ParSpec'                    : 0,
               'ParSpec_Dmax_TGR'           : 2,
               'ParSpec_Dmax_charge'        : 0,
               'EsGB'                       : 0,
               'charge'                     : 0,

               #===========================#
               # Default prior parameters. #
               #===========================#

               'gr-time-prior'              : 1,
               'dist-flat-prior'            : 0,
               'ds-amp-flat-prior'          : 0,
               'mf-time-prior'              : 0.0

}

    max_len_keyword = len('gaussian-noise-white-sigma')
    #General input read.
    for key in input_par:
        keytype = type(input_par[key])
        try:
            if ('ds-modes' in key):
                input_par[key] = json.loads(Config.get("input",'{}'.format(key)))
            elif('mode' in key):
                input_par[key]=ast.literal_eval(Config.get("input",key))
            else:
                input_par[key]=keytype(Config.get("input",key))
        except (KeyError, configparser.NoOptionError, TypeError):
            pass
        print(("{name} : {value}".format(name=key.ljust(max_len_keyword), value=input_par[key])))

    if(input_par['run-tag']==''):
        input_par['run-tag']=input_par['output'].split('/')[-1]

    #Set up likelihood specific inputs.
    if(input_par['truncate']):
        assert not(input_par['Dirac-comb'] or input_par['Zeroing-data']), "Running with truncation is incompatible with Dirac comb or zeroing out the data."
        if not(input_par['analysis-duration']):
            raise Exception("Running with the 'truncate' option requires an 'analysis-duration' option to be passed (in seconds).")
        elif((input_par['signal-chunksize']/2.) < input_par['analysis-duration']):
            raise Exception("Analysis duration ({})  must be shorter than half of the signal chunksize ({})".format(input_par['analysis-duration'], input_par['signal-chunksize']/2.))
        else:
            input_par['analysis-duration-n'] = int(input_par['analysis-duration'] * input_par['sampling-rate'])
    print(("{name} : {value}".format(name='analysis-duration-n'.ljust(max_len_keyword), value=input_par['analysis-duration-n'])))

    #Set detector input and check for incompatibilites.
    try:
        assert not(Config.get("input",'trigtime-H1') is not None), "You are running with an old config file. trigtime-H1 is now deprecated in favour of trigtime (of the correspondent ref-det)."
    except(configparser.NoOptionError):
        pass

    input_par['detectors'] = [det for det in (input_par['detectors']).split(',')]
    len_det = len(input_par['detectors'])

    if(input_par['sky-frame'] == 'default'):
        if(len_det > 1): input_par['sky-frame'] = 'detector'
        else:            input_par['sky-frame'] = 'equatorial'
    elif(input_par['sky-frame'] == 'detector'):
        check = None
        try: check = Config.getfloat("Priors","fix-ra")
        except: pass
        try: check = Config.getfloat("Priors","fix-dec")
        except: pass
        assert (check == None), "Fixed sky position parameters are inconsistent with respect to the 'sky-frame = detector' option selected. If you want to fix ra and dec, please pass the 'sky-frame = equatorial' option."
    elif(input_par['sky-frame'] == 'equatorial'):
        check = None
        try: check = Config.getfloat("Priors","fix-azimuth")
        except: pass
        try: check = Config.getfloat("Priors","fix-cos_altitude")
        except: pass
        assert (check == None), "Fixed sky position parameters are inconsistent with respect to the 'sky-frame = equatorial' option selected. If you want to fix azimuth and cos_altitude, please pass the 'sky-frame = detector' option."
    else:
        raise ValueError("Invalid option for sky position sampling.")

    assert not((len_det == 1) and (input_par['sky-frame'] == 'detector')), "You cannot select detector frame using only a single detector. It needs at least two of them. Please select the skyframe 'default' or 'equatorial' option."

    # Try to fetch the required data from the files included in the package or from the PYRING_PREFIX path.
    for data_string in ['data', 'acf', 'psd']:
        for det in input_par['detectors']:
            if(not(input_par['{}-{}'.format(data_string, det)]=='')):

                package_datapath = utils.import_datafile_path(input_par['{}-{}'.format(data_string, det)])
                PYRING_PREFIX    = utils.set_prefix(warning_message=False)
                custom_datapath  = os.path.join(PYRING_PREFIX, input_par['{}-{}'.format(data_string, det)])
                
                if(os.path.exists(package_datapath)):  input_par['{}-{}'.format(data_string, det)] = package_datapath
                elif(os.path.exists(custom_datapath)): input_par['{}-{}'.format(data_string, det)] = custom_datapath
                else:                                  pass

    # Do some cleaning of the json format for dictionary reading.

    try:
        n_ds_modes = {}
        for key in list(input_par['inject-n-ds-modes'].keys()):
            if (input_par['inject-n-ds-modes'][key] > 0):
                key = key[0]
                n_ds_modes[key] = int(input_par['inject-n-ds-modes'][key])
                assert ((key=='s') or (key=='v') or (key=='t')), "Supported polarisations are: s (scalar perturbations), v (vector perturbations), t (tensor perturbations). The requested polarization {} is not supported.".format(key)
        input_par['inject-n-ds-modes'] = n_ds_modes
        print(("{name} : {value}".format(name='inject-n-ds-modes'.ljust(max_len_keyword), value=input_par['inject-n-ds-modes'])))
    except (AttributeError, KeyError):
        pass

    try:
        n_ds_modes = {}
        for key in list(input_par['n-ds-modes'].keys()):
            if (input_par['n-ds-modes'][key] > 0):
                key = key[0]
                n_ds_modes[key] = int(input_par['n-ds-modes'][key])
                if not((key=='s') or (key=='v') or (key=='t')):
                    raise ValueError("Supported polarisations are: s (scalar perturbations), v (vector perturbations), t (tensor perturbations). The requested polarization {} is not supported.".format(key))
        input_par['n-ds-modes'] = n_ds_modes
        print("{name} : {value}".format(name='n-ds-modes'.ljust(max_len_keyword), value=input_par['n-ds-modes']))
    except (AttributeError, KeyError):
        pass

    # A few sanity checks
    if (len_det > 1):
        assert not(not (('H1' in input_par['detectors']) or ('L1' in input_par['detectors']))), "When running with more than one detector, H1 and L1 are currently required for sky parameters.\nIn case you don't like this, please edit the code by yourself."
        if ('H1'==input_par['ref-det']): input_par['nonref-det'] = 'L1'
        else:                            input_par['nonref-det'] = 'H1'
    else:
        input_par['nonref-det'] = ''
    if not((input_par['ds-ordering']=='freq') or (input_par['ds-ordering']=='tau') or (input_par['ds-ordering']=='amp')):
        raise ValueError('Unknown ds-ordering method selected.')
    if not((input_par['noise-averaging-method']=='mean') or (input_par['noise-averaging-method']=='median')):
        raise ValueError('Unknown noise-averaging method selected.')

    #=================================================================#
    # Print git info on a file (if running from inside a repository). #
    #=================================================================#

    try:
        if (input_par['run-type']=='full' or input_par['run-type']=='psd-only'):
            os.system('mkdir -p {}/Noise'.format(input_par['output']))
            os.system('mkdir -p {}/Plots'.format(input_par['output']))
            os.system('mkdir -p {}/Nested_sampler'.format(input_par['output']))
            os.system('cp {} {}/.'.format(opts.config_file, input_par['output']))
            git_info = open(os.path.join(input_par['output'], 'git_info.txt'), 'w')
            pipe1 = str(subprocess.Popen("git branch | grep \* | cut -d ' ' -f2", shell=True, stdout=subprocess.PIPE).stdout.read())[2:-1]
            pipe2 = str(subprocess.Popen("git log --pretty=format:'%H' -n 1 ", shell=True, stdout=subprocess.PIPE).stdout.read())[2:-1]
            git_info.write('pyRing\nbranch: {}\t commit: {}\n'.format(pipe1, pipe2))
            pipe1 = str(subprocess.Popen("git config user.name", shell=True, stdout=subprocess.PIPE).stdout.read())[2:-1]
            pipe2 = str(subprocess.Popen("git config user.email", shell=True, stdout=subprocess.PIPE).stdout.read())[2:-1]
            git_info.write('Author: {} {}'.format(pipe1, pipe2))
            pipe = str(subprocess.Popen("git diff", shell=True, stdout=subprocess.PIPE).stdout.read())[2:-1]
            git_info.write('\n\nGit diff:\n{}'.format(pipe))
            git_info.close()
    except:
        pass

    #============================#
    # Select time prior options. #
    #============================#

    try:
        input_par['gr-time-prior'] = ast.literal_eval(Config.get("Priors",'gr-time-prior'))
    except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
        pass
    print("{name} : {value}".format(name='gr-time-prior'.ljust(max_len_keyword), value=input_par['gr-time-prior']))
           
    try:
        input_par['dist-flat-prior'] = ast.literal_eval(Config.get("Priors",'dist-flat-prior'))
    except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
        pass
    print("{name} : {value}".format(name='dist-flat-prior'.ljust(max_len_keyword), value=input_par['dist-flat-prior']))
           
    try:
        input_par['ds-amp-flat-prior'] = ast.literal_eval(Config.get("Priors",'ds-amp-flat-prior'))
    except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
        pass
    print("{name} : {value}".format(name='ds-amp-flat-prior'.ljust(max_len_keyword), value=input_par['ds-amp-flat-prior']))

    #Compatibility checks
    try:
        assert not(Config.getfloat("Plot",'mf')), "You are running with an old config file. Now the final mass used in the time prior computation must be passed through 'mf-time-prior' option in the 'Priors' section."
    except(configparser.NoOptionError, configparser.NoSectionError):
        pass
    try:
        input_par['mf-time-prior'] = Config.getfloat("Priors",'mf-time-prior')
    except(configparser.NoOptionError, configparser.NoSectionError):
        pass
    print(("{name} : {value}".format(name='mf-time-prior'.ljust(max_len_keyword), value=input_par['mf-time-prior'])))

    if not(input_par['injection-approximant']==''):

        #==============================================================================#
        # Injections section: initialize injection parameters for each waveform model. #
        #==============================================================================#

        injection_parameters     = {}

        injection_angles_default = {'ra'           : 0.0,
                                    'dec'          : 0.0,
                                    'psi'          : 0.0,
                                    'cos_altitude' : 0.0,
                                    'azimuth'      : 0.0
                                   }
        for j in list(injection_angles_default.keys()):
            try:
                injection_parameters[j] = Config.getfloat("Injection",j)
            except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                injection_parameters[j] = injection_angles_default[j]

        if ((input_par['injection-approximant']=='Damped-sinusoids') or (input_par['injection-approximant']=='Morlet-Gabor-wavelets')):
            print("\n----Setting up an injection using a superposition of {} ----\nI\'ll be injecting the following parameters:\n\n".format(input_par['injection-approximant']))
            injection_parameters_default = {'A'  : 1e-21,
                                            'f'  : 100.0,
                                            'tau': 0.007,
                                            'phi': 0.0,
                                            't'  : 0.0
                                            }

            for par in injection_parameters_default.keys():
                injection_parameters[par] = {}
                for pol in input_par['inject-n-ds-modes'].keys():
                    injection_parameters[par][pol] = []
                    for i in range(0, input_par['inject-n-ds-modes'][pol]):
                        k = '{}_{}_{}'.format(par,pol,i)
                        try:
                            injection_parameters[par][pol].append(Config.getfloat("Injection",k))
                        except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                            injection_parameters[par][pol].append(injection_parameters_default[par])

        if (input_par['injection-approximant']=='Kerr'):
            print("\n----Setting up a Kerr injection----\nI'll be injecting the following parameters:\n\n")
            injection_parameters_default = {'t0'              : 0.004,
                                            'Mf'              : 67.0,
                                            'af'              : 0.67,
                                            'logdistance'     : 6.0857,
                                            'cosiota'         : 1.0,
                                            'phi'             : 0.0,
                                            'alpha'           : 8.*np.pi, # Bekenstein value for area quantization
                                            'Q'               : 0.0, # Absolute value of the adimensional electric charge,
                                            'kerr-amplitudes' : {(2,2,-2,0): 0.0, (2,2,-1,0): 0.0, (2,2,0,0): 0.0, (2,2,1,0): 0.0, (2,2,2,0): 1.0},
                                            'kerr-phases'     : {(2,2,-2,0): 0.0, (2,2,-1,0): 0.0, (2,2,0,0): 0.0, (2,2,1,0): 0.0, (2,2,2,0): 0.0},
                                            'kerr-domegas'    : {(2,2,-2,0): 0.0, (2,2,-1,0): 0.0, (2,2,0,0): 0.0, (2,2,1,0): 0.0, (2,2,2,0): 0.0},
                                            'kerr-dtaus'      : {(2,2,-2,0): 0.0, (2,2,-1,0): 0.0, (2,2,0,0): 0.0, (2,2,1,0): 0.0, (2,2,2,0): 0.0}
                                            }

            #Temporary constraint. To be relaxed.
            warnings.warn("Imposing non-precessing Kerr amplitude symmetry for both injection and recovery (to be relaxed in future versions).")
            sys.stdout.write("Imposing non-precessing Kerr amplitude symmetry for both injection and recovery (to be relaxed in future versions).\n\n")

            input_par['amp-non-prec-sym'] = 1
            for p in list(injection_parameters_default.keys()):
                try:
                    if ('kerr-' in p):
                        injection_parameters[p] = json.loads(Config.get("Injection",p))
                    else:
                        partype = type(injection_parameters_default[p])
                        injection_parameters[p] = partype(Config.get("Injection",p))
                except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    injection_parameters[p] = injection_parameters_default[p]

            # Do some cleaning of the json format.
            try:
                Kerr_amps_complex = {}
                for key in list(injection_parameters['kerr-amplitudes'].keys()):
                    # Syntax: (s,l,m,n)
                    if ('-' in key):
                        new_key = (int(key[0]), int(key[1]), -int(key[3]), int(key[4]))
                    else:
                        new_key = (int(key[0]), int(key[1]),  int(key[2]), int(key[3]))
                    Kerr_amps_complex[new_key] = injection_parameters['kerr-amplitudes'][key]*np.exp(1j*injection_parameters['kerr-phases'][key])
                injection_parameters['kerr-amplitudes'] = Kerr_amps_complex
            except (AttributeError, KeyError):
                pass
            try:
                Kerr_domegas_dict = {}
                for key in list(injection_parameters['kerr-domegas'].keys()):
                    # Syntax: (s,l,m,n)
                    if ('-' in key):
                        new_key = (int(key[0]), int(key[1]), -int(key[3]), int(key[4]))
                    else:
                        new_key = (int(key[0]), int(key[1]),  int(key[2]), int(key[3]))
                    Kerr_domegas_dict[new_key] = injection_parameters['kerr-domegas'][key]
                injection_parameters['kerr-domegas'] = Kerr_domegas_dict
            except (AttributeError, KeyError):
                pass
            try:
                Kerr_dtaus_dict = {}
                for key in list(injection_parameters['kerr-dtaus'].keys()):
                    # Syntax: (s,l,m,n)
                    if ('-' in key):
                        new_key = (int(key[0]), int(key[1]), -int(key[3]), int(key[4]))
                    else:
                        new_key = (int(key[0]), int(key[1]),  int(key[2]), int(key[3]))
                    Kerr_dtaus_dict[new_key] = injection_parameters['kerr-dtaus'][key]
                injection_parameters['kerr-dtaus'] = Kerr_dtaus_dict
            except (AttributeError, KeyError):
                pass

        if (input_par['injection-approximant']=='MMRDNS'):
            utils.review_warning()
            print("\n----Setting up a MMRDNS injection----\nI'll be injecting the following parameters:\n\n")
            injection_parameters_default = {'t0'          : 0.004,
                                            'Mf'          : 67.0,
                                            'af'          : 0.67,
                                            'eta'         : 0.25,
                                            'logdistance' : 6.0857,
                                            'cosiota'     : 1.0,
                                            'phi'         : 0.0
                                            }

            for p in list(injection_parameters_default.keys()):
                try:
                    partype = type(injection_parameters_default[p])
                    injection_parameters[p] = partype(Config.get("Injection",p))
                except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    injection_parameters[p] = injection_parameters_default[p]

        if (input_par['injection-approximant']=='MMRDNP'):
            print("\n----Setting up a MMRDNP injection----\nI'll be injecting the following parameters:\n\n")
            injection_parameters_default = {'t0'          : 0.004,
                                            'm1'          : 35.0,
                                            'm2'          : 32.0,
                                            'chi1'        : 0.0,
                                            'chi2'        : 0.0,
                                            'logdistance' : 6.0857,
                                            'cosiota'     : 1.0,
                                            'phi'         : 0.0
                                            }

            for p in list(injection_parameters_default.keys()):
                try:
                    partype = type(injection_parameters_default[p])
                    injection_parameters[p] = partype(Config.get("Injection",p))
                except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    injection_parameters[p] = injection_parameters_default[p]

            injection_parameters['Mi']   = injection_parameters['m1'] + injection_parameters['m2']
            injection_parameters['Mf']   = bbh_final_mass_projected_spins(injection_parameters['m1'], injection_parameters['m2'], injection_parameters['chi1'], injection_parameters['chi2'], 0.0, 0.0, 'UIB2016')
            injection_parameters['af']   = bbh_final_spin_projected_spins(injection_parameters['m1'], injection_parameters['m2'], injection_parameters['chi1'], injection_parameters['chi2'], 0.0, 0.0, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)
            injection_parameters['eta']  = (injection_parameters['m1']*injection_parameters['m2'])/(injection_parameters['Mi'])**2
            injection_parameters['chis'] = (injection_parameters['m1']*injection_parameters['chi1'] + injection_parameters['m2']*injection_parameters['chi2'])/(injection_parameters['Mi'])
            injection_parameters['chia'] = (injection_parameters['m1']*injection_parameters['chi1'] - injection_parameters['m2']*injection_parameters['chi2'])/(injection_parameters['Mi'])

        if (input_par['injection-approximant']=='TEOBResumSPM'):
            print("\n----Setting up a TEOBResumSPM injection----\nI'll be injecting the following parameters:\n\n")
            injection_parameters_default = {'t0'          : 0.004,
                                            'm1'          : 50.0,
                                            'm2'          : 50.0,
                                            'chi1'        : 0.0,
                                            'chi2'        : 0.0,
                                            'phi22'       : 0.0,
                                            'phi21'       : 0.0,
                                            'phi33'       : 0.0,
                                            'phi32'       : 0.0,
                                            'phi31'       : 0.0,
                                            'phi44'       : 0.0,
                                            'phi43'       : 0.0,
                                            'phi42'       : 0.0,
                                            'phi41'       : 0.0,
                                            'phi55'       : 0.0,
                                            'cosiota'     : 1.0,
                                            'logdistance' : 6.0857,
                                            'phi'         : 0.0
                                            }

            for p in list(injection_parameters_default.keys()):
                try:
                    partype = type(injection_parameters_default[p])
                    injection_parameters[p] = partype(Config.get("Injection",p))
                except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    injection_parameters[p] = injection_parameters_default[p]

            injection_parameters['M'] = injection_parameters['m1'] + injection_parameters['m2']
            injection_parameters['q'] = injection_parameters['m1']/injection_parameters['m2']

            #For the documentation on final state fits, see https://lscsoft.docs.ligo.org/lalsuite/lalinference/namespacelalinference_1_1imrtgr_1_1nrutils.html#a351987f8201d32f50af2fd38a7e4190e
            injection_parameters['af'] = bbh_final_spin_projected_spins(injection_parameters['m1'], injection_parameters['m2'], injection_parameters['chi1'], injection_parameters['chi2'], 0.0, 0.0, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)
            injection_parameters['Mf'] = bbh_final_mass_projected_spins(injection_parameters['m1'], injection_parameters['m2'], injection_parameters['chi1'], injection_parameters['chi2'], 0.0, 0.0, 'UIB2016')

        if (input_par['injection-approximant']=='KHS_2012'):
            utils.review_warning()
            print("\n----Setting up a KHS_2012 injection----\nI'll be injecting the following parameters:\n\n")
            injection_parameters_default = {'t0'          : 0.004,
                                            'Mf'          : 67.0,
                                            'af'          : 0.67,
                                            'eta'         : 0.25,
                                            'chi_eff'     : 0.0,
                                            'logdistance' : 6.0857,
                                            'cosiota'     : 1.0,
                                            'phi'         : 0.0
                                            }

            for p in list(injection_parameters_default.keys()):
                try:
                    partype = type(injection_parameters_default[p])
                    injection_parameters[p] = partype(Config.get("Injection",p))
                except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                    injection_parameters[p] = injection_parameters_default[p]

        if ((input_par['injection-approximant']=='NR') or ('LAL' in input_par['injection-approximant'])):

            #FIXME: Section C of IMRPhenomX model paper https://dcc.ligo.org/DocDB/0165/P2000011/003/IMRPhenomXHM.pdf
            # says that the angles that enters the spherical harmonics 'phi' = pi/2 - phiref
            # Currently we pass phi = phiref, so there should be a disagreement of pi/2 wrt the injected value.
            # If this convention is valid for all wfs, included NR, then we should implement it in the injections as well.
            if (input_par['injection-approximant']=='NR'):
                print("\n----Setting up a NR injection----\nI'll be injecting the following parameters:\n\n")
                injection_parameters_default = {'M'                  : 70.0,
                                                'dist'               : 400.0,
                                                'incl'               : 0.0,
                                                'phi'                : 0.0,
                                                'NR-ID'              : '0180',
                                                'NR-catalog'         : 'SXS',
                                                'resolution-level'   : -1
                                                }

                for j in list(injection_parameters_default.keys()):
                    keytype = type(injection_parameters_default[j])
                    try:
                        injection_parameters[j] = keytype(Config.get("Injection",j))
                    except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                        injection_parameters[j] = injection_parameters_default[j]

                assert not(injection_parameters['resolution-level'] == -1), "A positive resolution level must be passed from the user."

                # For more details on the LVC NR injection infrastructure see this paper: arxiv-1703.01076 or this wiki page https://www.lsc-group.phys.uwm.edu/ligovirgo/cbcnote/Waveforms/NR/InjectionInfrastructure

                # NR metadata
                PYRING_PREFIX = utils.set_prefix()
                utils.check_NR_dir()

                NR_catalog                          = injection_parameters['NR-catalog']
                NR_ID                               = injection_parameters['NR-ID']
                resolution_level                    = injection_parameters['resolution-level']
                injection_parameters['NR-datafile'] = os.path.join(PYRING_PREFIX, 'data/NR_data/lvcnr-lfs/{0}/{0}_BBH_{1}_Res{2}.h5'.format(NR_catalog, NR_ID, resolution_level))
                NR_injection                        = h5py.File(injection_parameters['NR-datafile'], 'r')

                # Binary parameters
                mass  = injection_parameters['M']
                m1_NR = NR_injection.attrs['mass1']
                m2_NR = NR_injection.attrs['mass2']
                # NR has unitary total mass, so we need to rescale the masses.
                injection_parameters['m1'] = m1_NR * mass / (m1_NR + m2_NR)
                injection_parameters['m2'] = m2_NR * mass / (m1_NR + m2_NR)
                injection_parameters['q']  = injection_parameters['m1']/injection_parameters['m2']
                injection_parameters['theta_LN'] = injection_parameters['incl']

                injection_parameters['f-lower-NR'] = NR_injection.attrs['f_lower_at_1MSUN']/mass  # this generates the whole NR waveform
                injection_parameters['f-ref']      = injection_parameters['f-lower-NR']
                injection_parameters['f-start']    = injection_parameters['f-lower-NR']
#                input_par['f-min-bp']            = injection_parameters['f-lower-NR']
                spins = lalsim.SimInspiralNRWaveformGetSpinsFromHDF5File(injection_parameters['f-ref'], mass, injection_parameters['NR-datafile'])
                injection_parameters['s1x_LALSim'], injection_parameters['s1y_LALSim'], injection_parameters['s1z_LALSim'] = spins[0], spins[1], spins[2]
                injection_parameters['s2x_LALSim'], injection_parameters['s2y_LALSim'], injection_parameters['s2z_LALSim'] = spins[3], spins[4], spins[5]
                NR_injection.close()

                spin_tolerance = 1e-3
                if(np.abs(injection_parameters['s1x_LALSim'])>=spin_tolerance or np.abs(injection_parameters['s1y_LALSim'])>=spin_tolerance or np.abs(injection_parameters['s2x_LALSim'])>=spin_tolerance or np.abs(injection_parameters['s2y_LALSim'])>=spin_tolerance):
                    raise ValueError("Precessing NR injections are not yet supported, need to edit the code to correctly define spin angles.")
                else:
                    if(injection_parameters['s1z_LALSim'] < 0): injection_parameters['tilt1']  = np.pi
                    else: injection_parameters['tilt1']  = 0.0
                    if(injection_parameters['s2z_LALSim'] < 0): injection_parameters['tilt2'] = np.pi
                    else: injection_parameters['tilt2']  = 0.0
    
                    injection_parameters['phi_12'] = 0.0

            else:
                print("\n----Setting up an IMR template injection----\nI'll be injecting the following parameters:\n\n")
                # If not explicitely specified (e.g. with the suffix _LALSim), all parameters are referred to the reference frame where the z-axis is fixed and aligned with the total angular momentum direction J
                injection_parameters_default = {'m1'                 : 35.0,
                                                'm2'                 : 35.0,
                                                's1'                 : 0.0,
                                                's2'                 : 0.0,
                                                'tilt1'              : 0.0,
                                                'tilt2'              : 0.0,
                                                'dist'               : 400.0,
                                                'incl'               : 0.0, #'incl' is *defined* as theta_JN
                                                'phi'                : 0.0,
                                                'phi_JL'             : 0.0,
                                                'phi_12'             : 0.0,
                                                'f-ref'              : 20.,
                                                'amp-order'          : -1,
                                                'phase-order'        : -1,
                                                }

                for j in list(injection_parameters_default.keys()):
                    keytype = type(injection_parameters_default[j])
                    try:
                        injection_parameters[j] = keytype(Config.get("Injection",j))
                    except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                        injection_parameters[j] = injection_parameters_default[j]

                # Set appropriate starting frequency in case where HMs are used and change bandpassing frequency accordingly.
                injection_parameters['f-start']  = lalsim.SimInspiralfLow2fStart(input_par['f-min-bp'], injection_parameters['amp-order'], lalsim.SimInspiralGetApproximantFromString(input_par['injection-approximant'].strip('LAL-')))

                # This step is needed because for precessing systems the reference frame used by LALSimulation to define the spins is different wrt the one used in NR or PE (both LALInference and pyRing). Full documentation and parameters definitions can be found here: https://lscsoft.docs.ligo.org/lalsuite/lalsimulation/group__lalsimulation__inference.html
                injection_parameters['theta_LN'], injection_parameters['s1x_LALSim'], injection_parameters['s1y_LALSim'], injection_parameters['s1z_LALSim'], injection_parameters['s2x_LALSim'], injection_parameters['s2y_LALSim'], injection_parameters['s2z_LALSim'] = lalsim.SimInspiralTransformPrecessingNewInitialConditions(injection_parameters['incl'],
                                                                              injection_parameters['phi_JL'],
                                                                              injection_parameters['tilt1'],
                                                                              injection_parameters['tilt2'],
                                                                              injection_parameters['phi_12'],
                                                                              injection_parameters['s1'],
                                                                              injection_parameters['s2'],
                                                                              injection_parameters['m1'],
                                                                              injection_parameters['m2'],
                                                                              injection_parameters['f-ref'],
                                                                              injection_parameters['phi'])

            #IMPROVEME: write document with details on our reference frame
           # This section is temporarily commented out, since gwsurrogate was giving installation problems.
           # try:
           #     q     = injection_parameters['m1']/injection_parameters['m2']
           #     M_tot = injection_parameters['m1']+injection_parameters['m2']
           #     chi1  = [injection_parameters['s1x_LALSim'], injection_parameters['s1y_LALSim'], injection_parameters['s1z_LALSim']]
           #     chi2  = [injection_parameters['s2x_LALSim'], injection_parameters['s2y_LALSim'], injection_parameters['s2z_LALSim']]
           #     injection_parameters['Mf'], injection_parameters['af'] = utils.final_state_surfinBH(M_tot, q, chi1, chi2, injection_parameters['f-ref'])
           # except:
            # Case where we are outside the validity region of the surrogate.
           # warnings.warn("\nSurrogate remnant fits failed with error {}.\nUsing analytical fits from UIB instead.".format(traceback.print_exc()))
            #FIXME: check the reference frame in which spin z-components should be specified
            chi1  = np.sqrt(injection_parameters['s1x_LALSim']**2 + injection_parameters['s1y_LALSim']**2 + injection_parameters['s1z_LALSim']**2)
            chi2  = np.sqrt(injection_parameters['s2x_LALSim']**2 + injection_parameters['s2y_LALSim']**2 + injection_parameters['s2z_LALSim']**2)
            tilt1 = injection_parameters['tilt1']
            tilt2 = injection_parameters['tilt2']

            #For the documentation on final state fits, see https://lscsoft.docs.ligo.org/lalsuite/lalinference/namespacelalinference_1_1imrtgr_1_1nrutils.html#a351987f8201d32f50af2fd38a7e4190e
            injection_parameters['af'] = bbh_final_spin_precessing(injection_parameters['m1'], injection_parameters['m2'], chi1, chi2, tilt1, tilt2, injection_parameters['phi_12'], 'UIB2016', truncate=bbh_Kerr_trunc_opts.trunc)
            injection_parameters['Mf'] = bbh_final_mass_projected_spins(injection_parameters['m1'], injection_parameters['m2'], chi1, chi2, tilt1, tilt2, 'UIB2016')

            injection_parameters['f_220']      = wf.QNM_fit(2,2,0).f(injection_parameters['Mf'], injection_parameters['af'])
            injection_parameters['tau_220']    = wf.QNM_fit(2,2,0).tau(injection_parameters['Mf'], injection_parameters['af'])
            injection_parameters['f_220_peak'] = utils.F_mrg_Nagar(injection_parameters['m1']*lal.MSUN_SI, injection_parameters['m2']*lal.MSUN_SI, injection_parameters['s1z_LALSim'], injection_parameters['s2z_LALSim'])

            try:
                injection_parameters['inject-modes'] = ast.literal_eval(Config.get("Injection",'inject-modes'))
            except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                injection_parameters['inject-modes'] = None
            try:
                injection_parameters['inject-l-modes'] = ast.literal_eval(Config.get("Injection",'inject-l-modes'))
            except (KeyError, configparser.NoOptionError, configparser.NoSectionError):
                injection_parameters['inject-l-modes'] = None

        if (input_par['sky-frame'] == 'detector'):
            check = None
            try: check = Config.getfloat("Injection","ra")
            except: pass
            try: check = Config.getfloat("Injection","dec")
            except: pass
            assert (check == None), "Injected sky position parameters are inconsistent with respect to the 'sky-frame = detector' option selected. If you want to inject ra and dec, please pass the 'sky-frame = equatorial' option."
        elif (input_par['sky-frame'] == 'equatorial'):
            check = None
            try: check = Config.getfloat("Injection","azimuth")
            except: pass
            try: check = Config.getfloat("Injection","cos_altitude")
            except: pass
            assert (check == None), "Injected sky position parameters are inconsistent with respect to the 'sky-frame = equatorial' option selected. If you want to inject azimuth and cos_altitude, please pass the 'sky-frame = detector' option."
        else:
            raise ValueError("Invalid option for sky position sampling.")

        for key in injection_parameters:
            print(("{name} : {value}".format(name=key.ljust(len('kerr-amplitudes')), value=injection_parameters[key])))
            input_par['injection-parameters'] = injection_parameters

    #===========================#
    # Select waveform template. #
    #===========================#

    if (input_par['template']=='Kerr'):
        signal_model = KerrModel(modes=input_par['kerr-modes'],**input_par)
    elif (input_par['template']=='Damped-sinusoids'):
        signal_model = DampedSinusoids(**input_par)
    elif (input_par['template']=='Morlet-Gabor-wavelets'):
        signal_model = MorletGaborWavelets(**input_par)
    elif (input_par['template']=='MMRDNS'):
        signal_model = MMRDNSModel(**input_par)
    elif (input_par['template']=='MMRDNP'):
        signal_model = MMRDNPModel(**input_par)
    elif (input_par['template']=='KHS_2012'):
        signal_model = KHS_2012Model(**input_par)
    elif (input_par['template']=='IMR'):
        signal_model = IMR_Ringdown_Model(**input_par)
    elif(input_par['template']=='TEOBResumSPM'):
        signal_model = TEOBPMModel(**input_par)
    else:
        raise Exception("Unknown template selected")

    if (input_par['run-type']=='psd-only'):
        print('ACF/PSD estimation done, psd-only option was selected. Exiting.')
        exit()

    #========================================#
    # Initialize default sampler parameters. #
    #========================================#

    print("\n----Setting up the sampler----\nI\'ll be running with the following sampler parameters:\n")
    sampler_params={'verbose' : 2,
                    'poolsize': 128,
                    'nthreads': 1,
                    'nlive'   : 1024,
                    'maxmcmc' : 1024,
                    'seed'    : 1234,
                    'resume'  : 1
                    }

    for key in sampler_params:
        if isinstance(sampler_params[key], int):
            try:
                sampler_params[key] = Config.getint("Sampler settings", key)
            except(KeyError, configparser.NoOptionError, configparser.NoSectionError):
                pass
            print(("{name} : {value}".format(name=key.ljust(len('nthreads')), value=sampler_params[key])))
    print('\n')

    #===========================================#
    # Output strain and compute noise evidence. #
    #===========================================#

    plots.plot_strain(signal_model.get_waveform, signal_model.detectors, signal_model.fixed_params, signal_model.tgps, filename = 'strain', strain_only = 1, **input_par)
    plots.plot_strain(signal_model.get_waveform, signal_model.detectors, signal_model.fixed_params, signal_model.tgps, whiten_flag=True, filename = 'strain_whitened', strain_only = 1, **input_par)
    logZ_noise = signal_model.logZnoise
    print('Noise evidence  : {}'.format(logZ_noise))

    if (input_par['run-type']=='full'):

        #=============================================#
        # Start the CPNest Nested Sampling algorithm. #
        #=============================================#

        print('\nStarting sampling using CPNest {} version.\n'.format(cpnest.__version__))

        work=cpnest.CPNest(signal_model,
                           verbose  = sampler_params['verbose'],
                           poolsize = sampler_params['poolsize'],
                           nthreads = sampler_params['nthreads'],
                           nlive    = sampler_params['nlive'],
                           maxmcmc  = sampler_params['maxmcmc'],
                           output   = input_par['output']+'/Nested_sampler',
                           seed     = sampler_params['seed'],
                           resume   = sampler_params['resume'])
        work.run()
        logZ_signal = work.NS.logZ
        print('Signal evidence : {}'.format(logZ_signal))
        logB = logZ_signal-logZ_noise
        print('{}: {}'.format('ln B'.ljust(len('Signal evidence ')), logB))
        x = work.get_posterior_samples(filename='posterior.dat')

        # Make an estimate of the SNR

        logL_max = x['logL'][-1]
        SNR = np.sqrt(2*(logL_max - logZ_noise))
        print(('{}: {}'.format('Estimated SNR'.ljust(len('Signal evidence ')), SNR)))

        if(input_par['truncate']):
            # FIXME: Compute the logB distribution, since in this case the data chunk is changing at each step.
            pass

    elif (input_par['run-type']=='post-processing'):

        #===============================================================#
        # If a NS run has already been performed, read out the results. #
        #===============================================================#

        # All the logs are natural logarithms

        x = np.genfromtxt(os.path.join(input_par['output'],'Nested_sampler/posterior.dat'),names=True,deletechars="")
        # genfromtxt removes - signs from column names by default, so set deletechars="" to disable validation
        logZ_signal = np.loadtxt(os.path.join(input_par['output'],'Nested_sampler/chain_{}_{}.txt_evidence.txt'.format(sampler_params['nlive'], sampler_params['seed'])))[0]
        print('Signal evidence : {}'.format(logZ_signal))
        logB = logZ_signal-logZ_noise
        print('{}: {}'.format('ln B'.ljust(len('Signal evidence ')), logB))
        logL_max = x['logL']
        SNR = np.sqrt(2*(logL_max[-1] - logZ_noise))
        print('{}: {}'.format('Estimated SNR'.ljust(len('Signal evidence ')), SNR))
    else:
        raise Exception('Unknown run type was selected.')

    outFile_evidence = open(os.path.join(input_par['output'],'Nested_sampler/Evidence.txt'), 'w')
    outFile_evidence.write('lnZ_noise \t lnZ_signal \t lnB \t Estimated_SNR \n')
    outFile_evidence.write('{} \t {} \t {} \t {} \n'.format(logZ_noise, logZ_signal, logB, SNR))
    outFile_evidence.close()

    #========================#
    # Prior railing section. #
    #========================#

    print('\nChecking for posterior railing:\n')

    try:
        railing_parameters  = []
        header = ''
        for (i,param) in enumerate(signal_model.names):
            Prior_bins = np.linspace(signal_model.bounds[i][0], signal_model.bounds[i][-1], 100)
            low_rail, high_rail = utils.railing_check(samples=x[param], prior_bins= Prior_bins, tolerance=2.0)
            header +='{par}_low\t{par}_up\t'.format(par=param)
            if(low_rail):
                railing_parameters.append(1)
                print(param, 'is railing against the lower prior bound.')
            else:
                railing_parameters.append(0)
            if(high_rail):
                railing_parameters.append(1)
                print(param, 'is railing against the upper prior bound.')
            else:
                railing_parameters.append(0)
        np.savetxt(os.path.join(input_par['output'], 'Nested_sampler/Parameters_prior_railing.txt'), np.column_stack(railing_parameters), fmt= "%d", header=header)
    except:
        warnings.warn("\nPrior railing file generation failed with error: {}.".format(traceback.print_exc()))

    #====================#
    # pesummary section. #
    #====================#
    if(input_par['pesummary']):
        try:
            print('\nCreating pesummary metafile...\n')
            os.system('summarypages --webdir {outdir}/Plots/pesummary_postproc \
                                    --samples {outdir}/Nested_sampler/posterior.dat \
                                    --config {conf} \
                                    --no_ligo_skymap \
                                    --verbose \
                                    --labels {runlabel}'.format(outdir=input_par['output'], conf=config_file, runlabel=input_par['run-tag']))
            #These data can be extracted as (e.g.): f.extra_kwargs[0]['other']['lnZ_noise']
            os.system('summarymodify --samples {outdir}/Plots/pesummary_postproc/samples/posterior_samples.h5 --overwrite --delimiter / --kwargs {runlabel}/lnZ_signal:{logZ_signal_value}'.format(outdir=input_par['output'], runlabel=input_par['run-tag'], logZ_signal_value=logZ_signal))
            os.system('summarymodify --samples {outdir}/Plots/pesummary_postproc/samples/posterior_samples.h5 --overwrite --delimiter / --kwargs {runlabel}/lnZ_noise:{logZ_noise_value}'.format(outdir=input_par['output'], runlabel=input_par['run-tag'], logZ_noise_value=logZ_noise))
            # If available add the information as an extra parameter (useful to estimate logB error). Since this is only printed, but not stored by cpnest, we extract it from the stderr when available (a bit ugly, but does the job).
            if not(input_par['screen-output'] or (input_par['run-type']=='post-processing')):
                try:
                    H_file = '{outdir}/stderr_pyRing.txt'.format(outdir=input_par['output'])
                    with open(H_file, 'r+') as fd:
                        contents = fd.readlines()
                        for line in contents:
                            if('Information' in line):
                                H = line.split('Information:')[-1]
                    fd.close()
                    os.system('summarymodify --samples {outdir}/Plots/pesummary_postproc/samples/posterior_samples.h5 --overwrite --delimiter / --kwargs {runlabel}/H:{H_value}'.format(outdir=input_par['output'], runlabel=input_par['run-tag'], H_value=H))
                except:
                    warnings.warn("\nInformation storage in pesumarry failed with error: {}.".format(traceback.print_exc()))
            os.system('mv {outdir}/Plots/pesummary_postproc/samples/posterior_samples.h5 {outdir}/Plots/pesummary_postproc/samples/{runlabel}_pesummary_metafile.h5'.format(outdir=input_par['output'], runlabel=input_par['run-tag']))
        except:
            warnings.warn("\nPESummary metafile generation failed with error: {}.".format(traceback.print_exc()))

    #=============================#
    # Plots common to all models. #
    #=============================#

    print('\nProducing plots...\n')

    if(('ra' in signal_model.fixed_params.keys()) or ('dec' in signal_model.fixed_params.keys()) or ('cos_altitude' in signal_model.fixed_params.keys()) or ('azimuth' in signal_model.fixed_params.keys()) or ('logdistance' in signal_model.fixed_params.keys())):
        print('Skipping sky position plot, since one of the sky position parameters was fixed.')
    else:
        try:                                                                                   plots.sky_location_plots(x, Config, **input_par)
        except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of sky position failed with error: {}.".format(traceback.print_exc()))
    if('t0' in signal_model.fixed_params.keys()):
        print('Skipping time plot, since time was fixed.')
    else:
        try:                                                                                   plots.t_start_plot(x['t0'], input_par['mf-time-prior'], **input_par)
        except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of start time failed with error: {}.".format(traceback.print_exc()))

    try:
        if (not(input_par['signal-chunksize']==input_par['noise-chunksize']) or not(input_par['window']) or not(input_par['window-onsource'])):
            warnings.warn("Whitened plot will not look sane, due to the lack of windowing or inconsistent noise and signal chunksize used.")
        plots.plot_strain(signal_model.get_waveform, signal_model.detectors, signal_model.fixed_params, signal_model.tgps, params=x, whiten_flag=True,  filename = 'reconstructed_waveform_whitened', **input_par)
        plots.plot_strain(signal_model.get_waveform, signal_model.detectors, signal_model.fixed_params, signal_model.tgps, params=x, whiten_flag=False, filename = 'reconstructed_waveform', **input_par)
        # Work in progress
#        plots.SNR_plots(signal_model.get_waveform, signal_model.detectors, signal_model.fixed_params, signal_model.tgps, params = x, **input_par)
    except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError):
        warnings.warn("\nWaveform generation failed with error: {}.".format(traceback.print_exc()))

    Mf_dist, af_dist = plots.read_Mf_af_IMR_posterior(Config, **input_par)

    #=========================================================#
    # Specific plots for different waveform model parameters. #
    #=========================================================#

    # IMPROVEME: skip plotting when we fix some of the intrinsic params, write a generic parameters handling structure to take care of this
    if (input_par['template']=='Kerr'):
        try:                                                                                   plots.Kerr_intrinsic_corner(x, **input_par)
        except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of intrinsic Kerr parameters failed with error: {}.".format(traceback.print_exc()))
        try:                                                                                                   plots.amplitudes_corner(x, **input_par)
        except(AttributeError, KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of amplitudes failed with error: {}.".format(traceback.print_exc()))
        if (input_par['inject-area-quantization']==1 and input_par['area-quantization']==1):
            try:                                                                                   plots.Kerr_intrinsic_alpha_corner(x, **input_par)
            except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of alpha failed with error: {}.".format(traceback.print_exc()))
        if(input_par['charge']):
            try:                                                                                   plots.Kerr_Newman_intrinsic_corner(x, **input_par)
            except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError): warnings.warn("\nPlot of intrinsic Kerr-Newman parameters failed with error: {}.".format(traceback.print_exc()))
    try:
        if ((input_par['template']=='Damped-sinusoids') or (input_par['template']=='Morlet-Gabor-wavelets')):
            plots.f_tau_amp_corner(x, **input_par)
            if((Mf_dist is not None) and (af_dist is not None)):
                Kerr_class = KerrModel(modes=input_par['kerr-modes'],**input_par)
                for pol in input_par['n-ds-modes'].keys():
                    for i in range(input_par['n-ds-modes'][pol]):
                        plots.f0_t0_gr(np.column_stack((x['f_{}_{}'.format(pol,i)],1e3*x['tau_{}_{}'.format(pol,i)])), Kerr_class.qnm_interpolants, Mf_dist, af_dist, i, **input_par)
        elif (input_par['template']=='TEOBResumSPM'):
            try:                          plots.TEOBPM_intrinsic_corner(x, **input_par)
            except(KeyError, ValueError): warnings.warn("\nTEOB intrinsic parameters plot failed.")
        elif (input_par['template']=='MMRDNP'):
            try:                          plots.MMRDNP_intrinsic_corner(x, **input_par)
            except(KeyError, ValueError): warnings.warn("\nMMRDNP intrinsic parameters plot failed.")
            try:                          plots.MMRDNP_amplitude_parameters_corner(x, **input_par)
            except(KeyError, ValueError): warnings.warn("\nMMRDNP amplitude parameters plot failed.")
            try:                          plots.MMRDNP_Mf_af_plot(x, **input_par)
            except(KeyError, ValueError): warnings.warn("\nMMRDNP final parameters plot failed.")

        else:
            try:                          plots.Mf_af_plot(x, Mf_dist, af_dist, **input_par)
            except(KeyError, ValueError): warnings.warn("\nPlot of Mf_af failed.")
            try:                          plots.orientation_corner(x, Config, **input_par)
            except(KeyError, ValueError): warnings.warn("\nPlot of orientation_corner failed.")
            if((input_par['template']=='Kerr') or (input_par['template']=='MMRDNP') or (input_par['template']=='TEOBResumSPM')):
                try:
                    if((input_par['domega-tgr-modes'] is not None) or (input_par['dtau-tgr-modes'] is not None)):
                        plots.omega_tau_eff_plot(x, **input_par)
                except:
                    warnings.warn("\nKerr deviation parameters plots failed.")
            elif (input_par['template']=='MMRDNS'):
                try:                          plots.MMRDNS_intrinsic_corner(x, **input_par)
                except(KeyError, ValueError): warnings.warn("\nMMRDNS plots failed.")

    except(KeyError, ValueError, configparser.NoOptionError, configparser.NoSectionError):
        warnings.warn("\nPlotting failed with error: {}.".format(traceback.print_exc()))

    #===============================================================#
    # Print execution time and move plots to appropriate directory. #
    #===============================================================#

    if (input_par['run-type']=='full'):
        execution_time = (time.time() - execution_time)/60.0
        print('Execution time (min): {}'.format(execution_time))
    if (input_par['run-type']=='full' or input_par['run-type']=='post-processing'):
        if any(plot.endswith(".png") for plot in os.listdir("{}/Nested_sampler/".format(input_par['output']))):
            os.system('mv {0}/Nested_sampler/*.png {0}/Plots/. '.format(input_par['output']))
        if any(plot.endswith(".pdf") for plot in os.listdir("{}/Nested_sampler/".format(input_par['output']))):
            os.system('mv {0}/Nested_sampler/*.pdf {0}/Plots/. '.format(input_par['output']))
        else: pass


if __name__=='__main__':
    main()
