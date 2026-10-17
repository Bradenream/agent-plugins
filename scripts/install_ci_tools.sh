#!/usr/bin/env bash
# CI-only Linux x64 tools. Pins must be reviewed against upstream releases.
set -euo pipefail
target="${1:?Provide a tools directory outside the repository}"
scratch="$(mktemp -d)"
trap 'rm -rf -- "$scratch"' EXIT
mkdir -p -- "$target"

install_tool() {
  local repo="$1" version="$2" asset="$3" checksum="$4" binary="$5"
  curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
    --tlsv1.2 --connect-timeout 15 --max-time 120 --retry 2 \
    "https://github.com/$repo/releases/download/v$version/$asset" -o "$scratch/$asset"
  printf '%s  %s\n' "$checksum" "$scratch/$asset" | sha256sum --check --status
  tar -xzf "$scratch/$asset" -C "$scratch" "$binary"
  test -f "$scratch/$binary" && test ! -L "$scratch/$binary"
  install -m 755 "$scratch/$binary" "$target/$binary"
}

install_tool gitleaks/gitleaks 8.30.1 gitleaks_8.30.1_linux_x64.tar.gz \
  551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb gitleaks
install_tool rhysd/actionlint 1.7.12 actionlint_1.7.12_linux_amd64.tar.gz \
  8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8 actionlint
