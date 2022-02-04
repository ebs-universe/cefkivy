
About this Fork
---------------
This is forked from rentouch/cefkivy for the sole purpose of making it pip 
installable and minimal maintenance to ensure functionality. 

  - At the time of the fork, upstream has remained unchanged 
  for 8 years. 
  - One pseudo fork has been published to PyPI with the cefkivy 
  package name with no apparant commits and/or no real version history.

As such, the original rentouch cefkivy repository is being forked here and 
will be made available as the `cefkivy-ebs` package on PyPI. 

If you are cnsidering using this, please note that: 

  - I do not really have the bandwidth to maintain this fork, nor the 
  direct experience needed to do anything more than minor tweaks. I will 
  make a best effort to keep this package installable with no / minimal 
  feature addition.
  - If upstream resumes development, or an alternate means to provide a 
  browser widget to Kivy is developed, this fork and the associated pypi 
  package will likely become unmaintained.
  - Issues are welcome. Those dealing with install and basic functionality 
  will be prioritized. Feature / upgrade requests, if meaningful, will be 
  left open.
  - Pull Requests are welcome, as long as the change they make breaks no 
  existing functionality.
  - If you are able and willing to take over or contribute to the development 
  of this package, please get in touch with me. Primarily, I anticipate 
  skilled time will needed to be invested to help bring this (and if 
  necessary, cefpython3) up to date and keep it there. 


Original README.md 
------------------


How to install
==============
Notes about the requirements.txt file:
The cefpython3 dependency is the cefpython python package built by Rentouch.
(used for CI). Please use your own version of cefpython either by
exporting the PYTHONPATH to the location of the built cefpython or by installing
cefpython globally.

You need the following dependencies installed listed in the requirements.txt


About this project
==================
This can be seen as a kivy/garden.cefpython fork. Rentouch needs more
flexibility in the repo itself (version numbers, room for experiments,
tighter integration with pip, by creating wheels etc...)


About the import of cefpython
=============================
It will try to import in the following order:
1. Cefpython binary in the PYTHONPATH
2. Cefpython binary globally installed
