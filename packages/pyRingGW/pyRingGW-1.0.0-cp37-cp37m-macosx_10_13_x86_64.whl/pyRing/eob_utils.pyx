#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: cdivision=True
#cython: language_level=3
#cython: embedsignature=True

from libc.math cimport cbrt, sqrt, exp, fabs

# Module to collect EOB utils


cdef double _sym_mass_ratio(double m1, double m2) nogil:

    cdef double q = m2/m1
    return q/((1.0+q)*(1.0+q))


cdef inline double _X_12(double m1, double m2) nogil:

    return (m1 - m2)/(m1 + m2)


cdef inline double _S_hat(double m1, double m2, double s1z, double s2z) nogil:

    return (m1*m1*s1z + m2*m2*s2z)/((m1+m2)*(m1+m2))


cdef inline double _S_bar(double m1, double m2, double s1z, double s2z) nogil:

    return 0.5*((m1*s1z - m2*s2z)/((m1+m2))+((m1-m2)*(m1*s1z + m2*s2z))/((m1+m2)*(m1+m2)))


cdef inline double _a_12(double m1, double m2, double s1z, double s2z) nogil:

    return (m1*s1z - m2*s2z)/(m1+m2)


cdef inline double _a_K(double m1, double m2, double s1z, double s2z) nogil:

    return (m1*s1z + m2*s2z)/(m1+m2)


cdef double _alpha1(double af, int l, int m) nogil:

    # This function computes the inverse of the dimensionless ringdown fundamental (n=0) damping time.

    cdef double res = 0.
    cdef double af2 = af*af
    cdef double af3 = af*af*af
    cdef double alpha1_c, alpha1_d

    if ((l==2) and (m==2)):
        res  = 0.08896*(1 - 1.90036*af + 0.86200*af2 + 0.0384893*af3)/(1 - 1.87933*af + 0.88062*af2)
    elif ((l==2) and (m==1)):
        res = 0.0889623*(1-1.31253*af-0.21033*af2+0.52502*af3)/(1-1.30041*af-0.1566*af2+0.46204*af3)
    elif ((l==3) and (m==3)):
        res = 0.0927030*(1-1.8310*af+0.7568*af2+0.0745*af3)/(1-1.8098*af+0.7926*af2+0.0196*af3)
    elif ((l==3) and (m==2)):
        res = 0.0927030*(1-1.58277*af+0.2783*af2+0.30503*af3)/(1-1.56797*af+0.3290*af2+0.24155*af3)
    elif ((l==3) and (m==1)):
        res = 0.0927030*(1-1.2345*af-0.30447*af2+0.5446*af3)/(1-1.2263*af-0.24223*af2+0.47738*af3)
    elif ((l==4) and (m==4)):
        res = 0.0941640*(1-1.8662*af+0.8248*af2+0.0417*af3)/(1-1.8514*af+0.8736*af2-0.0198*af3)
    elif ((l==4) and (m==3)):
        res = 0.0941640*(1-1.7177*af+0.5320*af2+0.1860*af3)/(1-1.7065*af+0.5876*af2+0.120939*af3)
    elif ((l==4) and (m==2)):
        res = 0.0941640*(1-1.44152*af+0.0542*af2+0.39020*af3)/(1-1.43312*af+0.1167*af2+0.32253*af3)
    elif ((l==4) and (m==1)):
        res = 0.190170*(1+1.0590157*af-0.8650630*af2-0.75222*af3)/(1+1.0654880*af-0.7830051*af2-0.65814*af3)
    elif ((l==5) and (m==5)):
        res = +0.0948705*(1-1.8845*af+0.8585*af2+0.0263*af3)/(1-1.8740*af+0.9147*af2-0.0384*af3)

    return res


cdef double _alpha21(double af, int l, int m) nogil:

    # This function computes the difference between the inverse of the dimensionless ringdown damping time of the first (n=1) and fundamental (n=0) overtones.
    cdef double res = 0.
    cdef double af2 = af*af
    cdef double af3 = af*af*af
    cdef double alpha21_c, alpha21_d

    if ((l==2) and (m==2)):
        res = 0.184953*(1 - 1.89397*af + 0.88126*af2 + 0.0130256*af3)/(1 - 1.83901*af + 0.84162*af2)
    elif ((l==2) and (m==1)):
        res = 0.184952*(1-1.1329*af-0.3520*af2+0.4924*af3)/(1-1.10334*af-0.3037*af2+0.4262*af3)
    elif ((l==3) and (m==3)):
        res = 0.188595*(1-1.8011*af+0.7046*af2+0.0968*af3)/(1-1.7653*af+0.7176*af2+0.0504*af3)
    elif ((l==3) and (m==2)):
        res = 0.188595*(1-1.5212*af+0.1563*af2+0.3652*af3)/(1-1.4968*af+0.1968*af2+0.3021*af3)
    elif ((l==3) and (m==1)):
        res = 0.188595*(1-1.035*af-0.3816*af2+0.4486*af3)/(1-1.023*af-0.3170*af2+0.3898*af3)
    elif ((l==4) and (m==4)):
        res = 0.190170*(1-1.8546*af+0.8041*af2+0.0507*af3)/(1-1.8315*af+0.8391*af2-0.0051*af3)
    elif ((l==4) and (m==3)):
        res = 0.190170*(1-1.6860*af+0.4724*af2+0.2139*af3)/(1-1.6684*af+0.5198*af2+0.1508*af3)
    elif ((l==4) and (m==2)):
        res = 0.190170*(1-1.38840*af+0.39333*af3)/(1-1.37584*af+0.0600017*af2+0.32632*af3)
    elif ((l==4) and (m==1)):
        res = 0.190170*(1+1.0590157*af-0.8650630*af2-0.75222*af3)/(1+1.0654880*af-0.7830051*af2-0.65814*af3)
    elif ((l==5) and (m==5)):
        res = 0.190947*(1-1.8780*af+0.8467*af2+0.0315*af3)/(1-1.8619*af+0.8936*af2-0.0293*af3)

    return res


cdef double _omega1(double af, int l, int m) nogil:

    # This function computes the dimensionless ringdown fundamental (n=0) frequency.

    cdef double res = 0.
    cdef double af2 = af*af
    cdef double af3 = af*af*af
    cdef double omega1_c, omega1_d

    if ((l==2) and (m==2)):
        res = 0.373672*(1 - 1.5367*af + 0.5503*af2)/(1 - 1.8700*af + 0.9848*af2 - 0.10943*af3)
    elif ((l==2) and (m==1)):
        res = 0.373672*(1-0.79546*af-0.1908*af2+0.11460*af3)/(1-0.96337*af-0.1495*af2+0.19522*af3)
    elif ((l==3) and (m==3)):
        res = 0.599443*(1-1.84922*af+0.9294*af2-0.07613*af3)/(1-2.18719*af+1.4903*af2-0.3014*af3)
    elif ((l==3) and (m==2)):
        res = +0.599443*(1-0.251*af-0.891*af2+0.2706*af3)/(1-0.475*af-0.911*af2+0.4609*af3)
    elif ((l==3) and (m==1)):
        res = +0.599443*(1-0.70941*af-0.16975*af2+0.08559*af3)/(1-0.82174*af-0.16792*af2+0.14524*af3)
    elif ((l==4) and (m==4)):
        res = 0.809178*(1-1.83156*af+0.9016*af2-0.06579*af3)/(1-2.17745*af+1.4753*af2-0.2961*af3)
    elif ((l==4) and (m==3)):
        res = +0.809178*(1-1.8397*af+0.9616*af2-0.11339*af3)/(1-2.0979*af+1.3701*af2-0.2675*af3)
    elif ((l==4) and (m==2)):
        res = +0.809178*(1-0.6644*af-0.3357*af2+0.1425*af3)/(1-0.8366*af-0.2921*af2+0.2254*af3)
    elif ((l==4) and (m==1)):
        res = +0.809178*(1-0.68647*af-0.1852590*af2+0.0934997*af3)/(1-0.77272*af-0.1986852*af2+0.1485093*af3)
    elif ((l==5) and (m==5)):
        res = 1.012295*(1-1.5659*af+0.5783*af2)/(1-1.9149*af+1.0668*af2-0.14663*af3)

    return res


cdef double _c3_A(double nu, double X12, double S_hat, double a12, int l, int m) nogil:

    cdef double res = 0., b1, b2, b3
    if ((l==2) and (m==2)):
        b1 = 0.1659421
        b2 = -0.2560047
        b3 = -0.9418946
        res = -0.5585 + 0.81196*nu + (-0.398576+b1*X12)*S_hat + (0.099805+b2*X12)*S_hat*S_hat + (0.72125+b3*X12)*S_hat*S_hat*S_hat
    elif ((l==2) and (m==1)):
        res = (0.23882-2.2982*nu+5.7022*nu*nu)/(1-7.7463*nu+27.266*nu*nu)
    elif ((l==3) and (m==3)):
        b1  = -0.3502608
        b2  = 1.587606
        b3  = -1.555325
        res = -0.41455+1.3225*nu+(b1+b2*X12+b3*X12*X12)*a12
    elif ((l==3) and (m==2)):
        res = (0.1877-3.0017*nu+19.501*nu*nu)/(1-1.8199*nu)-exp(-703.67*(nu-2/9)*(nu-2/9))
    elif ((l==3) and (m==1)):
        res = (3.5042-55.171*nu+217*nu*nu)/(1-15.749*nu+605.17*nu*nu*nu)
    elif ((l==4) and (m==4)):
        b1  = -9.614738
        b2  = 122.461125
        res = -0.41591 +3.2099*nu+b1*nu*S_hat+b2*nu*S_hat*S_hat
    elif ((l==4) and (m==3)):
        res = (-0.02833+2.8738*nu-31.503*nu*nu+93.513*nu*nu*nu)/(1-10.051*nu+156.14*nu*nu*nu)
    elif ((l==4) and (m==2)):
        res = (0.27143-2.2629*nu+4.6249*nu*nu)/(1-7.6762*nu+15.117*nu*nu)
    elif ((l==4) and (m==1)):
        res = 11.47+10.936*nu
    elif ((l==5) and (m==5)):
        if (a12==0.): res = (-0.19751+3.607*nu-14.898*nu*nu)/(1-20.046*nu+108.42*nu*nu)
        else:         res = (-7.063079+65.464944*nu+(+(-2.055335-0.585373*X12)*a12+(-12.631409+19.271346*X12)*a12*a12))

    return res


cdef double _c3_phi(double nu, double X12, double S_hat, int l, int m) nogil:

    cdef double res = 0., b1, b2, b3, b4
    if ((l==2) and (m==2)):
        b1  = -1.323643
        b2  = -3.555007
        b3  = 7.011267
        b4  = 32.737824
        res = 3.8436 + 0.71565*nu + (5.12794+b1*X12)*S_hat + (9.9136+b2*X12)*S_hat*S_hat + (-4.1075+b3*X12)*S_hat*S_hat*S_hat +(-31.5562+b4*X12)*S_hat*S_hat*S_hat*S_hat
    elif ((l==2) and (m==1)):
        res = (2.6269-37.677*nu+181.61*nu*nu)/(1-16.082*nu+89.836*nu*nu)
    elif ((l==3) and (m==3)):
        b1  = -0.634377
        b2  = 5.983525
        b3     = -5.881900
        res = 3.0611 -6.1597*nu+(b1+b2*X12+b3*X12*X12)*S_hat
    elif ((l==3) and (m==2)):
        res = (0.90944-1.8924*nu+3.6848*nu*nu)/(1-8.9739*nu+21.024*nu*nu)
    elif ((l==3) and (m==1)):
        if (nu>0.08271): nu_x = 0.08271
        else: nu_x = nu
        res = (-6.1719+29.617*nu_x+254.24*nu_x*nu_x)/(1-1.5435*nu_x)
    elif ((l==4) and (m==4)):
        b1  = 7.911653
        b2  = 21.181688
        res = (3.6662-30.072*nu +76.371*nu*nu)/(1-3.5522*nu)+((-4.9184+b1*X12)*S_hat+(-15.6772+b2*X12)*S_hat*S_hat)
    elif ((l==4) and (m==3)):
        res = (2.284-23.817*nu+70.952*nu*nu)/(1-10.909*nu+30.723*nu*nu)
    elif ((l==4) and (m==2)):
        res = (2.2065-17.629*nu+65.372*nu*nu)/(1-4.7744*nu+3.1876*nu*nu)
    elif ((l==4) and (m==1)):
        if (nu>=10/121): res = -6.0286+46.632*nu
        else:            res = -2.1747
    elif ((l==5) and (m==5)):
        if S_hat==0.: res = 0.83326+10.945*nu
        else:         res = (-1.510167+30.569461*nu+(+((-2.687133+4.873750*X12))*S_hat+(-14.629684+19.696954*X12)*S_hat*S_hat))

    return res


cdef double _c4_phi(double nu, double X12, double S_hat, int l, int m) nogil:

    cdef double res = 0., b1, b2, b3, nu_d
    if ((l==2) and (m==2)):
        b1  = 0.779683
        b2  = -0.069638
        res = 1.4736 + 2.2337 * nu + (8.26539 + b1*X12 ) * S_hat + (14.2053 + b2*X12) *S_hat*S_hat
    elif ((l==2) and (m==1)):
        res = (4.355-53.763*nu+188.06*nu*nu)/(1-18.427*nu+147.16*nu*nu)
    elif ((l==3) and (m==3)):
        b1  = -3.877528
        b2  = 12.043300
        b3  = -6.524665
        res = 1.789-5.6684*nu+(b1+b2*X12+b3*X12*X12)*S_hat
    elif ((l==3) and (m==2)):
        res = (2.3038-50.79*nu+334.41*nu*nu)/(1-18.326*nu+99.54*nu*nu)
    elif ((l==3) and (m==1)):
        res = (3.6485+5.4536*nu)
    elif ((l==4) and (m==4)):
        b1  = 11.746452
        b2  = 34.922883
        res = 0.21595+23.216*nu+(-3.4207+b1*X12)*S_hat+(-15.5383+b2*X12)*S_hat*S_hat
    elif ((l==4) and (m==3)):
        res = (2.4966-6.2043*nu)/(1-252.47*nu*nu*nu*nu)
    elif ((l==4) and (m==2)):
        if (nu>=2.5/12.25): res = (132.56-1155.5*nu+2516.8*nu*nu)/(1-3.8231*nu)
        else: res = (-0.58736+16.401*nu)/(1-4.5202*nu)
    elif ((l==4) and (m==1)):
        res = 1.6629+11.497*nu
    elif ((l==5) and (m==5)):
        if S_hat==0.: res = (0.45082-9.5961*nu+52.88*nu*nu)/(1-19.808*nu+99.078*nu*nu)
        else:         res = (-1.383721+56.871881*nu+((+7.198729-3.870998*X12)*S_hat+(-25.992190+36.882645*X12)*S_hat*S_hat))

    return res


cdef inline double _dOmega(double omega1, double Mf, double omega_peak) nogil:

    return omega1 - Mf * omega_peak


cdef double _amplitude_peak(double nu, double X12, double S_hat, double a12, double S_bar, double aK, double omega_peak, int l, int m) nogil:

    cdef double res = 0., scale
    cdef double ATP, ATPc, AS, Aorb, A_spin, a1Amp, a2Amp, a3Amp, a1AmpS, a2AmpS, a3AmpS, a1, a2, a3, Amax_tp, Amax1, Amax2, orb_A, num_A, denom_A, A_orb, S_bar21, Aspin
    cdef double b1, b2, b3, b4, b5, b6, b7, b8, b9, b1Amp, b2Amp, b3Amp, b4Amp, b11Amp, b12Amp, b13Amp, b14Amp, b21Amp, b22Amp, b23Amp, b24Amp, b31Amp, b32Amp, b33Amp, b34Amp, b1Amax, b2Amax, b3Amax
    cdef double c13Amp, c14Amp, c23Amp, c24Amp, c11Amp, c12Amp, c21Amp, c22Amp, c31Amp, c32Amp, c41Amp, c42Amp, c1Amp, c2Amp, c3Amp, c4Amp, c5Amp, c6Amp, c1Amax, c2Amax, c3Amax, c4Amax

    if ((l==2) and (m==2)):

        scale   = 1 - S_hat*omega_peak
        # Orbital fits calibrated to the non-spinning SXS data
        Amax_tp = 1.44959

        Amax1 	= -0.041285
        Amax2 	= 1.5971

        orb_A	= Amax_tp*(1+Amax1*nu+Amax2*nu*nu)

        # Equal Mass fit calibrated to the q=1 SXS data
        b1Amax 	= -0.741
        b2Amax  = -0.0887
        b3Amax	= -1.094

        # Unequal Mass corrections to the q=1 fit based on SXS, BAM and TP data
        c1Amax  = 0.4446696
        c2Amax  = -0.3254310
        c3Amax  = 0.4582812
        c4Amax  = -0.2124477
        num_A   = 1+((b1Amax+c1Amax*X12)/(1+c2Amax*X12))*S_hat+b2Amax*S_hat*S_hat
        denom_A = 1+((b3Amax+c3Amax*X12)/(1+c4Amax*X12))*S_hat
        res     = orb_A*scale*num_A*(1/denom_A)

    elif ((l==2) and (m==1)):

        ATP 	= 0.523877
        A_orb   = ATP*X12*(1+3.3362232268*nu+3.4708521429*nu*nu)/(1+4.7623643259*nu)
        b1      = +0.891139
        b2 		= -5.191702
        b3 		= +3.480139
        b4 		= +10.237782
        b5 		= -13.867475
        b6 		= +10.525510
        if (nu==0.25):
            S_bar21 = - fabs(S_bar)
            AS      = ((-0.4281863+b1*nu+b2*nu*nu)*S_bar21+(-0.335659+b3*nu+b4*nu*nu)*S_bar21*S_bar21)/(1+(+0.828923+b5*nu+b6*nu*nu)*S_bar21)
        else:
            AS      = ((-0.4281863+b1*nu+b2*nu*nu)*S_bar+(-0.335659+b3*nu+b4*nu*nu)*S_bar*S_bar)/(1+(+0.828923+b5*nu+b6*nu*nu)*S_bar)
        res = (A_orb+AS)

    elif ((l==3) and (m==3)):

        ATPc    = 0.5660165890*X12
        a1Amp   = -0.22523
        a2Amp   = 3.0569
        a3Amp   = -0.396851
        Aorb    = (1+a1Amp*nu + a2Amp*nu*nu)/(1+a3Amp*nu)
        b1Amp   = 0.100069
        b2Amp   = -0.455859
        c1Amp   = -0.401156
        c2Amp   = -0.141551
        c3Amp   = -15.4949
        c4Amp   = 1.84962
        c5Amp   = -2.03512
        c6Amp   = -4.92334
        b1Amp   = (b1Amp+c1Amp*nu)/(1+c2Amp*nu+c3Amp*nu*nu)
        b2Amp   = (b2Amp+c4Amp*nu)/(1+c5Amp*nu+c6Amp*nu*nu)
        Aspin   = (b1Amp*a12)/(1+b2Amp*a12)
        res     = ATPc*Aorb + Aspin

    elif ((l==3) and (m==2)):

        ATP 	= 0.199020
        a1      = -6.06831
        a2      = 10.7505
        a3      = -3.68883
        b1      = -0.258378
        b2      = 0.679163
        c11Amp  = 4.36263
        c12Amp  = -12.5897
        c13Amp  = -7.73233
        c14Amp  = 16.2082
        c21Amp  = 3.04724
        c22Amp  = 46.5711
        c23Amp  = 2.10475
        c24Amp  = 56.9136

        A_orb   = ATP*(1-3*nu)*(1 + a1*nu + a2*nu*nu)/(1 + a3*nu)
        b1      = (b1 + c11Amp*nu + c12Amp*nu*nu)/(1 + c13Amp*nu + c14Amp*nu*nu)
        b2      = (b2 + c21Amp*nu + c22Amp*nu*nu)/(1 + c23Amp*nu + c24Amp*nu*nu)

        A_spin  = (1+b1*aK)/(1+b2*aK)
        scale   = 1+aK*cbrt(omega_peak/2)
        res = A_orb*scale*A_spin

    elif ((l==3) and (m==1)):

        ATP = 0.0623783
        res = ATP*X12*(1-5.49*nu+10.915*nu*nu)

    elif ((l==4) and (m==4)):

        ATPc    = 0.2766182761
        a1Amp   = -3.7082
        a2Amp   = 0.280906
        a3Amp   = -3.71276
        Aorb    = (1-3*nu)*(1+a1Amp*nu + a2Amp*nu*nu)/(1+a3Amp*nu)
        b1Amp   = -0.316647
        b2Amp   = -0.062423
        b3Amp   = -0.852876
        b11Amp  = 1.2436
        b12Amp  = -1.60555
        b13Amp  = -4.05685
        b14Amp  = 1.59143
        b21Amp  = 0.837418
        b22Amp  = -2.93528
        b23Amp  = -11.5591
        b24Amp  = 34.1863
        b31Amp  = 0.950035
        b32Amp  = 7.95168
        b33Amp  = -1.26899
        b34Amp  = -9.72147

        a1AmpS  = (b1Amp + b11Amp*nu + b12Amp*nu*nu)/(1 + b13Amp*nu + b14Amp*nu*nu)
        a2AmpS  = (b2Amp + b21Amp*nu + b22Amp*nu*nu)/(1 + b23Amp*nu + b24Amp*nu*nu)
        a3AmpS  = (b3Amp + b31Amp*nu + b32Amp*nu*nu)/(1 + b33Amp*nu + b34Amp*nu*nu)

        Aspin   = (1+a1AmpS*S_hat+a2AmpS*S_hat*S_hat)/(1+a3AmpS*S_hat)
        scale   = 1-0.5*S_hat*omega_peak
        res     = ATPc*Aorb*Aspin*scale

    elif ((l==4) and (m==3)):

        if (nu==0.25):
            b1 		= 0.00452129
            b2 		= -0.00471163
            b3 		= 0.0291409
            b4 		= -0.351031
            res     = (b1+b2*a12+b3*a12*a12)/(1+b4*a12)
        else:
            ATP 	= 0.0941576
            a1Amp 	= -5.74386
            a2Amp 	= 12.6016
            a3Amp 	= -3.27435
            A_orb   = ATP*X12*(1-2*nu)*(1+a1Amp*nu+a2Amp*nu*nu)/(1+a3Amp*nu)
            b1      = +0.249099
            b2 		= -7.345984
            b3 		= +108.923746
            b4 		= -0.104206
            b5 		= +7.073534
            b6 		= -44.374738
            b7 		= +3.545134
            b8 		= +1.341375
            b9 		= -19.552083
            AS      = (+((-0.02132252+b1*nu)/(1+b2*nu+b3*nu*nu))*aK+((+0.02592749+b4*nu)/(1+b5*nu+b6*nu*nu))*aK*aK)/(1+((-0.826977+b7*nu)/(1+b8*nu+b9*nu*nu))*aK)
            res     = A_orb+AS

    elif ((l==4) and (m==2)):

        ATP 	= 0.0314270
        a1Amp   = -4.56243
        a2Amp   = 6.4522

        b1Amp   = -1.63682
        b2Amp   = 0.854459
        b3Amp   = 0.120537
        b4Amp   = -0.399718

        c11Amp  = 6.53943
        c12Amp  = -4.00073
        c21Amp  = -0.638688
        c22Amp  = -3.94066
        c31Amp  = -0.482148
        c32Amp  = -3.9999999923319502
        c41Amp  = 1.25617
        c42Amp  = -4.04848
        A_orb   = ATP*(1-3*nu)*(1+a1Amp*nu+a2Amp*nu*nu)
        b1      = (b1Amp + c11Amp*nu)/(1 + c12Amp*nu)
        b2      = (b2Amp + c21Amp*nu)/(1 + c22Amp*nu)
        b3      = (b3Amp + c31Amp*nu)/(1 + c32Amp*nu)
        b4      = (b4Amp + c41Amp*nu)/(1 + c42Amp*nu)
        AS      = (1+b1*S_hat + b2*S_hat*S_hat)/(1+b3*S_hat+b4*S_hat*S_hat)
        res     = A_orb*AS*(1+aK*cbrt(omega_peak/2))

    elif ((l==4) and (m==1)):

        ATP = 0.00925061
        res = ATP*X12*(1-2*nu)*(1-8.4449*nu+26.825*nu*nu)/(1-1.2565*nu)

    elif ((l==5) and (m==5)):

        ATP = 0.151492
        b1 	= +5.720690
        b2 	= +44.868515
        b3 	= +12.777090
        b4 	= -42.548247
        res = ATP*X12*(1-2*nu)*(1-0.29628*nu+6.4207*nu*nu)+(+((+0.04360530)/(1+b1*nu+b2*nu*nu))*a12)/(1+((-0.5769451)/(1+b3*nu+b4*nu*nu))*a12)

    return res


cdef double _omega_peak(double nu, double X12, double S_hat, double aK, int l, int m) nogil:

    cdef double res = 0., orb, num, denom
    cdef double omg_tp, omgTP, omg1, omg2, omgOrb, omgS
    cdef double b1, b2, b3, b4, b1Omg, b2Omg, b3Omg, b4Omg, b11Omg, b12Omg, b13Omg, b14Omg, b21Omg, b22Omg, b23Omg, b24Omg, b31Omg, b32Omg, b33Omg, b34Omg, b41Omg, b42Omg, b43Omg, b44Omg
    cdef double c1, c2, c3, c4, c1Omg, c2Omg, c5Omg, c6Omg, c11Omg, c12Omg, c13Omg, c21Omg, c22Omg, c23Omg, c31Omg, c32Omg, c33Omg, c41Omg, c42Omg, c43Omg
    cdef double omgorb, omgspin, OmgOrb, Omgspin
    cdef double n1Omg, n2Omg, d1Omg, d2Omg
    cdef double a1Omg, a2Omg, a3Omg, a4Omg

    if ((l==2) and (m==2)):

        omg_tp 		= 0.273356
        omg1 		= 0.84074
        omg2 		= 1.6976
        orb         = omg_tp*(1+omg1*nu + omg2*nu*nu)

        # Equal Mass fit calibrated to the q=1 SXS data
        b1 			= -0.42311
        b2    		= -0.066699
        b3     		= -0.83053

        # Unequal Mass corrections to the q=1 fit based on SXS, BAM and TP data
        c1    		= 0.066045
        c2		    = -0.23876
        c3      	= 0.76819
        c4      	= -0.9201
        num         = 1+((b1+c1*X12)/(1+c2*X12))*S_hat + b2*S_hat*S_hat
        denom       = 1+((b3+c3*X12)/(1+c4*X12))*S_hat
        res         = (orb*num/denom)

    elif ((l==2) and (m==1)):

        omgTP  = 0.290672
        a1Omg  = -0.563075
        a2Omg  = 3.28677

        b1Omg  = 0.179639
        b2Omg  = -0.302122

        c11Omg = -1.20684
        c21Omg = 0.425645

        omgOrb = omgTP*(1+a1Omg*nu+a2Omg*nu*nu)
        b1     = (b1Omg + c11Omg*nu)
        b2     = (b2Omg + c21Omg*nu)
        omgS   = (1+b1*S_hat + b2*S_hat*S_hat)
        res    = omgOrb*omgS

    elif ((l==3) and (m==3)):

        omgTP   = 0.4541278937
        a1Omg   = 1.08224
        a2Omg   = 2.59333
        b1Omg   = -0.406161
        b2Omg   = -0.0647944
        b3Omg   = -0.748126
        c1Omg   = 0.85777
        c2Omg   = -0.70066
        c5Omg   = 2.97025
        c6Omg   = -3.96242

        b1Omg   = (b1Omg+c1Omg*nu)/(1+c2Omg*nu)
        b3Omg   = (b3Omg+c5Omg*nu)/(1+c6Omg*nu)

        omgorb  = 1 + a1Omg*nu + a2Omg*nu*nu
        omgspin = (1+b1Omg*S_hat+b2Omg*S_hat*S_hat)/(1+b3Omg*S_hat)

        res     = omgTP*omgorb*omgspin

    elif ((l==3) and (m==2)):

        omgTP  = 0.451817
        a1Omg  = -9.13525
        a2Omg  = 21.488
        a3Omg  = -8.81384
        a4Omg  = 20.0595

        b1Omg  = -0.458126
        b2Omg  = 0.0474616
        b3Omg  = -0.486049

        c11Omg = 3.25319
        c12Omg = 0.535555
        c13Omg = -8.07905
        c21Omg = 1.00066
        c22Omg = -1.1333
        c23Omg = 0.601572

        b1     = (b1Omg + c11Omg*X12 + c12Omg*X12*X12)/(1+c13Omg*X12)
        b2     = (b2Omg + c21Omg*X12 + c22Omg*X12*X12)/(1+c23Omg*X12)
        b3     = b3Omg
        omgOrb = omgTP*(1+a1Omg*nu+a2Omg*nu*nu)/(1+a3Omg*nu+a4Omg*nu*nu)
        omgS   = (1+b1*aK + b2*aK*aK)/(1+b3*aK)

        res    = omgOrb*omgS

    elif ((l==3) and (m==1)):

        omgTP = 0.411755
        res   = omgTP*(1+7.5362*nu*nu)/(1-2.7555*nu+38.572*nu*nu)

    elif ((l==4) and (m==4)):

        omgTP   = 0.6356586393
        n1Omg   = -0.964614
        n2Omg   = -11.1828
        d1Omg   = -2.08471
        d2Omg   = -6.89287
        b1Omg   = -0.445192
        b2Omg   = -0.0985658
        b3Omg   = -0.0307812
        b4Omg   = -0.801552

        b11Omg  = -0.92902
        b12Omg  = 10.86310
        b13Omg  = -4.44930
        b14Omg  = 3.01808
        b21Omg  = 0
        b22Omg  = 1.62523
        b23Omg  = -7.70486
        b24Omg  = 15.06517
        b31Omg  = 0
        b32Omg  = 0
        b33Omg  = 0
        b34Omg  = 0
        b41Omg  = 0.93790
        b42Omg  = 8.36038
        b43Omg  = -4.85774
        b44Omg  = 4.80446

        a1Omg   = (b1Omg + b11Omg*nu + b12Omg*nu*nu)/(1 + b13Omg*nu + b14Omg*nu*nu)
        a2Omg   = (b2Omg + b21Omg*nu + b22Omg*nu*nu)/(1 + b23Omg*nu + b24Omg*nu*nu)
        a3Omg   = (b3Omg + b31Omg*nu + b32Omg*nu*nu)/(1 + b33Omg*nu + b34Omg*nu*nu)
        a4Omg   = (b4Omg + b41Omg*nu + b42Omg*nu*nu)/(1 + b43Omg*nu + b44Omg*nu*nu)

        OmgOrb  = (1 + n1Omg*nu + n2Omg*nu*nu)/(1 + d1Omg*nu + d2Omg*nu*nu)
        Omgspin = (1+a1Omg*S_hat + a2Omg*S_hat*S_hat + a3Omg*S_hat*S_hat*S_hat)/(1+a4Omg*S_hat)

        res     = omgTP*OmgOrb*Omgspin

    elif ((l==4) and (m==3)):

        omgTP = 0.636870
        a1Omg   = -9.02463
        a2Omg   = 21.9802
        a3Omg   = -8.75892
        a4Omg   = 20.5624

        b1Omg   = -0.973324
        b2Omg   = -0.109921
        b3Omg   = -1.08036

        c11Omg  = 11.5224
        c12Omg  = -26.8421
        c13Omg  = -2.84285
        c21Omg  = 3.51943
        c22Omg  = -12.1688
        c23Omg  = -3.96385
        c31Omg  = 5.53433
        c32Omg  = 3.73988
        c33Omg  = 4.219

        omgOrb  = omgTP*(1+a1Omg*nu+a2Omg*nu*nu)/(1+a3Omg*nu+a4Omg*nu*nu)
        b1      = (b1Omg + c11Omg*nu + c12Omg*nu*nu)/(1 + c13Omg*nu)
        b2      = (b2Omg + c21Omg*nu + c22Omg*nu*nu)/(1 + c23Omg*nu)
        b3      = (b3Omg + c31Omg*nu + c32Omg*nu*nu)/(1 + c33Omg*nu)
        omgS    = (1+b1*S_hat + b2*S_hat*S_hat)/(1+b3*S_hat)
        res     = omgOrb*omgS

    elif ((l==4) and (m==2)):

        omgTP   = 0.6175331548
        a1Omg   = -7.44121
        a2Omg   = 14.233
        a3Omg   = -6.61754
        a4Omg   = 11.4329

        b1Omg   = -2.37589
        b2Omg   = 1.97249
        b3Omg   = -2.36107
        b4Omg   = 2.16383

        c11Omg  = 10.1045
        c12Omg  = -6.94127
        c13Omg  = 12.1857
        c21Omg  = -1.62866
        c22Omg  = -2.6756
        c23Omg  = -4.7536
        c31Omg  = 10.071
        c32Omg  = -6.7299
        c33Omg  = 12.0377
        c41Omg  = -8.56139
        c42Omg  = -5.27136
        c43Omg  = 5.10653

        omgOrb  = omgTP*(1+a1Omg*nu+a2Omg*nu*nu)/(1+a3Omg*nu+a4Omg*nu*nu)
        b1      = (b1Omg + c11Omg*nu)/(1 + c12Omg*nu + c13Omg*nu*nu)
        b2      = (b2Omg + c21Omg*nu)/(1 + c22Omg*nu + c23Omg*nu*nu)
        b3      = (b3Omg + c31Omg*nu)/(1 + c32Omg*nu + c33Omg*nu*nu)
        b4      = (b4Omg + c41Omg*nu)/(1 + c42Omg*nu + c43Omg*nu*nu)
        omgS    = (1+b1*S_hat + b2*S_hat*S_hat)/(1+b3*S_hat+b4*S_hat*S_hat)
        res     = omgOrb*omgS

    elif ((l==4) and (m==1)):

        omgTP = 0.552201
        res   = omgTP*(1-10.876*nu+37.904*nu*nu)/(1-11.194*nu+42.77*nu*nu)

    elif ((l==5) and (m==5)):

        omgTP = 0.818117
        b1 	  = +1.487294
        b2 	  = -2.058537
        b3 	  =  +1.454248
        b4    = -1.301284
        res   = omgTP*(1-2.8918*nu-3.2012*nu*nu)/(1-3.773*nu)*(1+((-0.332703+b1*nu)/(1+b2*nu))*S_hat)/(1+((-0.675738+b3*nu)/(1+b4*nu))*S_hat)

    return res


cdef double _JimenezFortezaRemnantMass(double m1, double m2, double chi1, double chi2) nogil:
    """
    Calculate the final mass with the aligned-spin NR fit
    by Xisco Jimenez Forteza, David Keitel, Sascha Husa et al.
    [LIGO-P1600270] [https://arxiv.org/abs/1611.00332]
    versions v1 and v2 use the same ansatz,
    with v2 calibrated to additional SXS and RIT data

    m1, m2: component masses
    chi1, chi2: dimensionless spins of two BHs
    Note: Here it is assumed that m1>m2.
    """

    cdef double m, msq, m1sq, m2sq, eta, eta2, eta3, eta4, Shat, Shat2, Shat3, chidiff, chidiff2, sqrt2, sqrt1m4eta

    m    = m1+m2
    msq  = m*m
    m1sq = m1*m1
    m2sq = m2*m2

    # symmetric mass ratio
    eta        = m1*m2/msq
    eta2       = eta*eta
    eta3       = eta2*eta
    eta4       = eta2*eta2
    # Stot = S1+S2 total spin. S1 = chi1*m1sq/msq spin angular momentum 1. Same for S2
    Shat       = (chi1*m1sq+chi2*m2sq)/(m1sq+m2sq) # effective spin, = msq*Stot/(m1sq+m2sq)
    Shat2      = Shat*Shat
    Shat3      = Shat2*Shat
    chidiff    = chi1 - chi2 # fit assumes m1>m2
    chidiff2   = chidiff*chidiff
    sqrt2      = sqrt(2.)
    sqrt1m4eta = sqrt(1. - 4.*eta)

    # rational-function Pade coefficients (exact) from Eq. (22) of 1611.00332v2
    cdef double b10 = 0.346
    cdef double b20 = 0.211
    cdef double b30 = 0.128
    cdef double b50 = -0.212

    # fit coefficients from Tables VII-X of 1611.00332v2
    # values at increased numerical precision copied from
    # https://git.ligo.org/uib-papers/finalstate2016/blob/master/LALInference/EradUIB2016v2_pyform_coeffs.txt
    # git commit f490774d3593adff5bb09ae26b7efc6deab76a42
    cdef double a2  = 0.5609904135313374
    cdef double a3  = -0.84667563764404
    cdef double a4  = 3.145145224278187
    cdef double b1  = -0.2091189048177395
    cdef double b2  = -0.19709136361080587
    cdef double b3  = -0.1588185739358418
    cdef double b5  = 2.9852925538232014
    cdef double f20 = 4.271313308472851
    cdef double f30 = 31.08987570280556
    cdef double f50 = 1.5673498395263061
    cdef double f10 = 1.8083565298668276
    cdef double f21 = 0.
    cdef double d10 = -0.09803730445895877
    cdef double d11 = -3.2283713377939134
    cdef double d20 = 0.01118530335431078
    cdef double d30 = -0.01978238971523653
    cdef double d31 = -4.91667749015812
    cdef double f11 = 15.738082204419655
    cdef double f31 = -243.6299258830685
    cdef double f51 = -0.5808669012986468

    # Calculate the radiated-energy fit from Eq. (27) of 1611.00332
    cdef double Erad = (((1. + -2.0/3.0*sqrt2)*eta + a2*eta2 + a3*eta3 + a4*eta4)*(1. + b10*b1*Shat*(f10 + f11*eta + (16. - 16.*f10 - 4.*f11)*eta2) + b20*b2*Shat2*(f20 + f21*eta + (16. - 16.*f20 - 4.*f21)*eta2) + b30*b3*Shat3*(f30 + f31*eta + (16. - 16.*f30 - 4.*f31)*eta2)))/(1. + b50*b5*Shat*(f50 + f51*eta + (16. - 16.*f50 - 4.*f51)*eta2)) + d10*sqrt1m4eta*eta2*(1. + d11*eta)*chidiff + d30*Shat*sqrt1m4eta*eta*(1. + d31*eta)*chidiff + d20*eta3*chidiff2

    # Convert to actual final mass
    cdef double Mf = m*(1.-Erad)

    return Mf


cdef double _JimenezFortezaRemnantSpin(double nu, double chi1, double chi2) nogil:
    cdef double xnu     = sqrt(1.0-4.0*nu)
    cdef double X1      = 0.5*(1+xnu)
    cdef double X2      = 0.5*(1-xnu)
    cdef double Dchi    = chi1-chi2
    cdef double S       = (X1*X1*chi1+X2*X2*chi2)/(X1*X1+X2*X2)
    cdef double a2      = 3.833
    cdef double a3      = -9.49
    cdef double a5      = 2.513

    # The functional form is taken from eq. (7), page 5.
    cdef double Lorb_spin_zero  = (1.3*a3*nu*nu*nu + 5.24*a2*nu*nu + 2.*sqrt(3)*nu)/(2.88*a5*nu + 1)

    # Coeffcients taken from Table II, page 6:
    cdef double b1      = 1.00096
    cdef double b2      = 0.788
    cdef double b3      = 0.654
    cdef double b5      = 0.840

    # These values are taken from Table III, page 7:
    cdef double f21     = 8.774
    cdef double f31     = 22.83
    cdef double f50     = 1.8805
    cdef double f11     = 0.345225*f21 + 0.0321306*f31 - 3.66556*f50 + 7.5397

    # These values are taken from Table IV, page 10
    cdef double f12     = 0.512
    cdef double f22     = -32.1
    cdef double f32     = -154
    cdef double f51     = -4.77

    # The following quantities were taken from the relation given in eq. (11),
    # page 7: fi3 = 64 - 64.*fi0 - 16.*fi1 - 4.*fi2
    cdef double f13     = 64 - 16.*f11 - 4.*f12
    cdef double f23     = 64 - 16.*f21 - 4.*f22
    cdef double f33     = 64 - 16.*f31 - 4.*f32
    cdef double f53     = 64 - 64.*f50 - 16.*f51

    # this transformation is given in eq. (9), page (7)
    cdef double b1t     = b1*(f11*nu + f12*nu*nu + f13*nu*nu*nu)
    cdef double b2t     = b2*(f21*nu + f22*nu*nu + f23*nu*nu*nu)
    cdef double b3t     = b3*(f31*nu + f32*nu*nu + f33*nu*nu*nu)
    cdef double b5t     = b5*(f50 + f51*nu + f53*nu*nu*nu)

    # The functional form is taken from eq. (8), page 6.
    cdef double Lorb_eq_spin  = (0.00954*b3t*S*S*S + 0.0851*b2t*S*S - 0.194*b1t*S)/(1 - 0.579*b5t*S)

    # These values are taken from Table IV, page 10:
    cdef double d10     = 0.322
    cdef double d11     = 9.33
    cdef double d20     = -0.0598
    cdef double d30     = 2.32
    cdef double d31     = -3.26

    # The functional form is taken from eq. (19a-c), page 10.
    cdef double A1      = d10*xnu*nu*nu*(d11*nu+1)
    cdef double A2      = d20*nu*nu*nu
    cdef double A3      = d30*xnu*nu*nu*nu*(d31*nu+1)

    # The functional form is taken from eq. (15), page 9.
    cdef double Lorb_uneq_mass  = A1*Dchi + A2*Dchi*Dchi + A3*S*Dchi

    return X1*X1*chi1+X2*X2*chi2 + Lorb_spin_zero + Lorb_eq_spin + Lorb_uneq_mass


cdef double _DeltaT(double m1,      # mass of the heavier BH (solar masses)
                    double m2,      # mass of the lighter BH (solar masses)
                    double s1z,     # spin of the heavier BH(adimensional)
                    double s2z,     # spin of the lighter BH (adimensional)
                    unsigned int l,
                    int m) nogil:
    
    cdef double res   = 0.0
    cdef double M     = m1+m2
    cdef double M2    = M*M
    cdef double nu    = m1*m2/M2
    cdef double nu2   = nu**2
    cdef double nu3   = nu**3
    cdef double X12   = (m1-m2)/M
    cdef double X12_2 = X12**2
    cdef double X12_3 = X12**3
    cdef double a0    = (m1*s1z + m2*s2z)/M
    cdef double a02   = a0*a0
    cdef double Shat  = (m1**2*s1z + m2**2*s2z)/M2
    cdef double Shat2 = Shat**2

    cdef double Dt_21_orb, Dt_21_S, Dt_32_orb, Dt_32_S, Dt_42_orb, Dt_42_S, orb
    cdef double a1Dt, a2Dt, a3Dt, a4Dt, b1Dtlm, b2Dtlm, c11Dtlm, c12Dtlm, c21Dtlm, c22Dtlm
    cdef double b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15
    cdef double n1, n2, d1, d2

    if(l==2 and m==2):
        
        res = 0.0

    elif(l==2 and m==1):
    
        Dt_21_orb = (11.75925*(1-4*nu) + 4*6.6264*nu)*(1-2.0728*nu*X12)
        c11Dtlm   = -1976.13
        c12Dtlm   = 3719.88
        c21Dtlm   = -2545.41
        c22Dtlm   = 5277.62
        b1Dtlm    = 0.0472289
        b2Dtlm    = 0.115583
        b1        = (b1Dtlm + c11Dtlm*X12)/(1 + c12Dtlm*X12)
        b2        = (b2Dtlm + c21Dtlm*X12)/(1 + c22Dtlm*X12)
        Dt_21_S   = 1 + b1*a0 + b2*a02
        res       = Dt_21_orb*Dt_21_S

    elif(l==3 and m==3):

        orb 	= 3.42593*(1 + 0.183349*nu+ 4.22361*nu2)
        b1 		= (-0.49791-1.9478*nu)/(1+13.9828*nu)
        b2 		= (-0.18754+1.25084*nu)/(1-3.41811*nu)
        b3 		= (-1.07291-1043.15*nu)/(1 + 1033.85*nu)
        res 	= orb*(1+b1*Shat+b2*Shat**2)/(1+b3*Shat)

    elif(l==3 and m==2):

        a1Dt      = -11.3497
        a2Dt      = 32.9144
        a3Dt      = -8.36579
        a4Dt      = 20.1017
        Dt_32_orb = 9.16665*(1 + a1Dt*nu+ a2Dt*nu2)/(1 + a3Dt*nu+ a4Dt*nu2)
        
        if (nu<0.2):
            b1    = -0.037634
            b2    = +12.456704
            b3    = +2.670868
            b4    = -12.255859
            b5    = +37.843505
            b6    = -25.058475
            b7    = +449.470722
            b8    = -1413.508735
            b9    = -11.852596
            b10   = +41.348059
            b11   = -5.650710
            b12   = -9.567484
            b13   = +173.182999
            b14   = -10.938605
            b15   = +35.670656

            Dt_32_S  = (1+((-0.34161+b1*nu+b2*nu2+b3*nu3)/(1+b4*nu+b5*nu2))*Shat+((-0.46107+b6*nu+b7*nu2+b8*nu3)/(1+b9*nu+b10*nu2))*Shat2)/(1+((+0.34744+b11*nu+b12*nu2+b13*nu3)/(1+b14*nu+b15*nu2))*Shat)
        else:
            b1    	= +2.497188
            b2 		= -7.532596
            b3 		= +4.645986
            b4 		= -3.652524
            b5 		= +3.398687
            b6 		= +7.054185
            b7 		= -12.260185
            b8 		= +5.724802
            b9 		= -3.242611
            b10		= +2.714232
            b11		= +2.614565
            b12		= -9.507583
            b13		= +7.321586
            b14		= -3.937568
            b15		= +4.584970
            Dt_32_S = (1+((+0.15477+b1*X12+b2*X12_2+b3*X12_3)/(1+b4*X12+b5*X12_2))*Shat+((-0.755639+b6*X12+b7*X12_2+b8*X12_3)/(1+b9*X12+b10*X12_2))*Shat2)/(1+((+0.21816+b11*X12+b12*X12_2+b13*X12_3)/(1+b14*X12+b15*X12_2))*Shat)
        res = Dt_32_orb*Dt_32_S

    elif(l==3 and m==1):
    
        res 	= 12.9338*(1-25.615*nu2)/(1+0.88803*nu+16.292*nu2)

    elif(l==4 and m==4):

        n1      = -8.35574
        n2      = 17.5288
        d1      = -6.50259
        d2      = 10.1575
        orb 	= 5.27778*(1 + n1*nu + n2*nu2)/(1 + d1*nu + d2*nu2)

        b1      = 0.00159701-2.28656*X12+1.66532*X12**2
        b2      = -1.14134-0.589331*X12+0.708784*X12**2
        res     = orb*(1+b1*Shat)/(1+b2*Shat)

    elif(l==4 and m==3):
        
        a1Dt = -11.2377
        a2Dt = 38.3177
        a3Dt = -7.29734
        a4Dt = 21.4267
        Dt_43_orb = 9.53705*(1+a1Dt*nu+a2Dt*nu2)/(1+a3Dt*nu+a4Dt*nu2)
        b1    	= +3.215984
        b2 	    = +42.133767
        b3 	    = -9.440398
        b4 	    = +35.160776
        b5 	    = +1.133942
        b6 	    = -10.356311
        b7 	    = -6.701429
        b8 	    = +10.726960
        b9 	    = -6.036207
        b10	    = +67.730599
        b11	    = -3.082275
        b12	    = +11.547917
        Dt_43_S  = (1+((-1.371832+b1*nu+b2*nu2)/(1+b3*nu+b4*nu2))*Shat +((+0.362375+b5*nu+b6*nu2)/(1+b7*nu+b8*nu2))*Shat2)/(1+((-1.0808402+b9*nu+b10*nu2)/(1+b11*nu+b12*nu2))*Shat)

        res     = Dt_43_orb*Dt_43_S

    elif(l==4 and m==2):
        
        Dt_42_orb    = 11.66665*(1-9.8446172795*nu+23.3229430582*nu2)/(1-5.7604819848*nu+7.1217930024*nu2)
        if nu<6./25.:
            b1      = 0
            b2      = 0
            b3      = 0
            b4      = 0
        else:
            b1   	= +24.604717
            b2		= -0.808279
            b3		= +62.471781
            b4		= +48.340961
        
        Dt_42_S  = (1+((-1.3002045+b1*nu)/(1+b2*nu))*Shat)/(1+((-0.9494348+b3*nu)/(1+b4*nu))*Shat)
        
        res     = Dt_42_orb*Dt_42_S

    elif(l==4 and m==1):

        res     = 13.1116*(1-9.6225*nu+38.451*nu2)/(1-7.7998*nu+32.405*nu2)

    elif(l==5 and m==5):

        res     = 6.561811*(1-12.198*nu+40.327*nu2)/(1-11.501*nu+39.431*nu2)
        
    return res


cdef double _DeltaPhi(double m1,      # mass of the heavier BH (solar masses)
                      double m2,      # mass of the lighter BH (solar masses)
                      double s1z,     # spin of the heavier BH(adimensional)
                      double s2z,     # spin of the lighter BH (adimensional)
                      unsigned int l,
                      int m) nogil:

    cdef double res   = 0.0
    cdef double M     = m1+m2
    cdef double M2    = M*M
    cdef double nu    = m1*m2/M2
    cdef double nu2   = nu**2
    cdef double nu3   = nu**3
    cdef double X12   = (m1-m2)/M
    cdef double X12_2 = X12**2
    cdef double X12_3 = X12**3
    cdef double a0    = (m1*s1z + m2*s2z)/M
    cdef double a02   = a0*a0
    cdef double Shat  = (m1**2*s1z + m2**2*s2z)/M2
    cdef double Shat2 = Shat**2

    if(l==2 and m==2):

        res = 0.0

    elif(l==2 and m==1):

        res = 0.0

    elif(l==3 and m==3):

        res = 0.0

    elif(l==3 and m==2):

        res = 0.0

    elif(l==3 and m==1):

        res = 0.0

    elif(l==4 and m==4):

        res = 0.0

    elif(l==4 and m==3):

        res = 0.0

    elif(l==4 and m==2):

        res = 0.0

    elif(l==4 and m==1):

        res = 0.0

    elif(l==5 and m==5):

        res = 0.0

    return res
