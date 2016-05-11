import sys
from pcp import pmapi
from cpmapi import PM_TYPE_U32,PM_TYPE_STRING
from cpmapi import PM_ERR_VALUE

class TotalRead():
    """It prints the total read operations, summed for all disks"""
    def __init__(self):
        self.context = None
        self.opts = pmapi.pmOptions()
        self.opts.pmSetShortOptions("V?")
        self.opts.pmSetLongOptionHeader("Options")
        self.opts.pmSetLongOptionVersion()
        self.opts.pmSetLongOptionHelp()
    def execute(self):
        if self.context:
            # Use a different metric to demonstrate as its easier to see whats going on
            metrics = ('proc.psinfo.threads',)
            pmids = self.context.pmLookupName(metrics)
            # print "PMID: ",pmids
            descs = self.context.pmLookupDescs(pmids)
            # print "Desc: ",descs
            result = self.context.pmFetch(pmids)
            print "type of result: ",type(result)
            if result.contents.numpmid != len(metrics):
                print "Got error here"
                raise pmapi.pmErr(PM_ERR_VALUE)
            num_inst = result.contents.get_numval(0)
            print "no of inst: ",num_inst
            print "Inst domain: ",descs[0].contents.indom
            internal_instance_ids,namelist = self.context.pmGetInDom(descs[0])

            ''' Print pids using the pmResult '''
            for i in range(num_inst):
                atom = self.context.pmExtractValue(
		                result.contents.get_valfmt(0),
		                result.contents.get_vlist(0,i),
		                descs[0].contents.type,
		                PM_TYPE_U32)
                external_name_offset = internal_instance_ids.index(result.contents.get_inst(0,i))
                external_name = namelist[external_name_offset]
                print "Threads: ",atom.ul, "Instance: ", external_name
            self.context.pmFreeResult(result)

    def connect(self):
        """Establish a PMAPI context Local using args """
        self.context = pmapi.pmContext.fromOptions(self.opts,sys.argv)
        if self.context:
            print "Connection Established"


if __name__ == "__main__":
    try:
        tr = TotalRead()
        tr.connect()
        tr.execute()
    except pmapi.pmErr as error:
        print "Error: ",error.message()
    except pmapi.pmUsageErr as usage:
        usage.message()
