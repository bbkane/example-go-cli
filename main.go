package main

import (
	"fmt"

	"go.bbkane.com/gocolor"
)

func main() {
	color, err := gocolor.Prepare(true)
	if err != nil {
		panic(err)
	}

	fmt.Println(
		color.Add(color.FgRed, "FgRed"),
	)
}
