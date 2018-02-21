#! /bin/python

import os
import sys

for i in os.listdir(sys.argv[1]):
	print '    "'+i.replace("_", " ").replace(".whs", "") + '": prefix + "'+sys.argv[1]+'/'+i+'",'

