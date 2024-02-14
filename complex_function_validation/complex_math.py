"""Complex functions

This module provides implementations of elementary functions on
complex arguments as decompositons of elementary functions on real
arguments.

that use
real functions as

"""

__version__ = '0.1'

import numpy

def make_complex(real, imag):
    complex_dtype = dict(float32=numpy.complex64, float64=numpy.complex128)[real.dtype.name]
    return numpy.array([real, imag], dtype=real.dtype).view(complex_dtype)[0]

@numpy.vectorize
def sin(z):
    """
    sin(z) = complex(sin(z.real) * cosh(z.imag), cos(z.real) * sinh(z.imag))
    """
    sn, cs = numpy.sin(z.real), numpy.cos(z.real)
    if 0:
        # match rate 100%
        # relies on the quality of sinh/cosh
        snh, csh = numpy.sinh(z.imag), numpy.cosh(z.imag)
    elif 0:
        # match rate 100%
        # relies on the quality of expm1 and exp
        # exp(x) - exp(-x) = exp(x) - 1 - (exp(-x) - 1) = expm1(x) - expm1(-x)
        e1m, e2m = numpy.expm1(z.imag), numpy.expm1(-z.imag)
        e1, e2 = numpy.exp(z.imag), numpy.exp(-z.imag)
        snh, csh = (e1m - e2m) / 2, (e1 + e2) / 2
    elif 1:
        # match rate 100%
        # relies on the quality of expm1
        # exp(x) - exp(-x) = exp(x) - 1 - (exp(-x) - 1) = expm1(x) - expm1(-x)
        # exp(x) + exp(-x) = exp(x) - 1 + (exp(-x) - 1) + 2 = 2 + expm1(x) + expm1(-x)
        e1m, e2m = numpy.expm1(z.imag), numpy.expm1(-z.imag)
        snh, csh = (e1m - e2m) / 2, (2 + e1m + e2m) / 2
    elif 0:
        # match rate 100%
        # relies on the quality of expm1
        # exp(x) - exp(-x) = exp(x) - 1 - (exp(-x) - 1) = expm1(x) - expm1(-x)
        # exp(x) + exp(-x) = exp(x) - 1 + (exp(-x) - 1) = 2 + expm1(x) + expm1(-x)
        # expm1(x) = exp(x) - 1
        # expm1(-x) = exp(-x) - 1 = exp(-x) (1 - exp(x)) = -exp(-x) * expm1(x)
        # exp(x) + exp(-x) = 2 + expm1(x) * (1 - exp(-x)) = 2 - expm1(x) * expm1(-x)
        e1m, e2m = numpy.expm1(z.imag), numpy.expm1(-z.imag)
        snh, csh = (e1m - e2m) / 2, (2 - e1m * e2m) / 2
    else:
        # match rate: 90.3%
        # inaccuracies rate: 4.8%
        # mismatch rate: 4.9%
        # jax/xla algorithm, snh is problematic when z.imag is small
        e1, e2 = numpy.exp(z.imag), numpy.exp(-z.imag)
        snh, csh = (e1 - e2) / 2, (e1 + e2) / 2
    if z.real == 0:
        # sin(im * 1j) = sinh(im) * 1j
        return make_complex(sn, snh)
    return make_complex(sn * csh, cs * snh)
