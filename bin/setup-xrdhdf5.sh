# setup-xrdhdf5.sh
#
# Set up the test version of xrootd that has hdf5 streaming enabled.
# We require the use have already set up xrootd and prepend streaming
# libs the same version and flavor to LD_LIBRARYPATH and LD_PRELOAD.

if [ -n "$XROOTD_LIB" ]; then
  XRDIR_LOC=/cvmfs/dune.opensciencegrid.org/products/dune/testproducts/xrootd
  XROOTD_LIB=$(echo $XROOTD_LIB | sed "s#.*/products/xrootd/#$XRDIR_LOC/#g")
  if [ ! -r $XROOTD_LIB ]; then
    echo setup-xrdhdf5: ERROR: Directory not found: $XROOTD_LIB >&2
  else
    export LD_LIBRARY_PATH=$XROOTD_LIB:${LD_LIBRARY_PATH}
    export LD_PRELOAD=$XROOTD_LIB/libXrdPosixPreload.so:${LD_PRELOAD}
  fi
else
  echo setup-xrfhdf5: ERROR: Please first set up xrootd, e.g. from dunesw. >&2
fi

