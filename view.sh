#!/bin/bash
# view <file> — instant local viewer. No server, no gallery, no manifest.
# images → your default viewer; video/audio → mpv (falls back to xdg-open).
f="$1"
[ -f "$f" ] || { echo "no such file: $f" >&2; exit 1; }
case "${f,,}" in
  *.png|*.jpg|*.jpeg|*.webp|*.gif|*.svg|*.pdf) xdg-open "$f" >/dev/null 2>&1 ;;
  *.mp4|*.webm|*.mov|*.mkv|*.avi)
    command -v mpv >/dev/null && setsid mpv --really-quiet "$f" >/dev/null 2>&1 &
      || setsid xdg-open "$f" >/dev/null 2>&1 &
    ;;
  *.mp3|*.wav|*.flac|*.m4a|*.ogg)
    command -v mpv >/dev/null && setsid mpv --really-quiet "$f" >/dev/null 2>&1 &
      || setsid xdg-open "$f" >/dev/null 2>&1 &
    ;;
  *) setsid xdg-open "$f" >/dev/null 2>&1 ;;
esac
echo "opened: $f"
