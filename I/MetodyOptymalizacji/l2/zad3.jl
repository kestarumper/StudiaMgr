# *********************************************
# Danych jest m zadan oraz trzy procesory wraz z 
# czasami wykonania i-tego zadania na j-tym procesorze
# i=1,..,m, j=1,2,3.
# Kazde zadanie musi byc wykonane najpierw na procesorze 1 potem na 2, i na 3
# Podac permutacje zadan minimalizujacych Cmax
# oznaczajacy czas zakonczenia ostatniego zadania na trzecim procesorze
# *********************************************

using JuMP
using Cbc
using DataFrames, Gadfly
import Cairo, Fontconfig


function zad3(d::Matrix{Int}, verbose = true)
	#  m - liczba zadan
	#  n - liczba procesorów
	#  d - macierz mxn zawierajaca czasy wykonania i-tego zadania na j-tym procesorze
	# verbose - true, to kominikaty solvera na konsole 

    (m, n) = size(d)
    B = sum(d) # duza liczba, symulujaca coś niemożliwego (bardzo wysoki koszt)
	
    model = Model(Cbc.Optimizer) # Cbc, dla MIP
  
    Task = 1:m
    Procesor = 1:n
    Sequence = [(j, i, k) for j in Procesor, i in Task, k in Task if i < k]
	
	#  zmienne moment rozpoczecia i-tego zadania na j-tej procesorze
	@variable(model, t[Task, Procesor] >= 0, Int) 
	# zmienna czas zakonczenia wykonawania wszystkich zadan 
	@variable(model, cmax >= 0)
	
	# potrzebne przy zamienia ograniczen zasobowych
	@variable(model, x[Sequence], Bin) 
	
	# minimalizacja czasu zakonczenia wszystkich zadan
	@objective(model, Min, cmax) 
	
	# moment rozpoczecia i-tego zadania na j+1-szym procesorze
	# moze zaczac sie dopiero gdy i-te zadanie skonczy sie na j-tym
	for i in Task, j in Procesor
		if j < n
			@constraint(model, t[i, j + 1] >= t[i, j] + d[i, j])
		end
	end
	
	# ograniczenie zasobów, tylko jedno zadanie wykonywane jest
	# w danym momencie na j-tym procesorze 
	for (j, i, k) in Sequence 
		@constraint(model, t[i, j] - t[k, j] + B * x[(j, i, k)]         >= d[k, j])                
		@constraint(model, t[k, j] - t[i, j] + B * (1 - x[(j, i, k)])   >= d[i, j])                
	end
	
	# cmax jest ostatnim wykonanym zadaniem na trzecim procesorze
	for i in Task
		@constraint(model, t[i, n] + d[i, n] <= cmax)
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
		return status, objective_value(model), value.(t)
	else
		return status, nothing, nothing
	end
end

# czasy wykonania i-tego zadania na j-tym procesorze 
a = [3,9,9,4,6,6,7]		# P1
b = [3,3,8,8,10,3,10]	# P2
c = [2,8,5,4,3,1,3]		# P3
d =  [a b c]       

(status, cmax, czasy) = zad3(d, true)

function getPermutation(m)
	return sortperm(Array(m[:,1]))
end

if status == MOI.OPTIMAL
    println("czasy rozpoczecia zadan: ", czasy)
	println("kolejność zadań: ", getPermutation(czasy))
	println("Cmax: ", cmax)
else
    println("Status: ", status)
end

function gantt(czasy)
	lines = []
    for (j, col) in enumerate(eachcol(czasy))
        println(j, col)
		perm = sortperm(col)
		result = []
		for i in perm
			push!(result, (i, col[i], col[i] + d[i, j]))
        end
        println(result)
		push!(lines, result)
	end
	return lines
end

lines = gantt(Int.(ceil.(czasy)))

function printTask(task)
    (id, tstart, tend) = task
    duration = tend - tstart + 1
    for i in 1:duration
        print(id)
    end
end

function printEmpty(n)
    for i in 1:n
        print(" ")
    end
end

for line in lines
    printEmpty(line[1][2])
    for i in eachindex(line)
        if i < length(line)
            a = line[i]
            (id1, tstart1, tend1) = a
            b = line[i+1]
            (id2, tstart2, tend2) = b
            diff = tstart2 - tend1
            printTask(a)
            printEmpty(diff)
        end
    end
    printTask(line[length(line)])
    println("")
end
