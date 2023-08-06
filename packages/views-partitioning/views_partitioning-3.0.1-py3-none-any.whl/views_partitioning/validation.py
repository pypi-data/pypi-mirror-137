

valid_time_period = lambda a,b: a < b & a >= 0
period_gt = lambda a,b: a[1]<b[0]
period_as_range = lambda p: range(p[0],p[1]+1)
non_overlapping = lambda a,b: (a[0]<b[0]&a[1]<b[0])|(a[0]>b[0]&a[0]>b[1])
