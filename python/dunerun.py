import os
import subprocess

def version():
    """Return package version string"""
    scom = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'dunesw-supportVersion')
    return subprocess.run(['bash', '-c', scom], capture_output=True).stdout.decode().strip()

class DuneRun:
    def __init__(self, senv='', sopt='', dbg=0, lev=0):
        """
        Ctor for class that runs dune commands.
        senv = ' ' - Run in bash (no dune set up).
               'dune' - Set up dune env but no products.
               'dunesw' - Set up dunesw.
        sopt = string passed to setup, e.g. 'e20:prof' for dunesw.
        dbg = Output level for messages here: 0 is quietest.
        lev = Output level (in addition to stdout, stderr) for run commands:
              0 - Command is executed with no extra messages.
              1 - Command is executed with informational messages."
              2 - Command and infomational messages are displayed. No command execution."
        """
        myname = 'DuneRun'
        self.dbg = dbg
        self.lev = lev
        self.scoms = []
        if len(senv):
            scom = ''
            sfil = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'setup-'+senv+".sh")
            if os.path.exists(sfil):
                if self.dbg>0: print(f"{myname}: Using setup file {sfil}")
                scom = sfil
                if len(sopt):
                    scom = scom + ' ' + sopt
                self.scoms.append(scom)
            else:
                print(f"{myname}: ERROR: Unable to find setup file {sfil}")
    def run(self, com):
        myname ='DuneRun::run'
        line = ' '
        for scom in self.scoms:
            line += 'source ' + scom
            if self.lev == 0:
                line += " 2>&1 1>/dev/null"
            line += '; '
        line += com
        if self.dbg: print(f"{myname}: {line}")
        #os.system(line)         # This uses sh instead of bash and can't parse setup-dunesw.sh
        subprocess.run(['bash', '-c', line])
