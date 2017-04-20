// gcc -m32 level3.c -o level3

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_LEN 64
int denyFlag = 0;

int main(int argc, char** argv) 
{
    char buffer[BUF_LEN];

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    printf("Give me something to say!\n");
    fflush(stdout);
    fgets(buffer, BUF_LEN, stdin);
    printf(buffer);

    if(0xCAFE == denyFlag)
    {
        puts("Wow, you got it!");
        system("cat ./flag.txt");   
    }
    else
    {
        puts("As my friend says,\"You get nothing! You lose! Good day, Sir!\"");
    }

    return 0;
}
