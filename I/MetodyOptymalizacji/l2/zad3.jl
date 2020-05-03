# *********************************************
# Author: Pawel Zielinski
# Danych jest m zadan i n maszyn oraz
# czasy wykonania i-tego zadania na j-tej maszynie
# i=1,..,m, j=1,...,n.
# Kazde zadanie musi byc wykonane najpierw na maszynie 1 potem na 2
# i tak do n.
# Podac harmonogram wykonania wszystkich zadan tak aby czas 
# zakonczenia calego procesu byl najmniejszy 
# *********************************************

using JuMP
# using CPLEX 
# using GLPK
using Cbc



function jobshop(d::Matrix{Int};
	             verbose = true)
    (m, n) = size(d)
	
#  m - liczba zadan
#  n - liczba maszyn
#  d - macierz mxn zawierajaca czasy wykonania i-tego zadania na j-tej maszynie
# verbose - true, to kominikaty solvera na konsole 


    B = sum(d) # duza liczba wraz z inicjalizacja
	
 # wybor solvera
 # model = Model(CPLEX.Optimizer) # CPLEX		
#  model = Model(GLPK.Optimizer) # GLPK
    model = Model(Cbc.Optimizer) # Cbc the solver for mixed integer programming
  
    Task = 1:m
    Machine = 1:n
    Precedence = [(j, i, k) for j in Machine, i in Task, k in Task if i < k]
	
	#  zmienne moment rozpoczecia i-tego zadania na j-tej maszynie
	@variable(model, t[Task,Machine] >= 0) 
	# zmienna czas zakonczenia wykonawania wszystkich zadan - makespan 
	@variable(model, ms >= 0)
	
	# zmienne pomocnicze 
	# potrzebne przy zamienia ograniczen zasobowych
	@variable(model, y[Precedence], Bin) 
	
	# minimalizacja czasu zakonczenia wszystkich zadan
	@objective(model,Min, ms) 
	
	
  # moment rozpoczecia i-tego zadania na j+1-szej maszynie 
  # musi >= od momentu zakonczenia i-tego zadania na j-tej maszynie   
	for i in Task, j in Machine
	  if j < n
			@constraint(model, t[i,j + 1] >= t[i,j] + d[i,j])
			 # t_ij>=t_kj+d_kj lub t_kj>=t_ij+d_ij 
		end
	end
	
	
  # ograniczenia zosobowe tj,. tylko jedno zadanie wykonywane jest
  # w danym momencie na j-tej maszynie 
	for (j, i, k) in Precedence 
	  @constraint(model, t[i,j] - t[k,j] + B * y[(j, i, k)]         >= d[k,j])                
	  @constraint(model, t[k,j] - t[i,j] + B * (1 - y[(j, i, k)])   >= d[i,j])                
    end
	# ms rowna sie czas zakonczenia wszystkich zadan na ostatniej maszynie	
	for i in Task
		 @constraint(model, t[i,n] + d[i,n] <= ms)
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
	
	

end # jobshop


a = [3,9,9,4,6,6,7]		# P1
b = [3,3,8,8,10,3,10]	# P2
c = [2,8,5,4,3,1,3]		# P3

# czasy wykonia i-tego zadania na j-tej maszynie 
d =  [a b c]       

println(d)
(status, makespan, czasy) = jobshop(d)

function getPermutation(m)
	return sortperm(Array(m[:,1]))
end


if status == MOI.OPTIMAL
	println("makespan: ", makespan)
    println("czasy rozpoczecia zadan: ", czasy)
	println("kolejność zadań: ", getPermutation(czasy))
else
    println("Status: ", status)
end