from pcp import pmcc
import itertools

class SimpleThreadReporter(pmcc.MetricGroupPrinter):
    def report(self, manager):
        group = manager["procinfo"]
        threads = group["proc.psinfo.threads"].netValues
        sorted_by_threads = sorted(threads, key=lambda thread: thread[2], reverse=True)
        for pmvalue, name, thread in itertools.islice(sorted_by_threads, 0, 10):
            print "Instance: ", pmvalue.inst, "Threads", thread

manager = pmcc.MetricGroupManager()
manager.printer = SimpleThreadReporter()
metrics = ['proc.psinfo.threads']
manager["procinfo"] = metrics

manager.run()