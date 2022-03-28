# Dunerun build Convention

David Adams  
March 2022  
Version 1.0.0

This page specifies the *dunerun build convention* for package building and installation.
Packages satisfying these requirements are said to be *dunerun-conformant*

The source for a package consists of files in a directory tree typically stored in a git
repository with the same name.
The top-level of that tree is required to provide a script *build* which builds and installs
the package at the location specified below and provides a setup script that can be sourced
to enable use of the package from a bash command line or subsequent applications like Root
or python.
After installation, the source and build areas can be removed or altered without affecting
this run time behavior.

The build is controlled by the following env variables as described below:

| Flag |   Variable |              [Default] |
|-----|---|---|
|  -i | DUNE_INSTALL_DIR   |  [$HOME/dune/install] |
|  -b | DUNE_BUILD_DIR     |  [$DUNE_INSTALL_DIR/../build]
|  -p | DUNE_INSTALL_BYPKG |  [true]
|  -v | DUNE_VERSION       |  [<undefined>]
|  -q | DUNE_QUALIFIER      |  [<undefined>]

## Installation

If DUNE_INSTALL_BYPKG has the value "true" or is undefined, then the installation is
*by-package* meaning it is done at 
at DUNE_INSTALL_DIR/\<PKGNAME> where \<PKGNAME> denotes the package name.
All files should be written in or below that directory and no other package should
write in that directory. The setup script for the package is
DUNE_INSTALL_DIR/\<PKGNAME>/setup.sh.

If DUNE_INSTALL_BYPKG has the value "false", the installation is directly in
subdirectories of DUNE_INSTALL_DIR including
* bin - included in PATH
* lib - included in LD_LIBRARY_PATH or equivalent
* python - included in PYTHONPATH
* include - included in INCLUDEPATH (?) 
* root
* setup - holds package setup scripts
* catalogs - file catalog for each installed package
with setup script written to setup/setup-PKGNAME.sh. That script will be run after
the installation area is set up in a manner to be specified in future versions of
this document. At minimum, the bin, lib and python directories are included in the
paths indicated above.

For any other value of DUNE_INSTALL_BYPKG, the build script may install by-package
or exit with error.
  
For installation by-package only, the setup script should prepend the appropriate
directories the sysetem paths. In both cases the setup should define the variable
<PKGNAME>_VERSION indicating the package version.
  
## DUNE software
The variables DUNE_VERSION and DUNE_QUAL repectively indicate the DUNE software
version and ups qualifier with which the release area is intended to be used.
  
## Build options
The build command line can include a list of options including the following
* help - show the supported options and their meanings (required)
* install - build and install the package (required)
* build - build without installing
* remove - remove the installed files (required)
* test - run tests on the installation
The list indicates which option are required for a package to be dunerun-conformant.
