# Lista 1 - Wybór lidera

**Adrian Mucha 236526**

## Zadanie 2

Histogramy przedstawiają rozkład empiryczny zmiennej losowej _L_ oznaczającej wybór lidera w _k-tym_ slocie dla obu scenariuszy.
![Example histogram](<histogram_n=1000_s=10000_v=(2,0.0).svg>)
_Znana liczba węzłów `n = 1000`_

![Example histogram](<histogram_n=2_s=10000_v=(3,1000.0).svg>)
_Znane górne ograniczenie na liczbę węzłów `n = 2, u = 1000`_

![Example histogram](<histogram_n=500_s=10000_v=(3,1000.0).svg>)
_Znane górne ograniczenie na liczbę węzłów `n = u / 2, u = 1000`_

![Example histogram](<histogram_n=1000_s=10000_v=(3,1000.0).svg>)
_Znane górne ograniczenie na liczbę węzłów `n = u, u = 1000`_

Powtarzając wielokrotnie doświadczenie (`samples = 10000`) otrzymujemy zbieżne wyniki.

Zmiennej losowa pochodzi z **rozkładu geometrycznego**, który opisuje prawdopodobieństwo otrzymania pierwszego sukcesu w k-tej próbie (k-tym slocie), czyli wyboru lidera.

W przypadku scenariusza drugiego możemy zauważyć, że numer rundy w którym zostanie wybrany lider (wartość oczekiwana) nie przekracza stałej `e` jeżeli każdy węzeł będzie nadawał z prawdopodobieństwem `1/n` (_Lemat 2_).

Dodatkowo, z każdym kolejnym slotem wzrasta nasze prawdopodobieństwo na sukces w wybraniu lidera w pierwszych `t` slotach (_Lemat 3_).

Jeżeli chodzi o scenariusz trzeci, to rozważane przypadki cechowały się różnymi stopniami powodzenia. Najlepiej radził sobie w przypadku tylko dwóch węzłów. Wraz ze wzrostem liczby węzłów spadało prawdopodobieństwo na wybór w początkowych rundach.

## Zadanie 3

Wartość oczekiwaną obliczono jako średnią arytmetyczną otrzymanych wyników (numer slotu w którym wybrano lidera).

| n    | EX                 | VarX                   |
| ---- | ------------------ | ---------------------- |
| 100  | 2.6855685568556855 | VarX=4.477873749971255 |
| 1000 | 2.6743674367436743 | VarX=4.526709916716245 |

_EX_ dla zmiennej losowej _L_ o rozkładnie _Geo_ jest równa _EX = 1/p_, natomiast wariancja wynosi _Var[L] = (1 - p) / p<sup>2</sup>_. Mamy _E[L] = 1/p < e = 2.71..._ oraz _Var[L] = 4.53_ co potwierdza słuszność otrzymanych wyników.

## Zadanie 4

W scenariuszu trzecim, w którym podzielono sloty na rundy obliczono prawdopodobieństwo wyboru lidera w jednej rundzie w następujący sposób. _Pr = ilość eksperymentów / ilość rund_ co daje nam miarę sukcesu wyboru lidera w jednej rundzie. Dokonano pomiarów i otrzymano następujące wyniki, które potwierdzają tezę twierdzenia zaprezentowanego na wykładzie.

| _n_  | _u_  | _λ_                |
| ---- | ---- | ------------------ |
| 2    | 100  | 0.804634695848085  |
| 50   | 100  | 0.7357268981753973 |
| 100  | 100  | 0.6350819255683984 |
| 2    | 1000 | 0.808996035919424  |
| 500  | 1000 | 0.7045230379033395 |
| 1000 | 1000 | 0.5785363031530228 |

Jak można zauważyć, wraz ze wzrostem `n`, które zbliża się ku ograniczeniu górnemu `u`, λ maleje i zbiega do wartości ≈ _0.579_, której nie przekracza.
