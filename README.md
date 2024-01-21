# Validate complex functions in array libraries

This research project provides a tool for validating the accuracy of
complex functions provided by various array libraries such as NumPy,
Jax, PyTorch and others. This tool is helpful for improving the
complex functions support in these libraries.

## Methodology

Consider complex-valued functions that are defined on a complex plane,
say, `sqrt`, `archsin`, etc. Array libraries typically support such
functions for array inputs having dtypes `complex64` and `complex128`
as a minimum.

In the following we use NumPy functions with dtype `complex128` as
reference functions that are assumed to produce correct values to all
possible inputs defined in a `complex` plane (`complex` can be either
`complex64` or `complex128`). The `complex` plane is a grid of complex
numbers that density is defined by the numerical characteristics of
the corresponding floating-point numbers (`float32` or `float64`).

To test a particular implementation of a complex function defined on a
`complex64` plane, we generate a grid of complex numbers that real and
imaginary parts can have a number of finite values ranging from the
minimal to maximal possible values of the corresponding floating-point
numbers as well as infinities such as `-inf` and `inf`.  Next, we
convert such a `complex64` grid to a `complex128` grid on which the
reference functions are evaluated. The evaluation of reference
functions leads to an array of `complex128` values that is converted
to `complex64` domain so that the results of `complex64` functions can
be compared against the reference values.

## Visualization

The comparison results of functions and the corresponding reference
functions are visualized as an image of the complex plane where each
point is labeled according to the comparison analysis. While such a
visualization is very rough, it is helpful for detecting regions where
a particular function is inaccurate, incorrect, or failing to produce
sensible result.

As an example, consider the comparison of `numpy.sqrt` function on
`complex64` inputs against the same function on `complex128`
inputs. The corresponding output of the tool is:

```
   +infj  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                                                                                  
    maxj  ~=c===========================c=~                                                                                                  
   1e33j  ~c=c=========================c=c~                                                                                                  
   1e28j  ~c==c=======================c==c~                                                                                                  
   1e22j  ~c=c=========================c=c~     Legend:                                                                                      
   1e17j  ~ccc===ccccccccc=ccccccccc===ccc~             = : values are equal (diff == 0)                                                     
   1e11j  ~cc===========================cc~             c : values are close (diff < eps * norm)                                             
    1e6j  ~c===c=c=================c=c===c~         [1-F] : values are close (diff < eps * norm * 10 ** n, n < resolution)                   
      1j  ~c=======ccccccc=ccccccc=======c~             x : values magnitudes are close (diff is approx. eps * norm * 10 ** resolution)      
   1e-5j  ~c=====c==c===========c==c=====c~             X : values are different (diff >= eps * norm * 10 ** resolution or one is non-finite)
  1e-11j  ~c======c===============c======c~             ~ : values are non-finite and of the same kind (-inf, inf, or nan)                   
  1e-16j  ~c========cccccc=cccccc========c~             I : one value is finite but other inf                                                
  1e-22j  ~==c===cc=====cc=cc=====cc===c==~             N : one value is not nan but other is nan                                            
  1e-27j  ~=========c====c=c====c=========~             M : one value is nan but other is not nan                                            
  1e-32j  ~======c==c====c=c====c==c======~                                                                                                  
   tinyj  ~=============cc=cc=============~                                                                                                  
      0j  ~===============================~                                                                                                  
  -tinyj  ~=============cc=cc=============~                                                                                                  
 -1e-32j  ~======c==c====c=c====c==c======~                                                                                                  
 -1e-27j  ~=========c====c=c====c=========~                                                                                                  
 -1e-22j  ~==c===cc=====cc=cc=====cc===c==~                                                                                                  
 -1e-16j  ~c========cccccc=cccccc========c~                                                                                                  
 -1e-11j  ~c======c===============c======c~                                                                                                  
  -1e-5j  ~c=====c==c===========c==c=====c~                                                                                                  
     -1j  ~c=======ccccccc=ccccccc=======c~                                                                                                  
   -1e6j  ~c===c=c=================c=c===c~                                                                                                  
  -1e11j  ~cc===========================cc~                                                                                                  
  -1e17j  ~ccc===ccccccccc=ccccccccc===ccc~                                                                                                  
  -1e22j  ~c=c=========================c=c~                                                                                                  
  -1e28j  ~c==c=======================c==c~                                                                                                  
  -1e33j  ~c=c=========================c=c~                                                                                                  
    minj  ~=c===========================c=~                                                                                                  
   -infj  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                                                                                  
       -inf      -1       0       1       +inf
          numpy.sqrt on complex64 plane
          vs
          numpy.sqrt on complex128 plane
```
(`tiny=1.1754944e-38`, `min=-3.4028235e+38`, `max=3.4028235e+38` for `complex64` dtype).

In the points labeled with `=`, the results of `numpy.sqrt` on
`complex64` and `complex128` inputs are identical, for instance:
```
>>> from numpy import sqrt, array, inf
>>> sqrt(array(1e6-1j, dtype='complex64')), sqrt(array(1e6-1j, dtype='complex128')).astype('complex64')
((1000-0.0005j), (1000-0.0005j))
```
In the points labeled with `c`, the corresponding results are not exactly equal but are close:
```
>>> sqrt(array(1e-5-1j, dtype='complex64')), sqrt(array(1e-5-1j, dtype='complex128')).astype('complex64')
((0.70711035-0.7071032j), (0.70711035-0.70710325j))
```

In the points labeled with `~`, the corresponding results are not
finite but still equal:
```
>>> sqrt(array(complex(1, -inf), dtype='complex64')), sqrt(array(complex(1, -inf), dtype='complex128')).astype('complex64')
((inf-infj), (inf-infj))
```

The conclusion from the above comparison is that `numpy.sqrt`
behaviour on `complex64` inputs is almost ideal: there are no points
where the corresponding results will differ considerably.

A more interesting example is about validating `square` on complex inputs (see [example.py](example.py)):
```
   +infj  N~~~~~~~~~~~~~~~N~~~~~~~~~~~~~~~N     +infj  NNNNN~~~~~~~~~~~N~~~~~~~~~~~NNNNN     +infj  NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN   
    maxj  NX~~~~~~~~~~~~~~~~~~~~~~~~~~~~~XN      maxj  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN      maxj  NX~~~~~~~XXXXXXXXXXXXXXXXXXXXX~XN   
   1e33j  NXX~~~~~~~~~~~~~~~~~~~~~~~~~~~XXN     1e33j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN     1e33j  N~X~~~~~XXXXXXXXXXXXXXXXXXXXX~X~N   
   4e27j  NXXX~~~~~~~~~~~~~~~~~~~~~~~~~XXXN     4e27j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN     4e27j  NX~X~~~XXXXXXXXXXXXXXXXXXXXX~X~~N   
   1e22j  NXXXX~~~~~~~~~~~~~~~~~~~~~~~XXXXN     1e22j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN     1e22j  NXX~X~XXXXXXXXXXXXXXXXXXXXX~X~~~N   
   5e16j  ~~~~~c=====================c~~~~~     5e16j  ~~~~~=======================~~~~~     5e16j  NXXX~22222222222222222222222~~~~N   
   2e11j  ~~~~~=c===================c=~~~~~     2e11j  ~~~~~=======================~~~~~     2e11j  NXXXX22222222222222222222222X~~~N   
    6e5j  ~~~~~==c=================c==~~~~~      6e5j  ~~~~~=======================~~~~~      6e5j  NXXXX22222222222222222222222XX~~N   
      2j  ~~~~~===c===============c===~~~~~        2j  ~~~~~=======================~~~~~        2j  NXXXX222ccccccccccccccccc222XXX~N   
   7e-6j  ~~~~~====c=============c====~~~~~     7e-6j  ~~~~~=======================~~~~~     7e-6j  NXXXX2222222222222222222=222XXXXN   
  2e-11j  ~~~~~=====c===========c=====~~~~~    2e-11j  ~~~~~=======================~~~~~    2e-11j  NXXXX2221222222222222222c222XXXXN   
  8e-17j  ~~~~~======c=========c======~~~~~    8e-17j  ~~~~~=======================~~~~~    8e-17j  NXXXX2221222222222222222=222XXXXN   
  3e-22j  ~~~~~=======================~~~~~    3e-22j  ~~~~~=======================~~~~~    3e-22j  NXXXX2221222=========222=222XXXXN   
  1e-27j  ~~~~~=======================~~~~~    1e-27j  ~~~~~=======================~~~~~    1e-27j  NXXXX2221222=========222=222XXXXN   
  3e-33j  ~~~~~=======================~~~~~    3e-33j  ~~~~~=======================~~~~~    3e-33j  NXXXX2221222=========222=222XXXXN   
   tinyj  ~~~~~=======================~~~~~     tinyj  ~~~~~=======================~~~~~     tinyj  NXXXX2221222=========222c222XXXXN   
      0j  N~~~~=======================~~~~N        0j  N~~~~=======================~~~~N        0j  NXXXX2221222=========222=222~~~~N   
  -tinyj  ~~~~~=======================~~~~~    -tinyj  ~~~~~=======================~~~~~    -tinyj  NXXXX2221222=========222c222XXXXN   
 -3e-33j  ~~~~~=======================~~~~~   -3e-33j  ~~~~~=======================~~~~~   -3e-33j  NXXXX2221222=========222=222XXXXN   
 -1e-27j  ~~~~~=======================~~~~~   -1e-27j  ~~~~~=======================~~~~~   -1e-27j  NXXXX2221222=========222=222XXXXN   
 -3e-22j  ~~~~~=======================~~~~~   -3e-22j  ~~~~~=======================~~~~~   -3e-22j  NXXXX2221222=========222=222XXXXN   
 -8e-17j  ~~~~~======c=========c======~~~~~   -8e-17j  ~~~~~=======================~~~~~   -8e-17j  NXXXX2221222222222222222=222XXXXN   
 -2e-11j  ~~~~~=====c===========c=====~~~~~   -2e-11j  ~~~~~=======================~~~~~   -2e-11j  NXXXX2221222222222222222c222XXXXN   
  -7e-6j  ~~~~~====c=============c====~~~~~    -7e-6j  ~~~~~=======================~~~~~    -7e-6j  NXXXX2222222222222222222=222XXXXN   
     -2j  ~~~~~===c===============c===~~~~~       -2j  ~~~~~=======================~~~~~       -2j  NXXXX222ccccccccccccccccc222XXX~N   
   -6e5j  ~~~~~==c=================c==~~~~~     -6e5j  ~~~~~=======================~~~~~     -6e5j  NXXXX22222222222222222222222XX~~N   
  -2e11j  ~~~~~=c===================c=~~~~~    -2e11j  ~~~~~=======================~~~~~    -2e11j  NXXXX22222222222222222222222X~~~N   
  -5e16j  ~~~~~c=====================c~~~~~    -5e16j  ~~~~~=======================~~~~~    -5e16j  NXXX~22222222222222222222222~~~~N   
  -1e22j  NXXXX~~~~~~~~~~~~~~~~~~~~~~~XXXXN    -1e22j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN    -1e22j  NXX~X~XXXXXXXXXXXXXXXXXXXXX~X~~~N   
  -4e27j  NXXX~~~~~~~~~~~~~~~~~~~~~~~~~XXXN    -4e27j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN    -4e27j  NX~X~~~XXXXXXXXXXXXXXXXXXXXX~X~~N   
  -1e33j  NXX~~~~~~~~~~~~~~~~~~~~~~~~~~~XXN    -1e33j  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN    -1e33j  N~X~~~~~XXXXXXXXXXXXXXXXXXXXX~X~N   
    minj  NX~~~~~~~~~~~~~~~~~~~~~~~~~~~~~XN      minj  NNNNN~~~~~~~~~~~~~~~~~~~~~~~NNNNN      minj  NX~~~~~~~XXXXXXXXXXXXXXXXXXXXX~XN   
   -infj  N~~~~~~~~~~~~~~~N~~~~~~~~~~~~~~~N     -infj  NNNNN~~~~~~~~~~~N~~~~~~~~~~~NNNNN     -infj  NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN   
          ^     ^      ^  ^  ^      ^     ^            ^     ^      ^  ^  ^      ^     ^            ^     ^      ^  ^  ^      ^     ^   
       -inf -2e11 -1e-27  0  1e-27  2e11  +inf      -inf -2e11 -1e-27  0  1e-27  2e11  +inf      -inf -2e11 -1e-27  0  1e-27  2e11  +inf
                                                                                                                                        
  CPU                                          CUDA                                         CUDA                                        
  numpy.square on complex64 plane              jax.numpy.square on complex64 plane          torch.square on complex64 plane             
  vs                                           vs                                           vs                                          
  CPU                                          CPU                                          CPU                                         
  numpy.square on complex128 plane             numpy.square on complex128 plane             numpy.square on complex128 plane            
                                                                                                                                        
Statistics:                                  Statistics:                                  Statistics:                                   
    match rate: 94.1%                            match rate: 90.4%                            match rate: 19.7%                         
    mismatch rate: 5.9%                          mismatch rate: 9.6%                          inaccuracies rate: 36.6%                  
                                                                                              mismatch rate: 43.7%                      
```
that demonstrates that different array libraries use different algorithms for evaluating complex functions.

# Results

- [NumPy vs JAX](numpy_jax_results/)
- [NumPy vs PyTorch](numpy_torch_results/)
- [NumPy vs JAX vs PyTorch](numpy_jax_torch_results/)
