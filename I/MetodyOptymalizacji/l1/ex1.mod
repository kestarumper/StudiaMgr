param n, integer, >= 1;

set range:= {1..n};

param A{i in range, j in range}:=1/(i+j-1);

param b{i in range} := sum{j in range} 1/(i+j-1);
param c{i in range} := b[i];

var x{i in range} >= 0;

minimize Cost: sum{i in range} x[i] * c[i];

s.t. w1{i in range} : sum{j in range} x[j]*A[i, j]=b[i];

solve;

display x;
display (sqrt(sum{i in range} (x[i] - 1) ^ 2) / sqrt(n));

data;

param n := 8;
end;