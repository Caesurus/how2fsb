// gcc -m32 level4.c -o level4

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_LEN 64
int denyFlag = 0;

int hidden()
{
  puts("Wow, you got it!");
  system("cat ./flag.txt");
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
