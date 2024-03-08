import os
import numpy
import warnings
from multiprocessing import Pool, set_start_method

import complex_function_validation as cfv
try:
    import mpmath
except ImportError:
    mpmath = None

function_names = [
    'exp', 'expm1',
    'log', 'log10', 'log2', 'log1p',
    'sqrt', 'square',
    'sin', 'cos', 'tan',
    'arcsin', 'arccos', 'arctan',
    'sinh', 'cosh', 'tanh',
    'arcsinh', 'arccosh', 'arctanh',
    'sinc',
]

dtype_list = ['complex64', 'complex128']
device_list = ['cpu', 'cuda']
pool_size = 2

def worker(args):
    array_libraries, index, fname, size_re, size_im, size_re2, size_im2, try_run = args
    warnings.simplefilter("ignore")

    if mpmath is not None:
        ref = cfv.MPMathFunction(fname, 'complex128')
    else:
        ref = cfv.NumpyFunction(fname, 'complex128')

    functions = []

    for cls in [item[1] for item in array_libraries[1:] if item[-1] is not None]:
        for dtype in dtype_list:
            for device in device_list:
                functions.append(cls(fname, dtype, device))

    cols = [fname]
    targets = {}
    for f in functions:
        if not f.is_valid:
            cols.append('N/A')
            continue

        image = cfv.ReportImage()
        image.generate_report(ref, [f], size_re=size_re, size_im=size_im)
        image.insert_text(-1, 0, f'\nVersions:\n    {ref.get_module_version()}')
        image.insert_text(-1, 0, f'    {f.get_module_version()}\n ')
        image.insert_legend(-1, 10)
        image.insert_text(-1, 0, '')
        image.insert_samples(-1, 0, 'xXIN23456789ABCDEFM')

        fn = f'{fname}_{ref.library_name}_{ref._dtype}_{ref._device}_versus_{f.library_name}_{f._dtype}_{f._device}.txt'
        print(fn)
        targets[fn] = str(image)

        if try_run:
            continue

        # for better statistics:
        image = cfv.ReportImage()
        image.generate_report(ref, [f], size_re=size_re2, size_im=size_im2)
        print('ok')
        stats = image.get_stats()[0]

        matches_rating = 100 * stats['matches'] / stats['total']
        inaccuracies_rating = 100 * stats['inaccuracies'] / stats['total']
        mismatches_rating = 100 * stats['mismatches'] / stats['total']

        if matches_rating == 100 and stats['inaccuracies']==0 and stats['mismatches'] == 0:
            rating = 'PERFECT'
        elif matches_rating == 100:
            rating = 'OK'
        elif matches_rating > 90:
            rating = 'GOOD'
        elif mismatches_rating > 50:
            rating = 'BAD'
        else:
            rating = 'POOR'
        cols.append(f'{rating} [{matches_rating:.0f}/{inaccuracies_rating:.0f}/{mismatches_rating:.0f} %](data/{os.path.basename(fn)})')

    return ' | '.join([''] + cols + ['']), targets

def main_results(array_libraries, target_dir='cfv_results', try_run=False):
    for _, _, version in array_libraries:
        if version is not None and 'dev' in version:
            target_dir += '_dev'
            break
    os.makedirs(os.path.join(target_dir, 'data'), exist_ok=True)

    if try_run:
        size_re = size_im = 12
    else:
        size_re = size_im = 40
    size_re2 = size_im2 = 200
    
    column_labels = ['Function']
    for lname, cls in [item[:2] for item in array_libraries[1:] if item[-1] is not None]:
        for dtype in dtype_list:
            for device in device_list:
                column_labels.append(f'{lname} {device}: {dtype}' + (' FTZ' if cls.apply_ftz(device) else ''))

    rows = [' | '.join([''] + column_labels + [''])]
    rows += [' | '.join(['', ':----'] + [':----:'] * (len(column_labels)-1) + [''])]

    args = []
    for index, fname in enumerate(function_names):
        args.append(
            (array_libraries, index, fname,
             size_re, size_im, size_re2, size_im2, try_run)
        )
    with Pool(min(pool_size, len(function_names))) as p:
        for row, targets in p.map(worker, args):
            rows.append(row)
            for fn, content in targets.items():
                if try_run:
                    print(fn)
                    print(content)
                else:
                    fn = os.path.join(target_dir, 'data', fn)
                    fd = open(fn, 'w')
                    fd.write(content)
                    fd.close()
                    print(f'Created {fn}')

    table = '\n'.join(rows)

    versions = '\n'.join([f'- {item[-1]}' for item in array_libraries if item[-1] is not None])

    if mpmath is not None:
        ref = cfv.MPMathFunction('exp', 'complex128')
    else:
        ref = cfv.NumpyFunction('exp', 'complex128')

    content = f'''
# Results

This document is generated using [Complex Function Validation](https://github.com/pearu/complex_function_validation) tool.

Array library versions:
{versions}

Reference library and dtype: {ref.library_name}, {ref._dtype}

## Table of match/inaccurracy/mismatch rates

{table}
'''

    if not try_run:
        fn = os.path.join(target_dir, 'README.md')
        fd = open(fn, 'w')
        fd.write(content)
        fd.close()
        print(f'Created {fn}')

if __name__ == '__main__':
    #set_start_method('spawn')
    set_start_method('forkserver')

    libs = dict(
        mpmath=('MPMath', cfv.MPMathFunction, cfv.MPMathFunction.get_module_version()),
        numpy=('NumPy', cfv.NumpyFunction, cfv.NumpyFunction.get_module_version()),
        jax=('JAX', cfv.JaxNumpyFunction, cfv.JaxNumpyFunction.get_module_version()),
        torch=('PyTorch', cfv.TorchFunction, cfv.TorchFunction.get_module_version()),
        complex_math=('ComplexMath', cfv.ComplexMathFunction, cfv.ComplexMathFunction.get_module_version())
    )

    if mpmath is not None:
        reflib = 'mpmath'
    else:
        reflib = 'numpy'
    
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if 1:
            main_results([libs[reflib], libs['jax']], target_dir=f'{reflib}_jax_results')
        if 0 and cfv.TorchFunction.get_module_version() is not None:
            main_results([libs[reflib], libs['torch']], target_dir=f'{reflib}_torch_results')
        if 0 and cfv.MPMathFunction.get_module_version() is not None:
            main_results([libs[reflib], libs['numpy']], target_dir=f'{reflib}_numpy_results')
        if 0:
            main_results([libs[reflib], libs['complex_math']], target_dir=f'{reflib}_complex_math_results')
