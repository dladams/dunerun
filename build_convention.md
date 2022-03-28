# Dunerun build Convention

David Adams  
March 2022
Version 1.0.0

This page specifies the *dunerun build convention* for package building and installation.
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
at DUNE_INSTALL_DIR/\<PKGNAME> where PKGNAME denotes the package name.
All files should be written in or below that directory and no other package should
write in that directory. The setup script for the package is
DUNE_INSTALL_DIR/PKGNAME/setup.sh.

If DUNE_INSTALL_BYPKG has the value "false", the installation is directly in
subdirectories of DUNE_INSTALL_DIR including
* bin - included in PATH
* include - included in LD_LIBRARY_PATH or equivalent
* lib - included in PYTHONPATH
* python
* root
* setup
with setup script written to setup/setup-PKGNAME.sh.

For any other value of DUNE_INSTALL_BYPKG, the build script may install by-package
or exit with error.
  
The setup script
