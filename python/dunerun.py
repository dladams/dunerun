import os

class DuneRun:
    def __init__(self, senv='', sopt='', dbg=0):
        myname = 'DuneRun'
        self.dbg = dbg
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
            line = line + 'source ' + scom + '; '
        line += com
        if self.dbg: print(f"{myname}: {line}")
        os.system(line)
