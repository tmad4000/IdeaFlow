#!/usr/bin/env python
'''import os;
os.system("python imtest.py");
raw_input();'''
from subprocess import Popen,PIPE
import sys

sys.path.append("~/code/som/ideaoverflow_angelhackbos/IdeaOverflow_angelhackbos/ideaflowapp/webapp/")
sys.path.append("~/code/som/ideaoverflow_angelhackbos/IdeaOverflow_angelhackbos/ideaflowapp/ideaflowapp/")

def testrun(cmdline):
   try:
      cmdout, cmderr = "",""
      cmdp = Popen(cmdline, shell=True,stdout=PIPE, stderr=PIPE)
      cmdout,cmderr =  cmdp.communicate()
      retcode = cmdp.wait()
      if retcode < 0:
         print >>sys.stderr, "Child was terminated by signal", -retcode
      else:
         return (retcode,cmdout,cmderr)
   except OSError, e:
      return (e,cmdout,cmderr)

def run():
	import subprocess
	#retcode = call('python', '~/code/som/imtest.py', shell=True)

#	process = subprocess.Popen(['python', '~/code/som/imtest.py'],stdout=PIPE)
	#x=testrun("python ~/code/som/imtest.py")
	#return process.communicate()
	s=""
	'''process = subprocess.Popen(['ls','-la'],stdout=PIPE)
	
	data = process.stdout.read()
	while( (data)  ):
		s=s+data
		data = process.stdout.read()'''

#	process = subprocess.Popen(['python', '~/code/som/imtest.py'],stdout=PIPE)
	'''process = subprocess.Popen(['python', '~/code/som/testsh.sh'],stdout=PIPE)


	data = process.stdout.read()
	while( (data)  ):
		s=s+data
		data = process.stdout.read()'''
	import os
#	return os.popen('python ~/code/som/imtest.py').read()
	return os.popen('~/code/som/testsh.sh').read()

		