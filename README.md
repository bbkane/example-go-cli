# example-go-cli

An example go CLI to demo and learn new Go tooling!

## Project status (2025-06-13)

I use `example-go-cli` to test CI/CD, so it's not really useful to anyone else.

## Convert to a new project

See [Go Project Notes](https://www.bbkane.com/blog/go-project-notes/#creating-a-new-go-project).

## Use

![./demo.gif](./demo.gif)

```bash
example-go-cli hello
```

## Install

- [Homebrew](https://brew.sh/):

```
brew install --cask bbkane/tap/example-go-cli
```

- [Scoop](https://scoop.sh/):

```
scoop bucket add bbkane https://github.com/bbkane/scoop-bucket
scoop install bbkane/example-go-cli
```

- Download Mac/Linux/Windows executable: [GitHub releases](https://github.com/bbkane/example-go-cli/releases)
- Go: `go install go.bbkane.com/example-go-cli@latest`
- Build with [goreleaser](https://goreleaser.com/) after cloning: `goreleaser release --snapshot --clean`

## Manual release validation

TODO: move this to Go tooling blog

Notes:

- `brew style` and `brew audit` currently reject arbitrary cask file paths and expect a cask name in a tap.
- Some output formatting from generated files may be autocorrectable by Homebrew style tools.
- `brew audit` may enable Homebrew developer mode automatically.

```bash
# Build snapshot artifacts locally.
goreleaser release --snapshot --clean --skip=publish

# Create a temporary local tap (one-time).
brew tap-new bbkane/localtest

# Copy generated cask into the local tap.
mkdir -p "$(brew --repository)/Library/Taps/bbkane/homebrew-localtest/Casks"
cp dist/homebrew/Casks/example-go-cli.rb "$(brew --repository)/Library/Taps/bbkane/homebrew-localtest/Casks/example-go-cli.rb"

# Rewrite generated GitHub release URLs to local file:// URLs.
rewrite_goreleaser_cask_urls_to_file.py \
	"$(brew --repository)/Library/Taps/bbkane/homebrew-localtest/Casks/example-go-cli.rb" \
	"$PWD/dist"

# some fail due to goreleaser's bad style
brew style --cask bbkane/localtest/example-go-cli

# for some reason the SHA mismatches?
brew audit --cask --strict --online bbkane/localtest/example-go-cli

# Install and smoke test. NOTE: when testing locally like this, the Apple security warning won't let tab completions install. Seems to work ok when installed from GitHub releases.
brew install --cask bbkane/localtest/example-go-cli
example-go-cli hello

# Cleanup.
brew uninstall --cask --force bbkane/localtest/example-go-cli
brew untap bbkane/localtest

# Disable Homebrew developer mode if it was enabled by tap-new.
brew developer off
```

## Notes

See [Go Project Notes](https://www.bbkane.com/blog/go-project-notes/) for notes on development tooling.
