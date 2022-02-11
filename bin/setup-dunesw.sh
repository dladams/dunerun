VERS=$(echo $1 | sed 's/:.*//g')
QUAL=${1:$((${#VERS}+1))}
if [ -z "$QUAL" ]; then QUAL=e20:prof; fi

if [ -n "$VERS -a -n "$QUAL"" ]; then
  source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh >/dev/null
  setup dunesw $VERS -q $QUAL >/dev/null
else
  echo setup-dunesw.sh: ERROR: Invalid release:quailifier: $1
fi
