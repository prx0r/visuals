#!/bin/bash
# view <file> — instant local viewer. No server, no gallery, no manifest.
# images → Falkon (existing instance = a tab, no RAM); video/audio → vlc;
# fallbacks ffplay → xdg-open. GUI env injected (IDE terminal has no DISPLAY).
f="$1"
[ -f "$f" ] || { echo "no such file: $f" >&2; exit 1; }
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/box/.Xauthority}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/1000}"
case "${f,,}" in
  *.png|*.jpg|*.jpeg|*.webp|*.gif|*.svg)
    if command -v falkon >/dev/null; then setsid falkon "$f" >/dev/null 2>&1 &
    elif command -v xdg-open >/dev/null; then setsid xdg-open "$f" >/dev/null 2>&1 &
    fi
    ;;
  *.pdf) setsid xdg-open "$f" >/dev/null 2>&1 ;;
  *.mp4|*.webm|*.mov|*.mkv|*.avi)
    if command -v vlc >/dev/null; then setsid vlc "$f" >/dev/null 2>&1 &
    elif command -v ffplay >/dev/null; then setsid ffplay -autoexit -reallyquiet "$f" >/dev/null 2>&1 &
    else setsid xdg-open "$f" >/dev/null 2>&1 &
    fi
    ;;
  *.mp3|*.wav|*.flac|*.m4a|*.ogg)
    if command -v vlc >/dev/null; then setsid vlc "$f" >/dev/null 2>&1 &
    elif command -v ffplay >/dev/null; then setsid ffplay -autoexit -reallyquiet "$f" >/dev/null 2>&1 &
    else setsid xdg-open "$f" >/dev/null 2>&1 &
    fi
    ;;
  *) setsid xdg-open "$f" >/dev/null 2>&1 ;;
esac
echo "opened: $f"
