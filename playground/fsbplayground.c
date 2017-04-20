// gcc -m32 fsbplayground.c -o fsbplayground

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_LEN 64

int g_intval = 0xAABBCCDD;
char str_lower[] = "abcdefghijklmnopqrstuvwxyz";
char str_upper[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
char command[] = "echo you just ran a command";
int g_intval2 = 0x11223344;


int hidden()
{
  system(command);
}

int main(int argc, char** argv) 
{
  int i, len = 0;
  char buffer[BUF_LEN];

  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);

  while(1)
  {

    printf("----------------------------------\n");
    printf("str_lower(%p): %s\n", str_lower, str_lower);
    printf("str_upper(%p): %s\n", str_upper, str_upper);
    printf("command  (%p): %s\n", command, command);
    printf("g_intval (%p): %p\n", &g_intval, g_intval); 
    printf("g_intval2(%p): %p\n", &g_intval2, g_intval2); 
    printf("----------------------------------\n");

    printf("Give me something to say!\n");
    fflush(stdout);
    fgets(buffer, BUF_LEN, stdin);
    len = strlen(buffer);
    if (2 > len) { break; }
    printf(buffer);
  }

  exit(0);
  return 0;
}
