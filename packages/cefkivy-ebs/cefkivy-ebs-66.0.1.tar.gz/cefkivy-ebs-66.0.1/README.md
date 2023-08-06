
About this Fork
---------------

This package builds on a lot of good work of other people, including the 
developers of :
  - [CEF](https://bitbucket.org/chromiumembedded/cef/src/master/)
  - [cefpython](https://github.com/cztomczak/cefpython)
  - The CEF [Kivy Garden flower](https://github.com/kivy-garden/garden.cefpython)
  - The [cefkivy](https://github.com/rentouch/cefkivy) fork of the Kivy Garden flower.

This is forked from `rentouch/cefkivy` for the sole purpose of making it pip 
installable and minimal maintenance to ensure functionality. 

  - At the time of the fork, upstream has remained unchanged 
  for 8 years. 
  - One pseudo fork has been published to PyPI with the cefkivy 
  package name with no apparent commits and/or no real version history.

As such, the original rentouch cefkivy repository is being forked here 
and will be made available as the `cefkivy-ebs` package on PyPI. 

Though the package will be installed as `cefkivy-ebs`, the actual 
importable package will still be `cefkivy`. As such, this fork and 
upstream cannot coexist in the same virtual environment. 

This package contains no EBS-specific code and has no dependencies 
outside of `cefpython3`, `kivy`, and the Python Standard Library. 
For detailed install notes, see [INSTALL.md](INSTALL.md).

If you are considering using this: 

  - I do not really have the bandwidth to maintain this fork. I will 
  make the best effort to keep this package installable with minimal 
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
  skilled time will need to be invested to help bring this (and `cefpython3`) 
  up to date and keep it there.

If you do end up using this package - especially if you do so in a 
production setting - please reach out to me and let me know by email at 
shashank at chintal dot in. The number of users, if any, is likely to 
determine how much effort I will put into maintaining this.

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
