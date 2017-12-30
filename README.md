# how2fsb
Format String Bugs (FSB) and tutorials on how to exploit them. 
A _Format String Bug_ is when an application passes user input directly to `printf()`. EG:
```
    fgets(buffer, BUF_LEN, stdin);
    printf(buffer);
```
This allows the user to do all sorts of fun stuff. 

This repo contains examples of _Format String Bug_ exploitable binaries that can be used to learn and practice. All these binaries are 32bit. Compiled on Ubuntu 16.04.

Suggested Order: Complete the tutorial in the playground section. This will give an indepth, hands on guide on how to exploit _Format String Bugs_. After that, try to solve levels 1-5.

### [Playground](./playground)
Please check this out to get a rundown of all the different things you can do with FSB (step by step guide). There is an interactive script that will let you attach to the playground application and peek/poke at memory and step through the assembly.

### [Level 1](./level1)
This level was taken directly from the PicoCTF2017 challenge "Ive Got A Secret". It's a great intro into FSB. I downloaded the source and recompiled it.

### [Level 2](./level2)
First write!!! Introduction into using %n or %hn.

### [Level 3](./level3)
Second write. Introduction into actually writing the value you want in a specific location.

### [Level 4](./level4)
This one introduces the concept of updating the GOT to redirect execution to do what we want.

### [Level 5](./level5)
This requires multiple writes to achive the desired result. You need to utilize all the knowledge gained on levels 1-4 to get the flag.

#### Required Reading:
[https://www.exploit-db.com/docs/28476.pdf](https://www.exploit-db.com/docs/28476.pdf)

[https://crypto.stanford.edu/cs155old/cs155-spring08/papers/formatstring-1.2.pdf](https://crypto.stanford.edu/cs155old/cs155-spring08/papers/formatstring-1.2.pdf)

