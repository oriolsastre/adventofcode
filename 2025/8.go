package main

import (
	"fmt"
	"math"
	"sort"
	"strconv"
)

func day8() {
	testInput := false
	input := getInput(2025, 8, testInput, false)
	inputArray := input2LineArray(input, true)
	nodes := input2Nodes(inputArray)

	var limit int
	if testInput {
		limit = 10
	} else {
		limit = 1000
	}
	connexions := crearConnexions(nodes, limit)

	fmt.Println("Solució primer problema:", maxConnexions(connexions, 3))
}

func input2Nodes(input []string) []*NodeConne {
	var nodes []*NodeConne
	for _, line := range input {
		splitLine := inputLineSplit(line, ",")
		if len(splitLine) == 3 {
			x, _ := strconv.Atoi(splitLine[0])
			y, _ := strconv.Atoi(splitLine[1])
			z, _ := strconv.Atoi(splitLine[2])
			nodes = append(nodes, &NodeConne{&Node{x, y, z, []Node{}}, 0})
		}
	}
	return nodes
}

func crearConnexions(nodes []*NodeConne, limit int) []*NodeConne {
	distancies := llistaDistanciaNodes(nodes, limit)
	nodes = minNodes(distancies)
	for i := range limit {
		node1 := (*distancies[i].node1)
		node2 := (*distancies[i].node2)
		max := math.Max(float64(node1.Connexio), float64(node2.Connexio))
		if max == 0 {
			distancies[i].node1.Connexio = i + 1
			distancies[i].node2.Connexio = i + 1
		} else if node1.Connexio > node2.Connexio {
			converteixConnexio(&distancies, node2.Connexio, node1.Connexio, i)
		} else if node2.Connexio > node1.Connexio {
			converteixConnexio(&distancies, node1.Connexio, node2.Connexio, i)
		}
	}
	return nodes
}
func maxConnexions(nodes []*NodeConne, max int) int {
	nodeConneMapa := make(map[int][]*NodeConne)
	for _, nodeConne := range nodes {
		if _, ok := nodeConneMapa[nodeConne.Connexio]; !ok {
			nodeConneMapa[nodeConne.Connexio] = []*NodeConne{}
		}
		a := nodeConneMapa[nodeConne.Connexio]
		if !nodeExisteix(a, nodeConne) {
			nodeConneMapa[nodeConne.Connexio] = append(nodeConneMapa[nodeConne.Connexio], nodeConne)
		}
	}
	var nodeConneSlice [][]*NodeConne
	for _, nC := range nodeConneMapa {
		nodeConneSlice = append(nodeConneSlice, nC)
	}
	sort.Slice(nodeConneSlice, func(i, j int) bool {
		return len(nodeConneSlice[i]) > len(nodeConneSlice[j])
	})
	total := 1
	for i := range max {
		total *= len(nodeConneSlice[i])
	}
	return total
}

func minNodes(distancies []Distancia) []*NodeConne {
	var minNodes []*NodeConne
	for i := range len(distancies) {
		if !nodeExisteix(minNodes, distancies[i].node1) {
			minNodes = append(minNodes, distancies[i].node1)
		}
		if !nodeExisteix(minNodes, distancies[i].node2) {
			minNodes = append(minNodes, distancies[i].node2)
		}
	}
	return minNodes
}

func nodeExisteix(nodes []*NodeConne, node *NodeConne) bool {
	for i := range len(nodes) {
		if (nodes)[i] == node {
			return true
		}
	}
	return false
}

func converteixConnexio(distancia *[]Distancia, origen int, desti int, index int) {
	for i := range index + 1 {
		if (*distancia)[i].node1.Connexio == origen {
			(*(*distancia)[i].node1).Connexio = desti
		}
		if (*distancia)[i].node2.Connexio == origen {
			(*(*distancia)[i].node2).Connexio = desti
		}
	}
}

func llistaDistanciaNodes(nodes []*NodeConne, limit int) []Distancia {
	var llistaDistancia []Distancia
	for i := range len(nodes) {
		for j := i + 1; j < len(nodes); j++ {
			n1 := nodes[i]
			n2 := nodes[j]
			distancia := distanciaNodes(*n1.Node, *n2.Node)
			if len(llistaDistancia) <= limit || distancia < llistaDistancia[len(llistaDistancia)-1].n {
				llistaDistancia = appendDistanciaOrdenat(llistaDistancia, &Distancia{nodes[i], nodes[j], distancia})
				if len(llistaDistancia) > limit {
					llistaDistancia = llistaDistancia[:limit]
				}
			}
		}
	}
	return llistaDistancia
}

func appendDistanciaOrdenat(llistaDistancia []Distancia, distancia *Distancia) []Distancia {
	newIndex := findIndexLess(llistaDistancia, distancia.n, 0, len(llistaDistancia))
	novaLlista := make([]Distancia, len(llistaDistancia)+1)
	copy(novaLlista[:newIndex], llistaDistancia[:newIndex])
	novaLlista[newIndex] = *distancia
	copy(novaLlista[newIndex+1:], llistaDistancia[newIndex:])
	return novaLlista
}

func findIndexLess(llista []Distancia, target float64, inici int, fi int) int {
	if fi <= inici {
		return inici
	}
	mid := (inici + fi) / 2

	if llista[mid].n < target {
		return findIndexLess(llista, target, mid+1, fi)
	} else if llista[mid].n > target {
		if mid == 0 || llista[mid-1].n < target {
			return mid
		}
		return findIndexLess(llista, target, inici, mid-1)
	} else {
		return mid
	}
}

type NodeConne struct {
	*Node
	Connexio int
}

type Distancia struct {
	node1 *NodeConne
	node2 *NodeConne
	n     float64
}
