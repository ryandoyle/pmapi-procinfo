import sys
import cpmapi
from pcp import pmapi

class ProcInfo():
    """ Fetch metric proc.psinfo.pid using pmFetchGroup() and display it.  """
    def __init__(self,argv):
        self.fg = None
        self.opts = pmapi.pmOptions()
        self.opts.pmSetShortOptions("V?")
        self.opts.pmSetLongOptionHeader("Options")
        self.opts.pmSetLongOptionVersion()
        self.opts.pmSetLongOptionHelp()
        self.opts.pmSetLongOptionHost()

    def connect(self):
        self.fg = pmapi.fetchgroup(cpmapi.PM_CONTEXT_HOST,"local:")
        ''' for cpuinfo getting information not available error'''
        self.cpuinfo = self.fg.extend_indom('kernel.percpu.cpu.user')
        ''' for pids getting error result size exceeded '''
        self.pids = self.fg.extend_indom('proc.psinfo.pid',maxnum=1000)
        self.tv = self.fg.extend_timestamp()
    def execute(self):
        print "in connect"
        self.fg.fetch()
        self.fg.fetch()         # if there is a metric which requires rate conversion then it needs at least two fetch operations
        # self.fg.fetch()
        print "Timestamp: ",self.tv()       #works fine

        print "CPUID\t\tCPUNAME\t\tValue"
        for (cpuid,cpuname,value) in self.cpuinfo():
            try:
                print(' %d \t\t %s \t\t%f' % (cpuid,cpuname,value()))
            except pmapi.pmErr as e:
                print "Error ",e.message()

        print "====================================================="

        print "PID\t\t\tNAME"
        for pid,pidname,value in self.pids():
            try:
                strip_index = pidname.find(" -")
                if strip_index > 0:
                    pidname = pidname[:strip_index]
                print('%d\t\t%s'%(value(),pidname))
            except:
                pass


if __name__ == "__main__":
    try:
        p = ProcInfo(sys.argv)
        p.connect()
        p.execute()
    except pmapi.pmErr as e:
        print "here 1"
        print "Error: ",e.message()
    except pmapi.pmUsageErr as e:
        usage.message()
