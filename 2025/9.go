package main

import (
	"fmt"
	"math"
	"strconv"
)

func day9() {
	testInput := false
	input := getInput(2025, 9, testInput, false)
	inputArray := input2LineArray(input, true)
	tiles := inputArray2Tiles(inputArray)

	// 4790063600
	fmt.Printf("Solució del 1er problema: %d\n", biggestRectangle(tiles))
}

func biggestRectangle(tiles []Tile) int {
	maxRectangle := 0
	for i := range len(tiles) - 1 {
		for j := i + 1; j < len(tiles); j++ {
			rectangle := rectangleArea(tiles[i], tiles[j])
			if rectangle > maxRectangle {
				maxRectangle = rectangle
			}
		}
	}
	return maxRectangle
}

func rectangleArea(tile1 Tile, tile2 Tile) int {
	dx := math.Abs(float64(tile1.x-tile2.x)) + 1
	dy := math.Abs(float64(tile1.y-tile2.y)) + 1
	return int(dx * dy)
}
func inputArray2Tiles(inputArray []string) []Tile {
	tiles := []Tile{}
	for _, line := range inputArray {
		lineArray := inputLineSplit(line, ",")
		if len(lineArray) == 2 {
			x, _ := strconv.Atoi(lineArray[0])
			y, _ := strconv.Atoi(lineArray[1])
			tiles = append(tiles, Tile{x, y})
		}
	}
	return tiles
}

type Tile struct {
	x int
	y int
}
