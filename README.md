# dunerun
Support for running commands and building SW for DUNE.

## Installation and set up
To install this package at MY-INSTALL-PATH:
<pre>
cd any-directory
git clone https://github.com/dladams/dunerun.git
./dunesw-support/build -i MY-INSTALL-PATH
</pre>
The option can be omitted if you have defined env variable DUNE_INSTALL_DIR.

To set up to use the package in this or any future session:
<pre>
source MY-INSTALL-PATH/setup.sh
</pre>

## Running from the linux command line
After the above setup, the command *dune-run* is available. To see the current options use the -h option:
<pre>
> dune-run -h
Usage: /home/dladams/proc/install/common/dunesw-support/bin/dune-run [-e ENV] [-r REL] [-d LEVEL] COM
Runs command COM in the environment defined by "source setup-ENV.sh REL"
  ENV - Environment name.
        Default is env variable DUNESW_SUPPORT_ENV.
        Provided here:
          dune - Sets up dune w/o any packages.
          dunesw - Sets up dune w/ dunesw with REL=VERS:QUAL
        If udefined or '.', the command is run without setup.
  REL - Release tag (e.g. v09_42_03_00 or v09_42_03_00:c7:prof)
        Default is env variable DUNESW_SUPPORT_RELEASE.
  LEVEL - 0 - Command is executed with no output from this script or
              from the setup (default)
          1 - Command is executed with informational messages.
          2 - Command and infomational messages are displayed w/o execution.
If both setup and release are provided then the release is
passed as an argument to the setup.
If only the setup is provided then the release is set up from CVMFS
</pre>
The environment *dune* locates the DUNE/larsoft software without setting up any packages. This is useful for issuing the usual ups command to see what packages are available, e.g.
<pre>
> dune-run -e dune ups list -aK+ dunesw
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "c7:prof" ""
</pre>

The environment *dunesw* sets up the specified version of that top-level DUNE package. For example, one can then ask for help:
<pre>
> dune-run -e dunesw -r v09_42_04_00:e20:prof duneHelp
Welcome to dunetpc 
Some available commands:
              duneHelp - Display information about the current setup of dunetpc.
                   lar - Run the art/larsoft event looop e.g. to process event data.
  product_sizes_dumper - Display the products and size in an event data file.
               fcldump - Display the resolved configuration for a fcl file.
               liblist - List available plugin libraries.
        pdChannelRange - Display protoDUNE channel grops and ranges.
           duneRunData - Display run data for a run.
           duneTestFcl - Test some high-level fcl configurations.
Use option "-h" with any of these for more information.
</pre>
Or run the fcl tests:
<pre>
> dune-run -e dunesw -r v09_42_04_00:c7:prof duneTestFcl
iceberg3_decode_reco.fcl is ok
iceberg4a_decode_reco.fcl is ok
iceberg4b_decode_reco.fcl is ok
iceberg5_decode_reco.fcl is ok
standard_reco_dune10kt_nu_1x2x6.fcl is ok
vdcoldbox_raw_dataprep.fcl is ok
vdcoldbox_raw_tdedataprep.fcl is ok
hdcoldbox_raw_dataprep.fcl is ok
protodune_dqm.fcl is ok
protodune_dqm2.fcl is ok
iceberg3_dqm1.fcl is ok
iceberg4_dqm1.fcl is ok
iceberg5cond_dqm1.fcl is ok
All 13 fcl files processed successfully.
</pre>

Significant time is required to set up up the *dunesw* environment when the each above commands are run. Use the special command 'shell' to start an interactive shell in the specified environment so this set up only has to be performed once. For example:
<pre>
> dune-run -e dunesw -r v09_42_04_00:c7:prof shell
dunesw-v09_42_04_00:c7:prof> duneHelp
Welcome to dunetpc 
Some available commands:
              duneHelp - Display information about the current setup of dunetpc.
                   lar - Run the art/larsoft event looop e.g. to process event data.
  product_sizes_dumper - Display the products and size in an event data file.
               fcldump - Display the resolved configuration for a fcl file.
               liblist - List available plugin libraries.
        pdChannelRange - Display protoDUNE channel grops and ranges.
           duneRunData - Display run data for a run.
           duneTestFcl - Test some high-level fcl configurations.
Use option "-h" with any of these for more information.
dunesw-v09_42_04_00:c7:prof> duneTestFcl
iceberg3_decode_reco.fcl is ok
iceberg4a_decode_reco.fcl is ok
iceberg4b_decode_reco.fcl is ok
iceberg5_decode_reco.fcl is ok
standard_reco_dune10kt_nu_1x2x6.fcl is ok
vdcoldbox_raw_dataprep.fcl is ok
vdcoldbox_raw_tdedataprep.fcl is ok
hdcoldbox_raw_dataprep.fcl is ok
protodune_dqm.fcl is ok
protodune_dqm2.fcl is ok
iceberg3_dqm1.fcl is ok
iceberg4_dqm1.fcl is ok
iceberg5cond_dqm1.fcl is ok
All 13 fcl files processed successfully.
dunesw-v09_42_04_00:c7:prof> exit
exit
>
</pre>

## Running from python
The python class *DuneRun* in module *dunerun* provides similar fuctionality at the python command line. For examples of use, see the [dunerun notebook](ipynb/dunerun.ipynb).

