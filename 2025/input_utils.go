package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func getInput(year uint16, day uint8, test bool, log bool) string {
	// Try to load input from file
	inputFromFile, err := loadInput(year, day, test)
	if err == nil {
		if log {
			fmt.Printf("Input for day %d/%d loaded from file:\n", year, day)
		}
		return inputFromFile
	} else if test {
		fmt.Printf("Input test for day %d/%d not found in file test\n", year, day)
		os.Exit(1)
	} else if log {
		fmt.Printf("Input for day %d/%d not found in file, downloading:\n", year, day)
	}

	// Load AoC Session token from file
	sessionFile, err := os.ReadFile("session.txt")
	if err != nil {
		if log {
			fmt.Println("Error reading session file:", err)
		}
		panic(err)
	}
	sessionToken := string(sessionFile)

	// Build URL
	url := fmt.Sprintf("https://adventofcode.com/%d/day/%d/input", year, day)

	// Make request
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		if log {
			fmt.Println("Error creating request:", err)
		}
		panic(err)
	}
	req.Header.Set("Cookie", fmt.Sprintf("session=%s", sessionToken))

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		if log {
			fmt.Println("Error making request:", err)
		}
		panic(err)
	}
	input, err := io.ReadAll(res.Body)
	if err != nil {
		if log {
			fmt.Println("Error reading response body:", err)
		}
		panic(err)
	}
	if log {
		fmt.Printf("Input for day %d/%d read correctly:\n", year, day)
	}
	os.WriteFile(fmt.Sprintf("inputs/%d_%d.txt", year, day), input, 0644)
	return string(input)
}

func loadInput(year uint16, day uint8, test bool) (string, error) {
	var filePath string
	if test {
		filePath = fmt.Sprintf("inputs/test/%d_%d.txt", year, day)
	} else {
		filePath = fmt.Sprintf("inputs/%d_%d.txt", year, day)
	}
	inputFile, err := os.ReadFile(filePath)
	if err != nil {
		return "", err
	}
	return string(inputFile), nil
}

func input2LineArray(input string) []string {
	return strings.Split(input, "\n")
}

func inputLineSplit(inputLine string, separator string) []string {
	inputLine = strings.TrimSpace(inputLine)
	return strings.Split(inputLine, separator)
}
