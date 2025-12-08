package main

import "math"

type Node struct {
	x     int
	y     int
	z     int
	veins []Node
}

func distanciaNodes(node1 Node, node2 Node) float64 {
	xDist := node1.x - node2.x
	yDist := node1.y - node2.y
	zDist := node1.z - node2.z

	return math.Sqrt(float64(xDist*xDist + yDist*yDist + zDist*zDist))
}

func (n *Node) afegirVei(node *Node, direccional bool) {
	if !n.veiExisteix(node) {
		n.veins = append(n.veins, *node)
	}
	if direccional {
		if node.veiExisteix(n) {
			node.veins = append(node.veins, *n)
		}
	}
}

func (n *Node) veiExisteix(node *Node) bool {
	existeix := false
	for _, v := range n.veins {
		if v.x == node.x && v.y == node.y && v.z == node.z {
			existeix = true
		}
	}
	return existeix
}
