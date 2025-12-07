package main

import (
	"fmt"
	"time"
)

func timer() func() {
	start := time.Now()
	return func() {
		fmt.Printf("\n\nExecution time: %s\n", time.Since(start))
	}
}

func removeDuplicateInt(ints []int) []int {
	seen := map[int]bool{}
	result := []int{}
	for _, i := range ints {
		if seen[i] {
			continue
		}
		seen[i] = true
		result = append(result, i)
	}
	return result
}

func invertMatrixStr(matrix [][]string) [][]string {
	invertedMatrix := make([][]string, len(matrix[0]))
	for i := range len(invertedMatrix) {
		invertedMatrix[i] = make([]string, len(matrix))
	}
	for i, row := range matrix {
		for j, col := range row {
			invertedMatrix[j][i] = col
		}
	}
	return invertedMatrix
}

// Mapes
type Mapa struct {
	mapa []string
	x    int
	y    int
}

func inMapa(x int, y int, mapa *Mapa) bool {
	return x >= 0 && x < mapa.x && y >= 0 && y < mapa.y
}

func (m Mapa) printMapa() {
	for _, line := range m.mapa {
		fmt.Println(line)
	}
	fmt.Println("x:", m.x, "y:", m.y)
}

// Strings
func canviarCharN(s string, n int, char string) string {
	if n < 0 || n >= len(s) {
		return s
	} else if n == 0 {
		return char + s[1:]
	} else if n == len(s)-1 {
		return s[:n] + char
	} else {
		return s[:n] + char + s[n+1:]
	}
}
