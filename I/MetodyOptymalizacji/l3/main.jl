# Autor - Adrian Mucha, 236526
# Metody optymalizacji - Lista 3
using JuMP
using GLPK
using LatexPrint

function readLineInts(file)
  return hcat(map(x -> parse(Int, x), split(readline(file)))...)
end

function readData(pathToFile)
  open(pathToFile) do file
    P = parse(Int, readline(file))
    result = []
    for p in 1:P
      m, n = readLineInts(file)
      costs = vcat([readLineInts(file) for i in 1:m]...)
      resources = vcat([readLineInts(file) for i in 1:m]...)
      capacity = readLineInts(file)
      push!(result, (p, m, n, costs, resources, capacity))
    end
    return result
  end
end

function solveIterativeModel(c, p, T, verbose = true)
  m, n = size(c)
  M = 1:m
  J = 1:n

  Machines = Array(M)
  Jobs = Array(J)
  F = [] # subgraph F ⊂ G

	for i in M
		for j in J
			@assert p[i, j] < T[i]
		end
	end

  graph = [(i, j) for i in M for j in J] # dense (complete, full) graph G

  iterCount = 0
  while length(Jobs) > 0
    model = Model(GLPK.Optimizer)
    @variable(model, x[M, J] >= 0)
    @objective(model, Min, sum(c[i, j] * x[i, j] for (i, j) in graph))
    for job in Jobs
      edges = [e for e in graph if e[2] == job] # edges that have endpoint in job node
      @constraint(model, sum(x[i, j] for (i, j) in edges) == 1)
    end
    for machine in Machines
      edges = [e for e in graph if e[1] == machine] # edges that start in machine node
      @constraint(model, sum(p[i, j] * x[i, j] for (i, j) in edges) <= T[machine])
    end

      # rozwiaz egzemplarz
  	if verbose
  		optimize!(model)
  	else
  		set_silent(model)
  		optimize!(model)
  		unset_silent(model)
  	end

  	status = termination_status(model)

	# println("SOLUTION")
	# println(solution)

	solution = value.(x)
	filter!(((i,j),) -> solution[i, j] != 0, graph) # remove every variable with x_ij = 0
	for i in M
		for j in Jobs
			if abs(solution[i, j] - 1.0) <= eps(Float64)
				push!(F, (i, j))
				filter!(job -> job != j, Jobs)
				T[i] -= p[i, j]
			end
		end
	end
	filter!(Machines) do i
		degree = length([e for e in graph if e[1] == i])
		!(degree == 1 || (degree == 2 && (sum([solution[i, j] for j in Jobs]) >= 1)))
	end
	iterCount += 1
  end
  return F, iterCount
end

println("")
filenames = ["gap$(i).txt" for i in 1:12]
table = []
for fname in filenames
	problems = readData("dataset/$(fname)")
	@show fname
	for problem in problems
	  p, m, n, costs, resources, capacity = problem

	  time = @elapsed F, iterCount = solveIterativeModel(deepcopy(costs), deepcopy(resources), deepcopy(capacity))

	  for i in 1:m
		  tasks = filter(x -> x[1] == i, F)
		  if length(tasks) > 0
			  resourceSum = sum(resources[x[1], x[2]] for x in tasks)
			  # println(i, " ", tasks, " ", resourceSum, " ", capacity[i], " ", resourceSum > 2 * capacity[i] ? "<===========" : "")
			  @assert resourceSum <= 2 * capacity[i] "< 2Ti dont hold"
		  end
	  end

	  resourceSums = [(i, capacity[i], sum(resources[x[1], x[2]] for x in F if x[1] == i), sum(resources[x[1], x[2]] for x in F if x[1] == i) / capacity[i]) for i in 1:m]

    # totalCost = mapreduce(((i, j),) -> costs[i, j], +, F)
	  # resourcesUsed = mapreduce(((i, j),) -> resources[i, j], +, F)
	  # totalCapacity = sum(capacity)
	  # ratio = resourcesUsed / totalCapacity
	  # avgResourcesUsed = resourcesUsed / length(capacity)
	  # avgCapacity = totalCapacity / length(capacity)
	  problemString = string("c", m, n, "-", p)

    maxRatio = -1
    maxResources = -1
    maxCapacity = -1
    for x in resourceSums
      (i, c, r, ratio) = x
      if maxRatio < ratio
        maxRatio = ratio
        maxResources = r
        maxCapacity = c
      end
    end

	  entry = (fname, problemString, iterCount, maxResources, maxCapacity, maxRatio, string(Int(round(time, digits=3) * 1000), "ms"))
	  @show entry
	  push!(table, entry)
	end
	println(repeat('-', 100))
end

table = vcat([hcat([i for i in row]...) for row in table]...)
tabular(table)
