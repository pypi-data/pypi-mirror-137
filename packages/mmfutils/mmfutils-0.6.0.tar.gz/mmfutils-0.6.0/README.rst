MMF Utils
=========

Small set of utilities: containers and interfaces.

This package provides some utilities that I tend to rely on during
development. Presently it includes some convenience containers, plotting
tools, and a patch for including
`zope.interface <http://docs.zope.org/zope.interface/>`__ documentation
in a notebook.

(Note: If this file does not render properly, try viewing it through
`nbviewer.org <http://nbviewer.ipython.org/urls/bitbucket.org/mforbes/mmfutils-fork/raw/tip/doc/README.ipynb>`__)

**Documentation:** http://mmfutils.readthedocs.org

**Source:**

-  https://alum.mit.edu/www/mforbes/hg/forbes-group/mmfutils: Permalink
   (will forward).
-  https://hg.iscimath.org/forbes-group/mmfutils: Current, in case the
   permalink fails.
-  https://github.com/forbes-group/mmfutils: Public read-only mirror.

**Issues:**
https://alum.mit.edu/www/mforbes/hg/forbes-group/mmfutils/issues

**Build Status**

|Documentation Status| |Build Status|

.. |Documentation Status| image:: https://readthedocs.org/projects/mmfutils/badge/?version=latest
   :target: https://mmfutils.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://cloud.drone.io/api/badges/forbes-group/mmfutils/status.svg
   :target: https://cloud.drone.io/forbes-group/mmfutils

Installing
----------

This package can be installed from
`PyPI <https://pypi.org/project/mmfutils/>`__:

.. code:: bash

   python3 -m pip install mmfutils

or, if you need to install from source, you can get it from one of the
repositories:

.. code:: bash

   python3 -m pip install hg+https://alum.mit.edu/www/mforbes/hg/forbes-group/mmfutils
   python3 -m pip install git+https://github.com/forbes-group/mmfutils

Usage
=====

Containers
----------

ObjectBase and Object
~~~~~~~~~~~~~~~~~~~~~

The ``ObjectBase`` and ``Object`` classes provide some useful features
described below. Consider a problem where a class is defined through a
few parameters, but requires extensive initialization before it can be
properly used. An example is a numerical simulation where one passes the
number of grid points :math:`N` and a length :math:`L`, but the
initialization must generate large grids for efficient use later on.
These grids should be generated before computations begin, but should
not be re-generated every time needed. They also should not be pickled
when saved to disk.

**Deferred initialization via the ``init()`` method:** The idea here
changes the semantics of ``__init__()`` slightly by deferring any
expensive initialization to ``init()``. Under this scheme,
``__init__()`` should only set and check what we call picklable
attributes: these are parameters that define the object (they will be
pickled in ``Object`` below) and will be stored in a list
``self.picklable_attributes`` which is computed at the end of
``ObjectBase.__init__()`` as the list of all keys in ``__dict__``. Then,
``ObjectBase.__init__()`` will call ``init()`` where all remaining
attributes should be calculated.

This allows users to change various attributes, then reinitialize the
object once with an explicit call to ``init()`` before performing
expensive computations. This is an alternative to providing complete
properties (getters and setters) for objects that need to trigger
computation. The use of setters is safer, but requires more work on the
side of the developer and can lead to complex code when different
properties depend on each other. The approach here puts all computations
in a single place. Of course, the user must remember to call ``init()``
before working with the object.

To facilitate this, we provide a mild check in the form of an
``initialized`` flag that is set to ``True`` at the end of the base
``init()`` chain, and set to ``False`` if any variables are in
``pickleable_attributes`` are set.

**Serialization and Deferred Initialization:** The base class
``ObjectBase`` does not provide any pickling services but does provide a
nice representation. Additional functionality is provided by ``Object``
which uses the features of ``ObjectBase`` to define ``__getstate__()``
and ``__setstate__()`` methods for pickling which pickle only the
``picklable_attributes``. Note: unpickling an object will **not** call
``__init__()`` but will call ``init()`` giving objects a chance to
restore the computed attributes from pickles.

-  **Note:** *Before using, consider if these features are really needed
   – with all such added functionality comes additional potential
   failure modes from side-interactions. The ``ObjectBase`` class is
   quite simple, and therefore quite safe, while ``Object`` adds
   additional functionality with potential side-effects. For example, a
   side-effect of support for pickles is that ``copy.copy()`` will also
   invoke ``init()`` when copying might instead be much faster. Thus, we
   recommend only using ``ObjectBase`` for efficient code.*

Object Example
^^^^^^^^^^^^^^

.. code:: ipython3

    ROOTDIR = !hg root
    ROOTDIR = ROOTDIR[0]
    import sys;sys.path.insert(0, ROOTDIR)
    
    import numpy as np
    
    from mmfutils.containers import ObjectBase, ObjectMixin
    
    class State(ObjectBase):  
        _quiet = False
        def __init__(self, N, L=1.0, **kw):
            """Set all of the picklable parameters, in this case, N and L."""
            self.N = N
            self.L = L
            
            # Now register these and call init()
            super().__init__(**kw)
            if not self._quiet:
                print("__init__() called")
            
        def init(self):
            """All additional initializations"""
            if not self._quiet:
                print("init() called")
            dx = self.L / self.N
            self.x = np.arange(self.N, dtype=float) * dx - self.L/2.0
            self.k = 2*np.pi * np.fft.fftfreq(self.N, dx)
    
            # Set highest momentum to zero if N is even to
            # avoid rapid oscillations
            if self.N % 2 == 0:
                self.k[self.N//2] = 0.0
    
            # Calls base class which sets self.initialized
            super().init()
                
        def compute_derivative(self, f):
            """Return the derivative of f."""        
            return np.fft.ifft(self.k*1j*np.fft.fft(f)).real
    
    s = State(256)
    print(s)  # No default value for L


.. parsed-literal::

    init() called
    __init__() called
    State(L=1.0, N=256)


.. code:: ipython3

    s.L = 2.0
    print(s)


.. parsed-literal::

    State(L=2.0, N=256)


One feature is that a nice ``repr()`` of the object is produced. Now
let’s do a calculation:

.. code:: ipython3

    f = np.exp(3*np.cos(2*np.pi*s.x/s.L)) / 15
    df = -2.*np.pi/5.*np.exp(3*np.cos(2*np.pi*s.x/s.L))*np.sin(2*np.pi*s.x/s.L)/s.L
    np.allclose(s.compute_derivative(f), df)




.. parsed-literal::

    False



Oops! We forgot to reinitialize the object… (The formula is correct, but
the lattice is no longer commensurate so the FFT derivative has huge
errors).

.. code:: ipython3

    print(s.initialized)
    s.init()
    assert s.initialized
    f = np.exp(3*np.cos(2*np.pi*s.x/s.L)) / 15
    df = -2.*np.pi/5.*np.exp(3*np.cos(2*np.pi*s.x/s.L))*np.sin(2*np.pi*s.x/s.L)/s.L
    np.allclose(s.compute_derivative(f), df)


.. parsed-literal::

    False
    init() called




.. parsed-literal::

    True



Here we demonstrate pickling. Note that using ``Object`` makes the
pickles very small, and when unpickled, ``init()`` is called to
re-establish ``s.x`` and ``s.k``. Generally one would inherit from
``Object``, but since we already have a class, we can provide pickling
functionality with ``ObjectMixin``:

.. code:: ipython3

    class State1(ObjectMixin, State):
        pass
    
    s = State(N=256, _quiet=True)
    s1 = State1(N=256, _quiet=True)

.. code:: ipython3

    import pickle, copy
    s_repr = pickle.dumps(s)
    s1_repr = pickle.dumps(s1)
    print(f"ObjectBase pickle:  {len(s_repr)} bytes")
    print(f"ObjectMixin pickle: {len(s1_repr)} bytes")


.. parsed-literal::

    ObjectBase pickle:  4396 bytes
    ObjectMixin pickle: 103 bytes


Note, however, that the speed of copying is significantly impacted:

.. code:: ipython3

    %timeit copy.copy(s)
    %timeit copy.copy(s1)


.. parsed-literal::

    2.58 µs ± 34.3 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
    27.1 µs ± 404 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)


Another use case applies when ``init()`` is expensive. If :math:`x` and
:math:`k` were computed in ``__init__()``, then using properties to
change both :math:`N` and :math:`L` would trigger two updates. Here we
do the updates, then call ``init()``. Good practice is to call
``init()`` automatically before any serious calculation to ensure that
the object is brought up to date before the computation.

.. code:: ipython3

    s.N = 64
    s.L = 2.0
    s.init()

Finally, we demonstrate that ``Object`` instances can be archived using
the ``persist`` package:

.. code:: ipython3

    import persist.archive
    a = persist.archive.Archive(check_on_insert=True)
    a.insert(s=s)
    
    d = {}
    exec(str(a), d)
    
    d['s']




.. parsed-literal::

    State(L=2.0, N=64, _quiet=True)



Container
~~~~~~~~~

The ``Container`` object is a slight extension of ``Object`` that
provides a simple container for storing data with attribute and
iterative access. These implement some of the `Collections Abstract Base
Classes from the python standard
library <https://docs.python.org/2/library/collections.html#collections-abstract-base-classes>`__.
The following containers are provided:

-  ``Container``: Bare-bones container extending the ``Sized``,
   ``Iterable``, and ``Container`` abstract ase classes (ABCs) from the
   standard ``containers`` library.
-  ``ContainerList``: Extension that acts like a tuple/list satisfying
   the ``Sequence`` ABC from the ``containers`` library (but not the
   ``MutableSequence`` ABC. Although we allow setting and deleting
   items, we do not provide a way for insertion, which breaks this
   interface.)
-  ``ContainerDict``: Extension that acts like a dict satisfying the
   ``MutableMapping`` ABC from the ``containers`` library.

These were designed with the following use cases in mind:

-  Returning data from a function associating names with each data. The
   resulting ``ContainerList`` will act like a tuple, but will support
   attribute access. Note that the order will be lexicographic. One
   could use a dictionary, but attribute access with tab completion is
   much nicer in an interactive session. The ``containers.nametuple``
   generator could also be used, but this is somewhat more complicated
   (though might be faster). Also, named tuples are immutable - here we
   provide a mutable object that is picklable etc. The choice between
   ``ContainerList`` and ``ContainerDict`` will depend on subsequent
   usage. Containers can be converted from one type to another.

Container Examples
^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from mmfutils.containers import Container
    
    c = Container(a=1, c=2, b='Hi there')
    print(c)
    print(tuple(c))


.. parsed-literal::

    Container(a=1, b='Hi there', c=2)
    (1, 'Hi there', 2)


.. code:: ipython3

    # Attributes are mutable
    c.b = 'Ho there'
    print(c)


.. parsed-literal::

    Container(a=1, b='Ho there', c=2)


.. code:: ipython3

    # Other attributes can be used for temporary storage but will not be pickled.
    import numpy as np
    
    c.large_temporary_array = np.ones((256,256))
    print(c)
    print(c.large_temporary_array)


.. parsed-literal::

    Container(a=1, b='Ho there', c=2)
    [[1. 1. 1. ... 1. 1. 1.]
     [1. 1. 1. ... 1. 1. 1.]
     [1. 1. 1. ... 1. 1. 1.]
     ...
     [1. 1. 1. ... 1. 1. 1.]
     [1. 1. 1. ... 1. 1. 1.]
     [1. 1. 1. ... 1. 1. 1.]]


.. code:: ipython3

    import pickle
    c1 = pickle.loads(pickle.dumps(c))
    print(c1)
    c1.large_temporary_array


.. parsed-literal::

    Container(a=1, b='Ho there', c=2)


::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-13-bd53d5116502> in <module>
          2 c1 = pickle.loads(pickle.dumps(c))
          3 print(c1)
    ----> 4 c1.large_temporary_array
    

    AttributeError: 'Container' object has no attribute 'large_temporary_array'


Contexts
--------

The ``mmfutils.contexts`` module provides two useful contexts:

``NoInterrupt``: This can be used to susspend ``KeyboardInterrupt``
exceptions until they can be dealt with at a point that is convenient. A
typical use is when performing a series of calculations in a loop. By
placing the loop in a ``NoInterrupt`` context, one can avoid an
interrupt from ruining a calculation:

.. code:: ipython3

    from mmfutils.contexts import NoInterrupt
    
    complete = False
    n = 0
    with NoInterrupt() as interrupted:
        while not complete and not interrupted:
            n += 1
            if n > 10:
                complete = True

Note: One can nest ``NoInterrupt`` contexts so that outer loops are also
interrupted. Another use-case is mapping. See
`doc/Animation.ipynb <Animation.ipynb>`__ for more examples.

.. code:: ipython3

    res = NoInterrupt().map(abs, range(-100, 100))
    np.sign(res)




.. parsed-literal::

    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1])



Interfaces
----------

The interfaces module collects some useful
`zope.interface <http://docs.zope.org/zope.interface/>`__ tools for
checking interface requirements. Interfaces provide a convenient way of
communicating to a programmer what needs to be done to used your code.
This can then be checked in tests.

.. code:: ipython3

    from mmfutils.interface import Interface, Attribute, verifyClass, verifyObject, implementer
    
    class IAdder(Interface):
        """Interface for objects that support addition."""
    
        value = Attribute('value', "Current value of object")
    
        # No self here since this is the "user" interface
        def add(other):
            """Return self + other."""

Here is a broken implementation. We muck up the arguments to ``add``:

.. code:: ipython3

    @implementer(IAdder)
    class AdderBroken(object):
        def add(self, one, another):
            # There should only be one argument!
            return one + another
    
    try:
        verifyClass(IAdder, AdderBroken)
    except Exception as e:
        print("{0.__class__.__name__}: {0}".format(e))
        


.. parsed-literal::

    BrokenMethodImplementation: The object <class '__main__.AdderBroken'> has failed to implement interface __main__.IAdder: The contract of __main__.IAdder.add(other) is violated because 'AdderBroken.add(self, one, another)' requires too many arguments.


Now we get ``add`` right, but forget to define ``value``. This is only
caught when we have an object since the attribute is supposed to be
defined in ``__init__()``:

.. code:: ipython3

    @implementer(IAdder)
    class AdderBroken(object):
        def add(self, other):
            return one + other
    
    # The class validates...
    verifyClass(IAdder, AdderBroken)
    
    # ... but objects are missing the value Attribute
    try:
        verifyObject(IAdder, AdderBroken())
    except Exception as e:
        print("{0.__class__.__name__}: {0}".format(e))    


.. parsed-literal::

    BrokenImplementation: The object <__main__.AdderBroken object at 0x11693cac0> has failed to implement interface __main__.IAdder: The __main__.IAdder.value attribute was not provided.


Finally, a working instance:

.. code:: ipython3

    @implementer(IAdder)
    class Adder(object):
        def __init__(self, value=0):
            self.value = value
        def add(self, other):
            return one + other
        
    verifyClass(IAdder, Adder) and verifyObject(IAdder, Adder())




.. parsed-literal::

    True



Interface Documentation
~~~~~~~~~~~~~~~~~~~~~~~

We also monkeypatch ``zope.interface.documentation.asStructuredText()``
to provide a mechanism for documentating interfaces in a notebook.

.. code:: ipython3

    from mmfutils.interface import describe_interface
    describe_interface(IAdder)




.. raw:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="generator" content="Docutils 0.16: http://docutils.sourceforge.net/" />
    <title>&lt;string&gt;</title>
    
    <div class="document">
    
    
    <p><tt class="docutils literal">IAdder</tt></p>
    <blockquote>
    <p>Interface for objects that support addition.</p>
    <p>Attributes:</p>
    <blockquote>
    <tt class="docutils literal">value</tt> -- Current value of object</blockquote>
    <p>Methods:</p>
    <blockquote>
    <tt class="docutils literal">add(other)</tt> -- Return self + other.</blockquote>
    </blockquote>
    </div>




Parallel
--------

The ``mmfutils.parallel`` module provides some tools for launching and
connecting to IPython clusters. The ``parallel.Cluster`` class
represents and controls a cluster. The cluster is specified by the
profile name, and can be started or stopped from this class:

.. code:: ipython3

    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    import numpy as np
    from mmfutils import parallel
    cluster = parallel.Cluster(profile='default', n=3, sleep_time=1.0)
    cluster.start()
    cluster.wait()  # Instance of IPython.parallel.Client
    view = cluster.load_balanced_view
    x = np.linspace(-6, 6, 100)
    y = view.map(lambda x:x**2, x)
    print(np.allclose(y, x**2))
    cluster.stop()


.. parsed-literal::

    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json


.. parsed-literal::

    INFO:root:Starting cluster: ipcluster start --daemonize --quiet --profile=default --n=3


.. parsed-literal::

    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json


.. parsed-literal::

    INFO:root:waiting for 3 engines
    INFO:root:0 of 3 running
    INFO:root:3 of 3 running
    INFO:root:Stopping cluster: ipcluster stop --profile=default


.. parsed-literal::

    True
    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json


If you only need a cluster for a single task, it can be managed with a
context. Be sure to wait for the result to be computed before exiting
the context and shutting down the cluster!

.. code:: ipython3

    with parallel.Cluster(profile='default', n=3, sleep_time=1.0) as client:
        view = client.load_balanced_view
        x = np.linspace(-6, 6, 100)
        y = view.map(lambda x:x**2, x, block=True)  # Make sure to wait for the result!
    print(np.allclose(y, x**2))


.. parsed-literal::

    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json


.. parsed-literal::

    INFO:root:Starting cluster: ipcluster start --daemonize --quiet --profile=default --n=3


.. parsed-literal::

    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json


.. parsed-literal::

    INFO:root:waiting for 3 engines
    INFO:root:0 of 3 running
    INFO:root:3 of 3 running
    INFO:root:Stopping cluster: ipcluster stop --profile=default


.. parsed-literal::

    Waiting for connection file: ~/.ipython/profile_default/security/ipcontroller-client.json
    True


If you just need to connect to a running cluster, you can use
``parallel.get_client()``.

Performance
-----------

The ``mmfutils.performance`` module provides some tools for high
performance computing. Note: this module requires some additional
packages including
`numexp <https://github.com/pydata/numexpr/wiki/Numexpr-Users-Guide>`__,
`pyfftw <http://hgomersall.github.io/pyFFTW/>`__, and the ``mkl``
package installed by anaconda. Some of these require building system
libraries (i.e. the `FFTW <http://www.fftw.org>`__). However, the
various components will not be imported by default.

Here is a brief description of the components:

-  ``mmfutils.performance.blas``: Provides an interface to a few of the
   scipy BLAS wrappers. Very incomplete (only things I currently need).
-  ``mmfutils.performance.fft``: Provides an interface to the
   `FFTW <http://www.fftw.org>`__ using ``pyfftw`` if it is available.
   Also enables the planning cache and setting threads so you can better
   control your performance.
-  ``mmfutils.performance.numexpr``: Robustly imports numexpr and
   disabling the VML. (If you don’t do this carefully, it will crash
   your program so fast you won’t even get a traceback.)
-  ``mmfutils.performance.threads``: Provides some hooks for setting the
   maximum number of threads in a bunch of places including the MKL,
   numexpr, and fftw.

Plotting
--------

Several tools are provided in ``mmfutils.plot``:

Fast Filled Contour Plots
~~~~~~~~~~~~~~~~~~~~~~~~~

``mmfutils.plot.imcontourf`` is similar to matplotlib’s ``plt.contourf``
function, but uses ``plt.imshow`` which is much faster. This is useful
for animations and interactive work. It also supports my idea of saner
array-shape processing (i.e. if ``x`` and ``y`` have different shapes,
then it will match these to the shape of ``z``). Matplotlib now provies
``plt.pcolourmesh`` which is similar, but has the same interface issues.

.. code:: ipython3

    %matplotlib inline
    from matplotlib import pyplot as plt
    import time
    import numpy as np
    from mmfutils import plot as mmfplt
    x = np.linspace(-1, 1, 100)[:, None]**3
    y = np.linspace(-0.1, 0.1, 200)[None, :]**3
    z = np.sin(10*x)*y**2
    plt.figure(figsize=(12,3))
    plt.subplot(141)
    %time mmfplt.imcontourf(x, y, z, cmap='gist_heat')
    plt.subplot(142)
    %time plt.contourf(x.ravel(), y.ravel(), z.T, 50, cmap='gist_heat')
    plt.subplot(143)
    %time plt.pcolor(x.ravel(), y.ravel(), z.T, cmap='gist_heat', shading='auto')
    plt.subplot(144)
    %time plt.pcolormesh(x.ravel(), y.ravel(), z.T, cmap='gist_heat', shading='auto')


.. parsed-literal::

    CPU times: user 9.48 ms, sys: 3.72 ms, total: 13.2 ms
    Wall time: 16.5 ms
    CPU times: user 38.2 ms, sys: 2.97 ms, total: 41.2 ms
    Wall time: 45 ms
    CPU times: user 126 ms, sys: 5.86 ms, total: 132 ms
    Wall time: 133 ms
    CPU times: user 4.43 ms, sys: 209 µs, total: 4.64 ms
    Wall time: 4.65 ms




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x124ec2130>




.. image:: README_files/README_60_2.png


Angular Variables
-----------------

A couple of tools are provided to visualize angular fields, such as the
phase of a complex wavefunction.

.. code:: ipython3

    %matplotlib inline
    from matplotlib import pyplot as plt
    import time
    import numpy as np
    from mmfutils import plot as mmfplt
    x = np.linspace(-1, 1, 100)[:, None]
    y = np.linspace(-1, 1, 200)[None, :]
    z = x + 1j*y
    
    plt.figure(figsize=(9,2))
    ax = plt.subplot(131)
    mmfplt.phase_contour(x, y, z, colors='k', linewidths=0.5)
    ax.set_aspect(1)
    
    # This is a little slow but allows you to vary the luminosity.
    ax = plt.subplot(132)
    mmfplt.imcontourf(x, y, mmfplt.colors.color_complex(z))
    mmfplt.phase_contour(x, y, z, linewidths=0.5)
    ax.set_aspect(1)
    
    # This is faster if you just want to show the phase and allows
    # for a colorbar via a registered colormap
    ax = plt.subplot(133)
    mmfplt.imcontourf(x, y, np.angle(z), cmap='huslp')
    ax.set_aspect(1)
    plt.colorbar()
    mmfplt.phase_contour(x, y, z, linewidths=0.5);



.. image:: README_files/README_63_0.png


Debugging
---------

A couple of debugging tools are provided. The most useful is the
``debug`` decorator which will store the local variables of a function
in a dictionary or in your global scope.

.. code:: ipython3

    from mmfutils.debugging import debug
    
    @debug(locals())
    def f(x):
        y = x**1.5
        z = 2/x
        return z
    
    print(f(2.0), x, y, z)


.. parsed-literal::

    1.0 2.0 2.8284271247461903 1.0


Mathematics
-----------

We include a few mathematical tools here too. In particular, numerical
integration and differentiation. Check the API documentation for
details.

Developer Instructions
======================

Complete code coverage information is provided in
``build/_coverage/index.html``.

.. code:: ipython3

    from IPython.display import HTML
    with open(os.path.join(ROOTDIR, 'build/_coverage/index.html')) as f:
        coverage = f.read()
    HTML(coverage)




.. raw:: html

    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Coverage report</title>
        <link rel="icon" sizes="32x32" href="favicon_32.png">
        <link rel="stylesheet" href="style.css" type="text/css">
        <script type="text/javascript" src="jquery.min.js"></script>
        <script type="text/javascript" src="jquery.ba-throttle-debounce.min.js"></script>
        <script type="text/javascript" src="jquery.tablesorter.min.js"></script>
        <script type="text/javascript" src="jquery.hotkeys.js"></script>
        <script type="text/javascript" src="coverage_html.js"></script>
        <script type="text/javascript">
            jQuery(document).ready(coverage.index_ready);
        </script>
    </head>
    <body class="indexfile">
    <div id="header">
        <div class="content">
            <h1>Coverage report:
                <span class="pc_cov">90%</span>
            </h1>
            <img id="keyboard_icon" src="keybd_closed.png" alt="Show keyboard shortcuts" />
            <form id="filter_container">
                <input id="filter" type="text" value="" placeholder="filter..." />
            </form>
        </div>
    </div>
    <div class="help_panel">
        <img id="panel_icon" src="keybd_open.png" alt="Hide keyboard shortcuts" />
        <p class="legend">Hot-keys on this page</p>
        <div>
        <p class="keyhelp">
            <span class="key">n</span>
            <span class="key">s</span>
            <span class="key">m</span>
            <span class="key">x</span>
            <span class="key">c</span> &nbsp; change column sorting
        </p>
        </div>
    </div>
    <div id="index">
        <table class="index">
            <thead>
                <tr class="tablehead" title="Click to sort">
                    <th class="name left headerSortDown shortkey_n">Module</th>
                    <th class="shortkey_s">statements</th>
                    <th class="shortkey_m">missing</th>
                    <th class="shortkey_x">excluded</th>
                    <th class="right shortkey_c">coverage</th>
                </tr>
            </thead>
            <tfoot>
                <tr class="total">
                    <td class="name left">Total</td>
                    <td>2209</td>
                    <td>213</td>
                    <td>85</td>
                    <td class="right" data-ratio="1996 2209">90%</td>
                </tr>
            </tfoot>
            <tbody>
                <tr class="file">
                    <td class="name left"><a href="mmfutils___init___py.html">mmfutils/__init__.py</a></td>
                    <td>13</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="13 13">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_containers_py.html">mmfutils/containers.py</a></td>
                    <td>113</td>
                    <td>2</td>
                    <td>0</td>
                    <td class="right" data-ratio="111 113">98%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_contexts_py.html">mmfutils/contexts.py</a></td>
                    <td>199</td>
                    <td>25</td>
                    <td>0</td>
                    <td class="right" data-ratio="174 199">87%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_debugging_py.html">mmfutils/debugging.py</a></td>
                    <td>49</td>
                    <td>0</td>
                    <td>3</td>
                    <td class="right" data-ratio="49 49">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_interface_py.html">mmfutils/interface.py</a></td>
                    <td>77</td>
                    <td>0</td>
                    <td>15</td>
                    <td class="right" data-ratio="77 77">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math___init___py.html">mmfutils/math/__init__.py</a></td>
                    <td>0</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="0 0">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_bases___init___py.html">mmfutils/math/bases/__init__.py</a></td>
                    <td>2</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="2 2">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_bases_bases_py.html">mmfutils/math/bases/bases.py</a></td>
                    <td>431</td>
                    <td>52</td>
                    <td>0</td>
                    <td class="right" data-ratio="379 431">88%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_bases_interfaces_py.html">mmfutils/math/bases/interfaces.py</a></td>
                    <td>37</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="37 37">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_bases_utils_py.html">mmfutils/math/bases/utils.py</a></td>
                    <td>41</td>
                    <td>11</td>
                    <td>0</td>
                    <td class="right" data-ratio="30 41">73%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_bessel_py.html">mmfutils/math/bessel.py</a></td>
                    <td>132</td>
                    <td>0</td>
                    <td>14</td>
                    <td class="right" data-ratio="132 132">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_differentiate_py.html">mmfutils/math/differentiate.py</a></td>
                    <td>61</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="61 61">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_integrate___init___py.html">mmfutils/math/integrate/__init__.py</a></td>
                    <td>212</td>
                    <td>12</td>
                    <td>16</td>
                    <td class="right" data-ratio="200 212">94%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_linalg_py.html">mmfutils/math/linalg.py</a></td>
                    <td>12</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="12 12">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_special_py.html">mmfutils/math/special.py</a></td>
                    <td>26</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="26 26">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_math_wigner_py.html">mmfutils/math/wigner.py</a></td>
                    <td>20</td>
                    <td>17</td>
                    <td>0</td>
                    <td class="right" data-ratio="3 20">15%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_optimize_py.html">mmfutils/optimize.py</a></td>
                    <td>26</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="26 26">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_parallel_py.html">mmfutils/parallel.py</a></td>
                    <td>128</td>
                    <td>5</td>
                    <td>8</td>
                    <td class="right" data-ratio="123 128">96%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_performance___init___py.html">mmfutils/performance/__init__.py</a></td>
                    <td>0</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="0 0">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_performance_blas_py.html">mmfutils/performance/blas.py</a></td>
                    <td>58</td>
                    <td>0</td>
                    <td>6</td>
                    <td class="right" data-ratio="58 58">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_performance_fft_py.html">mmfutils/performance/fft.py</a></td>
                    <td>92</td>
                    <td>3</td>
                    <td>6</td>
                    <td class="right" data-ratio="89 92">97%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_performance_numexpr_py.html">mmfutils/performance/numexpr.py</a></td>
                    <td>9</td>
                    <td>0</td>
                    <td>7</td>
                    <td class="right" data-ratio="9 9">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_performance_threads_py.html">mmfutils/performance/threads.py</a></td>
                    <td>9</td>
                    <td>0</td>
                    <td>8</td>
                    <td class="right" data-ratio="9 9">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_plot___init___py.html">mmfutils/plot/__init__.py</a></td>
                    <td>4</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="4 4">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_plot_animation_py.html">mmfutils/plot/animation.py</a></td>
                    <td>82</td>
                    <td>19</td>
                    <td>0</td>
                    <td class="right" data-ratio="63 82">77%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_plot_cmaps_py.html">mmfutils/plot/cmaps.py</a></td>
                    <td>10</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="10 10">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_plot_rasterize_py.html">mmfutils/plot/rasterize.py</a></td>
                    <td>29</td>
                    <td>1</td>
                    <td>0</td>
                    <td class="right" data-ratio="28 29">97%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_solve___init___py.html">mmfutils/solve/__init__.py</a></td>
                    <td>0</td>
                    <td>0</td>
                    <td>0</td>
                    <td class="right" data-ratio="0 0">100%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_solve_broyden_py.html">mmfutils/solve/broyden.py</a></td>
                    <td>319</td>
                    <td>64</td>
                    <td>0</td>
                    <td class="right" data-ratio="255 319">80%</td>
                </tr>
                <tr class="file">
                    <td class="name left"><a href="mmfutils_testing_py.html">mmfutils/testing.py</a></td>
                    <td>18</td>
                    <td>2</td>
                    <td>2</td>
                    <td class="right" data-ratio="16 18">89%</td>
                </tr>
            </tbody>
        </table>
        <p id="no_rows">
            No items found using the specified filter.
        </p>
    </div>
    <div id="footer">
        <div class="content">
            <p>
                <a class="nav" href="https://coverage.readthedocs.io">coverage.py v5.5</a>,
                created at 2021-04-28 01:48 -0700
            </p>
        </div>
    </div>
    </body>
    </html>




Change Log
==========

REL: 0.5.4
----------

-  Drop support for Python 3.5.
-  Use `Nox <https://nox.thea.codes>`__ for testing (see
   `Notes.md <../Notes.md>`__)

REL: 0.5.3
----------

Allow Python 3.8. Previous version required ``python <= 3.7`` due to an
`issue with
ipyparallel <https://github.com/ipython/ipyparallel/issues/396>`__. This
has been resolved with revision 6.2.5 which is available with ``conda``.

REL: 0.5.1
----------

API changes:

-  Split ``mmfutils.containers.Object`` into ``ObjectBase`` which is
   simple and ``ObjectMixin`` which provides the picking support.
   Demonstrate in docs how the pickling can be useful, but slows
   copying.

REL: 0.5.0
----------

API changes:

-  Python 3 support only.
-  ``mmfutils.math.bases.interface`` renamed to
   ``mmfutils.math.bases.interfaces``.
-  Added default class-variable attribute support to
   e\ ``mmfutils.containers.Object``.
-  Minor enhancements to ``mmfutils.math.bases.PeriodicBasis`` to
   enhance GPU support.
-  Added ``mmfutils.math.bases.interfaces.IBasisLz`` and support in
   ``mmfutils.math.bases.bases.PeriodicBasis`` for rotating frames.
-  Cleanup of build environment and tests.

   -  Single environment ``_mmfutils`` now used for testing and
      documentation.

REL: 0.4.13
-----------

API changes:

-  Use ``@implementer()`` class decorator rather than
   ``classImplements`` or ``implements`` in all interfaces.
-  Improve ``NoInterrupt`` context. Added ``NoInterrupt.unregister()``:
   this allows ``NoInterrupt`` to work in a notebook cell even when the
   signal handlers are reset. (But only works in that one cell.)
-  Added Abel transform ``integrate2`` to Cylindrical bases.

Issues:

-  Resolved issue #22: Masked arrays work with ``imcontourf`` etc.
-  Resolved issue #23: ``NoInterrupt`` works well except in notebooks
   due to `ipykernel issue
   #328 <https://github.com/ipython/ipykernel/issues/328>`__.
-  Resolved issue #24: Python 3 is now fully supported and tested.

REL: 0.4.10
-----------

API changes:

-  Added ``contourf``, ``error_line``, and ``ListCollections`` to
   ``mmfutils.plot``.
-  Added Python 3 support (still a couple of issues such as
   ``mmfutils.math.integrate.ssum_inline``.)
-  Added ``mmf.math.bases.IBasisKx`` and update ``lagrangian`` in bases
   to accept ``k2`` and ``kx2`` for modified dispersion control (along
   x).
-  Added ``math.special.ellipkinv``.
-  Added some new ``mmfutils.math.linalg`` tools.

Issues:

-  Resolved issue #20: ``DyadicSum`` and
   ``scipy.optimize.nonlin.Jacobian``
-  Resolved issue #22: imcontourf now respects masked arrays.
-  Resolved issue #24: Support Python 3.

REL: 0.4.9
----------

*< incomplete >*

REL: 0.4.7
----------

API changes:

-  Added ``mmfutils.interface.describe_interface()`` for inserting
   interfaces into documentation.
-  Added some DVR basis code to ``mmfutils.math.bases``.
-  Added a diverging colormap and some support in ``mmfutils.plot``.
-  Added a Wigner Ville distribution computation in
   ``mmfutils.math.wigner``
-  Added ``mmfutils.optimize.usolve`` and ``ubrentq`` for finding roots
   with ```uncertanties`` <https://pythonhosted.org/uncertainties/>`__
   support.

Issues:

-  Resolve issue #8: Use
   ```ipyparallel`` <https://github.com/ipython/ipyparallel>`__ now.
-  Resolve issue #9: Use `pytest <https://pytest.org>`__ rather than
   ``nose`` (which is no longer supported).
-  Resolve issue #10: PYFFTW wrappers now support negative ``axis`` and
   ``axes`` arguments.
-  Address issue #11: Preliminary version of some DVR basis classes.
-  Resolve issue #12: Added solvers with
   ```uncertanties`` <https://pythonhosted.org/uncertainties/>`__
   support.
