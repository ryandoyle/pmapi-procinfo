# pmapi-procinfo

### pcp-procinfo.py
Simple code to print pids and the names from proc.psinfo.pid metric using pmFetch().

Sample:

```

ram@ram-Lenovo:~/workspace/pmapi-procinfo$ python pcp-procinfo.py 
Connection Established
no of instances:  268
PID			Name
1 		000001 /sbin/init splash
2 		000002 (kthreadd)
3 		000003 (ksoftirqd/0)
5 		000005 (kworker/0:0H)
7 		000007 (rcu_sched)
8 		000008 (rcu_bh)
......
```

### pcp-procinfo_fg.py
Simple code to print per cpu user time (can be zero if idle) and current process info using pmFetchGroup()

Use:    
```
ram@ram-Lenovo:~/workspace/pmapi-procinfo$ python pcp-procinfo_fg.py 
in connect
Timestamp:  2016-05-13 11:25:53.668610
CPUID		CPUNAME		Value
 0 		 cpu0 		0.000000
 1 		 cpu1 		0.000000
 2 		 cpu2 		0.000000
 3 		 cpu3 		0.000000
=====================================================
PID			NAME
1		000001 /sbin/init splash
2		000002 (kthreadd)
3		000003 (ksoftirqd/0)
5		000005 (kworker/0:0H)
7		000007 (rcu_sched)

```
