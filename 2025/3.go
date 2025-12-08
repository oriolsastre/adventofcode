package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func day3() {
	testInput := false
	input := getInput(2025, 3, testInput, false)
	inputArray := input2LineArray(input, true)
	joltageSum2 := 0
	joltageSum12 := 0
	for _, line := range inputArray {
		joltage2 := findBiggestJoltage(line, 2)
		joltageSum2 += joltage2
		joltage12 := findBiggestJoltage(line, 12)
		joltageSum12 += joltage12
	}
	// 17100
	fmt.Printf("Solució del 1er problema: %d\n", joltageSum2)
	// 170418192256861
	fmt.Printf("Solució del 2n problema: %d\n", joltageSum12)
}

func findBiggestJoltage(bank string, batteries int) int {
	bank = strings.TrimSpace(bank)
	var joltage = 0
	leftIndex := 0
	for battery := range batteries {
		var maxJoltage int
		for i := leftIndex; i < len(bank)-(batteries-battery-1); i++ {
			batteryJoltage, _ := strconv.Atoi(string(bank[i]))
			if batteryJoltage > maxJoltage {
				maxJoltage = batteryJoltage
				leftIndex = i + 1
			}
			if maxJoltage == 9 {
				break
			}
		}
		joltage += maxJoltage * int(math.Pow10(batteries-battery-1))
	}

	return joltage
}
