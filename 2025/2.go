package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func day2() {
	testInput := false
	input := getInput(2025, 2, testInput, false)
	ids := inputLineSplit(input, ",")
	var invalidIds []int
	var sumInvalidIds int
	for _, id := range ids {
		for _, invalidId := range searchInvalidIds(id) {
			invalidIds = append(invalidIds, invalidId)
		}
	}
	for _, invId := range invalidIds {
		sumInvalidIds += invId
	}
	// 54234399924
	fmt.Printf("Solució del problema: %d\n", sumInvalidIds)
	// 70187097315
}

func searchInvalidIds(rangeStr string) []int {
	var invalidIds = []int{}

	rang := strings.Split(rangeStr, "-")
	start, errS := strconv.Atoi(rang[0])
	end, errE := strconv.Atoi(rang[1])
	if errS != nil || errE != nil {
		panic("Converting str to int failed")
	}
	n := start
	// for l := int(math.Ceil(float64(len(rang[0])) / float64(2))); l <= len(rang[1])/2; l++ {
	for l := 1; l <= len(rang[1])/2; l++ {
		for n >= start && n <= end {
			if isInvalidId(n, l) {
				invalidIds = append(invalidIds, n)
			}
			n = getNextRepeatedNumber(n, l)
		}
		n = start
	}

	// fmt.Println(int(math.Ceil(float64(3) / 2)))

	return removeDuplicateInt(invalidIds)
}

func getNextRepeatedNumber(n int, lenght int) int {
	// A retornar
	var nextNumber int
	// Copia a manipular
	copyN := n
	// Mida de n
	nSize := int(math.Trunc(math.Log10(float64(n))) + 1)
	// fmt.Println("Size:", nSize)
	if nSize%lenght != 0 || nSize == lenght {
		nextSize := nSize + 1
		for nextSize%lenght != 0 {
			nextSize++
		}
		copyN = int(math.Pow10(nextSize))
		nSize = nextSize
	}
	// fmt.Println("Next size:", nSize)
	strNumber := strconv.Itoa(copyN)
	var strNextNumber string
	for i := 0; i < (nSize / lenght); i++ {
		strNextNumber += strNumber[:lenght]
	}
	nextNumber, _ = strconv.Atoi(strNextNumber)
	if nextNumber <= n {
		strNextNumber = ""
		toRepeat, _ := strconv.Atoi(strNumber[:lenght])
		toRepeat++
		toRepeat10 := math.Log10(float64(toRepeat))
		if toRepeat10 == math.Trunc(toRepeat10) {
			nSize += lenght
			toRepeat = int(math.Pow10(int(toRepeat10) - 1))
		}
		for i := 0; i < (nSize / lenght); i++ {
			strNextNumber += strconv.Itoa(toRepeat)
		}
		nextNumber, _ = strconv.Atoi(strNextNumber)
	}
	return nextNumber
}

func isInvalidId(n int, length int) bool {
	nSize := int(math.Trunc(math.Log10(float64(n))) + 1)
	if nSize%length != 0 || nSize <= length {
		return false
	}
	nStr := strconv.Itoa(n)
	for i := 0; i < (nSize/length)-1; i++ {
		if nStr[i*length:(i+1)*length] != nStr[(i+1)*length:(i+2)*length] {
			return false
		}
	}
	return true
}
