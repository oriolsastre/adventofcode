package main

import (
	"math"
)

type Graph struct {
	nodes       []Node
	edges       Edges
	direccional bool
}
type Node struct {
	id    string
	x     int
	y     int
	z     int
	veins []*Node
}
type Edges map[string][]string

func distanciaNodes(node1 Node, node2 Node) float64 {
	xDist := node1.x - node2.x
	yDist := node1.y - node2.y
	zDist := node1.z - node2.z

	return math.Sqrt(float64(xDist*xDist + yDist*yDist + zDist*zDist))
}
func creaGraph(direccional bool) Graph {
	return Graph{nodes: []Node{}, edges: Edges{}, direccional: direccional}
}

func (n *Node) afegirVei(vei *Node) *Node {
	vE, v := n.veiExisteix(vei)
	if !vE {
		n.veins = append(n.veins, vei)
		return vei
	} else {
		return v
	}

}
func (n *Node) veiExisteix(node *Node) (bool, *Node) {
	for i, v := range n.veins {
		if v.id == node.id {
			return true, n.veins[i]
		}
	}
	return false, nil
}

func (g *Graph) nodeExisteix(node Node) (bool, *Node) {
	for i, n := range g.nodes {
		if n.id == node.id {
			return true, &(g.nodes[i])
		}
	}
	return false, nil
}

func (g *Graph) afegirNode(node Node) *Node {
	existeix, n := g.nodeExisteix(node)
	if !existeix {
		gNodes := &(g.nodes)
		*gNodes = append(*gNodes, node)
		return &node
	} else {
		return n
	}
}

func (g *Graph) afegirEdge(origen Node, desti Node) {
	ex1, og := g.nodeExisteix(origen)
	ex2, dt := g.nodeExisteix(desti)
	if !ex1 || !ex2 {
		panic("Algun dels nodes no existeix")
	}

	if _, ok := g.edges[og.id]; !ok {
		g.edges[og.id] = []string{}
	}
	// Afegir origen -> desti
	g.edges[og.id] = append(g.edges[og.id], dt.id)

	if g.direccional && og.id != dt.id {
		if _, ok := g.edges[dt.id]; !ok {
			g.edges[dt.id] = []string{}
		}
		// Afegir desti -> origen
		g.edges[dt.id] = append(g.edges[dt.id], og.id)
	}
}

func (g *Graph) iniciarVeins() {
	for nodeS, veinsS := range g.edges {
		_, node := g.nodeExisteix(Node{id: nodeS})
		for _, veiS := range veinsS {
			_, vei := g.nodeExisteix(Node{id: veiS})
			node.afegirVei(vei)
		}
	}
}
