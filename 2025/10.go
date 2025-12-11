package main

import (
	"fmt"
	"math"
	"slices"
	"strconv"
)

func day10() {
	testInput := false
	input := getInput(2025, 10, testInput, false)
	inputArray := input2LineArray(input, true)
	machines := inputArray2Machines(inputArray)

	indicatorMinButtons, joltageMinButtons := minButtons(machines)

	// 509
	fmt.Printf("Solució del 1er problema: %d\n", indicatorMinButtons)
	//
	fmt.Printf("Solució del 2n problema: %d\n", joltageMinButtons)
}

func minButtons(machines []Machine) (int, int) {
	combCache := CombCache{}

	indicatorMinButtons := 0
	joltageMinButtons := 0
	for _, machine := range machines {
		nButtons := len(machine.buttons)
		binComb := combinations(2, nButtons, &combCache)

		indicatorMinButtons += minIndicatorMachine(machine, binComb)
	}

	return indicatorMinButtons, joltageMinButtons

}

func minIndicatorMachine(machine Machine, combinations []Bin) int {
	for _, comb := range combinations {
		result := 0
		pos := binaryOnes(comb.n)
		for _, p := range pos {
			result ^= buttonToBinInt(machine.buttons[p])
		}
		if result == int(machine.indicator) {
			return comb.w
		}
	}
	return 0
}
func buttonToBinInt(button Button) int {
	bin := 0
	for _, b := range button {
		bin += int(math.Pow(2, float64(b)))
	}
	return bin
}
func combinations(base int, power int, cache *CombCache) []Bin {
	if _, ok := (*cache)[power]; !ok {
		(*cache)[power] = map[int][]Bin{}
	}
	if combs, ok := (*cache)[power][base]; ok {
		return combs
	}
	var combinations []Bin
	max := int(math.Pow(float64(base), float64(power)))
	for n := 1; n < max; n++ {
		var bin Bin
		bin.n = n
		bin.w = nWeight(n, base)
		bin.b = base
		bin.d = nDigits(n, base)
		combinations = append(combinations, bin)
	}
	slices.SortFunc(combinations, func(a Bin, b Bin) int {
		return a.w - b.w
	})
	if _, ok := (*cache)[power][base]; !ok {
		(*cache)[power][base] = combinations
	}
	return combinations
}

func nWeight(n int, base int) int {
	if base == 2 {
		return binaryWeigth(n)
	}
	weigth := 0
	fmt.Println(n, ",", base)
	nBase := strconv.FormatInt(int64(n), base)
	for _, char := range nBase {
		x, _ := strconv.Atoi(string(char))
		weigth += x
	}
	return weigth
}
func nDigits(n int, base int) []int {
	digits := []int{}
	nBase := strconv.FormatInt(int64(n), base)
	for i := range len(nBase) {
		char := nBase[len(nBase)-i-1]
		x, _ := strconv.Atoi(string(char))
		digits = append(digits, x)
	}
	return digits
}

func binaryWeigth(bin int) int {
	weigth := 0
	for bin > 0 {
		weigth += bin & 1
		bin >>= 1
	}
	return weigth
}
func binaryOnes(bin int) []int {
	var ones []int
	for i := 0; bin > 0; i++ {
		if bin&1 == 1 {
			ones = append(ones, i)
		}
		bin >>= 1
	}
	return ones
}

// Input processing
func inputArray2Machines(inputArray []string) []Machine {
	var machines []Machine
	for _, line := range inputArray {
		machine := inputLine2Machine(line)
		machines = append(machines, machine)
	}
	return machines
}
func inputLine2Machine(line string) Machine {
	var machine Machine
	lineArray := inputLineSplit(line, " ")
	indicatorS := lineArray[0]
	joltageS := lineArray[len(lineArray)-1]
	buttonsS := lineArray[1 : len(lineArray)-1]

	machine.size = len(indicatorS) - 2
	machine.indicatorS = indicatorS[1 : len(indicatorS)-1]
	machine.indicator = indicatorSToIndicator(indicatorS)
	machine.buttons = buttonStoButtons(buttonsS)
	machine.Joltage = joltageStoJoltage(joltageS)

	return machine
}

// Machine processing
func indicatorSToIndicator(indicatorS string) Indicator {
	var indicator Indicator
	indicatorS = indicatorS[1 : len(indicatorS)-1]
	for i, char := range indicatorS {
		base := 0
		if char == '#' {
			base = 1
		}
		pow := i
		indicator += Indicator(base * int(math.Pow(2, float64(pow))))
	}
	return indicator
}
func buttonStoButtons(buttonsS []string) []Button {
	var buttons []Button
	for _, buttonS := range buttonsS {
		bS := inputLineSplit(buttonS[1:len(buttonS)-1], ",")
		var button Button
		button = arrayStoArrayInt(bS)
		buttons = append(buttons, button)
	}
	return buttons
}
func joltageStoJoltage(joltageS string) Joltage {
	var joltage Joltage
	joltage = arrayStoArrayInt(inputLineSplit(joltageS[1:len(joltageS)-1], ","))
	return joltage
}
func arrayStoArrayInt(array []string) []int {
	var arrayInt []int
	for _, n := range array {
		num, _ := strconv.Atoi(n)
		arrayInt = append(arrayInt, num)
	}
	return arrayInt
}

type Indicator int
type Button []int
type Joltage []int

type Machine struct {
	size       int
	indicator  Indicator
	indicatorS string
	buttons    []Button
	Joltage    Joltage
}

type Bin struct {
	n int
	w int
	b int
	d []int
}
type CombCache map[int]map[int][]Bin
