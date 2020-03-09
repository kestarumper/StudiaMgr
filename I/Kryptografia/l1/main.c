#include <stdlib.h>
#include <stdio.h>

#define MAX 1000
#define multiplier 16807LL

int r[MAX];
int _i;
void mysrand(int seed)
{
    r[0] = seed;
    for (_i = 1; _i < 31; _i++)
    {
        r[_i] = (multiplier * r[_i - 1]) % RAND_MAX;
        if (r[_i] < 0)
        {
            r[_i] += RAND_MAX;
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
    r[_i % 344] = r[(_i + 313) % 344] + r[(_i + 341) % 344];
    unsigned int val = r[_i % 344];
    _i = (_i + 1) % 344;
    return val >> 1;
}

int main(int argc, char *argv[])
{
    int j, r1, r2, r3, r4, nloops, seed;

    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <seed> <nloops>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    seed = atoi(argv[1]);
    nloops = atoi(argv[2]);

    srand(seed);
    mysrand(seed);

    int tab[60];
    printf("seed: %d\n", seed);
    for (j = 0; j < nloops; j++)
    {
        r1 = rand();
        tab[j % 60] = r1;
        r2 = myrand();
        printf("r[%d] = r[%d] + r[%d] | %d / %d\n", _i - 1 % 344, (_i - 1 + 313) % 344, (_i - 1 + 341) % 344, r1, r2);
        // printf("rand=%d | myrand=%d\n", r1, r2);
    }

    int prediction_1 = (tab[0] + tab[28]) % RAND_MAX;
    if (prediction_1 < 0)
        prediction_1 += RAND_MAX;

    int prediction_2 = (tab[1] + tab[29]) % RAND_MAX;
    if (prediction_2 < 0)
        prediction_2 += RAND_MAX;

    int next_1 = rand();
    tab[j++ % 60] = next_1;

    int next_2 = rand();
    tab[j++ % 60] = next_2;

    printf("TEST: %d == %d\n", prediction_1, next_1);
    printf("TEST: %d == %d\n", prediction_2, next_2);

    exit(EXIT_SUCCESS);
}
