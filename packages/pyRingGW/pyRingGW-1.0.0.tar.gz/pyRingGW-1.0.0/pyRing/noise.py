# -*- coding: utf-8 -*-
#Standard python imports
from __future__        import division
from io                import StringIO
from scipy.interpolate import interp1d
from scipy.linalg      import inv, toeplitz, cholesky
from scipy.signal      import butter, filtfilt, welch, tukey, decimate
from scipy.stats       import multivariate_normal
import matplotlib.mlab as mlab, matplotlib.pyplot as plt, numpy as np, os, sys, warnings

#LVC imports
from gwpy.timeseries import TimeSeries
try:
    from glue import datafind
except(ImportError, ModuleNotFoundError):
    pass

#Package internal imports
from pyRing               import plots
from pyRing.inject_signal import inject_IMR_signal, inject_ringdown_signal
from pyRing.utils         import review_warning
try:
    from gwmodel.powerspectrum import mesa as mem
except(ImportError, ModuleNotFoundError):
    pass


def resize_nan_strain(strain, start_time, trig_time, onsource_length, dt):

    srate              = 1./dt
    trig_time_idx      = int((trig_time-start_time)*srate)
    first_idx_onsource = int((trig_time-(onsource_length/2.)-start_time)*srate)
    last_idx_onsource  = int((trig_time+(onsource_length/2.)-start_time)*srate)
    first_nan_index    = None
    last_nan_index     = len(strain)-1

    for j in range(first_idx_onsource, last_idx_onsource):
        assert not(np.isnan(strain[j])), "Nans present on the onsource chunk, resize the onsource chunk to a segment which does not contain nans."
    for i in range(len(strain)):
        if(first_nan_index == None):
            if(np.isnan(strain[i])):
                first_nan_index = i
        else:
            if not(np.isnan(strain[i])):
                last_nan_index = i-1
                break
    # Since we raise an error in the case where the nans overlap with the onsource chunk, now the only possibility is that the nan block is either to the left or to the right with respect to the onsource chunk.
    if(last_nan_index < trig_time_idx):
        sys.stdout.write('Nans present in the [{0:.2f}, {1:.2f}]s interval (before signal).\nResizing data to the [{2}, {3}]s interval. Remaining length: {4}s\n'.format(start_time+first_nan_index*dt, start_time+last_nan_index*dt, int(start_time+(last_nan_index+1)*dt), int(start_time+(len(strain))*dt), int((len(strain)-(last_nan_index+1))*dt)))
        new_start_time = start_time+(last_nan_index+1)*dt
        return strain[last_nan_index+1:], new_start_time
    else:
        sys.stdout.write('Nans present in the [{0:.2f}, {1:.2f}]s interval (after signal).\nResizing data to the [{2}, {3}]s interval. Remaining length: {4}s\n'.format(start_time+first_nan_index*dt, start_time+last_nan_index*dt, int(start_time), int(start_time+(first_nan_index-1)*dt), int((first_nan_index-1)*dt)))
        new_start_time = start_time
        return strain[:first_nan_index-1], new_start_time

def chunks(times, strain, chunksize, avoid=None, window=False, alpha=0.1):
    """
        Divide the data in chunks. Skip the 0th and the last chunks which have filter ringing from downsampling.
    """
    if avoid is None:
        avoid = times[0]-1e6 # dummy value
    if window:
        win      = tukey(chunksize,alpha=alpha)
    else:
        win      = np.ones(chunksize)
    #The integer division is needed in case the chunk length in seconds is not a sub-multiple of the total strain length (e.g. after quality veto cuts)
    for j in range(1,len(strain)//chunksize):
        if not times[chunksize*j] < avoid < times[chunksize*(j+1)]:
            yield strain[chunksize*j:chunksize*(j+1)]*win

def acf(y, fft=True, simple_norm=False):

    """
        Returns the autocorrelation function: R[i] = sum_n x[n]*x[n+i]
        Returns an array spanned by the index i.
        If `fft`, uses FT method, see section 'Efficient computation' of 'https://en.wikipedia.org/wiki/Autocorrelation#cite_note-3
    """

    N = len(y)

    if fft:
        # ACF computation using FFT.
        Y=np.fft.fft(y)
        # We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        R = np.real(np.fft.ifft(Y*Y.conj()))
        # Divide by an additional factor of 1/N since we are taking two fft and one ifft without unitary normalization, see: https://docs.scipy.org/doc/numpy/reference/routines.fft.html#module-numpy.fft
        acf_normed = R/N
    else:
        # ACF computation without FFT.
        acf_numpy = np.correlate(y, y, mode='full')[N-1:]
        # FIXME: describe the difference between the two normalizations.
        if simple_norm:
            acf_normed = acf_numpy[:N] / N
        else:
            acf_normed = acf_numpy[:N] / (N - np.arange(N))

    return acf_normed

def fetch_data(ifo, tstart, tend, channel=None, path=None, verbose=0, tag=None):

    """
        Fetch data for a particular event

        ifo: IFO name ('H1' etc)
        tstart, tend: start and end time to find
        path: Local path to save file. If file exists it will be read from disk rather than fetched
        channel: Channel to read from frame data. If 'GWOSC' will fetch open data
        verbose: Print some info

        Returns a gwpy.TimeSeries object
    """

    # If file was previously saved, open it.
    if path is not None and os.path.exists(path):
        tseries = TimeSeries.read(path,start=tstart,end=tend)
        if verbose:
            sys.stdout.write('Reading from local file '+path)
        return tseries

    # If not, then see if it is on GWOSC.
    if channel=='GWOSC':
        #When downloading public data, fetch them with the highest possible sampling rate, then pyRing will down-sample internally, if required. This is needed to avoid incompatibilities between GWOSC down-sampling and the pyRing internal one. The actual function used to down-sample is the same, but differences in things like the length of data stretch can affect filtering at the borders and hence the Bayes Factors. 
        tseries = TimeSeries.fetch_open_data(ifo, tstart, tend, sample_rate = 16384, verbose=verbose, cache=True, tag=u"{0}".format(tag))
    else:
        # Read from authenticated data.
        if channel is None:
            raise Exception('Channel not specified when fetching frame data.')
        tseries = TimeSeries.get(channel, tstart, tend, verbose=verbose)
    if path is not None:
        tseries.write(path)

    return tseries


#FIXME: this function is too big and should be split.
def load_data(ifo, fname, **kwargs):

    """
        Reads the strain or downloads it using gwpy.
        Computes the ACF either from the directly data or from given file input ACF/PSD.
        Injects a template if requested.
    """

    sys.stdout.write('\nReading data...\n')
    # General parameters that are always needed.
    triggertime       = kwargs['trigtime']
    fft_acf           = kwargs['fft-acf']
    signal_chunk_size = kwargs['signal-chunksize']
    noise_chunk_size  = kwargs['noise-chunksize']
    srate             = kwargs['sampling-rate']
    f_min_bp          = kwargs['f-min-bp']
    f_max_bp          = kwargs['f-max-bp']
    alpha_window      = kwargs['alpha-window']
    signal_seglen     = np.int(srate*signal_chunk_size)
    noise_seglen      = np.int(srate*noise_chunk_size)
    psd_window        = tukey(noise_seglen,alpha_window)
    psd_window_norm   = np.sum(psd_window**2)/noise_seglen
    assert not(triggertime is None), "No triggertime given."

    # Start to read the data.
    if not(kwargs['data-{}'.format(ifo)]==''):
        # If a data file is passed, check that no contrasting option (generate gaussian-noise or download data) is passed.
        if (not(kwargs['gaussian-noise']=='')):
            raise ValueError("If 'gaussian-noise' is selected, no data must be passed.")
        else:
            if not(kwargs['ignore-data-filename']):
                warnings.warn("The file name is expected to follow LIGO-Virgo conventions 'DET-FRAMETYPE-STARTTIME--DATALEN.txt', e.g.: 'H-H1_GWOSC_4_V1-1126259446-32.txt'. See https://www.gw-openscience.org for more infomation. This requirement can be relaxed by activating the 'ignore-data-filename' option.")
                assert not(fname==''), "Data are empty. Either pass valid data or select one of the 'download-data' or 'gaussian-noise' options."
                if not('.gwf' in fname):
                    ifo_name, fr_type, starttime, T = ((fname.split('/'))[-1]).strip('.txt').split('-')
                    rawstrain = np.loadtxt(fname)
                else:
                    ifo_name, fr_type, starttime, T = ((fname.split('/'))[-1]).strip('.gwf').split('-')
                    channel   = kwargs['channel-{}'.format(ifo)]
                    tseries   = TimeSeries.read(fname, channel)
                    rawstrain = np.array(tseries.data)
                starttime     = float(starttime)
                T             = float(T)
                dt            = T/len(rawstrain)
            else:
                # If the file name does not follow LVK conventions, times corresponding to the given strain must also be passed in the file (this could be made more general by passing custom {starttime, srate, T}, but this way is probably more stable).
                times, rawstrain = np.loadtxt(fname, unpack=True)
                starttime        = float(times[0])
                dt               = float(times[1] - times[0])
                T                = dt * len(rawstrain)
            srate_dt = 1./dt
            sys.stdout.write('\nLoaded {} starting at {} length {}s.\n'.format(fname,starttime,T))
    else:
        # If no data file was passed either download them or generate them yourself.
        if(kwargs['download-data'] == 1):
            T         = float(kwargs['datalen-download'])
            channel   = kwargs['channel-{}'.format(ifo)]
            starttime = np.int(triggertime)-(T/2.)
            endtime   = np.int(triggertime)+(T/2.)

            if((kwargs['gw-data-find']==1) and not(kwargs['gw-data-type-{}'.format(ifo)]=='')):
                connection = datafind.GWDataFindHTTPConnection()
                cache      = connection.find_frame_urls(ifo[0], kwargs['gw-data-type-{}'.format(ifo)], starttime, endtime, urltype='file')
                tseries    = TimeSeries.read(cache, channel)
            else:
                sys.stdout.write('\nUsing GWPY to download data.\n')
                tag        = kwargs['tag']
                tseries    = fetch_data(ifo, starttime, endtime, channel=channel, path=None, verbose=2, tag=tag)
            rawstrain               = np.array(tseries.data)
            dt                      = tseries.dt.to_value()
            srate_dt                = tseries.sample_rate.to_value()
            sys.stdout.write('\nLoaded channel {} starting at {} length {}s.\n'.format(channel,starttime,T))
        elif(not(kwargs['gaussian-noise']=='')):
            
            # If requested by the user, fix the noise seed.
            if not(kwargs['gaussian-noise-seed']==-1):
                if(  ifo=='H1'): np.random.seed(kwargs['gaussian-noise-seed'])
                elif(ifo=='L1'): np.random.seed(kwargs['gaussian-noise-seed']+1)
                elif(ifo=='V1'): np.random.seed(kwargs['gaussian-noise-seed']+2)
                else: raise ValueError("Noise generation for this detector not supported. Please add the detector to the noise generation.")
            
            T            = int(kwargs['injection-T'])
            starttime    = triggertime - T/2.
            dt           = 1.0/srate
            srate_dt     = srate
            if not(kwargs['run-type']=='post-processing'):
                if(kwargs['gaussian-noise']=='white'):
                    sys.stdout.write('Generating white gaussian noise with zero mean and sigma = {}.\n'.format(kwargs['gaussian-noise-white-sigma']))
                    rawstrain = np.random.normal(loc=0.0, scale=kwargs['gaussian-noise-white-sigma'], size=int(T*srate))
                elif('coloured' in kwargs['gaussian-noise']):
                    assert (signal_seglen==noise_seglen), "The injected psd is being interpolated on a frequency set determined by the noise seglen. A consistent signal seglen is required to obtain an unbiased estimation."
                    if not(kwargs['acf-{}'.format(ifo)]==''):
                        times_cgn, ACF_cgn  = kwargs['acf-{}'.format(ifo)]
                        C_cgn               = toeplitz(ACF_cgn)
                        cgn                 = multivariate_normal(mean = np.zeros(C_cgn.shape[0]), cov = C_cgn)
                        rawstrain           = cgn.rvs()
                    elif not(kwargs['psd-{}'.format(ifo)]==''):
                        psd_file            = kwargs['psd-{}'.format(ifo)]
                        sys.stdout.write('Generating coloured gaussian noise with zero mean and PSD given by {}\n'.format(psd_file))
                        freqs_file, psd_cgn = np.loadtxt(psd_file, unpack=True)
                        if('ASD' in psd_file):
                            warnings.warn("An ASD was passed, thus the ASD is being squared to compute the PSD.")
                            psd_cgn = psd_cgn*psd_cgn
                        N_points  = int(T*srate)
                        psd_cgn   = interp1d(freqs_file, psd_cgn, fill_value='extrapolate', bounds_error=False)
                        freqs_cgn = np.fft.rfftfreq(N_points, d = dt)
                        df_cgn    = np.diff(freqs_cgn)[0]
                        if(kwargs['gaussian-noise'] == 'coloured-TD'):
                            # FIXME: when chosen fixing a gaussian-noise-seed, it gives a MemoryError. To be tested.
                            review_warning()
                            sys.stdout.write('Generating the noise in time domain.\n')
                            # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
                            ACF_cgn             = 0.5*np.real(np.fft.irfft(psd_cgn(freqs_cgn)*df_cgn))*N_points
                            C_cgn              = toeplitz(ACF_cgn)
                            cgn                = multivariate_normal(mean = np.zeros(C_cgn.shape[0]), cov = C_cgn)
                            rawstrain          = cgn.rvs()
                        elif(kwargs['gaussian-noise'] == 'coloured-FD'):
                            sys.stdout.write('Generating the noise in frequency domain.\n')
                            # Range in which LIGO-Virgo noise is under control. Exact values are unimportant, since the PSD will be estimated from the generated strain after bandpassing is potentially applied.
                            f_min_inj = np.max([11.0, freqs_cgn.min()])
                            f_max_inj = np.min([4096., freqs_cgn.max()])
                            kmin = np.int(f_min_inj/df_cgn)
                            kmax = np.int(f_max_inj/df_cgn)
                            frequencies      = df_cgn*np.arange(0,N_points/2.+1)
                            frequency_strain = np.zeros(len(frequencies), dtype = np.complex64)
                            for i in range(kmin, kmax+1):
                                sigma_cgn = 0.5*np.sqrt(psd_cgn(frequencies[i])/df_cgn)
                                frequency_strain[i] = np.random.normal(0.0,sigma_cgn)+1j*np.random.normal(0.0,sigma_cgn)
                            rawstrain = np.real(np.fft.irfft(frequency_strain))*df_cgn*N_points
                        else:
                            raise ValueError("To generate gaussian noise, the allowed options are: 'white', 'coloured-TD', 'coloured-FD'.")
                    else:
                        raise Exception("If coloured gaussian noise is selected, an ACF or PSD from which the noise should be generated must be passed in input.")
                else:
                    raise ValueError("Unknown gaussian noise option selected.")
                np.savetxt(os.path.join(kwargs['output'],'Noise','rawstrain_gaussian_noise_{}_{:d}_{:d}_{:d}.txt'.format(ifo, int(starttime), int(T), int(srate))), rawstrain)
            else:
                sys.stdout.write('Reading the strain previously generated with gaussian noise.\n')
                rawstrain = np.loadtxt(os.path.join(kwargs['output'],'Noise','rawstrain_gaussian_noise_{}_{:d}_{:d}_{:d}.txt'.format(ifo, int(starttime), int(T), int(srate))))
        else:
            raise Exception("Either pass a data file, download data or generate data.")

    assert not((noise_chunk_size > T) or (signal_chunk_size > T)), "Noise ({} s) and signal ({} s) seglens must be shorter than data duration ({})".format(noise_chunk_size, signal_chunk_size, T)

    if (not(kwargs['data-{0}'.format(ifo)]=='') or (kwargs['download-data'] == 1)):
        # If there are nans, resize the strain to the longest segment which contains no nans.
        no_nans = 0
        while(no_nans == 0):
            if((np.isnan(rawstrain).any())):
                sys.stdout.write('Nans found in the data. Resizing strain.\n')
                new_rawstrain, new_starttime = resize_nan_strain(rawstrain, starttime, triggertime, signal_chunk_size, dt)
                starttime = new_starttime
                rawstrain = new_rawstrain
            else:
                no_nans = 1
        # Recompute the total length after resizing.
        T = len(rawstrain)*dt

    if(kwargs['bandpassing']):
        # Bandpassing section.
        sys.stdout.write('Bandpassing the raw strain between [{}, {}] Hz.\n'.format(f_min_bp, f_max_bp))
        # Create a Butterworth bandpass filter between [f_min, f_max] and apply it with the function filtfilt.
        bb, ab = butter(4, [f_min_bp/(0.5*srate_dt), f_max_bp/(0.5*srate_dt)], btype='band')
        strain = filtfilt(bb, ab, rawstrain)
    else:
        sys.stdout.write('No bandpassing applied.\n')
        strain = rawstrain
    # Check that the sample rate from the data is the same passed in the configuration file. In case they are different, either downsample or throw an error.
    if (srate > srate_dt):
        raise ValueError("You requested a sample rate higher than the data sampling.")
    elif (srate < srate_dt):
        sys.stdout.write('Downsampling detector data from {} to {} Hz, decimate factor {}\n'.format(srate_dt, srate, int(srate_dt/srate)))
        strain = decimate(strain, int(srate_dt/srate), zero_phase=True)
        dt     = 1./srate
    else:
        pass

    # Compute the index of the trigtime (estimate of the coalescence time of a signal or the time at which the injection should be placed).
    index_trigtime = int((triggertime-starttime)*srate)

    # Find the on-source chunk, centred on triggertime.
    mask = np.ones(len(strain), dtype=bool)
    if not((signal_seglen%2)==0):
        on_source_strain = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
        mask[range(index_trigtime-signal_seglen//2,index_trigtime+signal_seglen//2+1,1)] = False
    else:
        on_source_strain = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
        mask[range(index_trigtime-signal_seglen//2,index_trigtime+signal_seglen//2,1)]   = False

    #Excise the on-source chunk to avoid including the signal in the PSD computation.
    psd_strain = tuple((strain)[mask])

    # While it is true that no FFT is applied to the on-source chunk, the ACF is computed on a windowed chunk, thus to make a consistent likelihood computation, also the onsource chunk must be windowed when no truncation is applied.
    if (kwargs['window-onsource'] and kwargs['window']):
        if(kwargs['truncate']):
            warnings.warn("The on-source chunk should not be windowed when truncating data.")
        else:
            assert (signal_seglen==noise_seglen), "If a window is applied, the length of the signal chunk and of the noise chunk must be the same, otherwise with the same Tukey alpha-parameter PSD will be underestimated. Either choose different alphas or equal lengths."
        on_source_window = tukey(signal_seglen, alpha=alpha_window)
        on_source_strain = on_source_strain*on_source_window

    times = np.linspace(starttime, starttime+T-dt, len(strain))

    # ACF computation section.
    sys.stdout.write('Computing the one-sided PSD with the Welch method and the standard ACF for comparison.\n')
    psd_welch, freqs_welch = mlab.psd(psd_strain,
                                      Fs     = srate,
                                      NFFT   = noise_seglen,
                                      window = psd_window,
                                      sides  = 'onesided')
    df_welch = np.diff(freqs_welch)[0]

    # Case where the ACF was pre-computed or the run was already performed.
    if (not(kwargs['acf-{}'.format(ifo)]=='') or (kwargs['run-type']=='post-processing')):
        if(kwargs['run-type']=='post-processing'):
            acf_file = os.path.join(kwargs['output'],'Noise','ACF_TD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate))
            sys.stdout.write('Post-processing. Reading ACF from {}\n'.format(acf_file))
        else:
            assert (fft_acf), "Cannot compute ACF in time domain and load it from file."
            assert (kwargs['psd-{}'.format(ifo)]==''), "Both a PSD and an ACF from file can't be passed."
            acf_file = kwargs['acf-{}'.format(ifo)]
            sys.stdout.write('ACF was passed. Reading ACF from {}\n'.format(acf_file))

        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function, see eq. 7.15 of Maggiore Vol.1
        # We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        time, ACF = np.loadtxt(acf_file, unpack=True)
        dt_acf    = time[1]-time[0]
        assert (dt_acf == dt), "ACF (%r) and data (%r) sampling rates do not agree."%(dt_acf, dt)
        psd_ACF, freqs_acf = 2*np.real(np.fft.rfft(ACF*dt)), np.fft.rfftfreq(len(ACF), d=dt)
        plots.plot_ACF(time        = time,
                       acf         = ACF,
                       label       = '$\mathrm{ACF \,\, from \,\, file}$',
                       output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_acf,
                               psd1        = psd_ACF,
                               label1      = "$\mathrm{PSD \,\, from \,\, loaded ACF}$",
                               freqs2      = freqs_welch,
                               psd2        = psd_welch,
                               label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))

        whitening_PSD = interp1d(freqs_acf, psd_ACF)

    # Case where the PSD was pre-computed.
    elif (not(kwargs['psd-{}'.format(ifo)]=='') and (kwargs['gaussian-noise']=='')):

        # OPTIMISEME: for gaussian noise this is avoided just because of the way injections studies were performed during the review. To be relaxed in post O3a.
        assert (kwargs['acf-{}'.format(ifo)]==''), "Both a PSD and an ACF from file can't be passed."
        psd_file = kwargs['psd-{}'.format(ifo)]
        sys.stdout.write('PSD was passed. Reading PSD from {} and generating ACF accordingly.\n'.format(psd_file))
        if('PESummary' in psd_file):
            psd_datafile = np.genfromtxt(psd_file, names=True)
            freqs_from_file, psd_from_file = psd_datafile['Frequency'], psd_datafile['Strain']
        else:
            freqs_from_file, psd_from_file = np.loadtxt(psd_file, unpack=True)
        if('ASD' in psd_file):
            psd_from_file = psd_from_file*psd_from_file

        # Restrict to sensitive band (needed because BW PSD saturates to ~1 outside sensitive band and it screws up the likelihood)
        f_min_psd       = max(f_min_bp, 20.0)
        f_max_psd       = min(f_max_bp, 2038.0)
        psd_from_file   = psd_from_file[freqs_from_file > f_min_psd]
        freqs_from_file = freqs_from_file[freqs_from_file > f_min_psd]
        psd_from_file   = psd_from_file[freqs_from_file < f_max_psd]
        freqs_from_file = freqs_from_file[freqs_from_file < f_max_psd]

        # OPTIMISEME: test if leaving the original freq axis does not create issues with the remainder of the code (will probably need to redefine time axis)
        psd_from_file_interp           = interp1d(freqs_from_file, psd_from_file, fill_value='extrapolate', bounds_error=False)
        freqs_default                  = np.fft.rfftfreq(noise_seglen, d = dt)
        df_default                     = np.diff(freqs_default)[0]
        psd_interp                     = psd_from_file_interp(freqs_default)
        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        ACF_psd = 0.5*np.real(np.fft.irfft(psd_interp*df_default))*noise_seglen
        acfs    = [acf(x) for x in chunks(times, strain, noise_seglen, avoid=triggertime, window=kwargs['window'], alpha=alpha_window)]

        if(kwargs['noise-averaging-method']=='mean'):
            ACF_TD = np.mean(np.array(acfs), axis=0)
        elif(kwargs['noise-averaging-method']=='median'):
            # FIXME: This option gives rise to a junk spectrum. Currently not understood.
            review_warning()
            ACF_TD = np.median(np.array(acfs), axis=0)

        plots.plot_ACF(time        = dt*np.arange(len(ACF_psd)),
                       acf         = ACF_psd,
                       label       = '$\mathrm{ACF \,\, from \,\, file \,\, PSD}$',
                       output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_psd.pdf'.format(ifo)))
        plots.plot_ACF(time        = dt*np.arange(len(ACF_TD)),
                       acf         = ACF_TD,
                       label       = '$\mathrm{time \,\, domain \,\, ACF}$',
                       output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_TD.pdf'.format(ifo)))
        plots.plot_ACF_compare(time1       = dt*np.arange(len(ACF_TD)),
                               acf1        = ACF_TD,
                               label1      = '$\mathrm{time \,\, domain \,\, ACF}$',
                               time2       = dt*np.arange(len(ACF_psd)),
                               acf2        = ACF_psd,
                               label2      = '$\mathrm{ACF \,\, from \,\, PSD}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_TD_vs_ACF_from_PSD.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_from_file,
                               psd1        = psd_from_file,
                               label1      = '$\mathrm{PSD \,\, from \,\, file}$',
                               freqs2      = freqs_welch,
                               psd2        = psd_welch,
                               label2      = '$\mathrm{Welch, \,\, frequency \,\, domain}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_file_vs_Welch.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_from_file,
                               psd1        = psd_from_file,
                               label1      = '$\mathrm{PSD \,\, from \,\, file}$',
                               freqs2      = freqs_default,
                               psd2        = psd_interp,
                               label2      = '$\mathrm{PSD \,\, interpolated}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_file_vs_interp.pdf'.format(ifo)))
        whitening_PSD = psd_from_file_interp
        ACF           = ACF_psd

        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_from_PSD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF)), ACF)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_TD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF_TD)), ACF_TD)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_file_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_from_file, psd_from_file)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_Welch_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))

    #Case where the PSD is to be computed following the MaxEnt method.
    elif (not(kwargs['maxent-psd']=='')):
        review_warning()
        assert (fft_acf), "Cannot compute ACF in time domain and compute MaxEnt PSD."
        freqs_default = np.fft.rfftfreq(noise_seglen, d = dt)
        df_default    = np.diff(freqs_default)[0]
        if(kwargs['maxent-psd']=='average'):
            sys.stdout.write('Computing the one-sided average PSD with the MESA method.\n')
            M_max       = int(2.*noise_seglen/np.log(2.*noise_seglen))
            psds        = [mem_psd(freqs_default, dt, data, M_max) for data in chunks(times, strain, noise_seglen, avoid=triggertime, window=kwargs['window'], alpha=alpha_window)]

            if(kwargs['noise-averaging-method']=='mean'):
                psd_maxent = np.mean(np.array(psds), axis=0)
            elif(kwargs['noise-averaging-method']=='median'):
                # TO-BE-TESTED
                review_warning()
                psd_maxent = np.median(np.array(psds), axis=0)

            ACF         = 0.5*np.real(np.fft.irfft(psd_maxent*df_default))*noise_seglen
        else:
            M_max = int(2.*signal_seglen/np.log(2.*signal_seglen))
            if(kwargs['maxent-psd']=='onsource-chunk'):
                sys.stdout.write('Computing the one-sided PSD with the MESA method on the onsource chunk.\n')
                if not((signal_seglen%2)==0):
                    data = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
                else:
                    data = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
            elif(kwargs['maxent-psd']=='pre-onsource-chunk'):
                sys.stdout.write('Computing the one-sided PSD with the MESA method on the pre-onsource chunk.\n')
                if not((signal_seglen%2)==0):
                    data = strain[index_trigtime-signal_seglen//2-signal_seglen:index_trigtime-signal_seglen//2+1]
                else:
                    data = strain[index_trigtime-signal_seglen//2-signal_seglen:index_trigtime-signal_seglen//2]
            elif(kwargs['maxent-psd']=='post-onsource-chunk'):
                sys.stdout.write('Computing the one-sided PSD with the MESA method on the post-onsource chunk.\n')
                if not((signal_seglen%2)==0):
                    data = strain[index_trigtime+signal_seglen//2:index_trigtime+signal_seglen//2+1+signal_seglen]
                else:
                    data = strain[index_trigtime+signal_seglen//2:index_trigtime+signal_seglen//2+signal_seglen]
            psd_maxent = mem_psd(freqs_default, dt, data, M_max)
            # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
            ACF = 0.5*np.real(np.fft.irfft(psd_maxent*df_default))*signal_seglen

        plots.plot_ACF(time        = dt*np.arange(len(ACF)),
                       acf         = ACF,
                       label       = '$\mathrm{ACF \,\, from \,\, MaxEnt}$',
                       output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_default,
                               psd1        = psd_maxent,
                               label1      = "$\mathrm{PSD \,\, from \,\, MaxEnt}$",
                               freqs2      = freqs_welch,
                               psd2        = psd_welch,
                               label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_MaxEnt_{}_{}_{}_{}_{}_{}.txt'.format(kwargs['maxent-psd'], ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_default, psd_maxent)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_Welch_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))
        whitening_PSD = psd_maxent

    #Case where the ACF is computed from the data.
    else:
        if not(kwargs['injection-approximant']==''):
            sys.stdout.write ('Although an injection was selected, the ACF is being computed from the strain.\n')
        else:
            sys.stdout.write('No ACF was passed. Estimating ACF.\n')
        acfs          = [acf(x, fft=fft_acf, simple_norm=kwargs['acf-simple-norm']) for x in chunks(times, strain, noise_seglen, avoid=triggertime, window=kwargs['window'], alpha=alpha_window)]

        if(kwargs['noise-averaging-method']=='mean'):
            ACF = np.mean(np.array(acfs), axis=0)
        elif(kwargs['noise-averaging-method']=='median'):
            # FIXME: This option gives rise to a junk spectrum. Currently not understood.
            review_warning()
            ACF = np.median(np.array(acfs), axis=0)

        freqs_default = np.fft.rfftfreq(noise_seglen, d=dt)
        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        psd_ACF       = 2*np.real(np.fft.rfft(ACF*dt))

        plots.plot_ACF(time        = dt*np.arange(len(ACF)),
                       acf         = ACF,
                       label       = '$\mathrm{ACF \,\, TD}$',
                       output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))

        if(kwargs['PSD-investigation']):
            review_warning()
            sys.stdout.write('Plotting PSDs relative to all chunks.\n')
            psds_acf = [2*np.real(np.fft.rfft(single_acf*dt)) for single_acf in acfs]
            plt.figure()
            for single_psd in psds_acf:
                plt.loglog(freqs_default, single_psd)
            plt.xlabel(r"$f\,(Hz)$",        fontsize=18)
            plt.ylabel(r"$S(f)\,(Hz^{-1})$",fontsize=18)
            plt.savefig(os.path.join(kwargs['output'],'Noise','{}_PSD_investigation.pdf'.format(ifo)), bbox_inches='tight')
            exit()

        plots.plot_PSD_compare(freqs1      = freqs_welch,
                               psd1        = psd_welch,
                               label1      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                               freqs2      = freqs_default,
                               psd2        = psd_ACF,
                               label2      = "$\mathrm{time \,\, domain}$",
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))

        if (not(kwargs['psd-{}'.format(ifo)]=='') and not(kwargs['gaussian-noise']=='')):
            # Case where you passed a PSD, generated gaussian noise with it and estimated the PSD from the noise generated. Check if the PSD injected resembles the estimation.
            freqs_from_file, psd_from_file = np.loadtxt(kwargs['psd-{}'.format(ifo)], unpack=True)
            if('ASD' in psd_file):
                psd_from_file = psd_from_file*psd_from_file
            plots.plot_PSD_compare(freqs1      = freqs_from_file,
                                   psd1        = psd_from_file,
                                   label1      = "$\mathrm{PSD \,\, from \,\, file}$",
                                   freqs2      = freqs_welch,
                                   psd2        = psd_welch,
                                   label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                                   output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_injected.pdf'.format(ifo)))

        if(kwargs['non-stationarity-check']):
            review_warning()
            #Check if there is any trend in PSD evolution.
            # color = iter(cm.viridis(np.linspace(0,1,len(acfs))))
            #FIXME(optional): tolerance needs to be tested. Stochastic group plenary talk LVC Sept 2019 used tolerance=0.2
            plt.figure()
            counter = 0
            #FIXME(optional): random value, test it
            tolerance = 4.0
            sys.stdout.write('Non-stationarity check (%f maximum tolerated variation)\n'%tolerance)
            for idx in range(len(acfs)):
                psd_x   = 2*np.real(np.fft.rfft(acfs[idx]*dt))
                if not(idx==0 or idx==(len(acfs)-1)):
                    psd_pre  = 2*np.real(np.fft.rfft(acfs[idx-1]*dt))
                    psd_post = 2*np.real(np.fft.rfft(acfs[idx+1]*dt))
                    for x in range(0, len(psd_x)):
                        statistic = np.abs(psd_x[x] - ((psd_post[x] + psd_pre[x])/2.))/psd_x[x]
                        if(statistic > tolerance): counter = counter + 1
                    sys.stdout.write('Number of non-stationary bins in chunk %d: %d/%d.\n'%(idx, counter, len(freqs_default)))
                    counter          = 0
        #        c = next(color)
        #        plt.loglog(freqs2, psd_x, lw=0.1, alpha=0.5, c=c)
        #    plt.xlabel(r"$f\,(Hz)$",        fontsize=18)
        #    plt.ylabel(r"$S(f)\,(Hz^{-1})$",fontsize=18)
        #    plt.legend()
        #    plt.savefig(os.path.join(kwargs['output'],'Noise','{}_PSD_variation.pdf'.format(ifo)), bbox_inches='tight')
        #            plt.close('all')

        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_TD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF)), ACF)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_from_ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_default, psd_ACF)))

        whitening_PSD = interp1d(freqs_default, psd_ACF)

    # Let's check if Plancherel theorem is verified by our ACF estimate
    # by using the fact that twice the Fourier transform of the ACF = one-sided PSD.
    # Since the psd is the one-sided, we only stored positive values, but Plancherel theorem must be evaluated on both positive and negative frequencies. Take into account the fact that the window absorbed some power.
    sys.stdout.write('Plancherel theorem E(f)/E(t) (expected value: 1) = {}\n'.format(psd_window_norm*2.*np.sum(df_welch*psd_welch**2)/np.sum(dt*(2.*ACF)**2)))

    # Restrict the ACF on the signal chunk and produce the covariance matrix from the ACF.
    if(kwargs['truncate']):
        ACF_signal = ACF[:kwargs['analysis-duration-n']]
        np.savetxt(kwargs['output']+'/Noise/ACF_TD_cropped_{}_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate, kwargs['analysis-duration']), ACF_signal)
    else:
        ACF_signal = ACF[:signal_seglen]
    Covariance_matrix_signal = toeplitz(ACF_signal)



    if not(kwargs['signal-chunksize']==kwargs['noise-chunksize']):
        warnings.warn("A different chunksize between signal and noise implies an incorrect normalization of the autocorrelation function. This configuration should not be used for production runs.")
    if (kwargs['chisquare-computation']):

        # Do a check of the reduced chisq, skipping the onsource chunk - useful for checking normalisation.
        Covariance_matrix                = toeplitz(ACF)
        Inverse_Covariance_matrix        = inv(Covariance_matrix)
        Inverse_covariance_matrix_signal = inv(Covariance_matrix_signal)
        chisq                            = [np.einsum('i,ij,j', x, Inverse_Covariance_matrix, x) for x in chunks(times, strain, noise_seglen, avoid=triggertime, window=kwargs['window'], alpha=alpha_window)]
        sys.stdout.write('Average reduced chisquare (expected value ~1) = {:.5f}\n'.format(np.mean(chisq)/Inverse_Covariance_matrix.shape[0]))

        # A value of onsource chisquare significantly different from 0 indicates that the data in this chunk do not follow the distribution of the noise, which is true if a signal is present.
        sigchisq=np.einsum('i,ij,j', on_source_strain, Inverse_covariance_matrix_signal, on_source_strain)
        sys.stdout.write('Chisquare on source (expected value >> 1): {}\n'.format(sigchisq))

    # Injection section.
    if not(kwargs['injection-approximant']==''):

        # Inject the NR signal
        if((kwargs['injection-approximant']=='NR') or ('LAL' in kwargs['injection-approximant'])):
            strain_injection = inject_IMR_signal(strain.shape[0], starttime, T, ifo, triggertime = triggertime, **kwargs)
        else:
            strain_injection = inject_ringdown_signal(strain.shape[0], starttime, T, ifo, triggertime = triggertime, **kwargs)

        # Pass as output for the strain the on-source chunk.
        if not((signal_seglen%2)==0):
            on_source_injection = strain_injection[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
        else:
            on_source_injection = strain_injection[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
        # Add noise on top of injection
        if not(kwargs['zero-noise']):
            sys.stdout.write('Adding noise on top of injection.\n')
            on_source_strain += on_source_injection
        else:
            on_source_strain  = on_source_injection
            sys.stdout.write('Zero noise injection selected.\n')
    else:
        assert not((kwargs['data-{}'.format(ifo)]=='') and (kwargs['download-data'] == 0)), "No data was passed and no injection has been selected. Exiting."

    # We are done with the strain.
    del rawstrain, strain

    # Return the time series, the covariance matrix and the PSD used in the whitened waveform plot.
    return on_source_strain, Covariance_matrix_signal, whitening_PSD

# From here onwards it's old and/or unused stuff.

def mem_psd(freqs_LAL, dt, data, M_max):

    review_warning()

    return mem.psd(freqs_LAL, dt, data, M_max)

def UNCHECKED_td_whiten(strain, inv_cov):

    """
        Perform time-domain whitening
        Parameters
        ====
        strain : np.ndarray
        inv_cov    : inverse covariance matrix

        Returns
        ====
        A whitened time-domain np.ndarray
    """
    review_warning()

    m = cholesky(inv_cov)

    return np.dot(strain,m)

def UNCHECKED_acf_from_ideal_psd(ASDtxtfile, fmin, srate, T):

    review_warning()
    def interpolate_psd(psd_in, f_in, df_out, fmin, srate):
        f_out = np.arange(fmin, srate/2., df_out)
        return f_out, np.interp(f_out, f_in, psd_in)

    # Read PSD from file
    f, asd  = np.loadtxt(ASDtxtfile, unpack = True)
    dt      = 1./srate
    psd     = asd**2

    # Interpolate PSD on a chosen set of frequencies
    fo, psd = interpolate_psd(psd, f, 1./T, f.min(), srate)

    # Build the ACF
    R   = np.fft.irfft(psd)*srate
    lag = np.linspace(0,T/2.,len(R))

    return lag, R

def UNCHECKED_estimated_acf(x):
    review_warning()
    n = len(x)
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    return r/np.arange(n, 0, -1)

def UNCHECKED_acf_finite(y,k):

  """
  Estimate directly from the data y
  Weighting by 1/(N-i) for lag i where N=len(y)
  k specifies the desired size of the ACF,
  i.e. the number of samples in the on-source segment
  """

  review_warning()
  N=len(y)
  R = [sum(y[:N-i]*y[i:N])/(N-i) for i in range(k)]

  return R

def UNCHECKED_estimate_cvm(datachunks,N_onsource):

  """
  Use the list datachunks of time series,
  estimate the CVM and return the covariance
  matrix of dimension N_onsource & N_onsource
  """

  review_warning()
  acfs=[acf_finite(x,N_onsource) for x in datachunks]
  ACF=np.array(acfs).mean(axis=0)
  ACF = ACF[:N_onsource]

  return toeplitz(ACF)
