// -------------------------------------------------------------- -*- C++ -*-
// File: ./examples/src/cpp/color.cpp
// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5724-Y48 5724-Y49 5724-Y54 5724-Y55 5725-A06 5725-A29
// Copyright IBM Corporation 1990, 2014. All Rights Reserved.
//
// Note to U.S. Government Users Restricted Rights:
// Use, duplication or disclosure restricted by GSA ADP Schedule
// Contract with IBM Corp.
// --------------------------------------------------------------------------

/* ------------------------------------------------------------

Problem Description
-------------------

The problem involves choosing colors for the countries on a map in
such a way that at most four colors (blue, white, yellow, green) are
used and no neighboring countries are the same color. In this exercise,
you will find a solution for a map coloring problem with six countries:
Belgium, Denmark, France, Germany, Luxembourg, and the Netherlands.

------------------------------------------------------------ */
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

/*
Feasible Solution
Belgium:     yellow
Denmark:     blue
France:      blue
Germany:     white
Luxembourg:  green
Netherlands: blue
*/
