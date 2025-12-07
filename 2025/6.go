package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

// !\\ L'última línia de l'input no la llegeixo bé i li haig d'afegir un espai en blanc final manulament.
func day6() {
	testInput := false
	input := getInput(2025, 6, testInput, false)
	inputArray := input2LineArray(input)
	problemes := inputArray2Problemes(inputArray)

	// 5977759036837
	fmt.Printf("Solució del 1er problema: %d\n", resolProblema(problemes))
	// 9630000828442
	fmt.Printf("Solució del 2n problema: %d\n", resolProblema(converteixMatriu(problemes)))

}

func inputArray2Problemes(input []string) [][]string {
	var problemes [][]string
	liniaOperands := input[len(input)-1]
	i := 0
	problema := 0
	for i < len(liniaOperands)-1 {
		mida := 1
		if esOperand(liniaOperands[i]) {
			j := i + 1
			for true {
				if j >= len(liniaOperands) || esOperand(liniaOperands[j]) {
					break
				}
				mida++
				j++
			}
			// fmt.Printf("Operand %s, mida %d\n", string(liniaOperands[i]), mida)
			problemes = append(problemes, []string{})
			for _, linia := range input {
				problemes[problema] = append(problemes[problema], linia[i:i+mida-1])
			}
			problema++
		}
		i += mida
	}
	return problemes
}
func esOperand(byte byte) bool {
	return string(byte) == "+" || string(byte) == "*"
}

func resolProblema(matriu [][]string) int {
	sumaTotal := 0
	for _, problema := range matriu {
		factorInicial, _ := strconv.Atoi(strings.TrimSpace(problema[0]))
		sumProblema := factorInicial
		operand := strings.TrimSpace(problema[len(problema)-1])
	forFactor:
		for _, factor := range problema[1 : len(problema)-1] {
			num, _ := strconv.Atoi(strings.TrimSpace(factor))
			// fmt.Printf("Factor: %d (%s), ", num, factor)
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

func converteixMatriu(matriu [][]string) [][]string {
	var convMatriu [][]string
	for i, problema := range matriu {
		convMatriu = append(convMatriu, []string{})
		mida := len(problema[len(problema)-1])
		for n := range mida {
			p := mida - n - 1
			factor := factorDeProblema(problema, p)
			convMatriu[i] = append(convMatriu[i], strconv.Itoa(factor))
		}
		operand := strings.TrimSpace(problema[len(problema)-1])
		convMatriu[i] = append(convMatriu[i], operand)
	}
	return convMatriu
}

func factorDeProblema(problema []string, pos int) int {
	valors := []int{}
	nFactors := len(problema) - 1
	for i := range nFactors {
		num, err := strconv.Atoi(string(problema[i][pos]))
		if err == nil {
			valors = append(valors, num)
		}
	}
	factor := 0
	for i, num := range valors {
		factor += num * int(math.Pow10(len(valors)-i-1))
	}
	return factor
}
