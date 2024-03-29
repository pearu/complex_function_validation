"""Complex function validation tool.
"""

import numpy
import contextlib
import importlib

from . import special_cases

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


def ftz(value):
    """Flush subnormals to zero.
    """
    tiny = numpy.finfo(value.dtype).tiny
    if value.dtype.kind == 'c':
        float_dtype = {8: numpy.float32, 16: numpy.float64, 32: numpy.float128}[value.dtype.itemsize]
        view = value.reshape((1,)).view(float_dtype)
        re = view[0]
        im = view[1]
        if numpy.isfinite(re) and re != 0 and abs(re) < tiny:
            view[0] *= 0
        if numpy.isfinite(im) and im != 0 and abs(im) < tiny:
            view[1] *= 0
        return view.view(value.dtype)[0]
    assert value.dtype.kind == 'f', value.dtype
    float_dtype = {4: numpy.float32, 8: numpy.float64, 16: numpy.float128}[value.dtype.itemsize]
    view = value.reshape((1,)).view(float_dtype)
    re = view[0]
    if numpy.isfinite(re) and re != 0 and abs(re) < tiny:
        view[0] *= 0
    return view.view(value.dtype)[0]

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
        if reference == value or str(reference) == str(value):
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
    return f'{value:1.0e}'.replace('e-0', 'e-').replace('e+0', 'e').replace('e+', 'e').replace('e0', '')


class ReportImage:
    """A helper class for visualizing function comparisons on text-terminal.
    """
    def __init__(self, height=0, width=0):
        self.image = numpy.full((height, width), b' ', dtype='c')
        self.stats = []
        self.image_slices = []
        self.reference_and_values = []
        self.unsaved_stats = []
        self.unsaved_image_slices = []
        self.unsaved_reference_and_values = []

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

    def insert_comparison(self, row, col, reference, values, inputs, save=True, apply_ftz=False):
        from collections import defaultdict
        row, col = self._fix_indices(row, col)
        self._ensure_index(row + reference.shape[0], col + reference.shape[1])
        stats = defaultdict(int)
        for i in range(reference.shape[0]):
            for j in range(reference.shape[1]):
                if apply_ftz:
                    reference[i, j] = ftz(reference[i, j])
                c = compare(reference[i, j], values[i, j])
                self.image[row + i, col + j] = c
                stats[c] += 1
        if save:
            self.image_slices.append((slice(row, row + reference.shape[0]), slice(col, col + reference.shape[1])))
            self.reference_and_values.append((reference, values, inputs))
            self.stats.append(stats)
        else:
            self.unsaved_image_slices.append((slice(row, row + reference.shape[0]), slice(col, col + reference.shape[1])))
            self.unsaved_reference_and_values.append((reference, values, inputs))
            self.unsaved_stats.append(stats)

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
            lst.append((b''.join(row)).decode().rstrip())
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
            apply_ftz = f.apply_ftz(f._device)
            np_samples = ComplexPlaneSampler(f.numpy_dtype)(size_re, size_im)
            np_samples_real = np_samples.real[size_im + 1:size_im + 2]

            np_ref_values = ref.evaluate(np_samples, f.numpy_dtype)
            np_ref_values_real = ref.evaluate(np_samples_real, f.numpy_real_dtype)

            np_values = f.evaluate(np_samples, f.numpy_dtype)
            np_values_real = f.evaluate(np_samples_real, f.numpy_real_dtype)

            hoffset = index * (imag_axis_width + map_width + 2)
            self.insert_comparison(voffset, hoffset + imag_axis_width, np_ref_values[::-1].copy(), np_values[::-1], np_samples[::-1], apply_ftz=apply_ftz)
            self.insert_imag_axis(voffset, hoffset + -2 + imag_axis_width, np_samples[::-1])

            self.insert_text(voffset + map_height + 1, hoffset + 10, "real line:", align='right')
            self.insert_comparison(voffset + map_height + 1, hoffset + imag_axis_width, np_ref_values_real.copy(), np_values_real, np_samples_real, save=False, apply_ftz=apply_ftz)

            self.insert_real_axis(voffset + map_height + 2, hoffset + imag_axis_width, np_samples[::-1])

            self.insert_text(voffset + map_height + 3 + 2, hoffset + imag_axis_width - 8, f'{f.title}\nvs\n{ref.title}')
            self.insert_text(voffset + map_height + 8 + 2, hoffset, '\nStatistics:')
            self.insert_text(voffset + map_height + 10 + 2, hoffset + 4, f'{self.stats_summary(self.stats[-1])}')

    def get_sample_indices(self, image, code):

        def show(image):
            rows = []
            for row in image[::-1]:
                rows.append((b''.join(row)).decode())
            return '\n'.join(rows)

        c_re, c_im = image.shape[0] // 2, image.shape[1] // 2
        samples = []
        for region_slice in [
                (slice(c_re + 1, image.shape[0]), slice(c_im + 1, image.shape[1])),
                (slice(0, c_re), slice(c_im + 1, image.shape[1])),
                (slice(c_re + 1, image.shape[0]), slice(0, c_im)),
                (slice(0, c_re), slice(0, c_im)),
                (slice(c_re, c_re+1), slice(0, image.shape[1])),
                (slice(0, image.shape[0]), slice(c_im, c_im+1))
        ]:
            region = image[region_slice]
            clusters = Clusters()
            for point in zip(*numpy.where(region == code.encode())):
                clusters.add(point)

            for cluster in clusters.clusters:
                x, y = cluster.center_point()
                samples.append((region_slice[0].start + x, region_slice[1].start + y))

        return samples

    def get_samples(self, code):
        samples = []
        reference, values, inputs = self.reference_and_values[-1]
        image = self.image[self.image_slices[-1]]
        for point in self.get_sample_indices(image, code):
            samples.append((reference[point], values[point], inputs[point]))

        reference, values, inputs = self.unsaved_reference_and_values[-1]
        image = self.image[self.unsaved_image_slices[-1]]
        for point in self.get_sample_indices(image, code):
            samples.append((reference[point], values[point], inputs[point]))

        return samples

    def insert_samples(self, row, col, codes):
        row, col = self._fix_indices(row, col)

        i = 0
        for code in codes:
            samples = self.get_samples(code)
            if samples:
                self.insert_text(row + i, col, f"Samples with code {code}:")
                i += 1
                for ref, value, input in samples:
                    self.insert_text(row + i, col, f"{input:55} -> {value:55} {ref:55}")
                    i += 1

        if i > 0:
            self.insert_text(row + i, col, f"Legend:\n    <input> -> <value> <reference value>")

class Cluster:

    def __init__(self):
        self.points = set()

    def contains(self, point):
        for x, y in self.points:
            for dx in {-1, 0, 1}:
                for dy in {-1, 0, 1}:
                    if point == (x + dx, y + dy):
                        return True
        return False

    def add(self, point):
        self.points.add(point)

    def merge_from(self, other):
        self.points.update(other.points)

    def __repr__(self):
        return f'{type(self).__name__}({self.points})'

    def center(self):
        sx, sy = 0, 0
        for x, y in self.points:
            sx += x
            sy += y
        return (sx / len(self.points), sy / len(self.points))

    def center_point(self):
        cx, cy = self.center()
        lst = []
        for x, y in self.points:
            lst.append((abs(x - cx) + abs(y - cy), (x, y)))
        return sorted(lst)[0][1]

class Clusters:

    def __init__(self):
        self.clusters = []

    def __repr__(self):
        return f'{type(self).__name__}({self.clusters})'

    def add(self, point):
        matching_clusters = []
        for index, cluster in enumerate(self.clusters):
            if cluster.contains(point):
                matching_clusters.append(index)

        if len(matching_clusters) == 0:
            self.clusters.append(Cluster())
            self.clusters[-1].add(point)
        elif len(matching_clusters) == 1:
            self.clusters[matching_clusters[0]].add(point)
        else:
            cluster = self.clusters[matching_clusters[0]]
            for index in reversed(matching_clusters[1:]):
                cluster.merge_from(self.clusters[index])
                del self.clusters[index]


class Function:
    """Base class to provider functions.
    """

    library_name = NotImplemented
    namespace = NotImplemented
    array_namespace = NotImplemented

    def __init__(self, name, dtype, device=''):
        self._name = name
        self._dtype = dtype
        self._real_dtype = dict(complex64='float32', complex128='float64', complex256='float64')[dtype]
        self._device = device or 'cpu'
        self._module = None
        self._array_module = None

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

    @classmethod
    def get_array_module(cls):
        try:
            return importlib.import_module(cls.array_namespace)
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
    def array_module(self):
        if self._array_module is None:
            self._array_module = self.get_array_module()
        return self._array_module

    @property
    def title(self):
        return f'{self._device.upper()}\n{self.namespace}.{self._name} on {self._dtype} plane'.strip()

    @property
    def dtype(self):
        return getattr(self.array_module, self._dtype)

    @property
    def real_dtype(self):
        return getattr(self.array_module, self._real_dtype)

    @property
    def numpy_dtype(self):
        return getattr(numpy, self._dtype)

    @property
    def numpy_real_dtype(self):
        return getattr(numpy, self._real_dtype)

    def from_numpy(self, data, dtype=None):
        if dtype is None:
            dtype = self.dtype
        return self.array_module.array(data, dtype=dtype)

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

    @classmethod
    def apply_ftz(cls, *args, **kwargs):
        raise NotImplementedError(cls.__name__)

    def evaluate(self, np_samples, numpy_dtype):
        if np_samples.dtype.kind == 'c':
            dtype = self.dtype
        dtype = {'c': self.dtype, 'f': self.real_dtype}[np_samples.dtype.kind]

        with self.context:
            samples = self.from_numpy(np_samples, dtype=dtype)
            values = self(samples)
            np_values = self.to_numpy(values, dtype=numpy_dtype)
        return np_values


class NumpyFunction(Function):

    library_name = 'NumPy'
    namespace = 'numpy'
    array_namespace = 'numpy'

    @property
    def is_valid(self):
        return self._device.lower() in {'cpu', ''}

    @classmethod
    def apply_ftz(cls, *args, **kwargs):
        return False


class ComplexMathFunction(NumpyFunction):
    library_name = 'ComplexMath'
    namespace = 'complex_function_validation.complex_math'
    array_namespace = 'numpy'

    @property
    def is_valid(self):
        return self._device.lower() in {'cpu', ''} and hasattr(self.get_module(), self._name)

    
class JaxNumpyFunction(Function):

    library_name = 'JAX'
    namespace = 'jax.numpy'
    array_namespace = 'jax.numpy'

    _jax_module = None
    
    @classmethod
    def get_module_version(cls):
        module = cls.get_module()
        if module is not None:
            import jax
            return f'jax {jax.__version__}'

    @classmethod
    def get_module(cls):
        if cls._jax_module is not None:
            return cls._jax_module
        import os
        os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION'] = '8'
        try:
            module = importlib.import_module(cls.namespace)
        except ImportError:
            module = None
        if module is not None:
            import jax
            # Workaround https://github.com/google/jax/issues/18032#issuecomment-1869072346
            import jaxlib.cuda._versions
            jaxlib.cuda._versions.cudnn_get_version()
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
        cls._jax_module = module
        return module

    @property
    def context(self):
        import jax
        jax.config.update("jax_enable_x64", True)
        return jax.default_device(jax.devices(self._device)[0])

    @property
    def is_valid(self):
        if self._device == 'cuda':
            import jax
            try:
                _ = jax.device_put(jax.numpy.ones(1), device=jax.devices('gpu')[0])
                return True
            except Exception as msg:
                return False
        return True

    @classmethod
    def apply_ftz(cls, device):
        return device in {'cpu', ''}

class TorchFunction(Function):

    library_name = 'PyTorch'
    namespace = 'torch'
    array_namespace = 'torch'

    @property
    def is_valid(self):
        if self._device == 'cuda':
            import torch.cuda
            return torch.cuda.is_available()
        return True

    def from_numpy(self, data, dtype=None):
        if dtype is None:
            dtype = self.dtype
        return self.module.tensor(data, dtype=dtype, device=self._device)

    def to_numpy(self, data, dtype=None):
        if dtype is None:
            dtype = self.numpy_dtype
        return numpy.array(data.cpu(), dtype=dtype)

    @classmethod
    def apply_ftz(cls, *args, **kwargs):
        return False


class MPMathFunction(Function):
    library_name = 'MPMath'
    namespace = 'mpmath'
    array_namespace = 'numpy'

    @property
    def is_valid(self):
        return self._device.lower() in {'cpu', ''}

    @classmethod
    def apply_ftz(cls, *args, **kwargs):
        return False

    @property
    def context(self):
        import mpmath
        precision = dict(float128=36, float64=18, float32=9)[self._real_dtype] + 2
        return mpmath.workdps(precision)

    def __call__(self, *args):
        mpmath = self.module
        assert len(args) == 1

        def tosymbolpair(x):
            if x.real == 0:
                re = '0'
            elif mpmath.isfinite(x.real):
                re = '+x' if x.real > 0 else '-x'
            else:
                re = str(x.real)
            if x.imag == 0:
                im = '0'
            elif mpmath.isfinite(x.imag):
                im = '+x' if x.imag > 0 else '-x'
            else:
                im = str(x.imag)
            return re, im

        def special_cases_func(name, x):
            is_real = False
            if isinstance(x, float):
                if (
                        (name in {'sqrt', 'log', 'log10', 'log2'} and x < 0)
                        or (name=='log1p' and x < -1)
                        or (name in {'asin', 'acos', 'atanh'} and abs(x) > 1)
                        or (name == 'acosh' and x < 1)
                ):
                    return float('nan')
                is_real = True
                x = mpmath.mpc(x, 0)
            elif isinstance(x, complex):
                x = mpmath.mpc(x.real, x.imag)
            else:
                assert 0, x

            if mpmath.isfinite(x.real) and mpmath.isfinite(x.imag):
                return

            re, im = tosymbolpair(x)
            if is_real and name in {'square'} and im == '0':
                # reset im when f(re+0j) is different from f(re)
                im = ''
            result = None
            if name in {'asin', 'atan', 'sin', 'tan'}:
                # TODO: implement the following transformations in special_cases.py
                # asin(z) = -j * asinh(j * z)
                # atan(z) = -j * atanh(j * z)
                # sin(z) = -j * sinh(j * z)
                # tan(z) = -j * tanh(j * z)
                name2 = dict(asin='asinh', atan='atanh', sin='sinh', tan='tanh')[name]
                # j * (re, im) = (-im, re)
                nim = {'+x': '-x', '-x': '+x', '+inf': '-inf', '-inf': '+inf'}.get(im)
                if nim is None:
                    assert im in {'nan', '0'}, im
                    nim = im
                re, im = nim, re
                re, im = getattr(special_cases, name2)[re, im]
                # -j * (re, im) = (im, -re)
                nre = {'+x': '-x', '-x': '+x', '+inf': '-inf', '-inf': '+inf'}.get(re)
                if nre is None:
                    if re in {'nan', '0', '+-inf'}:
                        nre = re
                    else:
                        nre = f'-({re})'
                re, im = im, nre
                r = [eval({'+-inf': 'nan'}.get(r_, r_),
                          dict(inf=mpmath.inf, nan=mpmath.nan, pi=mpmath.pi,
                               sin=mpmath.sin, cos=mpmath.cos, im=x.real,
                            log=mpmath.log)) for r_ in [re, im]]
                result = mpmath.mpc(*r)
            elif name == 'cos':
                #  cos(z) = cosh(j * z)
                # j * (re, im) = (-im, re)
                nim = {'+x': '-x', '-x': '+x', '+inf': '-inf', '-inf': '+inf'}.get(im)
                if nim is None:
                    assert im in {'nan', '0'}, im
                    nim = im
                re, im = nim, re
                r = special_cases.cosh[re, im]
                r = [eval({'+-inf': 'nan'}.get(r_, r_), dict(pi=mpmath.pi, inf=mpmath.inf, nan=mpmath.nan,
                                                             sin=mpmath.sin, cos=mpmath.cos, im=x.real)) for r_ in r]
                return mpmath.mpc(*r)
            elif hasattr(special_cases, name):
                r = getattr(special_cases, name)[re, im]
                r = [eval({'+-inf': 'nan'}.get(r_, r_), dict(inf=mpmath.inf, nan=mpmath.nan, pi=mpmath.pi,
                                                             sin=mpmath.sin, cos=mpmath.cos, im=x.imag,
                                                             log=mpmath.log)) for r_ in r]
                result = mpmath.mpc(*r)

            if is_real and result is not None:
                result = result.real

            return result

        name = dict(arcsin='asin',
                    arccos='acos',
                    arctan='atan',
                    arcsinh='asinh',
                    arccosh='acosh',
                    arctanh='atanh',
                    ).get(self._name, self._name)

        if name == 'log2':
            mp_func = getattr(self.module, 'log')

            def ext_func(x):
                return mp_func(x, 2)
            
        elif name == 'square':
            mp_func = getattr(self.module, 'power')

            def ext_func(x):
                return mp_func(x, 2)

        elif name == 'abs':
            mp_hypot = getattr(self.module, 'hypot')

            def ext_func(x):
                return mp_hypot(x.real, x.imag)

        else:
            ext_func = getattr(self.module, name)

        def ext_func_with_special_cases(x):

            r = special_cases_func(name, x)
            if r is None:
                r = ext_func(x)

            if isinstance(r, (float, complex)):
                pass
            elif isinstance(x, complex):
                r = complex(r)
            elif isinstance(x, float):
                if isinstance(r, mpmath.mpc):
                    assert r.imag==0 or mpmath.isnan(r.imag), (name, x, r)
                    r = r.real
                assert isinstance(r, mpmath.mpf), (name, x, r)
                r = float(r)
            else:
                assert 0, (name, x, r)
            return r

        f = numpy.vectorize(ext_func_with_special_cases)

        return f(*args)
