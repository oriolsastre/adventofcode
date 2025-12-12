package main

import "fmt"

func day11() {
	testInput := false
	input := getInput(2025, 11, testInput, false)
	inputArray := input2LineArray(input, true)

	graph := input2Graph(inputArray)
	totsCamins := graph.trobarTotsCamins("you", "out")

	// 791
	fmt.Printf("La solució del 1er problema es: %d\n", totsCamins)
}

func (g *Graph) trobarTotsCamins(origen string, desti string) int {
	g.iniciarVeins()
	var root, target *Node
	for _, node := range g.nodes {
		if node.id == origen {
			root = &node
		}
		if node.id == desti {
			target = &node
		}
	}
	if root == nil || target == nil {
		return 0
	}
	stack := NodeStack{}
	stack.add(root)
	camins := 0
	for stack.len() > 0 {
		node := stack.pop()
		if node.id == desti {
			camins++
			continue
		}
		for _, vei := range node.veins {
			stack.add(vei)
		}
	}
	return camins
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
	node := Node{id: id, veins: []*Node{}}
	exiteix, nd := g.nodeExisteix(node)
	if exiteix {
		return nd
	}
	// append(g.nodes, node)
	return g.afegirNode(node)
}

type NodeStack []*Node

func (n *NodeStack) len() int {
	return len(*n)
}
func (n *NodeStack) add(node *Node) {
	newTop := []*Node{node}
	*n = append(newTop, *n...)
}

func (n *NodeStack) pop() *Node {
	top := (*n)[0]
	*n = (*n)[1:]
	return top
}
