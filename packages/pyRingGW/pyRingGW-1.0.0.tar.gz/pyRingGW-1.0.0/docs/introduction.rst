Introduction
-------------

``pyRing`` is a python package for black hole (BH) ringdown analysis, model comparison and parameter estimation.
The package is tailored for the analysis of the post-merger phase of Compact Binary Coalescence (CBC) Gravitational-wave (GW) signals using a native time-domain likelihood formulation. It is integrated with standard LIGO-Virgo-Kagra software and supports:

* Ringdown analyses of interferometric or simulated GW data using a variety of ringdown waveform models. All of them are analytical templates, some of them are calibrated to Numerical Relativity (NR).
* Parametrised tests of General Relativity (GR), by adding parametrised deviations to the spectrum frequencies and damping times.
* Quasi-normal modes (QNM) spectrum predictions for emissions alternative to the Kerr solution.

The main usage features of the software have been internally reviewed for scientific usage from the LIGO-Virgo-Kagra (LVK) collaboration and the code is routinely used to produce catalogs of BH ringdown properties and tests of GR in the merger-ringdown regime by the LVK collaboration. 
