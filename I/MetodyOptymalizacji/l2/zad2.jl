# *******************************************************
# Author: Adrian Mucha
# Optymalny zestaw podprogramow do obliczenia
# zadanych funkcji skladajacych sie na caly program
# z ograniczeniem pamieci i minimalizacja czasu wykonania
# *******************************************************


using JuMP
using GLPK

struct SubProgram
    name::Tuple{Int, Int}
    r::Int
    t::Int
end

function zad2(P::Matrix{SubProgram}, I::Vector{Int}, M::Int, verbose = true)
    # P - biblioteka podprogramow
    # I - pozdbior funkcji do obliczenia
    # M - górne ograniczenie na pamięć
    # verbose - true, to kominikaty solvera na konsole	
	
    # wybor solvera
    model = Model(GLPK.Optimizer) # GLPK
	# model = Model(Cbc.Optimizer) # Cbc the solver for mixed integer programming
	
	m, n = size(P)
	Programs = 1:m
	SubPrograms = 1:n

    # Które podprogramy wybrać do obliczenia funkcji
	@variable(model, x[Programs, SubPrograms], Bin)
	
	# minimalizacja sumy czasu wykonania
	@objective(model, Min, sum(P[i,j].t * x[i,j] for i in Programs, j in SubPrograms))
	
	# wybrane podprogramy nie przekraczają łącznie ograniczeń pamięci
    @constraint(model, sum(P[i,j].r * x[i,j] for i in Programs, j in SubPrograms) <= M)
    
    # uwzględniaj tylko zlecone funkcje (jeden podprogram na zleconą funkcję)
    for i in I
        @constraint(model, sum(x[i,j] for j in SubPrograms) == 1)
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

m = 3
n = 4

M = 10
I = [1,3]

function subprogramFactory(i::Int, j::Int)
    mem = i * j
    time = Int(floor(100 / mem))
    return SubProgram((i, j), mem, time)
end

# Podprogramy
P = [subprogramFactory(i, j) for i in 1:m, j in 1:n]

(status, fcelu, subprograms) = zad2(P, I, M, true)

function getSubprograms(xs)
    m, n = size(xs)
    subprograms = []
    for i in 1:m
        for j in 1:n
            if xs[i, j] > 0
                push!(subprograms, (i, j))
            end
        end
    end
    return subprograms
end

if status == MOI.OPTIMAL
    subprogramIndexes = getSubprograms(subprograms)
    subprogramInstances = map(i -> P[i[1], i[2]], subprogramIndexes)
    memTotal = reduce(+, map(p -> p.r, subprogramInstances); init=0)
    println("Wybrane podprogramy: ", subprograms)
    println("Program P, sklada sie z nastepujacych funkcji: ", subprogramInstances)
    println("Zużyta pamięć: ", memTotal, "b")
    println("Czas wykonania programu P: ", fcelu, "ms")
else
    println("Status: ", status)
end
