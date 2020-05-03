# *********************************************
# Author: Adrian Mucha
# Szukanie informacji w rozproszonej chmurze
# *********************************************


using JuMP
using GLPK

function zad3(n::Int, a::Vector, b::Vector, c::Vector, verbose = true)
    #  n - liczba zadan
    #  k - liczba serwerów
    #  Tj - czas przeszukiwania serwera j
    #  qij - czy i'ta cecha znajduje się na j'tym serwerze
    # verbose - true, to kominikaty solvera na konsole 		
	
    # wybor solvera
    model = Model(GLPK.Optimizer) # GLPK
	# model = Model(Cbc.Optimizer) # Cbc the solver for mixed integer programming
	
    Zadania = 1:n
    Procesory = 1:3

    # permutacje zadań
    @variable(model, 1 <= x[Zadania] <= n, Int)
    
    # rozpoczęcie zadań na osi oczasu
    @variable(model, 0 <= timeStart[Procesory, Zadania], Int)
    
	# minimalizacja czasu zakończenia ostatniego zadania 
    # @objective(model, Min, sum(x[i] for i in Zadania))
    @objective(model, Min, timeStart[3, n])
    
    
    # permutacja wykorzystuje wszystkie zadania
    # for i in Zadania
    #     @constraint(model, count(v -> (v == i), x) == 1)
    # end
	
    # zadania nie nachodzą na siebie
    for (j, t) in zip(Procesory, [a, b, c])
        for i in Zadania
            if i == length(Zadania)
                break
            end
            # @constraint(model, timeStart[j, x[i]] + t[x[i]] <= timeStart[j, x[i+1]])
            @constraint(model, timeStart[j, i] + t[x[i]] <= timeStart[j, i+1])
        end
    end
    
    # nie rozpoczynaj zadania nim sie nie zakonczy na poprzednim procesorze
    for (j, t) in zip(Procesory, [a, b, c])
        if j == length(Procesory)
            break
        end
        for i in Zadania
            # @constraint(model, timeStart[j, x[i]] + t[x[i]] <= timeStart[j + 1, x[i]])
            @constraint(model, timeStart[j, i] + t[x[i]] <= timeStart[j + 1, i])
        end
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

# ile zadań
n = 4

a = [10, 12, 30, 30]
b = [15, 13, 12, 30]
c = [35, 20, 14, 30]

(status, fcelu, permutacja) = zad3(n, a, b, c, true)

if status == MOI.OPTIMAL
    println("funkcja celu: ", fcelu)
    println("Które permutacja: ", permutacja)
else
    println("Status: ", status)
end
