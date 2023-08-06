# Base image
FROM continuumio/miniconda3

# Base packages
RUN \
  apt-get update -qy && \
  apt-get upgrade -qy && \
  apt-get install -qy \
    graphviz \
    pandoc \
    python3-pip \
    zip

RUN \
  conda install -c conda-forge phono3py

RUN \
  pip3 install --upgrade \
    pip \
  && \
  pip3 install --upgrade \
    coverage \
    flake8 \
    nbmake \
    pytest \
    twine \
    xdoctest

# Packages needed for hiphive
# (The version limit on numpy is dictated by numba.)
RUN \
  pip3 install \
    h5py \
    numba \
    'numpy<1.21' \
    sympy \
  && \
  pip3 install \
    ase \
    scikit-learn \
    scipy \
    spglib

# Packages for building documentation
RUN \
  pip3 install --upgrade \
    sphinx_autodoc_typehints \
    sphinx-rtd-theme \
    sphinx_sitemap \
    sphinxcontrib-bibtex \
    cloud_sptheme \
    nbsphinx

# Packages for running examples
RUN \
  pip3 install \
    pandas \
    phonopy

CMD /bin/bash
