import os
import numpy
import complex_function_validation as cfv

function_names = [
    'exp', 'log', 'log10',
    'sqrt', 'square',
    'sin', 'cos', 'tan',
    'arcsin', 'arccos', 'arctan',
    'sinh', 'cosh', 'tanh',
    'arcsinh', 'arccosh', 'arctanh',
]

def main_results(array_libraries, target_dir='cfv_results'):
    os.makedirs(os.path.join(target_dir, 'data'), exist_ok=True)

    size_re = size_im = 40
    size_re2 = size_im2 = 200
    
    column_labels = ['Function', 'NumPy: complex64']
    for lname in [item[0] for item in array_libraries[1:] if item[-1] is not None]:
        for dtype in ['complex64', 'complex128']:
            for device in ['cpu', 'cuda']:
                column_labels.append(f'{lname} {device}: {dtype}')

    rows = [' | '.join([''] + column_labels + [''])]
    rows += [' | '.join(['', ':----'] + [':----:'] * (len(column_labels)-1) + [''])]
    for index, fname in enumerate(function_names):

        ref = cfv.NumpyFunction(fname, 'complex128')
        functions = [cfv.NumpyFunction(fname, 'complex64')]

        for cls in [item[1] for item in array_libraries[1:] if item[-1] is not None]:
            for dtype in ['complex64', 'complex128']:
                for device in ['cpu', 'cuda']:
                    functions.append(cls(fname, dtype, device))
        cols = [fname]
        for f in functions:
            if not f.is_valid:
                cols.append('N/A')
                raise
                continue

            image = cfv.ReportImage()
            image.generate_report(ref, [f], size_re=size_re, size_im=size_im)
            image.insert_text(-1, 0, f'\nVersions:\n    {ref.get_module_version()}')
            image.insert_text(-1, 0, f'    {f.get_module_version()}\n ')
            image.insert_legend(-1, 10)

            fn = os.path.join(target_dir, 'data', f'{fname}_{ref.library_name}_{ref._dtype}_{ref._device}_versus_{f.library_name}_{f._dtype}_{f._device}.txt')
            fd = open(fn, 'w')
            fd.write(str(image))
            fd.close()
            print(f'Created {fn}')

            # for better statistics:
            image = cfv.ReportImage()
            image.generate_report(ref, [f], size_re=size_re2, size_im=size_im2)

            stats = image.get_stats()[0]

            matches_rating = 100 * stats['matches'] / stats['total']
            inaccuracies_rating = 100 * stats['inaccuracies'] / stats['total']
            mismatches_rating = 100 * stats['mismatches'] / stats['total']

            if matches_rating == 100:
                rating = 'PERFECT'
            elif matches_rating > 90:
                rating = 'GOOD'
            elif mismatches_rating > 50:
                rating = 'BAD'
            else:
                rating = 'POOR'
            cols.append(f'{rating}: [{matches_rating:.1f}/{inaccuracies_rating:.1f}/{mismatches_rating:.1f} %](data/{os.path.basename(fn)})')

        rows.append(' | '.join([''] + cols + ['']))

    table = '\n'.join(rows)

    versions = '\n'.join([f'- {item[-1]}' for item in array_libraries if item[-1] is not None])
    
    content = f'''
# Results

This document is generated using [Complex Function Validation](https://github.com/pearu/complex_function_validation) tool.

Array library versions:
{versions}

Reference library and dtype: {ref.library_name}, {ref._dtype}

## Table of match/inaccurracy/mismatch rates

{table}
'''

    fn = os.path.join(target_dir, 'README.md')
    fd = open(fn, 'w')
    fd.write(content)
    fd.close()
    print(f'Created {fn}')

if __name__ == '__main__':

    array_libraries = [
        ('NumPy', cfv.NumpyFunction, cfv.NumpyFunction.get_module_version()),
        ('JAX', cfv.JaxNumpyFunction, cfv.JaxNumpyFunction.get_module_version()),
        ('PyTorch', cfv.TorchFunction, cfv.TorchFunction.get_module_version()),
    ]

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # main_results(array_libraries, target_dir='numpy_jax_torch_results')
        main_results(array_libraries[:1], target_dir='numpy_jax_results')
        main_results(array_libraries[::2], target_dir='numpy_torch_results')
