# duneproxy.py
#
# David Adams
# March 2022

import subprocess
import dunerun

class DuneProxy:

    @staticmethod
    def time():
        """Return the time [seconds] for with the proxy sill be valid."""
        cpr = subprocess.run(['voms-proxy-info', '-actimeleft'], capture_output=True)
        if cpr.returncode == 0: return int(cpr.stdout.decode().strip())
        return 0

    @staticmethod
    def have_kerberos_credentials():
        """Returns true if the user has kerberos credentials."""
        cpr = subprocess.run(['klist'], capture_output=True)
        return cpr.returncode == 0

    def __init__(self, nopassword_kinit, tmin=60):
        """
        Class to check manage the user's VOMS proxy.
        Arguments:
          nopassword_kinit - Set True if kerberos credentials can be obtained without
                             user-suppplited password. In that case this class will
                             generate those as needed. Otherwise the user is prompted
                             to perform the kinit.
          tmin - Minimum remaining time [sec] for which is_valid returns True.
        """
        self.nopassword_kinit = nopassword_kinit
        self.tmin = tmin

    def is_valid(self):
        """Return if a valid proxy with t > tmin is present."""
        return self.time() > self.tmin

    def get_proxy(self, force=True, lev=0):
        """
        Attempt to obtain a VOMS proxy.
        If force is not True, no action is taken if a valid proxy (t > tmin)
        already exists.
        """
        # We use DuneRun so we can kx509 from cvmfs.
        # it is not installed at EAF.
        dune = dunerun.DuneRun('dune', shell=True, lev=lev)
        dune.run('setup kx509')
        dune.run('kx509 --minhours 12')
        dune.run('voms-proxy-init -noregen -rfc -voms dune:/dune/Role=Analysis')
