cmding
======

Cmder is a simple module which aims to bring enjoyable experience for 
running shell commands in Python.

By wrapping Python `subprocess.Popen`, cmder provides a convenient way for you to run any 
shell command through Python and offers some additional features.

Installation
------------

```shell
pip install cmder
```

Features
--------
- Running any command using either a string or a list. 
- Running any command like you run them from the shell. The pipe and redirection operations 
  are native permitted due to the pre-filled argument `shell=True`.
- Automatically reformat the command.  Break long command string into multiple lines and format 
  them nicely.
- Profile command running time and memory usage. Using `/usr/bin/time` to profile the time and memory 
  usage of the running command.
  

Usage
-----

Import the module and call `run` the same way you call `subprocess.run` with two additional 
keyword argument: `msg` and `pmt`. `msg` cam be a simple string for display a message 
before and after running the command. Set `pmt` to True or False will enable or disable time and 
memory profiling feature. Since `cmder.run` wrappers `subprocess.Popen`, all other keyword arguments 
allowed for `subprocess.Popen` are also allowed here.

```python
import cmder
cmder.run('ls -lh', msg='List files with details ...', pmt=True)
```

Note: 
  - Without a message string passed by `msg`, profiling time and memory will be ignored even the 
    `pmt` argument was set to True.
    

Limitations
-----------

1. Since the time and memory profiling depends on GNU version `/usr/bin/time`, it does not work 
  on BSD system.
2. Since the argument `shell=True` was pre-filled when call `subprocess.Popen`, user should be aware 
  of the potential security issue and use this module with caution.




