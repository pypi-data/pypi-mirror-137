wavestate.bunch
=================

Utility classes providing "Bunch" containers. These are dictionaries with
attribute access of the elements. They wrap any lower level dictionaries they
output, so the interface mimics the "struct" container from Matlab.

Bunch
------

The Bunch class is a lightweight wrapper for dictionaries to allow attribute
access as a means to access elements with less syntax. Bunch does not copy
assigned dictionaries, it wraps them. This is unlike some other implementations
such as gwinc.Struct.

```python
d = dict(A=1, B=2, d2=dict(C=1))

b1 = Bunch(d)
print(b1.A)
print(b1.d2.C)
```

or 

```python
b2 = dict(A=1, B=2, d2=dict(C=1))
print(b2.A)
print(b2.d2.C)
```

A useful pattern while developing and debugging code, particularly while refactoring large
blocks of code into functions is

```python
def code_block(arg1, arg2, arg3, ...):
    ...
    a = 1
    b = 2
    ...
    return Bunch(locals())
    
ret = code_block(...)
ret.a
```

which is a lightweight way to access elements from the code_block that is
promoted into a function.

DeepBunch
-----------
There are a collection of more advanced containers
DeepBunch allows speculative access of elements, such that if it is missing
an attribute, a temporary is created such that 

```python
A = DeepBunch()
A.B.C.D = 1
```

is acceptable.

and 

```
if A.B.C.E:
  raise Exception('The above test evaluates to False')
```

and in this case, no intermediate dictionaries are actually created until a value is assigned to a leaf.


HDFDeepBunch
---------------

h5py is not a required dependency of wavestate.bunch, but if it is installed
then one can import the `HDFDeepBunch`, which provides a similar interface to
the DeepBunch, but uses HDF5 files as a back-end, with internal handling of
numpy arrays.

