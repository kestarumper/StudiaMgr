package main

import (
	"container/list"
	"fmt"
	"math"
)

type Data struct {
	state       []int
	permutation []int
	steps       int
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
		index += state[i] * int(math.Pow(float64(n+1), float64(n-i-1)))
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

func runProcesor(i int, result []int) {
	n := len(result)
	if i == 0 {
		if result[0] == result[n-1] {
			result[0] = (result[n-1] + 1) % (n + 1)
		}
	} else {
		if result[i] != result[i-1] {
			result[i] = result[i-1]
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

func generateAllPermutations(n int) [][]int {
	orig := makeRange(0, n-1)
	list := make([][]int, factorial(n))
	i := 0
	for p := make([]int, len(orig)); p[0] < len(p); nextPerm(p) {
		list[i] = getPerm(orig, p)
		i++
	}
	return list
}

func compareStates(a, b []int) bool {
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func worker(originalState, checkedStates []int, permutations [][]int, steps, nProcesors int) {
	// struktury Data wsadzamy do kolejki
	// wsadzamy je do struktury Data
	queue := list.New()
	for _, permutation := range permutations {
		queue.PushBack(Data{makeCopy(originalState), permutation, steps})
	}

	// dopoki kolejka nie jest pusta
	for queue.Len() > 0 {
		// zdejmij strukture Data
		d := queue.Front()
		data := d.Value.(Data)

		// dla kazdego elementu z rundy for [0, 2, 3, 1]
		newStep := data.steps
		newState := data.state
		flag := true
		for _, procesorID := range data.permutation {
			// sprawdz czy jest sukces lub czy jestes w znanym stanie
			if checkStabilization(newState) {
				// sprobuj wpisac dlugosc do listy odwiedzonych checkedStates[i] = max(checkedStates[i], length)
				markVisited(originalState, checkedStates, newStep)
				flag = false
				break
			} else if !compareStates(newState, originalState) && isVisited(newState, checkedStates) {
				uid := stateUUID(newState)
				markVisited(originalState, checkedStates, newStep+checkedStates[uid])
				flag = false
				break
			}
			// zmien wartosc procesorow
			oldState := makeCopy(newState)
			runProcesor(procesorID, newState)
			if !compareStates(oldState, newState) {
				// zwieksz glebokosc drzewa o jeden jesli stan sie zmienil
				newStep++
			}
		}

		if flag {
			// wygeneruj wszystkie rundy i wrzuc nowe Data do kolejki
			for _, permutation := range permutations {
				queue.PushBack(Data{makeCopy(newState), permutation, newStep})
			}
		}

		queue.Remove(d) // Dequeue
	}
}

func markVisited(state []int, checkedStates []int, value int) {
	uuid := stateUUID(state)
	checkedStates[uuid] = int(math.Max(float64(checkedStates[uuid]), float64(value)))
}

func isVisited(state []int, checkedStates []int) bool {
	uuid := stateUUID(state)
	result := checkedStates[uuid] != -1
	return result
}

func main() {
	n := 4

	numberOfStates := int(math.Pow(float64(n+1), float64(n))) // (n+1)^n

	checkedStates := make([]int, numberOfStates)
	for i := range checkedStates {
		checkedStates[i] = -1
	}

	// generujemy wszystkie mozlwie rundy (permutacje listy [0...n-1])
	permutations := generateAllPermutations(n)
	for state := make([]int, n); state != nil; state = incState(state) {
		worker(makeCopy(state), checkedStates, permutations, 0, n)
	}

	fmt.Println("Longest path:", maxSteps(checkedStates))
}
