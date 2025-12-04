package main

import "fmt"

func day4() {
	testInput := false
	input := getInput(2025, 4, testInput, false)
	inputMapa := input2LineArray(input)
	for i, line := range inputMapa {
		if len(line) == 0 {
			fmt.Println(i)
		}
	}
	mapa := Mapa{mapa: inputMapa, x: len(inputMapa[0]), y: len(inputMapa)}
	totalRotllos := 0
	rotllosAccessibles := processaMapa(&mapa)

	// 1346
	fmt.Printf("Solució del 1er problema: %d\n", rotllosAccessibles)

	for rotllosAccessibles > 0 {
		totalRotllos += rotllosAccessibles
		rotllosAccessibles = processaMapa(&mapa)
	}

	// 8493
	fmt.Printf("Solució del 2n problema: %d\n", totalRotllos)
	mapa.printMapa()

}

func processaMapa(mapa *Mapa) int {
	var rotllos int
	newMapa := Mapa{mapa: make([]string, mapa.y), x: mapa.x, y: mapa.y}
	copy(newMapa.mapa, mapa.mapa)
	for y, line := range mapa.mapa {
		cLine := line
		for x, char := range line {
			if char == '@' {
				if rotlloAcessible(x, y, mapa) {
					cLine = canviarCharN(cLine, x, ".")
					newMapa.mapa[y] = cLine
					rotllos++
				}
			}
		}
	}
	mapa.mapa = newMapa.mapa

	return rotllos
}

func rotlloAcessible(x int, y int, mapa *Mapa) bool {
	var veins int
	for x1 := -1; x1 <= 1; x1++ {
		for y1 := -1; y1 <= 1; y1++ {
			if inMapa(x+x1, y+y1, mapa) && !(x == 0 && y == 0) {
				if mapa.mapa[y+y1][x+x1] == '@' {
					veins++
				}
			}
		}
	}
	return veins <= 4
}
