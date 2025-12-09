package main

import (
	"fmt"
	"math"
	"slices"
	"strconv"
)

func day9() {
	testInput := false
	input := getInput(2025, 9, testInput, false)
	inputArray := input2LineArray(input, true)
	// tiles := inputArray2Tiles(inputArray)
	tiles := inputArray2TilesReduced(inputArray)

	// 4790063600
	fmt.Printf("Solució del 1er problema: %d\n", biggestRectangle(tiles))

	//1516172795
	fmt.Printf("Solució del 2n problema: %d\n", biggestCleanRectangle(tiles))
}

func biggestRectangle(tiles []Tile) int {
	maxRectangle := 0
	for i := range len(tiles) - 1 {
		for j := i + 1; j < len(tiles); j++ {
			rectangle := createRectangle(tiles[i], tiles[j])
			rectangleArea := rectangleArea(rectangle)
			if rectangleArea > maxRectangle {
				maxRectangle = rectangleArea
			}
		}
	}
	return maxRectangle
}

func biggestCleanRectangle(tiles []Tile) int {
	edges := tiles2Edges(tiles)
	maxRectangle := 0
	rectangleCache := []Rectangle{}
	for i := range len(tiles) - 1 {
		for j := i + 1; j < len(tiles); j++ {
			rectangle := createRectangle(tiles[i], tiles[j])
			rectangleArea := rectangleArea(rectangle)
			if rectangleArea > maxRectangle {
				if !rectangleInCache(rectangle, rectangleCache) {
					hRedTile := hasRedTile(rectangle, tiles)
					hEdge := hasEdge(rectangle, edges, tiles)
					if !hRedTile && !hEdge {
						if rectangleInsedShape(rectangle, edges, tiles) {
							maxRectangle = rectangleArea
						} else {
							rectangleCache = append(rectangleCache, rectangle)
						}
					} else {
						rectangleCache = append(rectangleCache, rectangle)
					}
				}
			}
		}
	}
	return maxRectangle
}

func hasRedTile(r Rectangle, tiles []Tile) bool {
	for _, tile := range tiles {
		if tile.x > r.minX && tile.x < r.maxX && tile.y > r.minY && tile.y < r.maxY {
			return true
		}
	}
	return false
}
func hasEdge(r Rectangle, edges Edges, tiles []Tile) bool {
	vEdges := edges.v
	hEdges := edges.h
	for x, yValues := range vEdges {
		if x > r.minX && x < r.maxX {
			for _, y := range yValues {
				if y > r.minY && y < r.maxY {
					if !tileExists(x, y, tiles) {
						return true
					}
				}
			}
		}
	}
	for y, xValues := range hEdges {
		if y > r.minY && y < r.maxY {
			for _, x := range xValues {
				if x > r.minX && x < r.maxX {
					if !tileExists(x, y, tiles) {
						return true
					}
				}
			}
		}
	}
	return false
}

func tileExists(x int, y int, tiles []Tile) bool {
	for _, tile := range tiles {
		if tile.x == x && tile.y == y {
			return true
		}
	}
	return false
}

func rectangleInCache(r Rectangle, cache []Rectangle) bool {
	for _, rC := range cache {
		if r.minX <= rC.minX && r.maxX >= rC.maxX && r.minY <= rC.minY && r.maxY >= rC.maxY {
			return true
		}
	}
	return false
}

func rectangleInsedShape(r Rectangle, edges Edges, tiles []Tile) bool {
	x := r.minX + (r.maxX-r.minX)/2
	y := r.minY + (r.maxY-r.minY)/2
	if numberOfCrossings(x, y, edges, tiles)%2 == 0 {
		return false
	}
	return true
}

// Des de el marge, que es fora, cada cop que es creua un edge. Parell, seguim fora, senar acabem dins.
// Miro en diagonal per no creuar edges directament. Tractar casos si creuem sobre cantonada.
func numberOfCrossings(x int, y int, edges Edges, tiles []Tile) int {
	dXY := int(math.Min(float64(x), float64(y)))
	originX := x - dXY
	originY := y - dXY

	crossings := 0

	for i := range dXY {
		iX := originX + i + 1
		iY := originY + i + 1

		if yValues, ok := edges.v[iX]; ok {
			if slices.Contains(yValues, iY) {
				crossings++
				continue
			}
		} else if xValues, ok := edges.h[iY]; ok {
			if slices.Contains(xValues, iX) {
				crossings++
				continue
			}
		}
		for _, tile := range tiles {
			if tile.x == iX && tile.y == iY {
				if math.Signbit(float64(tile.dX)) == math.Signbit(float64(tile.dY)) {
					crossings++
					break
				}
			}
		}

	}
	return crossings
}

func rectangleArea(rectangle Rectangle) int {
	dx := rectangle.maxX - rectangle.minX + 1
	dy := rectangle.maxY - rectangle.minY + 1
	return dx * dy
}

func tiles2Edges(tiles []Tile) Edges {
	edges := Edges{v: map[int][]int{}, h: map[int][]int{}}
	for i, tile := range tiles {
		nTileI := (i + 1) % len(tiles)
		if tile.y == tiles[nTileI].y {
			// Horizontal edge
			if _, ok := edges.h[tile.y]; !ok {
				edges.h[tile.y] = []int{}
			}
			minX := int(math.Min(float64(tile.x), float64(tiles[nTileI].x)))
			maxX := int(math.Max(float64(tile.x), float64(tiles[nTileI].x)))
			for x := minX; x <= maxX; x++ {
				edges.h[tile.y] = append(edges.h[tile.y], x)
			}
		} else if tile.x == tiles[nTileI].x {
			// Vertical edge
			if _, ok := edges.v[tile.x]; !ok {
				edges.v[tile.x] = []int{}
			}
			minY := int(math.Min(float64(tile.y), float64(tiles[nTileI].y)))
			maxY := int(math.Max(float64(tile.y), float64(tiles[nTileI].y)))
			for y := minY; y <= maxY; y++ {
				edges.v[tile.x] = append(edges.v[tile.x], y)
			}
		}
	}
	return edges
}
func inputArray2Tiles(inputArray []string) []Tile {
	tiles := []Tile{}
	for i, line := range inputArray {
		nextI := (i + 1) % len(inputArray)
		lineArray := inputLineSplit(line, ",")
		nextLineArray := inputLineSplit(inputArray[nextI], ",")
		if len(lineArray) == 2 && len(nextLineArray) == 2 {
			x, y := lineArray2Int(lineArray)
			nX, nY := lineArray2Int(nextLineArray)
			tiles = append(tiles, Tile{x, y, nX - x, nY - y})
		}
	}
	return tiles
}

func inputArray2TilesReduced(inputArray []string) []Tile {
	arrayInt := [][]int{}
	minX := math.Inf(1)
	minY := math.Inf(1)
	for _, line := range inputArray {
		lineArray := inputLineSplit(line, ",")
		if len(lineArray) == 2 {
			x, y := lineArray2Int(lineArray)
			arrayInt = append(arrayInt, []int{x, y})
			if float64(x) < minX {
				minX = float64(x)
			}
			if float64(y) < minY {
				minY = float64(y)
			}
		}
	}
	tiles := []Tile{}
	for i, tileInt := range arrayInt {
		nextI := (i + 1) % len(arrayInt)
		nextTileInt := arrayInt[nextI]
		x := tileInt[0] - int(minX) + 1
		y := tileInt[1] - int(minY) + 1
		nX := nextTileInt[0] - int(minX) + 1
		nY := nextTileInt[1] - int(minY) + 1
		tiles = append(tiles, Tile{x, y, nX - x, nY - y})
	}
	return tiles
}
func lineArray2Int(lineArray []string) (int, int) {
	if len(lineArray) == 2 {
		x, _ := strconv.Atoi(lineArray[0])
		y, _ := strconv.Atoi(lineArray[1])
		return x, y
	}
	return 0, 0
}

type Tile struct {
	x  int
	y  int
	dX int
	dY int
}

type Rectangle struct {
	minX int
	maxX int
	minY int
	maxY int
}

type Edges struct {
	h map[int][]int
	v map[int][]int
}

func createRectangle(t1 Tile, t2 Tile) Rectangle {
	minX := int(math.Min(float64(t1.x), float64(t2.x)))
	maxX := int(math.Max(float64(t1.x), float64(t2.x)))
	minY := int(math.Min(float64(t1.y), float64(t2.y)))
	maxY := int(math.Max(float64(t1.y), float64(t2.y)))
	return Rectangle{minX, maxX, minY, maxY}
}
