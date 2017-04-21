# FSB Playground

This serves as an example of how a FSB can be utilized and provides a working exploit template that can be used to build on to.

You are encouraged to modify and play around with various aspects of the script and use it to get a better understanding of how to exploit a FSB or to play with the application itself.

Try running the [tutorial_example.py](./tutorial_example.py) and reading through what it's doing. 

It does have a dependancy on: [pwntools](https://github.com/Gallopsled/pwntools) please head over there and look up how to install this excellent python module.

It is also recommended that you use something to make the use of GDB a bit 'friendlier'.
I would recommend using one of the following:
 - [pwndbg](https://github.com/pwndbg/pwndbg)
 - [PEDA](https://github.com/longld/peda)

If you run the script with the `-d` option it will cause gdb to attach to the running process with the breakpoint set at exactly the right place before the vulnerable `printf()` call is made.

You can then look at the various parameters passed to the `printf()` statement and poke around the memory and stack etc...
