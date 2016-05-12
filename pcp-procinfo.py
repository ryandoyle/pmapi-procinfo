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
            metrics = ('proc.psinfo.pid',)
            pmids = self.context.pmLookupName(metrics)
            # print "PMID: ",pmids
            descs = self.context.pmLookupDescs(pmids)
            # print "Desc: ",descs
            result = self.context.pmFetch(pmids)
            if result.contents.numpmid != len(metrics):
                print "Got error here"
                raise pmapi.pmErr(PM_ERR_VALUE)
            num_inst = result.contents.get_numval(0)
            print "no of instances: ",num_inst
            # print "Inst domain: ",descs[0].contents.indom
            ''' Get external_names '''
            internal_instance_ids,external_names = self.context.pmGetInDom(descs[0])

            ''' Get values (pids) from the pmResult '''
            print "PID\t\t\tName"
            for i in range(num_inst):
                atom = self.context.pmExtractValue(
		                result.contents.get_valfmt(0),
		                result.contents.get_vlist(0,i),
		                descs[0].contents.type,
		                PM_TYPE_U32)

                #Get the name by either looking from the offset in the extername list
                # external_name_offset = internal_instance_ids.index(result.contents.get_inst(0,i))
                # external_name = external_names[external_name_offset]

                # Or lookup with pmNameInDom(pmdesc, internal_instance_id)
                external_name = self.context.pmNameInDom(descs[0], result.contents.get_inst(0,i))


                ''' Strip options from the external_name, a space followed by a - can be considered an option'''
                strip_options_index = external_name.find(" -")
                if strip_options_index > 0:
                    print atom.ul, "\t\t", external_name[:strip_options_index]
                else:
                    print atom.ul, "\t\t", external_name
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
