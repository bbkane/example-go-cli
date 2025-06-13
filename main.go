package main

import (
	"go.bbkane.com/warg"
	"go.bbkane.com/warg/command"
	"go.bbkane.com/warg/flag"
	"go.bbkane.com/warg/section"
	"go.bbkane.com/warg/value/scalar"
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
				hello,
				command.NewFlag(
					"--name",
					"Person to greet",
					scalar.String(),
					flag.Required(),
				),
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
