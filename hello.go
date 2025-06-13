package main

import (
	"fmt"

	"go.bbkane.com/warg/wargcore"
)

func hello(ctx wargcore.Context) error {
	name := ctx.Flags["--name"].(string)
	fmt.Printf("Hello %s!!\n", name)
	return nil
}
