package main

import (
	"go.bbkane.com/warg"
	"go.bbkane.com/warg/section"
)

var version string

func buildApp() warg.App {
	app := warg.New(
		"example-go-cli",
		section.New(
			"Example Go CLI",
			section.Command(
				"hello",
				"Say hello",
				hello,
			),
			section.ExistingCommand("version", warg.VersionCommand()),
		),
		warg.ExistingGlobalFlag("--color", warg.ColorFlag()),
		warg.OverrideVersion(version),
	)
	return app
}

func main() {
	app := buildApp()
	app.MustRun()
}
