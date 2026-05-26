#!/usr/bin/env bash

# Replace goreleaser completion line in .goreleaser.yml files.
# Matches any binary name and adds bash/fish shells alongside zsh.
# Usage: ./fix_goreleaser_completions.sh /path/to/repo1 /path/to/repo2 ...
# Or run from a repo directory with no args to patch the local .goreleaser.yml

set -euo pipefail

OLD_PAT='generate_completions_from_executable\(bin/"[^"]*", "completion", shells: \[:zsh\]\)'
SED_EXPR='s|generate_completions_from_executable(bin/"\([^"]*\)", "completion", shells: \[:zsh\])|generate_completions_from_executable(bin/"\1", "completion", shells: [:bash, :fish, :zsh])|g'

patch_file() {
	local file="$1"
	if [[ ! -f "$file" ]]; then
		echo "SKIP: $file not found"
		return
	fi
	if grep -qE "$OLD_PAT" "$file"; then
		sed -i "$SED_EXPR" "$file"
		echo "PATCHED: $file"
	else
		echo "NO MATCH: $file"
	fi
}

if [[ $# -eq 0 ]]; then
	patch_file ".goreleaser.yml"
else
	for repo in "$@"; do
		echo "Processing repo: $repo"
		# patch_file "${repo}/.goreleaser.yml"
		go get go.bbkane.com/warg@v0.40.2
		go test ./...
		git add .
		git commit -m 'Update warg'
	done
fi
