import complex_function_validation as cfv

function_name = 'square'
ref = cfv.NumpyFunction(function_name, 'complex128')
functions = [
    cfv.NumpyFunction(function_name, 'complex64'),
    cfv.JaxNumpyFunction(function_name, 'complex64', 'cuda'),
    cfv.TorchFunction(function_name, 'complex64', 'cuda'),
]

image = cfv.ReportImage()
image.generate_report(ref, functions, size_re=15)
print(image)
