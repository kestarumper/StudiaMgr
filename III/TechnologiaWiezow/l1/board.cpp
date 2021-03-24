/* ------------------------------------------------------------

Zadanie 30 pkt. (kamień)
-------------------

Rozłupać kamień o wadze 40 kilogramów na cztery kawałki, tak aby stosując te
kawałki jako odważniki, możliwe było odważenie każdej z czterdziestu całkowitych
wag 1, 2, . . . , 40.
Napisz program który znajduje wagi tych czterech kawałków kamienia.

------------------------------------------------------------ */

// This define is here to "fix imports" for my VSCode intelisense
#define ILOUSESTL
#include <ilcp/cp.h>

bool canGet(IloInt pos, IloInt x, IloInt y)
{
  return x >= 0 && x < 5 && y >= 0 && y < 5;
}

IloIntExpr getStarSum(IloEnv env, IloIntVarArray &arr, IloInt cx, IloInt cy, IloInt size)
{
  IloIntExpr sum(env);
  for (IloInt i = -1; i < 2; i++)
  {
    IloInt pos = 5 * (cy + i) + cx;
    if (canGet(pos, cx, cy + i))
    {
      sum += arr[pos];
    }
  }
  for (IloInt j = -1; j < 2; j+=2)
  {
    IloInt pos = 5 * cy + (cx + j);
    if (canGet(pos, cx + j, cy))
    {
      sum += arr[pos];
    }
  }
  return sum;
}

int main(int, const char *[])
{
  IloEnv env;

  const IloInt initial[] = {
      1, 1, 1, 1, 1,
      1, 1, 0, 1, 1,
      1, 0, 0, 0, 1,
      1, 1, 0, 1, 1,
      1, 1, 1, 1, 1};
  try
  {
    IloModel model(env);

    // Params
    IloInt boardSize = 25;
    IloInt lowerWeightBound = 0;
    IloInt upperWeightBound = 1;

    // Variables
    IloIntVarArray board(env, boardSize, lowerWeightBound, upperWeightBound);

    for (IloInt cy = 0; cy < 5; cy++)
    {
      for (IloInt cx = 0; cx < 5; cx++)
      {
        model.add((getStarSum(env, board, cx, cy, boardSize) % 2) == initial[cy * 5 + cx]);
      }
    }

    IloCP cp(model);
    if (cp.solve())
    {
      cp.out() << std::endl
               << cp.getStatus() << " Solution" << std::endl;
      for (IloInt i = 0; i < boardSize; i++)
      {
        if(cp.getValue(board[i]) == 1) {
          cp.out() << "Pole\t" << i << std::endl;
        }
      }
    }
  }
  catch (IloException &ex)
  {
    env.out() << "Error: " << ex << std::endl;
  }
  env.end();
  return 0;
}
