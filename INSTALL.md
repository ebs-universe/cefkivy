
cefkivy-ebs
===========

preliminary notes
-----------------

 * Everything here is only for `python3`. If you want to use `python2`, work through the process independently.   
 * `cefkivy` is a wrapper / adapter which uses `cefpython3` under the hood to provide a widget for use in Kivy applications.
 * `cefpython3` provides python bindings to the `cef` library
 * `cef` provides a way to embed a specific chromium version in other applications.
 * The latest release of `cefpython3` is built for version 66.
 * `cefpython3` does not support ARM. See [cztomczak/cefpython #267](https://github.com/cztomczak/cefpython/issues/267).
 * `cefpython3` does not support Android.`
 * `cefpython3` builds for linux stop at version 66.0, which only supports upto python 3.7.x. Version 66.1, which supports later python versions, has only been officially built for Windows. See [cztomczak/cefpython #609](https://github.com/cztomczak/cefpython/issues/609).
 * To avoid losing one's mind, this guide is going to be focussed on Python 3.7.x installed using pyenv on an x86-64 linux machine and targeted against Chromium 66 only.
 * We're going to start with the Quick Installation using prebuilt binaries from github releases.


quick installation on x86-64 / amd64
-------------------------------------

 * Build, if any, is based on [Quick build instructions for Linux](https://github.com/cztomczak/cefpython/blob/master/docs/Build-instructions.md#quick-build-instructions-for-linux).
 * Installation tested on `Ubuntu 20.04.3`, for (hopefully) eventual deployment on Debian `buster` or `bullseye`.

Since we're restricted to `python 3.7.x`, there's a good chance that we're not using system python. `pyenv` by default [does not build the shared library](https://github.com/pyenv/pyenv/issues/443#issuecomment-142006706) ( :| ), so rebuild the interpreter with 

``` 
$ export PYTHON_CONFIGURE_OPTS="--enable-shared" 
$ pyenv install -v 3.7.8
$ pyenv rehash
```

If you already have 3.7.8 installed, this should not break exisiting virtual environments. It will replace the interpreter with the freshly built one, though, so if you are using something quirky already, be careful. See [this SO answer](https://stackoverflow.com/a/58508429).

Also create and activate the python `virtualenv` you want to use.

```
$ pyenv virtualenv 3.7.8 cef-37
$ pyenv activate cef-37
```

At this point, you can install `cefpython3` from `pip` as usual. Confirm that it works by atleast importing `cefpython3`. 

```
$ pip install cefpython3
...
$ python
Python 3.7.8 (default, May 22 2021, 02:40:56) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cefpython3
>>> 
```

Additionally, you can run the cefpython example and make sure it works by itself.

```
$ git clone https://github.com/cztomczak/cefpython.git
$ cd cefpython/examples/
$ python hello_world.py
```

Assuming it worked so far, install `cefkivy-ebs` and run the example provided in the repository to ensure it works. 

```
$ pip install cefkivy-ebs
$ cefkivy-example
```

If it did not work, you might need to build your own version of `libcef.so`. I have not yet had to do this, and it is not documented here.
