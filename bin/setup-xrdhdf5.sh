XRDIR_TOM=/dune/app/users/trj/xrootd542/install/lib64
FLAV=$(basename $UPS_DIR)
XRDIR_LOC=/cvmfs/dune.opensciencegrid.org/products/dune/testproducts/xrootd
XROOTD_LIB=$(echo $XROOTD_LIB | sed "s#.*/products/xrootd/#$XRDIR_LOC/#g")

if [ ! -r $XROOTD_LIB ]; then
  echo $MYNAME: ERROR: Directory not found: $XROOTD_LIB
else
  export LD_LIBRARY_PATH=$XROOTD_LIB:${LD_LIBRARY_PATH}
  export LD_PRELOAD=$XROOTD_LIB/libXrdPosixPreload.so:${LD_PRELOAD}
fi

