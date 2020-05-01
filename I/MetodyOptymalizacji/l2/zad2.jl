# *********************************************
# Author: Adrian Mucha
# Szukanie informacji w rozproszonej chmurze
# *********************************************


using JuMP
using GLPK

struct SubProgram
    name::Tuple{Int, Int}
    r::Int
    t::Float64
end

function zad2(P::Array{SubProgram, 2}, I::Vector{Int}, M::Int, verbose = true)
    #  n - liczba zadan
    #  k - liczba serwerów
    #  Tj - czas przeszukiwania serwera j
    #  qij - czy i'ta cecha znajduje się na j'tym serwerze
    # verbose - true, to kominikaty solvera na konsole	
	
    # wybor solvera
    model = Model(GLPK.Optimizer) # GLPK
	# model = Model(Cbc.Optimizer) # Cbc the solver for mixed integer programming
	
	m, n = size(P)
	Programs = 1:m
	SubPrograms = 1:n

	println("Programy range", Programs)
	println("SubProgramy range", SubPrograms)

    # Które podprogramy wybrać do obliczenia funkcji
	@variable(model, x[Programs, SubPrograms], Bin)
	
	# minimalizacja sumy czasu wykonania
	@objective(model, Min, sum(P[i,j].t * x[i,j] for i in Programs, j in SubPrograms))
	
	# dostęp do każdej cechy w conajmniej jednym wybranym serwerze
    @constraint(model, sum(P[i,j].r * x[i,j] for i in Programs, j in SubPrograms) <= M)

    for i in Programs
        @constraint(model, sum(x[i,j] for j in SubPrograms) >= 1)
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
    time = 1 / mem * 10
    return SubProgram((i, j), mem, time)
end

# Podprogramy
P = [subprogramFactory(i, j) for i in 1:m, j in 1:n]

(status, fcelu, subprograms) = zad2(P, I, M, true)

function listSubprograms(xs)
    m, n = size(xs)
    for i in 1:m
        for j in 1:n
            if xs[i, j] > 0
                println("P", i, j)
            end
        end
    end
end

if status == MOI.OPTIMAL
    println("funkcja celu: ", fcelu)
    println("Które serwery: ", subprograms)
    listSubprograms(subprograms)
else
    println("Status: ", status)
end
