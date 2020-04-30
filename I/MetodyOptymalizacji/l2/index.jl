# *********************************************
# Author: Adrian Mucha
# Szukanie informacji w rozproszonej chmurze
# *********************************************


using JuMP
using GLPK

function cloud(T::Vector{Float64}, q::Array{Int,2}, verbose = true)
    #  n - liczba zadan
    #  k - liczba serwerów
    #  Tj - czas przeszukiwania serwera j
    #  qij - czy i'ta cecha znajduje się na j'tym serwerze
    # verbose - true, to kominikaty solvera na konsole 		
	
    # wybor solvera
    model = Model(GLPK.Optimizer) # GLPK
	# model = Model(Cbc.Optimizer) # Cbc the solver for mixed integer programming
	
	n, k = size(q)
	Cechy = 1:n
	Serwery = 1:k

	println("cechy", Cechy)
	println("serwery", Serwery)

	@variable(model, x[Serwery], Bin)
	
	# minimalizacja sumy czasów dostępów do serwerów
	@objective(model, Min, sum(T[j] * x[j] for j in Serwery))
	
	# dostęp do każdej cechy w conajmniej jednym wybranym serwerze
	for i in Cechy
		@constraint(model, sum(x[j] * q[i,j] for j in Serwery) >= 1)
	end
	
	print(model) # drukuj model
    # rozwiaz egzemplarz
	if verbose
		optimize!(model)		
	else
		set_silent(model)
		optimize!(model)
		unset_silent(model)
	end

	status = termination_status(model)

	if status == MOI.OPTIMAL
		 return status, objective_value(model), value.(x)
	 else
		 return status, nothing, nothing
	 end
end

# czasy przeszukiwania j'tego serwera
T = [1.0, 2.0, 3.0]

# znajdowanie się cechy i'tej w j'tym serwerze
q = [
    1 0 1;
    0 0 1;
	0 1 0;
	0 1 0;
]


(status, fcelu, serwery) = cloud(T, q, true)

if status == MOI.OPTIMAL
    println("funkcja celu: ", fcelu)
    println("Które serwery: ", serwery)
else
    println("Status: ", status)
end
