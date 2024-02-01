
# Results

This document is generated using [Complex Function Validation](https://github.com/pearu/complex_function_validation) tool.

Array library versions:
- mpmath 1.3.0
- jax 0.4.24.dev20240130+66308c30a

Reference library and dtype: MPMath, complex128

## Table of match/inaccurracy/mismatch rates

 | Function | JAX cpu: complex64 FTZ | JAX cuda: complex64 | JAX cpu: complex128 FTZ | JAX cuda: complex128 | 
 | :---- | :----: | :----: | :----: | :----: | 
 | exp | GOOD [100/0/0 %](data/exp_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/exp_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | log | GOOD [100/0/0 %](data/log_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/log_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | log10 | GOOD [96/3/1 %](data/log10_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | POOR [90/9/1 %](data/log10_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | log2 | GOOD [99/0/1 %](data/log2_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [99/0/1 %](data/log2_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | log1p | POOR [56/0/44 %](data/log1p_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | POOR [57/0/43 %](data/log1p_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | sqrt | GOOD [99/1/0 %](data/sqrt_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [100/0/0 %](data/sqrt_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | square | GOOD [96/0/3 %](data/square_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [97/0/3 %](data/square_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | sin | POOR [83/7/10 %](data/sin_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | POOR [85/3/12 %](data/sin_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | cos | GOOD [99/1/0 %](data/cos_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [99/0/0 %](data/cos_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | tan | BAD [34/9/57 %](data/tan_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [35/4/61 %](data/tan_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arcsin | BAD [12/15/73 %](data/arcsin_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [22/5/73 %](data/arcsin_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arccos | BAD [39/2/59 %](data/arccos_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [40/1/60 %](data/arccos_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arctan | BAD [38/6/56 %](data/arctan_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [32/2/66 %](data/arctan_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | sinh | POOR [82/8/10 %](data/sinh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | POOR [85/3/11 %](data/sinh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | cosh | GOOD [98/2/0 %](data/cosh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [99/1/0 %](data/cosh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | tanh | GOOD [98/2/0 %](data/tanh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | GOOD [98/2/0 %](data/tanh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arcsinh | BAD [27/8/65 %](data/arcsinh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [38/2/60 %](data/arcsinh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arccosh | BAD [34/2/64 %](data/arccosh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [39/1/60 %](data/arccosh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | arctanh | POOR [47/5/48 %](data/arctanh_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [32/2/65 %](data/arctanh_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
 | sinc | BAD [20/8/72 %](data/sinc_MPMath_complex128_cpu_versus_JAX_complex64_cpu.txt) | N/A | BAD [24/4/73 %](data/sinc_MPMath_complex128_cpu_versus_JAX_complex128_cpu.txt) | N/A | 
