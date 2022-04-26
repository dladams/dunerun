#!/usr/bin/env python

import dunerun
t = dunerun.DuneProxy.time()
if not t > 0:
  p = dunerun.DuneProxy()
  p.check_proxy()
  t = dunerun.DuneProxy.time()
if t > 0:
  print(f"Proxy time remaining is {t} sec")
else:
  print("Unable to obtain proxy")
