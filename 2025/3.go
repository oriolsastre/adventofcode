package main

import (
	"fmt"
	"strconv"
	"strings"
)

func day3() {
	testInput := false
	input := getInput(2025, 3, testInput, false)
	inputArray := input2LineArray(input)
	joltageSum := 0
	for _, line := range inputArray {
		joltage := findBiggestJoltage(line)
		joltageSum += joltage
	}
	// 17100
	fmt.Printf("Solució del 1er problema: %d\n", joltageSum)
}

func findBiggestJoltage(bank string) int {
	bank = strings.TrimSpace(bank)
	var bigL int
	var bigR int
	var indexL int
	for i := range len(bank) - 1 {
		bankIint, _ := strconv.Atoi(string(bank[i]))
		if bankIint > bigL {
			bigL = bankIint
			indexL = i
		}
		if bigL == 9 {
			break
		}
	}
	for j := range len(bank) - indexL - 1 {
		bankJint, _ := strconv.Atoi(string(bank[len(bank)-j-1]))
		if bankJint > bigR {
			bigR = bankJint
		}
		if bigR == 9 {
			break
		}
	}
	return bigL*10 + bigR
}
