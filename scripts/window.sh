# Window hook for .github/scripts/capture-windows.sh: foot runs the shared session
# from docs/PREVIEWS.md with each theme.
# Requires: foot, fastfetch, eza.
# shellcheck shell=bash
name=foot

launch() {
  printf '[main]\ninclude=%s\nfont=%s:size=11\npad=8x8\n' "$root/themes/kanagawa-$1.ini" "$font" >"$work/foot-$1.ini"
  printf 'foot -c %s -T kanagawa %s %s' "$work/foot-$1.ini" "$session" "$1"
}
