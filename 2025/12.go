package main

import (
	"fmt"
	"strconv"
	"strings"
)

func day12() {
	testInput := false
	input := getInput(2025, 12, testInput, false)
	inputArray := input2LineArray(input, true)
	presents, regions := parseInput(inputArray)

	// 599
	fmt.Printf("La solució del 1er problema es: %d\n", regionsAptes(presents, regions))

}

func regionsAptes(presents []Present, regions []Region) int {
	regionsAptes := 0
	for _, regio := range regions {
		if regioPresents(regio, presents) {
			regionsAptes++
		}
	}
	return regionsAptes
}

func regioPresents(regio Region, presents []Present) bool {
	presentsRegio := presentsPerRegio(regio, presents)
	areaRegio := regio.x * regio.y
	areaPresents := 0
	for _, present := range presentsRegio {
		areaPresents += present.x * present.y
	}
	// Solució incompleta.
	// Només miro si caben sense encaixar
	if areaRegio < areaPresents {
		return false
	}
	return true
}

func presentsPerRegio(regio Region, presents []Present) []Present {
	presentsRegio := []Present{}
	for index, n := range regio.presents {
		for range n {
			presentsRegio = append(presentsRegio, presents[index])
		}
	}
	return presentsRegio
}

func parseInput(inputArray []string) ([]Present, []Region) {
	var presents []Present
	var regions []Region
	for i := 0; i < len(inputArray); {
		line := inputArray[i]
		// Capçalera de regal
		if len(line) == 2 {
			present := Present{[]string{}, 0, 0}
			j := 1
			for {
				if i+j >= len(inputArray) {
					break
				}
				lineJ := inputArray[i+j]
				_, err := strconv.Atoi(string(lineJ[0]))
				if err == nil {
					break
				}
				present.present = append(present.present, lineJ)
				j++
			}
			present.x = len(present.present[0])
			present.y = len(present.present)
			presents = append(presents, present)
			i += j - 1
		} else {
			regioArr := strings.Split(line, ":")
			regio := Region{0, 0, []int{}}
			sizeArr := strings.Split(regioArr[0], "x")
			regio.x, _ = strconv.Atoi(sizeArr[0])
			regio.y, _ = strconv.Atoi(sizeArr[1])
			presentArr := strings.Split(regioArr[1], " ")
			for _, presentS := range presentArr {
				presentInt, err := strconv.Atoi(presentS)
				if err == nil {
					regio.presents = append(regio.presents, presentInt)
				}
			}
			regions = append(regions, regio)
		}
		i++
	}
	return presents, regions
}

type Present struct {
	present []string
	x       int
	y       int
}

type Region struct {
	x        int
	y        int
	presents []int
}
