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
	// 81536
	fmt.Println("Solució primer problema:", maxConnexions(connexions, 3))
	ultConn := ultimaConnexio(nodes)
	distXUltConn := distanciaXConnexio(ultConn)
	// 7017750530
	fmt.Printf("Solucion segon problema: %d", int(distXUltConn))
}

func input2Nodes(input []string) []*NodeConne {
	var nodes []*NodeConne
	for _, line := range input {
		splitLine := inputLineSplit(line, ",")
		if len(splitLine) == 3 {
			x, _ := strconv.Atoi(splitLine[0])
			y, _ := strconv.Atoi(splitLine[1])
			z, _ := strconv.Atoi(splitLine[2])
			nodes = append(nodes, &NodeConne{&Node{x, y, z, []*Node{}}, 0})
		}
	}
	return nodes
}

func crearConnexions(nodes []*NodeConne, limit int) []*NodeConne {
	distancies := llistaDistanciaNodes(nodes)
	var minNodes []*NodeConne
	for i := range limit {
		connexio := distancies.pop()
		node1 := connexio.node1
		node2 := connexio.node2
		if !nodeExisteix(minNodes, node1) {
			minNodes = append(minNodes, node1)
		}
		if !nodeExisteix(minNodes, node2) {
			minNodes = append(minNodes, node2)
		}
		max := math.Max(float64(node1.Circuit), float64(node2.Circuit))
		if max == 0 {
			node1.Circuit = i + 1
			node2.Circuit = i + 1
		} else if node1.Circuit > node2.Circuit {
			converteixCircuit(minNodes, node2.Circuit, node1.Circuit)
		} else if node2.Circuit > node1.Circuit {
			converteixCircuit(minNodes, node1.Circuit, node2.Circuit)
		}
	}
	return minNodes
}

func ultimaConnexio(nodes []*NodeConne) Connexio {
	for _, node := range nodes {
		node.Circuit = 0
	}
	distancies := llistaDistanciaNodes(nodes)
	i := 0
	for len(distancies) > 0 {
		connexio := distancies.pop()
		i++
		node1 := connexio.node1
		node2 := connexio.node2
		max := math.Max(float64(node1.Circuit), float64(node2.Circuit))
		if max == 0 {
			node1.Circuit = i
			node2.Circuit = i
		} else if node1.Circuit > node2.Circuit {
			ogValue := node2.Circuit
			node2.Circuit = node1.Circuit
			if ogValue != 0 {
				converteixCircuit(nodes, ogValue, node1.Circuit)
			}
		} else if node2.Circuit > node1.Circuit {
			ogValue := node1.Circuit
			node1.Circuit = node2.Circuit
			if ogValue != 0 {
				converteixCircuit(nodes, ogValue, node2.Circuit)
			}
		}
		numCircuits := circuitsGraph(nodes)
		if numCircuits == 1 && nodes[0].Circuit > 0 {
			return connexio
		}
	}
	return Connexio{}
}

func circuitsGraph(graph []*NodeConne) int {
	nodeConneMapa := nodeConnToMap(graph)
	var nodeConneSlice [][]*NodeConne
	for _, nC := range nodeConneMapa {
		nodeConneSlice = append(nodeConneSlice, nC)
	}
	return len(nodeConneSlice)
}

func maxConnexions(nodes []*NodeConne, max int) int {
	nodeConneMapa := nodeConnToMap(nodes)
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

func nodeConnToMap(nodes []*NodeConne) map[int][]*NodeConne {
	nodeConneMapa := make(map[int][]*NodeConne)
	for _, nodeConne := range nodes {
		if _, ok := nodeConneMapa[nodeConne.Circuit]; !ok {
			nodeConneMapa[nodeConne.Circuit] = []*NodeConne{}
		}
		a := nodeConneMapa[nodeConne.Circuit]
		if !nodeExisteix(a, nodeConne) {
			nodeConneMapa[nodeConne.Circuit] = append(nodeConneMapa[nodeConne.Circuit], nodeConne)
		}
	}
	return nodeConneMapa
}

func nodeExisteix(nodes []*NodeConne, node *NodeConne) bool {
	for i := range len(nodes) {
		if (nodes)[i] == node {
			return true
		}
	}
	return false
}

func converteixCircuit(nodes []*NodeConne, origen int, desti int) {
	for _, node := range nodes {
		if node.Circuit == origen {
			node.Circuit = desti
		}
	}
}

func llistaDistanciaNodes(nodes []*NodeConne) DistanciaMinHeap {
	var distanciaHeap DistanciaMinHeap
	for i := range len(nodes) {
		n1 := nodes[i]
		for j := i + 1; j < len(nodes); j++ {
			n2 := nodes[j]
			distancia := distanciaNodes(*n1.Node, *n2.Node)
			connexio := Connexio{nodes[i], nodes[j], distancia}
			distanciaHeap.insert(connexio)
		}
	}

	return distanciaHeap
}
func distanciaXConnexio(connexio Connexio) float64 {
	return float64(connexio.node1.x) * float64(connexio.node2.x)
}

type NodeConne struct {
	*Node
	Circuit int
}

type Connexio struct {
	node1 *NodeConne
	node2 *NodeConne
	n     float64
}

type DistanciaMinHeap []Connexio

func (h *DistanciaMinHeap) insert(n Connexio) {
	*h = append(*h, n)
	h.swapParent(len(*h) - 1)
}

func (h *DistanciaMinHeap) pop() Connexio {
	connexio := (*h)[0]
	(*h)[0] = (*h)[len((*h))-1]
	(*h) = (*h)[:len((*h))-1]
	h.swapChild(0)
	return connexio
}

func (h *DistanciaMinHeap) swapChild(i int) {
	lChildI := 2*i + 1
	rChildI := 2*i + 2

	var minChildI int

	// No children
	if lChildI >= len((*h)) {
		return
	}

	if rChildI >= len((*h)) {
		minChildI = lChildI
	} else {
		if (*h)[lChildI].n < (*h)[rChildI].n {
			minChildI = lChildI
		} else {
			minChildI = rChildI
		}
	}
	if (*h)[i].n > (*h)[minChildI].n {
		(*h)[minChildI], (*h)[i] = (*h)[i], (*h)[minChildI]
		h.swapChild(minChildI)
	}
}

func (h *DistanciaMinHeap) swapParent(i int) {
	if i == 0 || i >= len((*h)) {
		return
	}
	parentIndex := (i - 1) / 2
	if (*h)[parentIndex].n > (*h)[i].n {
		(*h)[parentIndex], (*h)[i] = (*h)[i], (*h)[parentIndex]
		h.swapParent(parentIndex)
	}
}

func (h DistanciaMinHeap) print() {
	for _, e := range h {
		fmt.Println(e.n, ", ", e.node1, ", ", e.node2)
	}
}
