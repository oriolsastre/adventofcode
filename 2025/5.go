package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func day5() {
	testInput := false
	input := getInput(2025, 5, testInput, false)
	inputArray := input2LineArray(input, true)
	ranges, values := getRangeValues(inputArray)

	// 770
	fmt.Printf("Solució del 1er problema: %d\n", getFreshIngredients(ranges, values))
	minRanges := minRanges(ranges)

	// 357674099117260
	fmt.Printf("Solució del 2n problema: %d\n", cardRanges(minRanges))
}

func getRangeValues(input []string) ([][]int, []int) {
	var ranges [][]int
	var values []int
	for _, line := range input {
		valorIntermig := strings.Split(line, "-")
		if len(valorIntermig) == 2 {
			range1, _ := strconv.Atoi(valorIntermig[0])
			range2, _ := strconv.Atoi(valorIntermig[1])
			ranges = append(ranges, []int{range1, range2})
		} else {
			value, _ := strconv.Atoi(line)
			values = append(values, value)
		}
	}
	return ranges, values
}

func getFreshIngredients(ranges [][]int, ingredients []int) int {
	freshIngredients := 0
	for _, ingredient := range ingredients {
		for _, rang := range ranges {
			if rang[0] <= ingredient && rang[1] >= ingredient {
				freshIngredients++
				break
			}
		}
	}
	return freshIngredients
}

func minRanges(ranges [][]int) [][]int {
	var newMinRanges [][]int
	for i := range len(ranges) {
		combinable, index := rangCombinable(ranges[i], newMinRanges)
		if combinable {
			newMinRanges = combinaRang(ranges[i], index, newMinRanges)
			newMinRanges = minRanges(newMinRanges)
		} else {
			newMinRanges = append(newMinRanges, ranges[i])
		}
	}
	return newMinRanges
}

func rangCombinable(targetRang []int, ranges [][]int) (bool, int) {
	for i, rang := range ranges {
		overlap, _ := rangesOverlap(targetRang, rang)
		if overlap {
			return overlap, i
		}
	}
	return false, -1
}

func combinaRang(rang []int, index int, ranges [][]int) [][]int {
	overlap, combRang := rangesOverlap(rang, ranges[index])
	if overlap {
		ranges[index] = combRang
	}
	return ranges
}

func rangesOverlap(range1 []int, range2 []int) (bool, []int) {
	if len(range1) == 0 || len(range2) == 0 {
		return false, nil
	}
	if (range1[0] >= range2[0] && range1[0] <= range2[1]) ||
		(range2[0] >= range1[0] && range2[0] <= range1[1]) {
		newRange := []int{int(math.Min(float64(range1[0]), float64(range2[0]))), int(math.Max(float64(range1[1]), float64(range2[1])))}
		return true, newRange
	}
	return false, nil
}

func cardRanges(ranges [][]int) int {
	card := 0
	for _, rang := range ranges {
		if len(rang) >= 2 {
			card += rang[1] - rang[0] + 1
		}
	}
	return card
}
