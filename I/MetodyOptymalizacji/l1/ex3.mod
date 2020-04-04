set Surowce;
set Produkty;
set ProduktyPodstawowe within Produkty;

param Profit{Produkty} >= 0;

param Ceny{Surowce} >= 0;
param Minimum{Surowce} >= 0;
param Maximum{Surowce} >= 0;

param Odpady{Surowce, Produkty} >= 0;
param CenaNiszczOdpad{Surowce, Produkty} >= 0;

var kup{Surowce} >= 0;
var przeznacz_surowiec{Surowce, Produkty} >=0; # zuzyj x surowca i na produkt j

# zniszcz odpad i powstały z produktu j
var zniszcz_odpad{Surowce, ProduktyPodstawowe} >= 0;

# zuzyj x odpadu powstałego z i na produkt j
var przeznacz_odpad{Surowce, ProduktyPodstawowe} >= 0;

maximize zysk:
    (
        (sum{j in ProduktyPodstawowe}
            (sum{i in Surowce}
                (przeznacz_surowiec[i,j] * (1 - Odpady[i, j]))
            ) * Profit[j]
        ) +
            (((sum{i in Surowce} przeznacz_odpad[i, 'A']) + przeznacz_surowiec[1, 'C']) * Profit['C']) +
            (((sum{i in Surowce} przeznacz_odpad[i, 'B']) + przeznacz_surowiec[2, 'D']) * Profit['D'])
    ) -
    (
        sum{i in Surowce} kup[i] * Ceny[i] +
        (sum{i in Surowce, j in ProduktyPodstawowe}
            zniszcz_odpad[i, j] * CenaNiszczOdpad[i, j])
    )
;

# Inne
s.t. min_max_surowiec{i in Surowce}:
    Minimum[i] <= kup[i] <= Maximum[i];

s.t. nie_wiecej_niz_masz{i in Surowce}:
    sum{j in Produkty} przeznacz_surowiec[i, j] <= kup[i];

s.t. limit_odpadu{i in Surowce, j in ProduktyPodstawowe}:
    przeznacz_odpad[i,j] <= przeznacz_surowiec[i,j] * Odpady[i,j];

s.t. brak_odpadow{i in Surowce, j in ProduktyPodstawowe}:
    przeznacz_surowiec[i,j] * Odpady[i,j] ==
    zniszcz_odpad[i,j] + przeznacz_odpad[i,j];

# Specyfikacja A
s.t. specyfikacja_A_1:
    przeznacz_surowiec[1, 'A'] >= 0.2 * sum{i in Surowce} przeznacz_surowiec[i, 'A'];
s.t. specyfikacja_A_2:
    przeznacz_surowiec[2, 'A'] >= 0.4 * sum{i in Surowce} przeznacz_surowiec[i, 'A'];
s.t. specyfikacja_A_3:
    przeznacz_surowiec[3, 'A'] <= 0.1 * sum{i in Surowce} przeznacz_surowiec[i, 'A'];

# Specyfikacja B
s.t. specyfikacja_B_1:
    przeznacz_surowiec[1, 'B'] >= 0.1 * sum{i in Surowce} przeznacz_surowiec[i, 'B'];
s.t. specyfikacja_B_3:
    przeznacz_surowiec[3, 'B'] <= 0.3 * sum{i in Surowce} przeznacz_surowiec[i, 'B'];

# Specyfikacja C
s.t. specyfikacja_C_1:
    przeznacz_surowiec[1, 'C'] ==
    0.2 * (przeznacz_surowiec[1, 'C'] + sum{i in Surowce} przeznacz_odpad[i, 'A']);

# Specyfikacja D
s.t. specyfikacja_D_2:
    przeznacz_surowiec[2, 'D'] ==
    0.3 * (przeznacz_surowiec[2, 'D'] + sum{i in Surowce} przeznacz_odpad[i, 'B']);

solve;

display kup;
display przeznacz_surowiec;
display przeznacz_odpad;
display zniszcz_odpad;
display zysk;

data;

set Surowce := 1 2 3;
set Produkty := A B C D;
set ProduktyPodstawowe := A B;

# profit za kg
param Profit := A 3
                B 2.5
                C 0.6
                D 0.5
;

# cena za kg
param Ceny :=   1 2.1
                2 1.6
                3 1.0
;

param Minimum := 1 2000
                 2 3000
                 3 4000
;

param Maximum := 1 6000
                 2 5000
                 3 7000
;

param Odpady:   A     B     :=
            1   0.1   0.2
            2   0.2   0.2
            3   0.4   0.5
;

param CenaNiszczOdpad:  A     B     :=
                    1   0.1   0.05
                    2   0.1   0.05
                    3   0.2   0.40
;

end;