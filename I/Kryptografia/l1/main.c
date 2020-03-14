#include <stdlib.h>
#include <stdio.h>

#define MAX 344
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

int prediction(int j, unsigned int t[])
{
    int n = (j - 31) % 344;
    int m = (j - 3) % 344;
    int k = j % 344;

    unsigned int result = (t[n] + t[m]) % RAND_MAX;
    if (result < 0)
        result += RAND_MAX;

    t[k] = result;

    printf("PREDICTION: t[%d] = t[%d] + t[%d]\n", k, n, m);
    return result;
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

    unsigned int tab[MAX];
    unsigned int tab2[MAX];
    for (j = 0; j < 31; j++)
    {
        r1 = rand();
        r2 = myrand();

        tab[j] = r1;
        tab2[j] = r1 + 1;

        printf("r[%d] = r[%d] + r[%d] | %d / %d\n", _i - 1 % 344, (_i - 1 + 313) % 344, (_i - 1 + 341) % 344, r1, r2);
    }

    for (int k = 0; k < nloops; k++)
    {
        unsigned int prediction_1 = prediction(j, tab);
        unsigned int prediction_2 = prediction(j++, tab2);
        unsigned int next_1 = rand();
        printf("TEST: %d == %d == %d\n", next_1, prediction_1, prediction_2);
    }

    exit(EXIT_SUCCESS);
}
