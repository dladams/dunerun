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

    def __init__(self, nopassword_kinit=False, tmin=60):
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

    def get_proxy(self, lev=0):
        """
        Attempt to obtain a VOMS proxy. Returns if that proxy is valid.
        """
        # We use DuneRun so we can kx509 from cvmfs.
        # it is not installed at EAF.
        dune = dunerun.DuneRun('dune', shell=True, lev=lev)
        if not self.have_kerberos_credentials():
            if not self.nopassword_kinit:
                raise Exception(f"{myname}: Kerberos credentials not found. Please run kinit.")
            dune.run('kinit')
        dune.run('setup kx509')
        dune.run('kx509 --minhours 12')
        dune.run('voms-proxy-init -noregen -rfc -voms dune:/dune/Role=Analysis')
        return self.is_valid()

    def check_proxy(self, lev=0):
        """Tries to get a proxy if we don't already have it."""
        if self.is_valid(): return True
        return self.get_proxy(lev)
