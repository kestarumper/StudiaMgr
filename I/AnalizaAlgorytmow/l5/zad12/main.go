package main

import (
	"fmt"
	"math"
	"sync"
	"time"
)

var GlobalMutex = &sync.Mutex{}

type Data struct {
	initialState []int
	state        []int
	steps        int
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

	end := true
	for _, v := range state {
		if v != n {
			end = false
			break
		}
	}

	if end {
		return nil
	}

	result := make([]int, n)
	copy(result, state)

	carry := 1
	for i := 0; i < n; i++ {
		result[i] = (result[i] + carry) % (n + 1)
		if result[i] == 0 {
			carry = 1
		} else {
			break
		}
	}

	return result
}

func maxSteps(arr []int) int {
	max := arr[0]
	for _, v := range arr {
		if max < v {
			max = v
		}
	}
	return max
}

func checkStabilization(state []int) bool {
	for i := 0; i < len(state)-1; i++ {
		if state[i] != state[i+1] {
			return false
		}
	}
	return true
}

func runProcesor(i int, state []int) []int {
	n := len(state)
	result := make([]int, n)
	copy(result, state)
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

func worker(in chan Data, next chan<- bool, checkedStates []int, nProcesors int, wg *sync.WaitGroup) {
	fmt.Println(">> WORKERK")
	defer wg.Done()

	var state []int
	var steps int

	for {
		select {
		case data := <-in:
			state = data.state
			steps = data.steps
			fmt.Println(">>", data)
		case <-time.After(1 * time.Second):
			fmt.Println("Self destruct <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			return
		}

		originalState := makeCopy(state)

		stabilized := checkStabilization(originalState)
		if stabilized {
			if steps == 0 {
				markVisited(originalState, checkedStates, 0)
			}
			continue
		}

		queue := make(chan Data)
		for procID := 0; procID < nProcesors; procID++ {
			state = runProcesor(procID, originalState)
			steps++

			if isVisited(state, checkedStates) {
				continue
			}

			stabilized = checkStabilization(state)
			if stabilized {
				markVisited(originalState, checkedStates, steps)
			} else {
				d := Data{originalState, state, steps}
				queue <- d
			}
		}
	}
}

func markVisited(state []int, checkedStates []int, value int) {
	GlobalMutex.Lock()
	uuid := stateUUID(state)
	checkedStates[uuid] = int(math.Max(float64(checkedStates[uuid]), float64(value)))
	GlobalMutex.Unlock()
}

func isVisited(state []int, checkedStates []int) bool {
	uuid := stateUUID(state)
	result := checkedStates[uuid] != -1
	return result
}

func main() {
	n := 3

	numberOfStates := int(math.Pow(float64(n+1), float64(n))) // (n+1)^n

	checkedStates := make([]int, numberOfStates)
	for i := range checkedStates {
		checkedStates[i] = -1
	}

	input := make(chan Data, n*numberOfStates+1)
	for state := make([]int, n); state != nil; state = incState(state) {
		input <- Data{state, state, 0}
	}

	next := make(chan bool, numberOfStates)

	var wg sync.WaitGroup
	for i := 0; i < n; i++ {
		wg.Add(1)
		go worker(input, next, checkedStates, n, &wg)
	}

	wg.Wait()
	fmt.Println("Longest path:", maxSteps(checkedStates))
}
