package main

import "core:fmt"
import "core:math"
import "core:math/rand"
import ry "vendor:raylib"

Node :: struct{
	split_dim: u32,
	split_value: f32,
	left: ^Node,
	right: ^Node,
}

build_tree :: proc (x1: []f32, x2: []f32, truth: []i32, n_points: int, depth: i32) -> ^Node {
	if depth == 0 {
		return nil
	}

	// Choose a random dimension to split on
	split_dim := cast(u32) rand.int31_max(2)

	// Choose a random value to split on
	split_value := rand.float32()

	// Split the data
	left_x1 := make([dynamic]f32, 0)
	left_x2 := make([dynamic]f32, 0)
	left_truth := make([dynamic]i32, 0)
	right_x1 := make([dynamic]f32, 0)
	right_x2 := make([dynamic]f32, 0)
	right_truth := make([dynamic]i32, 0)

	defer {
		delete(left_x1)
		delete(left_x2)
		delete(left_truth)
		delete(right_x1)
		delete(right_x2)
		delete(right_truth)
	}

	for i in 0..<n_points {
		if x1[i] < split_value {
			append(&left_x1, x1[i])
			append(&left_x2, x2[i])
			append(&left_truth, truth[i])
		} else {
			append(&right_x1, x1[i])
			append(&right_x2, x2[i])
			append(&right_truth, truth[i])
		}
	}

	// Recursively build the tree
	left := build_tree(left_x1[:], left_x2[:], left_truth[:], len(left_x1), depth-1)
	right := build_tree(right_x1[:], right_x2[:], right_truth[:], len(right_x1), depth-1)

	node := new(Node)
	node.split_dim = split_dim
	node.split_value = split_value
	node.left = left
	node.right = right

	return node
}

main :: proc() {
	tree := Node{
		split_dim=0,
		split_value=0.5,
		left=nil,
		right=nil,
	}

	n_points :: 100
	radius : f32 : 0.3

	x1 := make([]f32, n_points*n_points)
	x2 := make([]f32, n_points*n_points)
	truth := make([]i32, n_points*n_points)

	defer {
		delete(x1)
		delete(x2)
		delete(truth)
	}

	for x in 0..<n_points {
		for y in 0..<n_points {
			x1[x*n_points + y] = f32(x) / f32(n_points)
			x2[x*n_points + y] = f32(y) / f32(n_points)
			truth[x*n_points + y] = i32(
				(math.pow(x1[x*n_points + y]-0.5, 2) + math.pow(x2[x*n_points + y]-0.5, 2)) < math.pow(radius, 2)
			)
		}
	}

	fmt.println("Hellope!", len(x1), math.sum(x1[:]))
	
	// Create a window and display the points
	ry.InitWindow(800, 800, "Hello, World!")
	defer ry.CloseWindow()

	ry.SetTargetFPS(60)

	for !ry.WindowShouldClose() {
		ry.BeginDrawing()
		ry.ClearBackground(ry.BLACK)

		for x in 0..<n_points {
			for y in 0..<n_points {
				ry.DrawPixel(i32(x1[x*n_points + y] * 800), i32(x2[x*n_points + y] * 800), ry.WHITE if bool(truth[x*n_points + y]) else ry.GREEN)
			}
		}
		ry.EndDrawing()
	}

}