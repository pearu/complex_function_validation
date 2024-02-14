
# Results

This document is generated using [Complex Function Validation](https://github.com/pearu/complex_function_validation) tool.

Array library versions:
- mpmath 1.3.0
- numpy 1.26.3

Reference library and dtype: MPMath, complex128

## Table of match/inaccurracy/mismatch rates

 | Function | NumPy cpu: complex64 | NumPy cuda: complex64 | NumPy cpu: complex128 | NumPy cuda: complex128 | 
 | :---- | :----: | :----: | :----: | :----: | 
 | exp | GOOD [100/0/0 %](data/exp_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/exp_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | expm1 | GOOD [99/1/0 %](data/expm1_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [99/1/0 %](data/expm1_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | log | GOOD [100/0/0 %](data/log_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/log_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | log10 | GOOD [98/1/1 %](data/log10_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [99/0/1 %](data/log10_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | log2 | GOOD [100/0/0 %](data/log2_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [99/0/1 %](data/log2_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | log1p | POOR [82/9/9 %](data/log1p_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [85/3/11 %](data/log1p_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | sqrt | GOOD [100/0/0 %](data/sqrt_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/sqrt_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | square | GOOD [96/0/3 %](data/square_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [97/0/3 %](data/square_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | sin | GOOD [100/0/0 %](data/sin_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | PERFECT [100/0/0 %](data/sin_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | cos | GOOD [100/0/0 %](data/cos_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | PERFECT [100/0/0 %](data/cos_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | tan | GOOD [99/1/0 %](data/tan_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [99/1/0 %](data/tan_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arcsin | GOOD [94/3/2 %](data/arcsin_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [87/2/11 %](data/arcsin_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arccos | GOOD [100/0/0 %](data/arccos_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/arccos_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arctan | GOOD [94/3/3 %](data/arctan_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [77/2/21 %](data/arctan_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | sinh | GOOD [100/0/0 %](data/sinh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | PERFECT [100/0/0 %](data/sinh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | cosh | GOOD [100/0/0 %](data/cosh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | PERFECT [100/0/0 %](data/cosh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | tanh | GOOD [99/1/0 %](data/tanh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | GOOD [99/1/0 %](data/tanh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arcsinh | GOOD [94/3/2 %](data/arcsinh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [87/2/11 %](data/arcsinh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arccosh | GOOD [95/0/5 %](data/arccosh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [88/0/12 %](data/arccosh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | arctanh | GOOD [94/3/3 %](data/arctanh_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | POOR [77/2/21 %](data/arctanh_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
 | sinc | BAD [21/3/76 %](data/sinc_MPMath_complex128_cpu_versus_NumPy_complex64_cpu.txt) | N/A | BAD [24/2/74 %](data/sinc_MPMath_complex128_cpu_versus_NumPy_complex128_cpu.txt) | N/A | 
