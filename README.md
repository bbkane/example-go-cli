# example-go-cli

An example go CLI to demo and learn new Go tooling!

## Convert to a new project

See [Go Project Notes](https://www.bbkane.com/blog/go-project-notes/#creating-a-new-go-project).

## Use

![./demo.gif](./demo.gif)

```bash
example-go-cli hello
```

## Install

- [Homebrew](https://brew.sh/): `brew install bbkane/tap/example-go-cli`
- [Scoop](https://scoop.sh/):

```
scoop bucket add bbkane https://github.com/bbkane/scoop-bucket
scoop install bbkane/example-go-cli
```

- Download Mac/Linux/Windows executable: [GitHub releases](https://github.com/bbkane/example-go-cli/releases)
- Go: `go install go.bbkane.com/example-go-cli@latest`
- Build with [goreleaser](https://goreleaser.com/) after cloning: `goreleaser release --snapshot --clean`

## Notes

See [Go Project Notes](https://www.bbkane.com/blog/go-project-notes/) for notes on development tooling.
