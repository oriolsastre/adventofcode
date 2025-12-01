package main

import (
	"fmt"
	"strconv"
)

func day1() {
	testInput := false
	input := getInput(2025, 1, testInput, false)
	inputArray := input2LineArray(input)

	count := 0
	count2 := 0
	dial := 50

	for _, line := range inputArray {
		if len(line) > 0 {
			direccio, valor := splitInstr(line)
			instruction(&dial, valor, direccio, &count2)
			if dial == 0 {
				count++
			}
		}
	}
	if testInput {
		fmt.Println("Usant input d'exemple")
	}
	// 1139
	fmt.Printf("Solució primer problema: %d\n", count)

	// 6684
	fmt.Printf("Solució segon problema: %d\n", count2)
}

func splitInstr(instr string) (int8, int) {
	var factor int8
	switch instr[0] {
	case 'L':
		factor = -1
	case 'R':
		factor = 1
	}

	valor, err := strconv.Atoi(instr[1:])
	if err != nil {
		panic(err)
	}

	return factor, valor
}

func instruction(dial *int, valor int, direccio int8, count2 *int) {
	// Sumem les voltes de mes
	*count2 += (valor / 100)
	valor %= 100

	inici := *dial
	final := (inici + (int(direccio) * valor))

	if final == 0 {
		// Caiem al zero exacte, sumem 1
		*count2++
	} else if final > 99 {
		// 1 tick per cada volta positiva feta
		final -= 100
		*count2++
	} else if final < 0 {
		// 1 tick per cada volta negativa feta
		final += 100
		// Anar a negatiu desde 0 no és un tick
		if inici != 0 {
			*count2++
		}
	}
	*dial = final % 100
}
