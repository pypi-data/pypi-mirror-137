from pyRing.waveform import QNM_fit

Mf = 100
af = 0.7

l,m,n = 2,2,0

f = QNM_fit(l,m,n).f(Mf, af)
tau = QNM_fit(l,m,n).tau(Mf, af)

print('(l,m,n)     = ({},{},{})'.format(l,m,n))
print('M_f [M_sun] = {:.3f}'.format(Mf))
print('a_f         = {:.3f}'.format(af))
print('f   [Hz]    = {:.3f}'.format(f))
print('tau [ms]    = {:.3f}'.format(tau*1e3))
