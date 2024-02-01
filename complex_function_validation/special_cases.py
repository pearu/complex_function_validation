# Reference: https://en.cppreference.com/w/cpp/numeric/complex/sinh
# sinh(conj(z)) == conj(sinh(z))
# sinh(-z) == -sinh(z)
sinh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),         # ?
    ('nan', '-inf'): ('nan', 'nan'),         # ?
    ('nan', '0'): ('nan', '0'),
    ('nan', '+x'): ('nan', 'nan'),
    ('nan', '-x'): ('nan', 'nan'),
    ('+inf', 'nan'): ('+-inf', 'nan'),
    ('+inf', '+inf'): ('+-inf', 'nan'),      # and domain error
    ('+inf', '-inf'): ('+-inf', 'nan'),      # sinh(inf-infj) = conj(sinh(inf+infj)) = (+-inf, nan)
    ('+inf', '0'): ('+inf', '0'),
    ('+inf', '+x'): ('+inf * cos(im)', '+inf * sin(im)'), # x = im
    ('+inf', '-x'): ('+inf * cos(-im)', '-inf * sin(-im)'), # x = -im, sinh(inf-xj) = conj(sinh(inf+xj)) = (+inf cos(x), -inf * sin(x))
    ('-inf', 'nan'): ('+-inf', 'nan'),       # sinh(-inf+nanj) = -sinh(inf+nanj) = (+-inf, nan)
    ('-inf', '-inf'): ('+-inf', 'nan'),      # sinh(-inf-infj) = -sinh(inf+infj) = (+-inf, nan)
    ('-inf', '+inf'): ('+-inf', 'nan'),      # sinh(-inf+infj) = -sinh(inf-infj) = (+-inf, nan)
    ('-inf', '0'): ('-inf', '0'),            # sinh(-inf+0j) = -sinh(inf+0j) = (-inf, 0)
    ('-inf', '+x'): ('-inf * cos(im)', '+inf * sin(im)'), # sinh(-inf+xj) = -sinh(inf-xj) = (-inf*cos(x), inf * sin(x))
    ('-inf', '-x'): ('-inf * cos(-im)', '-inf * sin(-im)'), # sinh(-inf-xj) = -sinh(inf+xj) = (-inf*cos(x), -inf*sin(x))
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('+-0', 'nan'),
    ('0', '+inf'): ('+-0', 'nan'),           # and domain error
    ('0', '-inf'): ('nan', 'nan'),           # see x->0
    ('+x', 'nan'): ('nan', 'nan'),
    ('+x', '+inf'): ('nan', 'nan'),
    ('+x', '-inf'): ('nan', 'nan'),          # sinh(x-infj) = conj(sinh(x+infj)) = (nan, nan)
    ('-x', 'nan'): ('nan', 'nan'),
    ('-x', '+inf'): ('nan', 'nan'),          # sinh(-x+infj) = -sinh(x-infj) = (nan, nan)
    ('-x', '-inf'): ('nan', 'nan'),          # sinh(-x-infj) = -sinh(x+infj) = (nan, nan)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/cosh
# cosh(conj(z)) == conj(cosh(z))
# cosh(z) == cosh(-z)
cosh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),          # ?
    ('nan', '-inf'): ('nan', 'nan'),          # ?
    ('nan', '0'): ('nan', '0'),               # 0 sign unspecified
    ('nan', '+x'): ('nan', 'nan'),            # and domain error
    ('nan', '-x'): ('nan', 'nan'),            # and domain error
    ('+inf', 'nan'): ('+inf', 'nan'),
    ('+inf', '+inf'): ('+-inf', 'nan'),      # and domain error
    ('+inf', '-inf'): ('+-inf', 'nan'),      # cosh(inf-infj) = conj(cosh(inf+infj)) = (+-inf, nan)
    ('+inf', '0'): ('+inf', '0'),
    ('+inf', '+x'): ('+inf * cos(im)', '+inf * sin(im)'),
    ('+inf', '-x'): ('+inf * cos(-im)', '+inf * sin(-im)'),
    ('-inf', 'nan'): ('+inf', 'nan'),       # cosh(-inf+nanj) = cosh(inf+nanj) = (+inf, nan)
    ('-inf', '-inf'): ('+-inf', 'nan'),      # cosh(-inf-infj) = cosh(inf+infj) = (+-inf, nan)
    ('-inf', '+inf'): ('+-inf', 'nan'),      # cosh(-inf+infj) = cosh(inf-infj) = (+-inf, nan)
    ('-inf', '0'): ('inf', '0'),            # cosh(-inf+0j) = cosh(inf+0j) = (inf, 0)
    ('-inf', '+x'): ('+inf * cos(im)', '+inf * sin(im)'), # cosh(-inf+xj) = cosh(inf-xj) = (inf*cos(x), inf*sin(x))
    ('-inf', '-x'): ('+inf * cos(-im)', '+inf * sin(-im)'), # cosh(-inf-xj) = cosh(inf+xj) = (inf*cos(x), inf*sin(x))
    ('0', '0'): ('1', '+0'),
    ('0', 'nan'): ('nan', '+-0'),
    ('0', '+inf'): ('nan', '+-0'),            # and domain error
    ('0', '-inf'): ('nan', 'nan'),            # see x->0
    ('+x', 'nan'): ('nan', 'nan'),
    ('+x', '+inf'): ('nan', 'nan'),
    ('+x', '-inf'): ('nan', 'nan'),           # cosh(x-infj) = conj(cosh(x+infj)) = (nan, nan)
    ('-x', 'nan'): ('nan', 'nan'),
    ('-x', '+inf'): ('nan', 'nan'),
    ('-x', '-inf'): ('nan', 'nan'),           # cosh(-x-infj) = cosh(x+infj) = (nan, nan)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/tanh
# tanh(conj(z)) == conj(tanh(z))
# tanh(-z) == -tanh(z)

tanh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),        # ?
    ('nan', '-inf'): ('nan', 'nan'),        # ?
    ('nan', '0'): ('nan', '0'),
    ('nan', '+x'): ('nan', 'nan'),          # and domain error
    ('nan', '-x'): ('nan', 'nan'),          # and domain error
    ('+inf', 'nan'): ('1', '+-0'),
    ('+inf', '+inf'): ('1', '+-0'),
    ('+inf', '-inf'): ('1', '+-0'),         # tanh(inf-infj) = conj(tanh(inf+infj)) = (1, +-0)
    ('+inf', '0'): ('1', '0'),
    ('+inf', '+x'): ('1', '+0'),
    ('+inf', '-x'): ('1', '-0'),            # tanh(inf-xj) = conj(tanh(inf+xj)) = (1, -0)
    ('-inf', 'nan'): ('-1', '-+0'),         # tanh(-inf+nanj) = -tanh(inf+nanj) = (-1, -+0)
    ('-inf', '-inf'): ('-1', '-+0'),        # tanh(-inf-infj) = -tanh(inf+infj) = (-1, -+0)
    ('-inf', '+inf'): ('-1', '-+0'),        # tanh(-inf+infj) = -tanh(inf-infj) = (-1, -+0)
    ('-inf', '0'): ('-1', '0'),             # tanh(-inf+0j) = -tanh(inf+0j) = (-1, 0)
    ('-inf', '+x'): ('-1', '+0'),           # tanh(-inf+xj) = -tanh(inf-xj) = (-1, +0)
    ('-inf', '-x'): ('-1', '-0'),           # tanh(-inf-xj) = -tanh(inf+xj) = (-1, -0)
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('0', 'nan'),
    ('0', '+inf'): ('0', 'nan'),            # and domain error
    ('0', '-inf'): ('nan', 'nan'),          # see x->0
    ('+x', 'nan'): ('nan', 'nan'),          # and domain error
    ('+x', '+inf'): ('nan', 'nan'),         # and domain error
    ('+x', '-inf'): ('nan', 'nan'),         # tanh(x-infj) = conj(tanh(x+infj)) = (nan, nan)
    ('-x', 'nan'): ('nan', 'nan'),          # and domain error
    ('-x', '+inf'): ('nan', 'nan'),         # tanh(-x+infj) = -tanh(x-infj) = (nan, nan)
    ('-x', '-inf'): ('nan', 'nan'),         # tanh(-x-infj) = -tanh(x+infj) = (nan, nan)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/asinh
# asinh(conj(z)) == conj(asinh(z))
# asinh(-z) == -asinh(z)
asinh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('+-inf', 'nan'),      # (+-inf, nan)
    ('nan', '-inf'): ('+-inf', 'nan'),      # asinh(nan-infj) = conj(asinh(nan+infj)) = (+-inf, nan)
    ('nan', '0'): ('nan', '0'),
    ('nan', '+x'): ('nan', 'nan'),          # or domain error
    ('nan', '-x'): ('nan', 'nan'),          # or domain error
    ('+inf', 'nan'): ('+inf', 'nan'),
    ('+inf', '+inf'): ('+inf', 'pi / 4'),
    ('+inf', '-inf'): ('+inf', '-pi / 4'),  # asinh(inf-infj) = conj(asinh(inf+infj)) = (+inf, -pi/4)
    ('+inf', '0'): ('+inf', '0'),           # (+inf, +x) -> (+inf, 0), (+inf, -x) -> (+inf, 0) as x->0
    ('+inf', '+x'): ('+inf', '0'),
    ('+inf', '-x'): ('+inf', '0'),          # asinh(inf-xj) = conj(asinh(inf+xj)) = (+inf, 0)
    ('-inf', 'nan'): ('-inf', 'nan'),       # asinh(-inf+nanj) = -asinh(inf+nanj) = (-inf, nan)
    ('-inf', '-inf'): ('-inf', '-pi / 4'),  # asinh(-inf-infj) = -asinh(inf+infj) = (-inf, -pi/4)
    ('-inf', '+inf'): ('-inf', 'pi / 4'),   # asinh(-inf+infj) = -asinh(inf-infj) = (-inf, pi/4)
    ('-inf', '0'): ('-inf', 'nan'),         # asinh(-inf+0j) = -asinh(inf+0j) = (-inf, nan)
    ('-inf', '+x'): ('-inf', '0'),          # sinh(-inf+xj) = -asinh(inf-xj) = (-inf, 0)
    ('-inf', '-x'): ('-inf', '0'),          # asinh(-inf-xj) = -asinh(inf+xj) = (-inf, 0)
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('nan', 'nan'),           # or domain error
    ('0', '+inf'): ('nan', 'pi / 2'),       # (+x, +inf) -> (+inf, pi/2), (-x, +inf) -> (-inf, pi/2) as x->0
    ('0', '-inf'): ('nan', '-pi / 2'),      # ditto
    ('+x', 'nan'): ('nan', 'nan'),          # or domain error
    ('+x', '+inf'): ('+inf', 'pi / 2'),
    ('+x', '-inf'): ('+inf', '-pi / 2'),    # asinh(x-infj) = conj(asinh(x+infj)) = (inf, -pi/2)
    ('-x', 'nan'): ('nan', 'nan'),          # or domain error
    ('-x', '+inf'): ('-inf', 'pi / 2'),     # asinh(-x+infj) = -asinh(x-infj) = (-inf, pi/2)
    ('-x', '-inf'): ('-inf', '-pi / 2'),    # asinh(-x-infj) = -asinh(x+infj) = (-inf, -pi/2)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/acos
# acos(z) = pi - acos(-z)
# acos(conj(z)) == conj(acos(z))
acos = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', '-inf'),
    ('nan', '-inf'): ('nan', 'inf'),         # acos(nan-infj) = conj(acos(nan+infj)) = (nan, inf)
    ('nan', '0'): ('nan', 'nan'),            # or domain error
    ('nan', '+x'): ('nan', 'nan'),           # or domain error
    ('nan', '-x'): ('nan', 'nan'),           # or domain error
    ('+inf', 'nan'): ('nan', '+-inf'),
    ('+inf', '+inf'): ('pi / 4', '-inf'),
    ('+inf', '-inf'): ('pi / 4', '+inf'),    # acos(inf-infj) = conj(acos(inf + infj)) = (pi/4, inf)
    ('+inf', '0'): ('0', 'nan'),             # (+inf, +x) -> (0, -inf), (+inf, -x) -> (0, +inf) as x->0
    ('+inf', '+x'): ('0', '-inf'),
    ('+inf', '-x'): ('0', '+inf'),           # acos(inf-xj) = conj(acos(inf+xj)) = (0, +inf)
    ('-inf', 'nan'): ('nan', '+-inf'),
    ('-inf', '-inf'): ('3 * pi / 4', '+inf'), # acos(-inf-infj) = conj(acos(-inf+infj)) = (3 * pi / 4, inf)
                                             # acos(-inf-infj) = pi - acos(inf+infj) = (pi - pi / 4, inf)
    ('-inf', '+inf'): ('3 * pi / 4', '-inf'),
    ('-inf', '0'): ('pi', 'nan'),            # see x->0
    ('-inf', '+x'): ('pi', '-inf'),
    ('-inf', '-x'): ('pi', '+inf'),           # acos(-inf - xj) = pi - acos(inf + xj) = (pi, inf)
                                             # acos(-inf - xj) = conj(acos(-inf + xj)) = (pi, inf)
    ('0', '0'): ('pi/2', '0'),
    ('0', 'nan'): ('pi/2', 'nan'),
    ('0', '+inf'): ('pi/2', '-inf'),         # see x->0
    ('0', '-inf'): ('pi/2', '+inf'),         # acos(0-infj) = conj(acos(0+infj)) = (pi/2, inf)
    ('+x', 'nan'): ('nan', 'nan'),           # or domain error
    ('+x', '+inf'): ('pi / 2', '-inf'),
    ('+x', '-inf'): ('pi / 2', 'inf'),       # acos(x-infj) = conf(acos(x+infj)) = (pi/2, inf)
    ('-x', 'nan'): ('nan', 'nan'),           # or domain error
    ('-x', '+inf'): ('pi / 2', '-inf'),
    ('-x', '-inf'): ('pi / 2', 'inf'),       # acos(-x-infj) = pi - acos(x+infj) = (pi/2, inf)
                                             # acos(-x-infj) = conj(acos(-x+infj)) = (pi/2, inf)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/acosh
# acosh(conj(z)) == conj(acosh(z))
# acosh(z) = j acos(z) when re(z) > 0
acosh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('+inf', 'nan'),
    ('nan', '-inf'): ('+inf', 'nan'),         # acosh(nan-infj) = conj(acos(nan+infj)) = (+inf, nan)
    ('nan', '0'): ('nan', 'nan'),             # or domain error
    ('nan', '+x'): ('nan', 'nan'),            # or domain error
    ('nan', '-x'): ('nan', 'nan'),            # or domain error
    ('+inf', 'nan'): ('+inf', 'nan'),
    ('+inf', '+inf'): ('+inf', 'pi / 4'),     # acosh(inf+infj) = j * acos(inf+infj) = j * (pi/4, -inf) = (inf, pi/4)
    ('+inf', '-inf'): ('+inf', '-pi / 4'),    # acos(inf-infj) = conj(acosh(inf + infj)) = (inf, -pi/4)
    ('+inf', '0'): ('+inf', '0'),             # see x->0
    ('+inf', '+x'): ('+inf', '0'),
    ('+inf', '-x'): ('+inf', '0'),            # acosh(inf-xj) = conj(acosh(inf+xj)) = (+inf, 0)
    ('-inf', 'nan'): ('+inf', 'nan'),
    ('-inf', '-inf'): ('+inf', '-3 * pi / 4'), # acosh(-inf-infj) = conj(acosh(-inf+infj)) = (inf, -3 * pi / 4)
    ('-inf', '+inf'): ('+inf', '3 * pi / 4'),
    ('-inf', '0'): ('+inf', 'nan'),           # see x->0
    ('-inf', '+x'): ('+inf', 'pi'),
    ('-inf', '-x'): ('+inf', '-pi'),          # acosh(-inf - xj) = conj(acosh(-inf + xj)) = (inf, -pi)
    ('0', '0'): ('0', 'pi / 2'),
    ('0', 'nan'): ('nan', 'pi / 2'),
    ('0', '+inf'): ('+inf', 'pi / 2'),        # see x->0
    ('0', '-inf'): ('+inf', '-pi / 2'),       # acosh(0-infj) = conj(acosh(0+infj)) = (inf, -pi/2)
    ('+x', 'nan'): ('nan', 'nan'),            # or domain error
    ('+x', '+inf'): ('+inf', 'pi / 2'),
    ('+x', '-inf'): ('inf', '-pi / 2'),       # acosh(x-infj) = conf(acosh(x+infj)) = (inf, -pi/2)
    ('-x', 'nan'): ('nan', 'nan'),            # or domain error
    ('-x', '+inf'): ('+inf', 'pi / 2'),
    ('-x', '-inf'): ('+inf', 'pi / 2'),       # acosh(-x-infj) = conj(acosh(-x+infj)) = (inf, -pi/2)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/atanh
# atanh(conj(z)) == conj(atanh(z))
# atanh(-z) == -atanh(z)
atanh = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('+-inf', 'pi / 2'),
    ('nan', '-inf'): ('+-inf', '-pi / 2'),   # atanh(nan-infj) = conj(atanh(nan+infj)) = (+-inf, -pi/2)
    ('nan', '0'): ('nan', 'nan'),
    ('nan', '+x'): ('nan', 'nan'),           # or domain error
    ('nan', '-x'): ('nan', 'nan'),           # or domain error
    ('+inf', 'nan'): ('0', 'nan'),
    ('+inf', '+inf'): ('0', 'pi / 2'),
    ('+inf', '-inf'): ('0', '-pi / 2'),      # atanh(inf-infj) = conj(atanh(inf+infj)) = (0, -pi/2)
    ('+inf', '0'): ('0', 'nan'),             # see x->9
    ('+inf', '+x'): ('0', 'pi / 2'),
    ('+inf', '-x'): ('0', '-pi / 2'),        # atanh(inf-xj) = conj(atanh(inf+xj)) = (0, -pi/2)
    ('-inf', 'nan'): ('0', 'nan'),           # atanh(-inf+nanj) = -atanh(inf+nanj) = (0, nan)
    ('-inf', '-inf'): ('0', '-pi / 2'),      # atanh(-inf-infj) = -atanh(inf+infj) = (0, -pi/2)
    ('-inf', '+inf'): ('0', 'pi / 2'),       # atanh(-inf+infj) = -atanh(inf-infj) = (0, pi/2)
    ('-inf', '0'): ('0', 'nan'),             # atanh(-inf+0j) = -atanh(inf+0j) = (0, nan)
    ('-inf', '+x'): ('0', 'pi / 2'),         # atanh(-inf+xj) = -atanh(inf-xj) = (0, pi/2)
    ('-inf', '-x'): ('0', '-pi / 2'),        # atanh(-inf-xj) = -atanh(inf+xj) = (0, -pi/2)
    ('0', '0'): ('0', '0'),
    ('1', '0'): ('+inf', '0'),               # and divbyzero error
    ('0', 'nan'): ('0', 'nan'),
    ('0', '+inf'): ('0', 'pi / 2'),          # see x->0
    ('0', '-inf'): ('0', '-pi / 2'),         # see x->0
    ('+x', 'nan'): ('nan', 'nan'),           # or domain error
    ('+x', '+inf'): ('0', 'pi / 2'),
    ('+x', '-inf'): ('0', '-pi / 2'),        # atanh(x-infj) = conj(atanh(x+infj)) = (0, -pi/2)
    ('-x', 'nan'): ('nan', 'nan'),           # or domain error
    ('-x', '+inf'): ('0', 'pi / 2'),         # atanh(-x+infj) = -atanh(x-infj) = (0, pi/2)
    ('-x', '-inf'): ('0', '-pi / 2'),        # atanh(-x-infj) = -atanh(x+infj) = (0, -pi/2)
}


# Reference: https://en.cppreference.com/w/cpp/numeric/complex/sqrt
# sqrt(conj(z)) == conj(sqrt(z))
sqrt = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('+inf', '+inf'),
    ('nan', '-inf'): ('nan', 'nan'),         # ?
    ('nan', '0'): ('nan', 'nan'),            # and domain
    ('nan', '+x'): ('nan', 'nan'),           # and domain error
    ('nan', '-x'): ('nan', 'nan'),           # and domain error
    ('+inf', 'nan'): ('+inf', 'nan'),
    ('+inf', '+inf'): ('+inf', '+inf'),
    ('+inf', '-inf'): ('+inf', '-inf'),      # sqrt(inf-infj) = conj(sqrt(inf+infj)) = (inf, -inf)
    ('+inf', '0'): ('+inf', '0'),
    ('+inf', '+x'): ('+inf', '+0'),
    ('+inf', '-x'): ('+inf', '-0'),         
    ('-inf', 'nan'): ('nan', '+-inf'),
    ('-inf', '-inf'): ('inf', '-inf'),       # sqrt(-inf-infj) = conj(sqrt(-inf+infj)) = (inf, -inf)
    ('-inf', '+inf'): ('+inf', '+inf'),
    ('-inf', '0'): ('0', 'nan'),             # see x->0
    ('-inf', '+x'): ('+0', '+inf'),
    ('-inf', '-x'): ('0', '-inf'),           # sqrt(-inf-xj) = conj(sqrt(-inf+xj)) = (0, -inf)
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('0', 'nan'),
    ('0', '+inf'): ('+inf', '+inf'),
    ('0', '-inf'): ('+inf', '-inf'),         # sqrt(0-infj) = conj(sqrt(0+infj)) = (inf, -inf)
    ('+x', 'nan'): ('nan', 'nan'),           # and domain error
    ('+x', '+inf'): ('+inf', '+inf'),
    ('+x', '-inf'): ('+inf', '-inf'),        # sqrt(x-infj) = conj(sqrt(x+infj)) = (inf, -inf)
    ('-x', 'nan'): ('nan', 'nan'),           # and domain error
    ('-x', '+inf'): ('+inf', '+inf'),
    ('-x', '-inf'): ('+inf', '-inf'),        # sqrt(-x-infj) = conj(sqrt(-x+infj)) = (inf, -inf)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/exp
# exp(conj(z)) == conj(exp(z))
exp = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),
    ('nan', '-inf'): ('nan', 'nan'),
    ('nan', '0'): ('nan', '+0'),
    ('nan', '+x'): ('nan', 'im'),            # and domain error
    ('nan', '-x'): ('nan', 'im'),            # and domain error
    ('+inf', 'nan'): ('+-inf', 'nan'),
    ('+inf', '+inf'): ('+-inf', 'nan'),      # and domain error
    ('+inf', '-inf'): ('+-inf', 'nan'),      # exp(inf-infj) = conj(exp(inf+infj)) = (+-inf, nan)
    ('+inf', '0'): ('+inf', '+0'),
    ('+inf', '+x'): ('+inf * cos(im)', '+inf * sin(im)'),
    ('+inf', '-x'): ('+inf * cos(-im)', '+inf * sin(-im)'),
    ('-inf', 'nan'): ('+-0', '+-0'),
    ('-inf', '-inf'): ('+-0', '+-0'),        # exp(-inf-infj) = conj(exp(-inf+infj)) = (+-0, +-0)
    ('-inf', '+inf'): ('+-0', '+-0'),
    ('-inf', '0'): ('+0 * cos(im)', '+0 * sin(im)'),
    ('-inf', '+x'): ('+0 * cos(im)', '+0 * sin(im)'),
    ('-inf', '-x'): ('+0 * cos(-im)', '+0 * sin(-im)'),
    ('0', '0'): ('1', '+0'),
    ('0', 'nan'): ('nan', 'nan'),            # and domain error
    ('0', '+inf'): ('nan', 'nan'),           # and domain error
    ('0', '-inf'): ('nan', 'nan'),           # exp(0-infj) = conj(exp(0+infj)) = (nan, nan)
    ('+x', 'nan'): ('nan', 'nan'),           # and domain error
    ('+x', '+inf'): ('nan', 'nan'),          # and domain error
    ('+x', '-inf'): ('nan', 'nan'),          # exp(x-infj) = conj(exp(x+infj)) = (nan, nan)
    ('-x', 'nan'): ('nan', 'nan'),           # and domain error
    ('-x', '+inf'): ('nan', 'nan'),          # and domain error
    ('-x', '-inf'): ('nan', 'nan'),          # exp(-x-infj) = conj(exp(-x+infj)) = (nan, nan)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/log
# log(conj(z)) == conj(log(z))
log = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('+inf', 'nan'),
    ('nan', '-inf'): ('+inf', 'nan'),         # log(nan-infj) = conj(log(nan+infj)) = (+inf, nan)
    ('nan', '0'): ('nan', 'nan'),             # and domain error
    ('nan', '+x'): ('nan', 'nan'),            # and domain error
    ('nan', '-x'): ('nan', 'nan'),            # and domain error
    ('+inf', 'nan'): ('+inf', 'nan'),
    ('+inf', '+inf'): ('+inf', 'pi / 4'),     # and domain error
    ('+inf', '-inf'): ('+inf', '-pi / 4'),    # log(inf-infj) = conj(log(inf+infj)) = (+inf, -pi/4)
    ('+inf', '0'): ('+inf', '+0'),            # see x->0
    ('+inf', '+x'): ('+inf', '+0'),
    ('+inf', '-x'): ('+inf', '-0'),           # log(inf-xj) = conj(log(inf+xj)) = (+inf, -0)
    ('-inf', 'nan'): ('+inf', 'nan'),
    ('-inf', '-inf'): ('+inf', '-3 * pi / 4'), # log(-inf-infj) = conj(log(-inf+infj)) = (+inf, -3pi/4)
    ('-inf', '+inf'): ('+inf', '3 * pi / 4'),
    ('-inf', '0'): ('+inf', 'nan'),           # see x->0
    ('-inf', '+x'): ('+inf', 'pi'),
    ('-inf', '-x'): ('+inf', '-pi'),          # log(-inf-xj) = conj(log(-inf+xj)) = (inf, -pi)
    ('0', '0'): ('-inf', '+0'),               # and divbyzero error
    ('0', 'nan'): ('nan', 'nan'),             # and domain error
    ('0', '+inf'): ('+inf', 'pi / 2'),
    ('0', '-inf'): ('+inf', '-pi / 2'),       # log(0-infj) = conj(log(0+infj)) = (+inf, -pi/2)
    ('1', '0'): ('0', '0'),
    ('1', 'nan'): ('nan', 'nan'),             # and domain error
    ('1', '+inf'): ('+inf', 'pi / 2'),
    ('1', '-inf'): ('+inf', '-pi / 2'),      # log(x-infj) = conj(log(x+infj)) = (+inf, -pi/2)
    ('+x', 'nan'): ('nan', 'nan'),            # and domain error
    ('+x', '+inf'): ('+inf', 'pi / 2'),
    ('+x', '-inf'): ('+inf', '-pi / 2'),      # log(x-infj) = conj(log(x+infj)) = (+inf, -pi/2)
    ('-x', 'nan'): ('nan', 'nan'),            # and domain error
    ('-x', '+inf'): ('+inf', 'pi / 2'),
    ('-x', '-inf'): ('+inf', '-pi / 2'),      # log(-x-infj) = conj(log(-x+infj)) = (+inf, -pi/2)
}

# Reference: https://en.cppreference.com/w/cpp/numeric/complex/log10
# log10(z) = log(z) / log(10)
log10 = dict((k, (f'({re})/log(10)', f'({im})/log(10)')) for k, (re, im) in log.items())

# log2(z) = log(z) / log(2)
log2 = dict((k, (f'({re})/log(2)', f'({im})/log(2)')) for k, (re, im) in log.items())

# log1p(z) = log(1 + z)
log1p = dict((({'0': '-1', '1': '0'}.get(k0, k0), k1), v) for (k0, k1), v in log.items())

# square(z) = (Re(z)**2 - Im(z)**2, 2*Re(z)*Im(z))
square = {
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),
    ('nan', '-inf'): ('nan', 'nan'),
    ('nan', '0'): ('nan', 'nan'),
    ('nan', '+x'): ('nan', 'nan'),
    ('nan', '-x'): ('nan', 'nan'),
    ('+inf', 'nan'): ('nan', 'nan'),
    ('+inf', '+inf'): ('nan', '+inf'),
    ('+inf', '-inf'): ('nan', '-inf'),
    ('+inf', '0'): ('+inf', 'nan'),
    ('+inf', ''): ('+inf', '0'),
    ('+inf', '+x'): ('+inf', '+inf'),
    ('+inf', '-x'): ('+inf', '-inf'),
    ('-inf', 'nan'): ('nan', 'nan'),
    ('-inf', '-inf'): ('nan', '+inf'),
    ('-inf', '+inf'): ('nan', '-inf'),
    ('-inf', '0'): ('+inf', 'nan'),
    ('-inf', ''): ('+inf', '0'),
    ('-inf', '+x'): ('+inf', '-inf'),
    ('-inf', '-x'): ('+inf', '+inf'),
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('nan', 'nan'),
    ('0', '+inf'): ('-inf', 'nan'),
    ('0', '-inf'): ('-inf', 'nan'),
    ('+x', 'nan'): ('nan', 'nan'),
    ('+x', '+inf'): ('-inf', '+inf'),
    ('+x', '-inf'): ('-inf', '-inf'),
    ('-x', 'nan'): ('nan', 'nan'),
    ('-x', '+inf'): ('-inf', '-inf'),
    ('-x', '-inf'): ('-inf', '+inf'),
}

# TODO: sinc(z) = sinh(j * z) / (j * z)

# j * (re, im) = (-im, re)
sinc_todo = {  # copy of sinh:
    ('nan', 'nan'): ('nan', 'nan'),
    ('nan', '+inf'): ('nan', 'nan'),
    ('nan', '-inf'): ('nan', 'nan'),
    ('nan', '0'): ('nan', '0'),
    ('nan', '+x'): ('nan', 'nan'),
    ('nan', '-x'): ('nan', 'nan'),
    ('+inf', 'nan'): ('+-inf', 'nan'),
    ('+inf', '+inf'): ('+-inf', 'nan'),
    ('+inf', '-inf'): ('+-inf', 'nan'),
    ('+inf', '0'): ('+inf', '0'),
    ('+inf', '+x'): ('+inf * cos(im)', '+inf * sin(im)'),
    ('+inf', '-x'): ('+inf * cos(-im)', '-inf * sin(-im)'),
    ('-inf', 'nan'): ('+-inf', 'nan'),
    ('-inf', '-inf'): ('+-inf', 'nan'),
    ('-inf', '+inf'): ('+-inf', 'nan'),
    ('-inf', '0'): ('-inf', '0'),
    ('-inf', '+x'): ('-inf * cos(im)', '+inf * sin(im)'),
    ('-inf', '-x'): ('-inf * cos(-im)', '-inf * sin(-im)'),
    ('0', '0'): ('0', '0'),
    ('0', 'nan'): ('+-0', 'nan'),
    ('0', '+inf'): ('+-0', 'nan'),
    ('0', '-inf'): ('nan', 'nan'),
    ('+x', 'nan'): ('nan', 'nan'),
    ('+x', '+inf'): ('nan', 'nan'),
    ('+x', '-inf'): ('nan', 'nan'),
    ('-x', 'nan'): ('nan', 'nan'),
    ('-x', '+inf'): ('nan', 'nan'),
    ('-x', '-inf'): ('nan', 'nan'),
}
