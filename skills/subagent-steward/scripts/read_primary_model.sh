#!/bin/sh

fallback() {
    printf '%s\n' '{"status":"fallback","model":null,"effort":null,"routing_policy":"sol","source":"sol_policy","reason":"runtime_unavailable"}'
    exit 0
}

if [ "$#" -gt 1 ]; then
    fallback
fi

case "$0" in
    */*) script_dir=${0%/*} ;;
    *) script_dir=. ;;
esac
script_dir=$(CDPATH= cd "$script_dir" 2>/dev/null && pwd -P) || fallback
reader_path=$script_dir/read_primary_model.py
[ -f "$reader_path" ] || fallback

probe='import json, os, re, sqlite3, sys; from pathlib import Path; from typing import Mapping; sys.exit(0 if sys.version_info >= (3, 9) else 1)'
selected_python=

if [ "$#" -eq 1 ]; then
    case "$1" in
        /*) ;;
        *) fallback ;;
    esac
    [ -f "$1" ] && [ -x "$1" ] || fallback
    "$1" -B -c "$probe" >/dev/null 2>&1 || fallback
    selected_python=$1
else
    for name in python3 python; do
        candidate=$(command -v "$name" 2>/dev/null) || continue
        case "$candidate" in
            *WindowsApps*|*windowsapps*|*WINDOWSAPPS*) continue ;;
        esac
        [ -f "$candidate" ] && [ -x "$candidate" ] || continue
        if "$candidate" -B -c "$probe" >/dev/null 2>&1; then
            selected_python=$candidate
            break
        fi
    done
fi

[ -n "$selected_python" ] || fallback
output=$("$selected_python" -B "$reader_path" 2>/dev/null) || fallback
[ -n "$output" ] || fallback
printf '%s\n' "$output"
