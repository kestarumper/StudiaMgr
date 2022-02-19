#define ILOUSESTL
#include <ilcp/cp.h>

int get(IloInt row, IloInt column, IloInt side)
{
  return row * 5 * 4 +
         column * 4 +
         side;
}

int main(int, const char *[])
{
  enum Side
  {
    RIGHT = 0,
    TOP = 1,
    LEFT = 2,
    BOTTOM = 3
  };

  IloEnv env;
  try
  {
    IloModel model(env);

    IloBoolVarArray tile(env, 5 * 5 * 4);

    // Wewnętrzne kafelki
    for (IloInt row = 1; row < 4; ++row)
    {
      for (IloInt column = 1; column < 4; ++column)
      {
        model.add(tile[get(row, column, Side::RIGHT)] == tile[get(row, column + 1, Side::LEFT)]);
        model.add(tile[get(row, column, Side::TOP)] == tile[get(row - 1, column, Side::BOTTOM)]);
        model.add(tile[get(row, column, Side::LEFT)] == tile[get(row, column - 1, Side::RIGHT)]);
        model.add(tile[get(row, column, Side::BOTTOM)] == tile[get(row + 1, column, Side::TOP)]);
      }
    }

    for (IloInt i = 1; i < 4; ++i)
    {
      model.add(tile[get(0, i, Side::RIGHT)] == tile[get(0, i + 1, Side::LEFT)]);
      model.add(tile[get(i, 0, Side::TOP)] == tile[get(i - 1, 0, Side::BOTTOM)]);
      model.add(tile[get(0, i, Side::LEFT)] == tile[get(0, i - 1, Side::RIGHT)]);
      model.add(tile[get(i, 0, Side::BOTTOM)] == tile[get(i + 1, 0, Side::TOP)]);

      model.add(tile[get(4, i, Side::RIGHT)] == tile[get(4, i + 1, Side::LEFT)]);
      model.add(tile[get(i, 4, Side::TOP)] == tile[get(i - 1, 4, Side::BOTTOM)]);
      model.add(tile[get(4, i, Side::LEFT)] == tile[get(4, i - 1, Side::RIGHT)]);
      model.add(tile[get(i, 4, Side::BOTTOM)] == tile[get(i + 1, 4, Side::TOP)]);
    }

    for (IloInt i = 0; i < 5; ++i)
    {
      model.add(tile[get(0, i, Side::TOP)] == 0);    // górny rząd
      model.add(tile[get(4, i, Side::BOTTOM)] == 0); // dolny rząd
      model.add(tile[get(i, 0, Side::LEFT)] == 0);   // lewy bok
      model.add(tile[get(i, 4, Side::RIGHT)] == 0);  // prawy bok
    }

    IloInt upperBoundary = 5;
    IloIntExprArray tileOne(env);
    IloIntExprArray tileTwo(env);
    IloIntExprArray tileThree(env);
    IloIntExprArray tileFour(env);
    IloIntExprArray tileFive(env);
    for (IloInt row = 0; row < 5; ++row)
    {
      for (IloInt column = 0; column < 5; ++column)
      {
        tileOne.add(
            tile[get(row, column, Side::RIGHT)] +
                tile[get(row, column, Side::TOP)] +
                tile[get(row, column, Side::LEFT)] +
                tile[get(row, column, Side::BOTTOM)] ==
            1);

        tileTwo.add(
            (tile[get(row, column, Side::RIGHT)] +
                 tile[get(row, column, Side::TOP)] +
                 tile[get(row, column, Side::LEFT)] +
                 tile[get(row, column, Side::BOTTOM)] ==
             2) *
            (tile[get(row, column, Side::RIGHT)] == tile[get(row, column, Side::LEFT)]));

        tileThree.add((tile[get(row, column, Side::RIGHT)] +
                           tile[get(row, column, Side::TOP)] +
                           tile[get(row, column, Side::LEFT)] +
                           tile[get(row, column, Side::BOTTOM)] ==
                       2) *
                      (tile[get(row, column, Side::RIGHT)] != tile[get(row, column, Side::LEFT)]));

        tileFour.add(tile[get(row, column, Side::RIGHT)] +
                         tile[get(row, column, Side::TOP)] +
                         tile[get(row, column, Side::LEFT)] +
                         tile[get(row, column, Side::BOTTOM)] ==
                     3);

        tileFive.add(tile[get(row, column, Side::RIGHT)] +
                         tile[get(row, column, Side::TOP)] +
                         tile[get(row, column, Side::LEFT)] +
                         tile[get(row, column, Side::BOTTOM)] ==
                     4);
      }
    }
    model.add(IloSum(tileOne) == upperBoundary);
    model.add(IloSum(tileTwo) == upperBoundary);
    model.add(IloSum(tileThree) == upperBoundary);
    model.add(IloSum(tileFour) == upperBoundary);
    model.add(IloSum(tileFive) == upperBoundary);

    IloCP cp(model);
    if (cp.solve())
    {
      cp.out() << cp.getStatus() << " Solution:" << std::endl;
      for (IloInt row = 0; row < 5; ++row)
      {
        for (IloInt column = 0; column < 5; ++column)
        {
          cp.out() << " " << (cp.getValue(tile[get(row, column, Side::TOP)]) == 1 ? "║" : " ") << " ";
        }
        cp.out() << std::endl;
        for (IloInt column = 0; column < 5; ++column)
        {
          cp.out() << (cp.getValue(tile[get(row, column, Side::LEFT)]) == 1 ? "═" : " ") << "█" << (cp.getValue(tile[get(row, column, Side::RIGHT)]) == 1 ? "═" : " ");
        }
        cp.out() << std::endl;
        for (IloInt column = 0; column < 5; ++column)
        {
          cp.out() << " " << (cp.getValue(tile[get(row, column, Side::BOTTOM)]) == 1 ? "║" : " ") << " ";
        }
        cp.out() << std::endl;
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
