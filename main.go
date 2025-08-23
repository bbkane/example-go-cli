package main

import (
	"fmt"

	"go.bbkane.com/warg"
)

var version string

func buildApp() warg.App {
	app := warg.New(
		"example-go-cli",
		version,
		warg.NewSection(
			"Example Go CLI",
			warg.NewSubCmd(
				"hello",
				"Say hello",
				func(ctx warg.CmdContext) error {
					fmt.Println("Hello from example-go-cli!")
					return nil
				},
			),
		),
	)
	return app
}

func main() {
	app := buildApp()
	app.MustRun()
}
