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

def main_results(target_dir='numpy_jax_torch_results'):
    os.makedirs(target_dir, exist_ok=True)

    size_re = size_im = 40
    size_re2 = size_im2 = 200

    array_libraries = [
        ('NumPy', cfv.NumpyFunction, cfv.NumpyFunction.get_module_version()),
        ('JAX', cfv.JaxNumpyFunction, cfv.JaxNumpyFunction.get_module_version()),
        ('PyTorch', cfv.TorchFunction, cfv.TorchFunction.get_module_version()),
    ]
    
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

            fn = os.path.join(target_dir, f'{fname}_{ref.library_name}_{ref._dtype}_{ref._device}_versus_{f.library_name}_{f._dtype}_{f._device}.txt')
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
            cols.append(f'{rating}: [{matches_rating:.1f}/{inaccuracies_rating:.1f}/{mismatches_rating:.1f} %]({os.path.basename(fn)})')

        rows.append(' | '.join([''] + cols + ['']))

    table = '\n'.join(rows)

    versions = [f'- {item[-1]}' for item in array_libraries if item[-1] is not None]
    
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
            
def main_numpy_complex128_vs_numpy_complex64(fname):
    ref = cfv.NumpyFunction(fname, 'complex128')
    functions = cfv.NumpyFunction.get_valid_functions(fname, 'complex64')
    image = cfv.ReportImage()
    stats = image.generate_report(ref, functions)

def main():
    size_re, size_im = 40, 40
    versions = set()
    for fname in function_names:
        ref = cfv.NumpyFunction(fname, 'complex128')
        functions = []
        functions.extend(cfv.NumpyFunction.get_valid_functions(fname, 'complex64'))
        functions.extend(cfv.JaxNumpyFunction.get_valid_functions(fname, 'complex64'))
        functions.extend(cfv.TorchFunction.get_valid_functions(fname, 'complex64'))

        image = cfv.ReportImage()
        image.generate_report(ref, functions, size_re=size_re, size_im=size_im)
        versions.update(f.get_module_version() for f in functions)

        image.insert_hline(0, '-')
        image.insert_hline(-1, '-')
        print(image)
        print()


    # Show legend and versions
    image = cfv.ReportImage()
    image.insert_legend(0, 10)
    image.insert_text(-1, 0, 'Versions:')
    for version in sorted(versions):
        image.insert_text(-1, 5, version)    
    print(image)    


if __name__ == '__main__':
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main_results()
