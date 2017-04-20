// gcc -m32 level5.c -o level5

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_LEN 64
int denyFlag = 0;
char NOPE_STR[] = "echo NOPE, nice try";

int hidden()
{
  puts("HAHAHA\n");
  system(NOPE_STR);
}

int main(int argc, char** argv) 
{
    char buffer[BUF_LEN];

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    printf("Give me something to say!\n");
    fflush(stdout);
    fgets(buffer, BUF_LEN, stdin);
    printf(buffer);

    exit(0);
}
