geodesic-chenhan
=================

This is an updated fork of the original [chenhan_cython](https://github.com/aalavandhaann/chenhan_cython) repo. It uses `pyproject.toml` to pre-install `Cython` and `autowrap` before the compilation step, so that you don't need to install it beforehand. It also has some slight changes to the C++ code to make it work for some
projects I'm working on.

Future work will focus on creating an interface for this module to work with the [Trimesh](https://github.com/mikedh/trimesh) library.
