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
