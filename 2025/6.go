package main

import (
	"fmt"
	"strconv"
	"strings"
)

func day6() {
	testInput := false
	input := getInput(2025, 6, testInput, false)
	inputArray := input2LineArray(input)
	inputMatrix := inputArray2Matrix(inputArray)

	// 5977759036837
	fmt.Printf("Solució del 1er problema: %d\n", resolProblema(inputMatrix))

}

func inputArray2Matrix(input []string) [][]string {
	var matrix [][]string
	for _, line := range input {
		matrixLine := strings.Split(line, " ")
		var cleanMatrixLine []string
		for _, char := range matrixLine {
			char = strings.TrimSpace(char)
			if len(char) > 0 {
				cleanMatrixLine = append(cleanMatrixLine, char)
			}
		}
		matrix = append(matrix, cleanMatrixLine)
	}
	return invertMatrixStr(matrix)
}

func resolProblema(matriu [][]string) int {
	sumaTotal := 0
	for _, problema := range matriu {
		factorInicial, _ := strconv.Atoi(problema[0])
		sumProblema := factorInicial
		operand := problema[len(problema)-1]
	forFactor:
		for _, factor := range problema[1 : len(problema)-1] {
			num, _ := strconv.Atoi(factor)
			switch operand {
			case "+":
				sumProblema += num
			case "*":
				sumProblema *= num
				if sumProblema == 0 {
					break forFactor
				}
			}
		}
		sumaTotal += sumProblema
	}
	return sumaTotal
}
