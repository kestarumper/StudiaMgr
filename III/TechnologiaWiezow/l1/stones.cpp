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

const char *Names[] = {"blue", "white", "yellow", "green"};

int main(int, const char *[])
{
  IloEnv env;
  try
  {
    IloModel model(env);

    // Params
    IloInt numberOfStones = 4;
    IloInt lowerWeightBound = 1;
    IloInt upperWeightBound = 40;

    // Variables
    IloIntVarArray stones(env, numberOfStones, lowerWeightBound, upperWeightBound);

    // Constraints
    for (IloInt weight = lowerWeightBound; weight <= upperWeightBound; weight++)
    {
      IloIntVarArray coefs(env, numberOfStones, -1, 1); // coefs in [-1, 0, 1]
      IloIntExprArray partials(env);
      for (IloInt c = 0; c < numberOfStones; c++)
      {
        partials.add(stones[c] * coefs[c]); // stones[0] * coefs[0]
      }
      // stones[0] * coefs[0] + stones[1] * coefs[1] + ... = weight
      model.add(IloSum(partials) == weight);
    }

    IloCP cp(model);
    if (cp.solve())
    {
      cp.out() << std::endl
               << cp.getStatus() << " Solution" << std::endl;
      for (IloInt i = 0; i < numberOfStones; i++)
      {
        cp.out() << "Kamien " << i << ":\t" << cp.getValue(stones[i]) << std::endl;
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
