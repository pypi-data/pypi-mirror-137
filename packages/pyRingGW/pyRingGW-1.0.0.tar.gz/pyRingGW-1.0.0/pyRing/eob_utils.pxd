cdef double _JimenezFortezaRemnantSpin(double nu, double chi1, double chi2) nogil
cdef double _JimenezFortezaRemnantMass(double m1, double m2, double chi1, double chi2) nogil
cdef double _omega_peak(double nu, double X12, double S_hat, double aK, int l, int m) nogil
cdef double _amplitude_peak(double nu, double X12, double S_hat, double a12, double S_bar, double aK, double omega_peak, int l, int m) nogil
cdef double _dOmega(double omega1, double Mf, double omega_peak) nogil
cdef double _c4_phi(double nu, double X12, double S_hat, int l, int m) nogil
cdef double _c3_phi(double nu, double X12, double S_hat, int l, int m) nogil
cdef double _c3_A(double nu, double X12, double S_hat, double a12, int l, int m) nogil
cdef double _omega1(double af, int l, int m) nogil
cdef double _alpha21(double af, int l, int m) nogil
cdef double _alpha1(double af, int l, int m) nogil
cdef double _a_K(double m1, double m2, double s1z, double s2z) nogil
cdef double _a_12(double m1, double m2, double s1z, double s2z) nogil
cdef double _S_bar(double m1, double m2, double s1z, double s2z) nogil
cdef double _S_hat(double m1, double m2, double s1z, double s2z) nogil
cdef double _X_12(double m1, double m2) nogil
cdef double _sym_mass_ratio(double m1, double m2) nogil
cdef double _DeltaT(double m1,double m2, double s1z, double s2z, unsigned int l, int m) nogil
cdef double _DeltaPhi(double m1, double m2, double s1z, double s2z, unsigned int l, int m) nogil
