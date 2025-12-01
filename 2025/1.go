package main

import (
	"fmt"
	"strconv"
)

func day1() {
	input := getInput(2025, 1, false)
	inputArray := input2LineArray(input)

	count := 0
	dial := 50

	for _, line := range inputArray {
		if len(line) > 0 {
			direccio, valor := splitInstr(line)
			instruction(&dial, valor, direccio)
			if dial == 0 {
				count++
			}
		}
	}
	// 1139
	fmt.Printf("Solució primer problema: %d", count)
}

func splitInstr(instr string) (int8, int) {
	var factor int8
	if instr[0] == 'L' {
		factor = -1
	} else if instr[0] == 'R' {
		factor = 1
	}

	valor, err := strconv.Atoi(instr[1:])
	if err != nil {
		panic(err)
	}

	return factor, valor
}

func instruction(inici *int, valor int, direccio int8) {
	*inici = (*inici + (int(direccio) * valor)) % 100
	if *inici < 0 {
		*inici += 100
	}
}
