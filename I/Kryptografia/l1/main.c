#include <stdlib.h>
#include <stdio.h>

#define MAX 1000
#define multiplier 16807LL
#define modulus 2147483647

int r[MAX];
int _i;
void mysrand(int seed)
{
    r[0] = seed;
    for (_i = 1; _i < 31; _i++)
    {
        r[_i] = (multiplier * r[_i - 1]) % modulus;
        if (r[_i] < 0)
        {
            r[_i] += modulus;
        }
    }
    for (_i = 31; _i < 34; _i++)
    {
        r[_i] = r[_i - 31];
    }
    for (_i = 34; _i < 344; _i++)
    {
        r[_i] = r[_i - 31] + r[_i - 3];
    }
}

int myrand()
{
    r[_i] = r[_i - 31] + r[_i - 3];
    return ((unsigned int)r[_i++]) >> 1;
}

int main(int argc, char *argv[])
{
    int j, r1, r2, nloops, seed;

    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <seed> <nloops>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    seed = atoi(argv[1]);
    nloops = atoi(argv[2]);

    srand(seed);
    mysrand(seed);

    printf("seed: %d\n", seed);
    for (j = 0; j < nloops; j++)
    {
        r1 = rand();
        r2 = myrand();
        printf("rand=%d | myrand=%d\n", r1, r2);
    }

    exit(EXIT_SUCCESS);
}