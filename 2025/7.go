package main

import "fmt"

func day7() {
	testInput := false
	input := getInput(2025, 7, testInput, false)
	inputArray := input2LineArray(input)

	mapa := Mapa{mapa: inputArray, x: len(inputArray[0]), y: len(inputArray)}

	// 1600
	fmt.Printf("Solució del 1er problema: %d\n", beamMapa(&mapa))
}

func startBeam(mapa *Mapa) int {
	var start int
	for i, char := range mapa.mapa[0] {
		if char == 'S' {
			start = i
			break
		}
	}
	return start
}

func beamMapa(mapa *Mapa) int {
	beamSplitCount := 0
	beamStart := startBeam(mapa)
	beams := []int{beamStart}
	for i := range len(mapa.mapa) - 1 {
		var newBeams []int
		for _, beam := range beams {
			switch mapa.mapa[i+1][beam] {
			case '.':
				newBeams = append(newBeams, beam)
			case '^':
				beamSplitCount++
				if inMapaX(beam-1, mapa) {
					newBeams = append(newBeams, beam-1)
				}
				if inMapaX(beam+1, mapa) {
					newBeams = append(newBeams, beam+1)
				}
			}
		}
		beams = removeDuplicateInt(newBeams)
	}
	return beamSplitCount
}
