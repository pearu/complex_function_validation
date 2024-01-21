"""Complex function validation tool.
"""

import numpy
import contextlib
import importlib


class ComplexPlaneSampler:
    """A sample array covering a complex plane for the given numpy dtype.
    """
    def __init__(self, dtype):
        self.dtype = dtype
        self.finfo = numpy.finfo(dtype)

    def __call__(self, size_re, size_im):
        """Return a 2-D array of complex numbers that covers the complex plane
        with a grid of samples.

        The size of the grid is (3 + 2 * size_im) x (3 + 2 * size_re)
        that includes infinity points, extreme finite points, and
        points from real and imaginary axis.

        For example:

        >>> print(ComplexPlaneSample(numpy.complex64)(0, 3)
        [[-inf          -infj   0.          -infj  inf          -infj]
         [-inf-3.4028235e+38j   0.-3.4028235e+38j  inf-3.4028235e+38j]
         [-inf-1.9999963e+00j   0.-1.9999963e+00j  inf-1.9999963e+00j]
         [-inf-1.1754944e-38j   0.-1.1754944e-38j  inf-1.1754944e-38j]
         [-inf+0.0000000e+00j   0.+0.0000000e+00j  inf+0.0000000e+00j]
         [-inf+1.1754944e-38j   0.+1.1754944e-38j  inf+1.1754944e-38j]
         [-inf+1.9999963e+00j   0.+1.9999963e+00j  inf+1.9999963e+00j]
         [-inf+3.4028235e+38j   0.+3.4028235e+38j  inf+3.4028235e+38j]
         [-inf          +infj   0.          +infj  inf          +infj]]
        """
        real_axis_points = numpy.zeros(3 + 2 * size_re, dtype=self.finfo.dtype)
        imag_axis_points = numpy.zeros(3 + 2 * size_im, dtype=self.finfo.dtype)

        logmin = numpy.log10(abs(self.finfo.min))
        logtiny = numpy.log10(self.finfo.tiny)
        logmax = numpy.log10(self.finfo.max)

        real_axis_points[1:size_re+1] = -numpy.logspace(logmin, logtiny, size_re, dtype=self.finfo.dtype)
        real_axis_points[-size_re-1:-1] = numpy.logspace(logtiny, logmax, size_re, dtype=self.finfo.dtype)
        if size_re > 1:
            real_axis_points[1] = self.finfo.min
            real_axis_points[-2] = self.finfo.max
        if size_re > 0:
            real_axis_points[size_re] = -self.finfo.tiny
            real_axis_points[-size_re-1] = self.finfo.tiny
        real_axis_points[0] = -numpy.inf
        real_axis_points[-1] = numpy.inf

        imag_axis_points[1:size_im+1] = -numpy.logspace(logmin, logtiny, size_im, dtype=self.finfo.dtype)
        imag_axis_points[-size_im-1:-1] = numpy.logspace(logtiny, logmax, size_im, dtype=self.finfo.dtype)
        if size_im > 1:
            imag_axis_points[1] = self.finfo.min
            imag_axis_points[-2] = self.finfo.max
        if size_im > 0:
            imag_axis_points[size_im] = -self.finfo.tiny
            imag_axis_points[-size_im-1] = self.finfo.tiny
        imag_axis_points[0] = -numpy.inf
        imag_axis_points[-1] = numpy.inf

        real_part = real_axis_points.reshape((-1, 3 + 2 * size_re)).repeat(3 + 2 * size_im, 0).astype(self.dtype)

        imag_part = imag_axis_points.repeat(2).view(self.dtype)
        imag_part.real[:] = 0
        imag_part = imag_part.reshape((3 + 2 * size_im, -1)).repeat(3 + 2 * size_re, 1)

        return real_part + imag_part


def compare_legend():
    return {
        '=': 'values are equal (diff == 0)',
        'c': 'values are close (diff < eps * norm)',
        '[1-F]': 'values are close (diff < eps * norm * 10 ** n, n < resolution)',
        'x': 'values magnitudes are close (diff is approx. eps * norm * 10 ** resolution)',
        'X': 'values are different (diff >= eps * norm * 10 ** resolution or one is non-finite)',
        '~': 'values are non-finite and of the same kind (-inf, inf, or nan)',
        'I': 'one value is finite but other inf',
        'N': 'one value is not nan but other is nan',
        'M': 'one value is nan but other is not nan',
    }


def compare(reference, value):
    """Return a string code that describes how value compares to
    reference value. See `compare_legend()` for descriptions.

    Both reference and value must have the same dtype and be numpy array object.
    """
    assert reference.dtype == value.dtype, (reference, value)
    finfo = numpy.finfo(value.dtype)
    if numpy.isfinite(reference):
        if numpy.isfinite(value):
            if reference == value:
                return '='
            diff = abs(reference - value)
            norm = max(abs(reference), abs(value))
            if diff < finfo.eps * norm:
                return 'c'
            reldiff = diff / norm / finfo.eps
            n = round(numpy.log10(reldiff))
            if n == finfo.precision:
                return 'x'
            elif n > finfo.precision:
                return 'X'
            return '123456789ABCDEF'[n]
        elif numpy.isinf(value):
            return 'I'
        else:
            return 'N'
    elif numpy.isinf(reference):
        if reference == value:
            return '~'
        elif numpy.isnan(value):
            return 'N'
        else:
            return 'X'
    else:
        if numpy.isnan(value):
            return '~'
        return 'M'


def valuetostr(value):
    f = numpy.finfo(value.dtype)
    if numpy.isnan(value): return 'nan'
    if numpy.isposinf(value): return '+inf'
    if numpy.isneginf(value): return '-inf'
    if value == 0: return '0'
    if value == f.max: return 'max'
    if value == f.min: return 'min'
    if value == f.tiny: return 'tiny'
    if value == -f.tiny: return '-tiny'
    #if abs(value) <= 100 and abs(value) >= 1:
    #    return f'{int(value)}'
    return f'{value:1.0e}'.replace('e-0', 'e-').replace('e+0', 'e').replace('e+', 'e').replace('e0', '')


class ReportImage:
    """A helper class for visualizing function comparisons on text-terminal.
    """
    def __init__(self, height=0, width=0):
        self.image = numpy.full((height, width), b' ', dtype='c')
        self.stats = []

    def _ensure_index(self, row, col):
        if row >= self.image.shape[0]:
            self.image = numpy.vstack((self.image, numpy.full((row - self.image.shape[0] + 1, self.image.shape[1]), ' ', dtype=self.image.dtype)))
        if col >= self.image.shape[1]:
            self.image = numpy.hstack((self.image, numpy.full((self.image.shape[0], col - self.image.shape[1] + 1), ' ', dtype=self.image.dtype)))

    def _fix_indices(self, row, col):
        if row < 0:
            row += self.image.shape[0] + 1
        if col < 0:
            col += self.image.shape[1] + 1
        return row, col

    def insert(self, row, col, subimage):
        row, col = self._fix_indices(row, col)
        self._ensure_index(row + subimage.shape[0], col + subimage.shape[1])
        self.image[row:row+subimage.shape[0], col:col+subimage.shape[1]] = subimage

    def insert_comparison(self, row, col, reference, values):
        from collections import defaultdict
        row, col = self._fix_indices(row, col)
        self._ensure_index(row + reference.shape[0], col + reference.shape[1])
        stats = defaultdict(int)
        for i in range(reference.shape[0]):
            for j in range(reference.shape[1]):
                c = compare(reference[i, j], values[i, j])
                self.image[row + i, col + j] = c
                stats[c] += 1
        self.stats.append(stats)

    def insert_imag_axis(self, row, col, samples):
        for i in range(samples.shape[0]):
            n = valuetostr(samples[i, 0].imag) + 'j'
            self.insert_text(row + i, col, n, align='right')

    def insert_real_axis(self, row, col, samples):
        last_j = -10
        for j in range(samples.shape[1]):
            n = valuetostr(samples[0, j].real)
            if n == '-tiny':
                continue
            if n == '0':
                self.insert_text(row, col + j, '^')
                self.insert_text(row + 1, col + j, n, align='left')
                break
            if j - len(n) <= last_j:
                continue
            last_j = j
            self.insert_text(row, col + j, '^')
            self.insert_text(row + 1, col + j + 1, n, align='right')                

        last_j = samples.shape[1] + 10
        for j in reversed(range(samples.shape[1])):
            n = valuetostr(samples[0, j].real)
            if n == 'tiny' or n == '0':
                break
            if j + len(n) >= last_j - 1:
                continue
            self.insert_text(row, col + j, '^')
            self.insert_text(row + 1, col + j, n, align='left')
            last_j = j
            
    def insert_text(self, row, col, text, align='left'):
        row, col = self._fix_indices(row, col)
        if '\n' in text:
            for i, line in enumerate(text.splitlines()):
                self.insert_text(row + i, col, line, align=align)
        elif align == 'left':
            self._ensure_index(row, col + len(text) - 1)
            self.image[row, col:col + len(text)] = text
        elif align == 'right':
            self._ensure_index(row, col)
            if len(text) > col:
                text = text[-col:]
            self.image[row, col - len(text): col] = text
        else:
            raise NotImplementedError(aligh)

    def insert_legend(self, row, col):
        row, col = self._fix_indices(row, col)
        self.insert_text(row, max(0, col - 10), 'Legend:')
        for i, (key, descr) in enumerate(compare_legend().items()):
            self.insert_text(row + i + 1, col, ':')
            self.insert_text(row + i + 1, col - 1, key, align='right')
            self.insert_text(row + i + 1, col + 2, descr, align='left')

    def insert_hline(self, row, char='-'):
        row, col = self._fix_indices(row, 0)
        self.insert_text(row, col, char * self.image.shape[1])
            
    def tostring(self):
        lst = []
        for row in self.image:
            lst.append((b''.join(row)).decode())
        return '\n'.join(lst)

    def __str__(self):
        return self.tostring()

    def get_stats(self):
        results = []
        for stats in self.stats:
            inaccuracies = sum(stats[n] for n in '123456789ABCDEF')
            mismatches = stats['x'] + stats['X'] + stats['N'] + stats['I'] + stats['M']
            matches = stats["="] + stats["c"] + stats["~"]
            total = inaccuracies + mismatches + matches
            results.append(dict(matches=matches, inaccuracies=inaccuracies, mismatches=mismatches, total=total))
        return results

    def stats_summary(self, stats):
        lines = []
        inaccuracies = sum(stats[n] for n in '123456789ABCDEF')
        mismatches = stats['x'] + stats['X'] + stats['N'] + stats['I'] + stats['M']
        matches = stats["="] + stats["c"] + stats["~"]
        total = inaccuracies + mismatches + matches
        lines.append(f'match rate: {100 * matches / total:3.1f}%')
        if inaccuracies:
            lines.append(f'inaccuracies rate: {100 * inaccuracies / total:3.1f}%')
        if mismatches:
            lines.append(f'mismatch rate: {100 * mismatches / total:3.1f}%')
        return '\n'.join(lines)

    def generate_report(self, ref, functions, size_re=None, size_im=None):
        """Generate a comparision report of reference and given functions.

        Parameters
        ----------
        ref: Function
        functions: a sequence of Function instances
        """
        if size_re is None:
            size_re = 50
        if size_im is None:
            size_im = size_re

        imag_axis_width = 10
        map_height, map_width = 2*size_im + 3, 2*size_re + 3
        voffset = 1
        stats_list = []
        for index, f in enumerate(functions):
            np_samples = ComplexPlaneSampler(f.numpy_dtype)(size_re, size_im)

            with ref.context:
                ref_samples = ref.from_numpy(np_samples)
                ref_values = ref(ref_samples)
                np_ref_values = ref.to_numpy(ref_values, dtype=f.numpy_dtype)

            with f.context:
                native_samples = f.from_numpy(np_samples)
                native_values = f(native_samples)
                np_values = f.to_numpy(native_values)

            hoffset = index * (imag_axis_width + map_width + 2) 
            self.insert_comparison(voffset, hoffset + imag_axis_width, np_ref_values[::-1], np_values[::-1])
            self.insert_imag_axis(voffset, hoffset + -2 + imag_axis_width, np_samples[::-1])
            self.insert_real_axis(voffset + map_height, hoffset + imag_axis_width, np_samples[::-1])

            self.insert_text(voffset + map_height + 3, hoffset + imag_axis_width - 8, f'{f.title}\nvs\n{ref.title}')
            self.insert_text(voffset + map_height + 8, hoffset, '\nStatistics:')
            self.insert_text(voffset + map_height + 10, hoffset + 4, f'{self.stats_summary(self.stats[-1])}')


class Function:
    """Base class to provider functions.
    """

    library_name = NotImplemented
    namsespace = NotImplemented

    def __init__(self, name, dtype, device=''):
        self._name = name
        self._dtype = dtype
        self._device = device or 'cpu'
        self._module = None

    @classmethod
    def get_module_version(cls):
        module = cls.get_module()
        if module is not None:
            version = getattr(module, '__version__')
            return f'{cls.namespace} {version}'
        
    @classmethod
    def get_module(cls):
        try:
            return importlib.import_module(cls.namespace)
        except ImportError:
            pass

    @property
    def is_valid(self):
        return True

    @property
    def module(self):
        if self._module is None:
            self._module = self.get_module()
        return self._module

    @property
    def title(self):
        return f'{self._device.upper()}\n{self.namespace}.{self._name} on {self._dtype} plane'.strip()

    @property
    def dtype(self):
        return getattr(self.module, self._dtype)

    @property
    def numpy_dtype(self):
        return getattr(numpy, self._dtype)

    def from_numpy(self, data):
        return self.module.array(data, dtype=self.dtype)

    def to_numpy(self, data, dtype=None):
        if dtype is None:
            dtype = self.numpy_dtype
        return numpy.array(data, dtype=dtype)
    
    def __call__(self, *args):
        return getattr(self.module, self._name)(*args)

    @property
    def context(self):
        return contextlib.nullcontext()

    @classmethod
    def get_valid_functions(cls, fname, dtype):
        result = []
        if cls.get_module() is not None:
            for device_ in ['cpu', 'cuda']:
                f = cls(fname, dtype, device_)
                if f.is_valid:
                    result.append(f)
        return result


class NumpyFunction(Function):

    library_name = 'NumPy'
    namespace = 'numpy'

    @property
    def is_valid(self):
        return self._device.lower() in {'cpu', ''}


class JaxNumpyFunction(Function):

    library_name = 'JAX'
    namespace = 'jax.numpy'

    @classmethod
    def get_module_version(cls):
        module = cls.get_module()
        if module is not None:
            import jax
            return f'jax {jax.__version__}'

    @classmethod
    def get_module(cls):
        try:
            module = importlib.import_module(cls.namespace)
        except ImportError:
            module = None
        if module is not None:
            import jax
            try:
                # Fixes RuntimeError: Backend 'cuda' failed to initialize:
                # Found cuDNN version 8700, but JAX was built against
                # version 8800, which is newer.
                #
                # cuDNN 8700 comes from importing torch
                #
                jax.devices('cuda')
            except Exception:
                pass
        return module

    @property
    def context(self):
        import jax
        return jax.default_device(jax.devices(self._device)[0])

    @property
    def is_valid(self):
        if self._device == 'cuda':
            import jax
            try:
                _ = jax.device_put(jax.numpy.ones(1), device=jax.devices('gpu')[0])
                return True
            except:
                return False
        return True


class TorchFunction(Function):

    library_name = 'PyTorch'
    namespace = 'torch'

    @property
    def is_valid(self):
        if self._device == 'cuda':
            import torch.cuda
            return torch.cuda.is_available()
        return True

    def from_numpy(self, data):
        return self.module.tensor(data, dtype=self.dtype, device=self._device)

    def to_numpy(self, data):
        return numpy.array(data.cpu(), dtype=self.numpy_dtype)