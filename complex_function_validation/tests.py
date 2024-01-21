import numpy

import complex_function_validation as cfv

def test_compare():
    dtype = numpy.complex64
    finfo = numpy.finfo(dtype)

    for s in [1, 10, 1e3, 1e-1, 1e-10, 1e20, 1e-20,
              -1, -10, -1e3, -1e-1, -1e-10, -1e20, -1e-20]:

        def v(value):
            return numpy.asarray(value * s, dtype=dtype)

        assert cfv.compare(v(0.1), v(0.1)) == '='
        assert cfv.compare(v(0.1234567), v(9.1234567)) == 'X'
        assert cfv.compare(v(0.1234567), v(0.0934567)) == 'x'
        assert cfv.compare(v(0.1234567), v(0.1334567)) == 'x'
        assert cfv.compare(v(0.1234567), v(0.1244567)) == '6'
        assert cfv.compare(v(0.1234567), v(0.1235567)) == '5'
        assert cfv.compare(v(0.1234567), v(0.1234667)) == '4'
        assert cfv.compare(v(0.1234567), v(0.1234577)) == '3'
        assert cfv.compare(v(0.1234567), v(0.1234568)) == '2'
        assert cfv.compare(v(0.123456789), v(0.123456779)) in '1c'
        assert cfv.compare(v(0.123456789), v(0.123456788)) in '=c'
        assert cfv.compare(v(0.123456789), v(0.123456780)) == 'c'

        assert cfv.compare(v(0.1), v(numpy.inf)) == 'I'
        assert cfv.compare(v(0.1), v(-numpy.inf)) == 'I'
        assert cfv.compare(v(0.1), v(numpy.nan)) == 'N'
        assert cfv.compare(v(numpy.inf), v(0.1)) == 'E'
        assert cfv.compare(v(numpy.nan), v(0.1)) == 'M'
        assert cfv.compare(v(numpy.inf), v(numpy.inf)) == '~'
        assert cfv.compare(v(numpy.inf), v(-numpy.inf)) == 'E'
        assert cfv.compare(v(numpy.nan), v(numpy.nan)) == '~'


def test_real_axis():
    for size in range(30):
        image = cfv.ReportImage()
        image.insert_real_axis(0, 10, cfv.ComplexPlaneSampler(numpy.complex64)(size, size)[::-1])
        s = str(image).split('\n')[-1].strip()
        expected = ['-inf0+inf',
                    '-inf 0 +inf',
                    '-inf  0  +inf',
                    '-inf   0   +inf',
                    '-inf    0    +inf',
                    '-inf -2  0  2  +inf',
                    '-inf      0      +inf',
                    '-inf  -2   0   2   +inf',
                    '-inf -1e-27 0 1e-27  +inf',
                    '-inf   -2    0    2    +inf',
                    '-inf -4e4     0     4e4  +inf',
                    '-inf -9e7      0      9e7  +inf',
                    '-inf  -6e3      0      6e3   +inf',
                    '-inf  -5e6       0       5e6   +inf',
                    '-inf  -1e9 -9e-33 0 9e-33  1e9   +inf',
                    '-inf -2e11 -1e-27  0  1e-27  2e11  +inf',
                    '-inf -1e13 -2e-23   0   2e-23  1e13  +inf',
                    '-inf -4e14 -2 -7e-34 0 7e-34  2  4e14  +inf',
                    '-inf -1e16 -4e-16     0     4e-16  1e16  +inf',
                    '-inf -2e17  -2 -4e-30  0  4e-30  2   2e17  +inf',
                    '-inf -3e18 -2e-6 -1e-34 0 1e-34  2e-6  3e18  +inf',
                    '-inf -3e19   -2 -3e-27   0   3e-27  2    3e19  +inf',
                    '-inf -2e20 -1e2 -4e-24    0    4e-24  1e2  2e20  +inf',
                    '-inf -1e21 -6e3 -3e-21     0     3e-21  6e3  1e21  +inf',
                    '-inf -8e21 -2e5 -1e-18      0      1e-18  2e5  8e21  +inf',
                    '-inf -4e22 -5e6 -2e-16       0       2e-16  5e6  4e22  +inf',
                    '-inf -2e23 -9e7 -3e-14 -1e-35 0 1e-35  3e-14  9e7  2e23  +inf',
                    '-inf -7e23 -1e9 -2 -5e-21      0      5e-21  2  1e9  7e23  +inf',
                    '-inf -2e24  -2e7 -4e-13 -5e-33  0  5e-33  4e-13  2e7   2e24  +inf',
                    '-inf -8e24  -3e8 -2 -2e-19       0       2e-19  2  3e8   8e24  +inf',
                    
                    ][size]
        assert s == expected
