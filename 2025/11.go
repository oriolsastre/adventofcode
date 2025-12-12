package main

import (
	"fmt"
	"slices"
)

func day11() {
	testInput := false
	input := getInput(2025, 11, testInput, false)
	inputArray := input2LineArray(input, true)

	graph := input2Graph(inputArray)
	totsCamins := graph.trobarTotsCamins("you", "out")

	// 791
	fmt.Printf("La solució del 1er problema es: %d\n", totsCamins)

	totesRutes := graph.trobarTotesRutes([]string{"svr", "fft", "dac", "out"})
	// 520476725037672
	fmt.Printf("La solució del 2n problema es: %d\n", totesRutes)
}

func (g *Graph) trobarTotsCamins(origen string, desti string) int {
	g.iniciarGraf()
	var root, target *Node
	for i, node := range g.nodes {
		if node.id == origen {
			root = &g.nodes[i]
		}
		if node.id == desti {
			target = &g.nodes[i]
		}
	}
	if root == nil || target == nil {
		return 0
	}
	stack := NodeStack{}
	stackElement := StackElement{node: root, cami: []string{root.id}}
	stack.add(stackElement)
	for stack.len() > 0 {
		sE := stack.pop()
		node := sE.node
		node.visitat = true
		if node.id == desti {
			sumaCaminsTrobats(sE.cami, &(g.nodes), 1)
		} else {
			for _, vei := range node.veins {
				if !vei.visitat {
					// Per evitar loops (que no n'hi hauria d'haver)
					if !slices.Contains(sE.cami, vei.id) {
						veiElement := StackElement{node: vei, cami: slices.Concat(sE.cami, []string{vei.id})}
						stack.add(veiElement)
					}
				} else {
					sumaCaminsTrobats(sE.cami, &(g.nodes), vei.camins)
				}
			}
		}
	}
	return root.camins
}
func (g *Graph) trobarTotesRutes(ruta []string) int {
	rutes := 1
	for i := range len(ruta) - 1 {
		origen := ruta[i]
		desti := ruta[i+1]
		rutes *= g.trobarTotsCamins(origen, desti)
	}
	return rutes
}

func input2Graph(input []string) Graph {
	graph := creaGraph(false)
	for _, line := range input {
		splitLine := inputLineSplit(line, " ")
		origenId := splitLine[0][:len(splitLine[0])-1]
		origen := graph.crearNodeAlGraf(origenId)
		for i := 1; i < len(splitLine); i++ {
			veiId := splitLine[i]
			vei := graph.crearNodeAlGraf(veiId)
			graph.afegirEdge(*origen, *vei)
		}
	}
	return graph
}

func (g *Graph) crearNodeAlGraf(id string) *Node {
	node := Node{id: id, veins: []*Node{}, visitat: false, camins: 0}
	exiteix, nd := g.nodeExisteix(node)
	if exiteix {
		return nd
	}
	return g.afegirNode(node)
}

func sumaCaminsTrobats(camins []string, nodes *[]Node, n int) {
	for _, cami := range camins {
		for i := range *nodes {
			if (*nodes)[i].id == cami {
				(*nodes)[i].camins += n
				break
			}
		}
	}
}

type StackElement struct {
	node *Node
	cami []string
}
type NodeStack []StackElement

func (n *NodeStack) len() int {
	return len(*n)
}
func (n *NodeStack) add(sE StackElement) {
	newTop := []StackElement{sE}
	*n = append(newTop, *n...)
}

func (n *NodeStack) pop() StackElement {
	top := (*n)[0]
	*n = (*n)[1:]
	return top
}
