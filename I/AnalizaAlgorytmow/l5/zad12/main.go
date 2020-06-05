package main

import (
	"container/list"
	"fmt"
	"math"
)

type Item struct {
	state       []int
	permutation []int
	steps       int
}

func copyArray(src []int) []int {
	dst := make([]int, len(src))
	copy(dst, src)
	return dst
}

func getStateID(state []int) int {
	n := len(state)
	index := 0
	for i := n - 1; i >= 0; i-- {
		index += state[i] * int(math.Pow(float64(n+1), float64(n-i-1)))
	}
	return index
}

func nextState(state []int) []int {
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

	carry := 1
	for i := 0; i < n; i++ {
		state[i] = (state[i] + carry) % (n + 1)
		if state[i] == 0 {
			carry = 1
		} else {
			break
		}
	}

	return state
}

func findMaxSteps(arr []int) int {
	max := arr[0]
	for _, v := range arr {
		if max < v {
			max = v
		}
	}
	return max
}

func isStabilized(state []int) bool {
	for i := 0; i < len(state)-1; i++ {
		if state[i] != state[i+1] {
			return false
		}
	}
	return true
}

func processorAction(procID int, result []int) {
	n := len(result)
	if procID == 0 {
		if result[0] == result[n-1] {
			result[0] = (result[n-1] + 1) % (n + 1)
		}
	} else {
		if result[procID] != result[procID-1] {
			result[procID] = result[procID-1]
		}
	}
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

func factorial(number int) int {
	result := 1
	for i := 2; i <= number; i++ {
		result *= i
	}
	return result
}

func makeRange(min, max int) []int {
	a := make([]int, max-min+1)
	for i := range a {
		a[i] = min + i
	}
	return a
}

func buildPermutations(n int) [][]int {
	orig := makeRange(0, n-1)
	list := make([][]int, factorial(n))
	i := 0
	for p := make([]int, len(orig)); p[0] < len(p); nextPerm(p) {
		list[i] = getPerm(orig, p)
		i++
	}
	return list
}

func areStatesEqual(a, b []int) bool {
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func processState(originalState, visitedStates []int, permutations [][]int, steps, nProcesors int) {
	queue := list.New()
	for _, permutation := range permutations {
		queue.PushBack(Item{copyArray(originalState), permutation, steps})
	}

	for queue.Len() > 0 {
		d := queue.Front()
		data := d.Value.(Item)

		// foreach permutation
		step := data.steps
		state := data.state
		flag := true
		for _, procesorID := range data.permutation {
			if isStabilized(state) {
				markVisited(originalState, visitedStates, step)
				flag = false
				break
			} else if !areStatesEqual(state, originalState) && isVisited(state, visitedStates) {
				uid := getStateID(state)
				markVisited(originalState, visitedStates, step+visitedStates[uid])
				flag = false
				break
			}

			// mutate processors
			oldState := copyArray(state)
			processorAction(procesorID, state)
			if !areStatesEqual(oldState, state) {
				// go deeper
				step++
			}
		}

		if flag {
			// generate new rounds based on calculated state
			for _, permutation := range permutations {
				queue.PushBack(Item{copyArray(state), permutation, step})
			}
		}

		queue.Remove(d) // Dequeue
	}
}

func markVisited(state []int, visitedStates []int, value int) {
	uuid := getStateID(state)
	visitedStates[uuid] = int(math.Max(float64(visitedStates[uuid]), float64(value)))
}

func isVisited(state []int, visitedStates []int) bool {
	uuid := getStateID(state)
	result := visitedStates[uuid] != -1
	return result
}

func main() {
	n := 4

	numberOfStates := int(math.Pow(float64(n+1), float64(n))) // (n+1)^n

	visitedStates := make([]int, numberOfStates)
	for i := range visitedStates {
		visitedStates[i] = -1
	}

	// generate all possible permutations of launching processors in any order
	permutations := buildPermutations(n)
	for state := make([]int, n); state != nil; state = nextState(state) {
		processState(copyArray(state), visitedStates, permutations, 0, n)
	}

	fmt.Println("Found longest path:", findMaxSteps(visitedStates))
}
