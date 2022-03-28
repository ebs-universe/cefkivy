
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

The original rentouch cefkivy repository is being forked here 
and will be made available as the `kivy_garden.ebs.cefkivy` package 
on PyPI. 

This package contains some minimal EBS-specific code and depends on 
[kivy_garden.ebs.core](https://github.com/ebs-universe/kivy_garden.ebs.core). 
This dependency is easily removed, but has been left in for the moment. 
In addition, the package depends on `cefpython3`, `kivy`, and the Python 
Standard Library. For detailed install notes, see [INSTALL.md](INSTALL.md).

If you are considering using this: 

  - I do not really have the bandwidth to maintain this fork. I will 
  make the best effort to keep this package installable with minimal 
  feature addition, but that's about it.
  - If upstream resumes development, or an alternate means to provide a 
  browser widget to Kivy is developed, this fork and the associated pypi 
  package will likely become unmaintained.
  - No work has been done to make sure this works on Mac, Windows, or Android. 
  There is unlikely to be ever any such work. That said, there is nothing that 
  I can think of which would break it on Mac/Windows, and trying to install 
  cefpython on Android is likely to be a fool's errand.
  - Issues are welcome. Those dealing with install and basic functionality 
  will be prioritized. Feature / upgrade requests, if meaningful, will be 
  left open.
  - Pull Requests are welcome, as long as the change they make breaks no 
  existing functionality.
  - If you are able and willing to take over or contribute to the development 
  of this package, please get in touch with me. Primarily, I anticipate 
  skilled time will need to be invested to help bring this (and `cefpython3`) 
  up to date and keep it there. Additionally, having someone to keep the 
  library functional on Mac/Windows would be helpful.

If you do end up using this package - especially if you do so in a 
production setting - please reach out to me and let me know by email at 
shashank at chintal dot in. The number of users, if any, is likely to 
determine how much effort I will put into maintaining this.


Current Status
==============

### Next

The package as it stands works, more or less. Development is suspended for the most part. 
I don't actually test this with very new version of things or new combinations of 
environment and dependencies, so if you find any issues please feel free to report them.
If you can provide a fix which does not break anything presently working, or if I can 
reproduce the issue, I will do what I can to fix it. 

Known Issues : 

  - Popups still don't work and are universally blocked. 
  - The enter key still doesn't work as expected on both the physical and virtual keyboards. 
  Not entirely certain if it is supposed to.
  - Touch gestures are broken. 
     - Left click works fine. Right click doesn't. 
     - Two finger scroll isn't really working, but might not be very 
     difficult to fix.
     - Drag remains disabled, and drag events are translated to scroll events.
     - Repurposing the drag events breaks interaction where drag is actually 
     needed. Things like OSM and Google Maps zoom (scroll) when the intent is 
     pan (drag).
     - Pinch to zoom is not implemented. 
  - Some restructuring of the Mixins is needed to better capture the dependencies and 
  create a reliable MRO. 
  - Documentation and examples need to be written up.

Future Steps are dependent on available time and bandwidth, and in some ways more so
on the cefpython version. Specifically, the following external updates might be important: 

  - cefpython 66.1 should provide support for python version(s) later than 3.7.x. See 
  https://github.com/cztomczak/cefpython/issues/609
  - Chromium 74 or so should provide `OnVirtualKeyboardRequested`, which could make
  triggering the virtual keyboard more reliable and remove the horrible JS injection.
  See https://bitbucket.org/chromiumembedded/cef/pull-requests/202/added-cefrenderhandler
  - The roadmap for Multitouch and gestures is not quite clear to me. 
  See https://github.com/cztomczak/cefpython/issues/57

### v66.0.11, April 2022

  - Migrate to the new kivy_garden flower format. 

### v66.0.6 - v66.0.10 March 2022

  - Minor bugfix / maintenance updates, closing out open development threads.

### v66.0.5, March 2022

  - JS injection reintroduced for Keyboard management.
  - Default Keyboard mode changed back to local.
  - Keyboard events changed to use `on_text_input` instead of `on_key_*`. This 
    removes the complexity of keycode processing. 'Special' characters are 
    still handled the old way.
  - Virtual Keyboard more or less works. Enter key doesn't seem to be 
    intuitive, might need work.

### v66.0.4, March 2022

  - Rationalize event and event handler chains. 
  - Cleanup additional blocks of dead code.
  - Restructure for maintainability.
  - Restructure and near full rewrite of touch processing.
    - Mouse scrolling functional
    - Right clicks still cause trouble.
    - Remove touch drag functionality and replace with touch scrolling (panning).
    - Drag vs Scroll causes significant unresolved breakage on websites such as OSM.

### v66.0.3, March 2022

  - Core support for message box-style dialogs implemented.
  - JS Dialogs implemented.
  - Block Messages implemented.
  - Popups suppressed entirely.

### v66.0.2, March 2022

  - Touch, virtual keyboard not yet tested.
  - JS in the LoadHandler stripped out completely to debug the keyboard 
    issue. This may eventually be reintroduced, but for now, it's not there. It
    seems likely it will be needed for a virtual keyboard.
  - Keyboard issue tracked down to KeyEvent dictionary structure having been 
    changed in cefpython3. A horribly messy keycode translation layer has 
    been added and keyboard input sort of works on unix.  
  - Keyboard made 'global' by default to simplify testing.
  - Application seems to exit fine now, uncertain why.

### v66.0.1, February 2022

  - Package installs fine on x86-64 and seems to basically run.
  - Application exit hangs. There probably needs to be an exit handler 
   or the shutdown callbacks need to be fixed.
  - Keyboard key-presses seem to work in popups but not in the main 
   browser widget. This needs to be fixed.
  - Virtual keyboard has not been seen. The code suggests it should have 
   appeared on its own, but it has not. This is yet to be investigated.
  - This version is a cleaned up and updated version of upstream with 
   no significant structural or functional changes. Cosmetic changes
   (refacoring) intended to support maintainability have been done. 

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
