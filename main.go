package main

import (
	"fmt"

	"go.bbkane.com/warg"
	"go.bbkane.com/warg/section"
	"go.bbkane.com/warg/wargcore"
)

var version string

func buildApp() wargcore.App {
	app := warg.New(
		"example-go-cli",
		version,
		section.New(
			"Example Go CLI",
			section.NewCommand(
				"hello",
				"Say hello",
				func(ctx wargcore.Context) error {
					fmt.Println("Hello from example-go-cli!")
					return nil
				},
			),
			section.CommandMap(warg.VersionCommandMap()),
		),
		warg.GlobalFlagMap(warg.ColorFlagMap()),
	)
	return app
}

func main() {
	app := buildApp()
	app.MustRun()
}
