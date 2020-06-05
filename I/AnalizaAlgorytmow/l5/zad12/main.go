package main

import (
	"fmt"
	"math"
)

type Data struct {
	state []int
	order []int
	id    int
}

func checkStabilization(state []int) bool {
	for i := 0; i < len(state)-1; i++ {
		if state[i] != state[i+1] {
			return false
		}
	}
	return true
}

func runProcesor(i int, arr []int) []int {
	n := len(arr)
	result := make([]int, n)
	copy(result, arr)
	if i == 0 {
		if result[0] == result[n-1] {
			result[0] = (result[n-1] + 1) % (n + 1)
		}
	} else {
		if result[i] != result[i-1] {
			result[i] = result[i-1]
		}
	}
	return result
}

func worker(in <-chan Data, out chan<- int, checkedStates []bool, statesStepsNumbers [][]int, nProcesors int) {
	for {
		dataPack := <-in

		inputState := dataPack.state
		order := dataPack.order
		id := dataPack.id

		steps := 0

		indexOrder := 0
		var beginState []int
		state := makeCopy(inputState)
		stabilized := checkStabilization(state)
		for !stabilized {
			if indexOrder == 0 {
				beginState = makeCopy(state)
			}

			state = runProcesor(order[indexOrder], state)

			indexOrder = (indexOrder + 1) % nProcesors
			if indexOrder == 0 {
				foundCycle := checkCycle(state, beginState)
				if foundCycle {
					break
				}
			}

			stabilized = checkStabilization(state)
			steps++
		}

		// calculates number of steps to get the success based on state and order of proccesses
		// get self stabilized without bumping into already seen example
		var stepsToStabilization int
		if checkStabilization(state) {
			stepsToStabilization = steps
		} else if isAlreadyChecked(state, checkedStates) { // bumped into already seen example
			if statesStepsNumbers[stateUUID(state)][id] == -1 { // already seen but cycle
				stepsToStabilization = -1
			} else { // already seen
				stepsToStabilization = steps + statesStepsNumbers[stateUUID(state)][id]
			}
		} else { // got cycled it's impossible to get self stabilized
			stepsToStabilization = -1
		}

		statesStepsNumbers[stateUUID(inputState)][id] = stepsToStabilization

		out <- 1
	}
}

func isAlreadyChecked(processorState []int, checkedStates []bool) bool {
	index := stateUUID(processorState)
	return checkedStates[index]
}

func checkCycle(a []int, b []int) bool {
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func makeCopy(src []int) []int {
	dst := make([]int, len(src))
	copy(dst, src)
	return dst
}

func stateUUID(state []int) int {
	n := len(state)
	index := 0
	for i := n - 1; i >= 0; i-- {
		index += state[i] * int(math.Pow(float64(n), float64(n-i-1)))
	}
	return index
}

func incState(state []int) []int {
	n := len(state)
	result := make([]int, n)
	copy(result, state)
	for i := 0; i < n; i++ {
		if result[i] < n {
			result[i]++
			return result
		} else if i < n-1 && result[i+1] < n {
			result[i] = 0
			result[i+1]++
			return result
		}
	}
	return nil
}

func factorial(number int) int {
	result := 1
	for i := 2; i <= number; i++ {
		result *= i
	}
	return result
}

func nextPerm(p []int) {
	for i := len(p) - 1; i >= 0; i-- {
		if i == 0 || p[i] < len(p)-i-1 {
			p[i]++
			return
		}
		p[i] = 0
	}
}

func getPerm(orig, p []int) []int {
	result := append([]int{}, orig...)
	for i, v := range p {
		result[i], result[i+v] = result[i+v], result[i]
	}
	return result
}

func max(arr [][]int) int {
	max := arr[0][0]
	for i := range arr {
		for j := range arr[i] {
			if max < arr[i][j] {
				max = arr[i][j]
			}
		}
	}
	return max
}

func main() {
	n := 4

	helper := make(chan int)
	defer close(helper)

	numberOfStates := int(math.Pow(float64(n+1), float64(n)))
	numberOfOrders := factorial(n)

	checkedStates := make([]bool, numberOfStates)
	statesStepsNumbers := make([][]int, numberOfStates)

	for i := 0; i < numberOfStates; i++ {
		statesStepsNumbers[i] = make([]int, numberOfOrders)
	}

	input := make(chan Data, numberOfStates)

	for i := 0; i < n; i++ {
		go worker(input, helper, checkedStates, statesStepsNumbers, n)
	}

	i := 0
	for state := make([]int, n); state != nil; state = incState(state) {
		initialOrder := []int{0, 1, 2, 3}
		id := 0
		for p := make([]int, len(initialOrder)); p[0] < len(p); nextPerm(p) {
			order := getPerm(initialOrder, p)
			fmt.Println("STATE:", state, "ORDER:", order)
			input <- Data{state, order, id}
			id++
		}

		// wait for all goroutines to stop
		goRoutinesFinished := 0
	label:
		for {
			select {
			case finished := <-helper:
				goRoutinesFinished += finished
			default:
				if goRoutinesFinished == numberOfOrders {
					break label
				}
			}
		}

		// check that goroutine was checked
		checkedStates[stateUUID(state)] = true
		// fmt.Println(initialState)
		i++
	}
	fmt.Println("Longest path:", max(statesStepsNumbers))
}
