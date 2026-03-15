#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: extract-video-transcript.sh <url> [output_file]" >&2
  exit 1
}

log() {
  echo "[extract-video-transcript] $*" >&2
}

is_youtube() {
  case "$1" in
    *youtube.com/*|*youtu.be/*) return 0 ;;
    *) return 1 ;;
  esac
}

write_output() {
  local destination="$1"
  local content="$2"

  mkdir -p "$(dirname "$destination")"
  printf "%s\n" "$content" >"$destination"
}

run_summarize() {
  local url="$1"
  shift
  summarize "$url" "$@" 2>/dev/null
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
fi

if ! command -v summarize >/dev/null 2>&1; then
  echo "Missing required dependency: summarize" >&2
  exit 127
fi

URL="$1"
OUTPUT="${2:-/dev/stdout}"
YOUTUBE_ARGS=()

if is_youtube "$URL"; then
  YOUTUBE_ARGS=(--youtube auto)
fi

log "Attempting raw transcript extraction"
if result="$(run_summarize "$URL" "${YOUTUBE_ARGS[@]}" --extract)" && [[ ${#result} -gt 100 ]]; then
  write_output "$OUTPUT" "$result"
  exit 0
fi

if is_youtube "$URL"; then
  log "Attempting yt-dlp transcript extraction"
  if result="$(run_summarize "$URL" --youtube yt-dlp --extract)" && [[ ${#result} -gt 100 ]]; then
    write_output "$OUTPUT" "$result"
    exit 0
  fi
fi

log "Transcript extraction failed; falling back to summary"
if result="$(run_summarize "$URL" "${YOUTUBE_ARGS[@]}" --length xxl)" && [[ ${#result} -gt 50 ]]; then
  note=$'--- NOTE: This is an LLM-generated summary, not a raw transcript. ---\n--- Claims may be paraphrased or omitted; verify carefully. ---\n'
  write_output "$OUTPUT" "${note}
${result}"
  exit 0
fi

echo "Unable to extract transcript or summary for: $URL" >&2
exit 1
