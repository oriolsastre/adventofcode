package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func day5() {
	testInput := true
	input := getInput(2025, 5, testInput, false)
	inputArray := input2LineArray(input)
	ranges, values := getRangeValues(inputArray)

	// 770
	fmt.Printf("Solució del 1er problema: %d\n", getFreshIngredients(ranges, values))
	minRanges := minimizeRanges(ranges)
	for _, rang := range minRanges {
		fmt.Println(rang)
	}
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

func minimizeRanges(ranges [][]int) [][]int {
	var newRanges [][]int
	for i, rang := range ranges {
		set := len(newRanges) + 1

		if len(rang) == 2 {
			rang = append(rang, set)
		} else {
			set = rang[2]
		}
		for _, rang2 := range ranges[i+1:] {
			overlap, combRange := rangesOverlap(rang, rang2)
			if overlap {
				if len(rang2) == 2 {
					rang2 = append(rang2, set)
				} else {
					set = rang2[2]
				}
				rang = append(combRange, set)
			}
		}
		if len(newRanges) < set {
			newRanges = append(newRanges, rang)
		} else {
			_, combRange := rangesOverlap(newRanges[set-1], rang)
			newRanges[set-1] = combRange
		}
	}

	return newRanges

}

func rangesOverlap(range1 []int, range2 []int) (bool, []int) {
	if (range1[0] >= range2[0] && range1[0] <= range2[1]) ||
		(range2[0] >= range1[0] && range2[0] <= range1[1]) {
		newRange := []int{int(math.Min(float64(range1[0]), float64(range2[0]))), int(math.Max(float64(range1[1]), float64(range2[1])))}
		return true, newRange
	}
	return false, nil
}

type combiRange struct {
	ranges [][]int
	id     int
}
