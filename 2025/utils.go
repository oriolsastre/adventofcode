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
