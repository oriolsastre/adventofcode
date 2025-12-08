package main

import "fmt"

func day7() {
	testInput := false
	input := getInput(2025, 7, testInput, false)
	inputArray := input2LineArray(input, true)

	mapa := Mapa{mapa: inputArray, x: len(inputArray[0]), y: len(inputArray)}

	beamCount, beams := beamMapa(&mapa)

	// 1600
	fmt.Printf("Solució del 1er problema: %d\n", beamCount)
	// 8632253783011
	fmt.Printf("Solució del 2n problema: %d\n", sumaCamins(beams))
}

func startBeam(mapa *Mapa) Beam {
	var start Beam
	for i, char := range mapa.mapa[0] {
		if char == 'S' {
			start = Beam{index: i, camins: 1}
			break
		}
	}
	return start
}

func beamMapa(mapa *Mapa) (int, []Beam) {
	beamSplitCount := 0
	beamStart := startBeam(mapa)
	beams := []Beam{beamStart}
	for i := range len(mapa.mapa) - 1 {
		var newBeams []Beam
		for _, beam := range beams {
			switch mapa.mapa[i+1][beam.index] {
			case '.':
				newBeams = appendBeam(newBeams, beam)
			case '^':
				beamSplitCount++
				if inMapaX(beam.index-1, mapa) {
					newBeams = appendBeam(newBeams, Beam{index: beam.index - 1, camins: beam.camins})
				}
				if inMapaX(beam.index+1, mapa) {
					newBeams = appendBeam(newBeams, Beam{index: beam.index + 1, camins: beam.camins})
				}
			}
		}
		beams = newBeams
	}
	return beamSplitCount, beams
}

func appendBeam(beams []Beam, beam Beam) []Beam {
	for i, b := range beams {
		if b.index == beam.index {
			beams[i].camins += beam.camins
			return beams
		}
	}
	return append(beams, beam)
}

func sumaCamins(beams []Beam) int {
	camins := 0
	for _, beam := range beams {
		camins += beam.camins
	}
	return camins
}

type Beam struct {
	index  int
	camins int
}
