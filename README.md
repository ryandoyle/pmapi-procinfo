# pmapi-procinfo

Simple code to print pids and the names from proc.psinfo.pid metric.

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
