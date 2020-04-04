set Cities;                         # travel endpoints
set CaravanType;                   # types of caravans
set E within Cities cross Cities;   # travel paths E_1 x E_2

# param Substitutions{CaravanType, CaravanType} >= 0;

param CostMultipliers{CaravanType} >= 0;

param Demands{Cities, CaravanType} integer, >= 0;   # Demand for each city and type
param Supplies{Cities, CaravanType} integer, >= 0;  # Supply for each city and type
param Distances{E}, integer >= 0;                 # Distances between city pairs

# Check that supply are enough for demand
check   sum{city in Cities, type in CaravanType} Demands[city, type] <=
        sum{city in Cities, type in CaravanType} Supplies[city, type]
;

var x{E, CaravanType} integer, >= 0;

minimize Cost:
        sum{(src, dest) in E, type in CaravanType}
                CostMultipliers[type] * Distances[src, dest] * x[src, dest, type];

# s.t. w2{dest in Cities, type in CaravanType}:
#         Demands[dest, type] - (sum{src in Cities} x[src, dest, type]) == 0;

s.t. w1{dest in Cities}:
        Demands[dest, 'Vip'] - (
                sum{src in Cities} x[src, dest, 'Vip'] - (
                        Demands[dest, 'Standard'] - sum{src in Cities} x[src, dest, 'Standard']
                )
        ) == 0;

s.t. standard_demand{dest in Cities}:
        Demands[dest, 'Standard'] - sum{src in Cities} x[src, dest, 'Standard'] >= 0;

s.t. suppliers{src in Cities, type in CaravanType}:
        Supplies[src, type] - (sum{dest in Cities} x[src, dest, type]) >= 0;

solve;

for {type in CaravanType, (src, dest) in E}
{
   for {{0}: x[src, dest, type] != 0} {
        printf "[%s --> %s] %d x %s\n", src, dest, x[src, dest, type],type;
   }
}
for {type in CaravanType} {
    printf "Total moved %s: %d\n", type, sum{(src, dest) in E} x[src, dest, type];
}
display Cost;

data;

set Cities := Warszawa Gdansk Szczecin Wroclaw Krakow Berlin Rostok Lipsk Praga Brno Bratyslawa Koszyce Budapeszt;
set CaravanType := Standard Vip;

# param Substitutions: Standard Vip :=
#         Standard    1   0
#         Vip         1   1
# ;

param CostMultipliers := Standard 1.0 Vip 1.15;

param Demands: Standard Vip :=
        Warszawa 0 4
        Gdansk 20 0
        Szczecin 0 0
        Wroclaw 8 0
        Krakow 0 8
        Berlin 16 4
        Rostok 2 0
        Lipsk 3 0
        Praga 0 4
        Brno 9 0
        Bratyslawa 4 0
        Koszyce 4 0
        Budapeszt 8 0
;

param Supplies : Standard Vip :=
        Warszawa 14 0
        Gdansk 0 2
        Szczecin 12 4
        Wroclaw 0 10
        Krakow 10 0
        Berlin 0 0
        Rostok 0 4
        Lipsk 0 10
        Praga 10 0
        Brno 0 2
        Bratyslawa 0 8
        Koszyce 0 4
        Budapeszt 0 4
;

param : E : Distances :=
        Berlin Berlin 0
        Bratyslawa Bratyslawa 0
        Brno Brno 0
        Gdansk Gdansk 0
        Koszyce Koszyce 0
        Krakow Krakow 0
        Lipsk Lipsk 0
        Praga Praga 0
        Rostok Rostok 0
        Szczecin Szczecin 0
        Warszawa Warszawa 0
        Wroclaw Wroclaw 0
        Budapeszt Budapeszt 0
        Berlin Bratyslawa 553
        Bratyslawa Berlin 553
        Berlin Brno 433
        Brno Berlin 433
        Berlin Budapeszt 689
        Budapeszt Berlin 689
        Berlin Koszyce 697
        Koszyce Berlin 697
        Berlin Lipsk 149
        Lipsk Berlin 149
        Berlin Praga 282
        Praga Berlin 282
        Berlin Rostok 195
        Rostok Berlin 195
        Bratyslawa Budapeszt 162
        Budapeszt Bratyslawa 162
        Bratyslawa Koszyce 313
        Koszyce Bratyslawa 313
        Brno Bratyslawa 122
        Bratyslawa Brno 122
        Brno Budapeszt 261
        Budapeszt Brno 261
        Brno Koszyce 344
        Koszyce Brno 344
        Gdansk Berlin 403
        Berlin Gdansk 403
        Gdansk Bratyslawa 699
        Bratyslawa Gdansk 699
        Gdansk Brno 591
        Brno Gdansk 591
        Gdansk Budapeszt 764
        Budapeszt Gdansk 764
        Gdansk Koszyce 652
        Koszyce Gdansk 652
        Gdansk Krakow 486
        Krakow Gdansk 486
        Gdansk Lipsk 539
        Lipsk Gdansk 539
        Gdansk Praga 556
        Praga Gdansk 556
        Gdansk Rostok 427
        Rostok Gdansk 427
        Gdansk Szczecin 288
        Szczecin Gdansk 288
        Gdansk Wroclaw 377
        Wroclaw Gdansk 377
        Koszyce Budapeszt 214
        Budapeszt Koszyce 214
        Krakow Berlin 531
        Berlin Krakow 531
        Krakow Bratyslawa 297
        Bratyslawa Krakow 297
        Krakow Brno 259
        Brno Krakow 259
        Krakow Budapeszt 293
        Budapeszt Krakow 293
        Krakow Koszyce 177
        Koszyce Krakow 177
        Krakow Lipsk 552
        Lipsk Krakow 552
        Krakow Praga 394
        Praga Krakow 394
        Krakow Rostok 698
        Rostok Krakow 698
        Lipsk Bratyslawa 492
        Bratyslawa Lipsk 492
        Lipsk Brno 384
        Brno Lipsk 384
        Lipsk Budapeszt 645
        Budapeszt Lipsk 645
        Lipsk Koszyce 699
        Koszyce Lipsk 699
        Lipsk Praga 203
        Praga Lipsk 203
        Praga Bratyslawa 290
        Bratyslawa Praga 290
        Praga Brno 185
        Brno Praga 185
        Praga Budapeszt 443
        Budapeszt Praga 443
        Praga Koszyce 516
        Koszyce Praga 516
        Rostok Bratyslawa 748
        Bratyslawa Rostok 748
        Rostok Brno 627
        Brno Rostok 627
        Rostok Budapeszt 880
        Budapeszt Rostok 880
        Rostok Koszyce 871
        Koszyce Rostok 871
        Rostok Lipsk 306
        Lipsk Rostok 306
        Rostok Praga 474
        Praga Rostok 474
        Szczecin Berlin 127
        Berlin Szczecin 127
        Szczecin Bratyslawa 615
        Bratyslawa Szczecin 615
        Szczecin Brno 493
        Brno Szczecin 493
        Szczecin Budapeszt 733
        Budapeszt Szczecin 733
        Szczecin Koszyce 703
        Koszyce Szczecin 703
        Szczecin Krakow 527
        Krakow Szczecin 527
        Szczecin Lipsk 276
        Lipsk Szczecin 276
        Szczecin Praga 373
        Praga Szczecin 373
        Szczecin Rostok 177
        Rostok Szczecin 177
        Szczecin Wroclaw 309
        Wroclaw Szczecin 309
        Warszawa Berlin 518
        Berlin Warszawa 518
        Warszawa Bratyslawa 533
        Bratyslawa Warszawa 533
        Warszawa Brno 459
        Brno Warszawa 459
        Warszawa Budapeszt 545
        Budapeszt Warszawa 545
        Warszawa Gdansk 284
        Gdansk Warszawa 284
        Warszawa Koszyce 391
        Koszyce Warszawa 391
        Warszawa Krakow 252
        Krakow Warszawa 252
        Warszawa Lipsk 603
        Lipsk Warszawa 603
        Warszawa Praga 518
        Praga Warszawa 518
        Warszawa Rostok 629
        Rostok Warszawa 629
        Warszawa Szczecin 454
        Szczecin Warszawa 454
        Warszawa Wroclaw 301
        Wroclaw Warszawa 301
        Wroclaw Berlin 295
        Berlin Wroclaw 295
        Wroclaw Bratyslawa 330
        Bratyslawa Wroclaw 330
        Wroclaw Brno 215
        Brno Wroclaw 215
        Wroclaw Budapeszt 427
        Budapeszt Wroclaw 427
        Wroclaw Koszyce 402
        Koszyce Wroclaw 402
        Wroclaw Krakow 236
        Krakow Wroclaw 236
        Wroclaw Lipsk 326
        Lipsk Wroclaw 326
        Wroclaw Praga 217
        Praga Wroclaw 217
        Wroclaw Rostok 470
        Rostok Wroclaw 470
;

end;