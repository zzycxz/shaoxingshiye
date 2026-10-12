#!/usr/bin/env bash
# skill_plug.sh — 技能动态插拔：按需挂载/卸载到 ZCode、Codex、Claude Code 的 skill 目录。
# 默认不安装；要用时 plug，用完 unplug。两个平台的 skill 列表都是会话启动时扫描，
# 挂卸后在新会话生效；已发现技能可在设置→skills 面板用开关临时停用。
#
# 用法:
#   scripts/skill_plug.sh on [--root agents|zcode|claude]  挂载（默认 agents：ZCode、Codex 与 Claude Code 都识别）
#   scripts/skill_plug.sh off                           卸载（清除全部根上的挂载）
#   scripts/skill_plug.sh status                        查看各根挂载状态
#
# 注意: 禁止双挂。各宿主合并多根时不做同名去重（路径即身份），同一技能
# 挂两个根会在列表里出现两次；换根前先 off。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

SKILL_NAME="$(awk '/^name:[[:space:]]*/{print $2; exit}' "$SKILL_DIR/SKILL.md")"
if [ -z "$SKILL_NAME" ]; then
  echo "错误: 无法从 $SKILL_DIR/SKILL.md 读取 name" >&2
  exit 1
fi

CLAUDE_ROOT="$HOME/.claude/skills"
ZCODE_ROOT="$HOME/.zcode/skills"
AGENTS_ROOT="$HOME/.agents/skills"

realpath_of() {
  python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$1" 2>/dev/null
}

root_path() {
  case "$1" in
    claude) echo "$CLAUDE_ROOT" ;;
    zcode) echo "$ZCODE_ROOT" ;;
    agents) echo "$AGENTS_ROOT" ;;
    *) echo "错误: 未知根 $1（可选 agents|zcode|claude）" >&2; exit 1 ;;
  esac
}

# 返回目标根里 $SKILL_NAME 的状态: missing | linked_here | linked_elsewhere | real_entry
entry_state() {
  local root entry
  root="$1"
  entry="$root/$SKILL_NAME"
  if [ ! -e "$entry" ] && [ ! -L "$entry" ]; then
    echo "missing"
  elif [ -L "$entry" ]; then
    if [ "$(realpath_of "$entry")" = "$(realpath_of "$SKILL_DIR")" ]; then
      echo "linked_here"
    else
      echo "linked_elsewhere"
    fi
  else
    echo "real_entry"
  fi
}

cmd_on() {
  local target="agents"
  while [ $# -gt 0 ]; do
    case "$1" in
      --root) target="$2"; shift 2 ;;
      *) echo "用法: skill_plug.sh on [--root agents|zcode|claude]" >&2; exit 1 ;;
    esac
  done
  local dest root state
  dest="$(root_path "$target")"

  for root in zcode claude agents; do
    state="$(entry_state "$(root_path "$root")")"
    if [ "$root" != "$target" ] && [ "$state" = "linked_here" ]; then
      echo "错误: 已挂在 $(root_path "$root")——各平台多根不去重或互相遮蔽，会列两次。先 off 再 on --root $target" >&2
      exit 1
    fi
    if [ "$root" = "$target" ] && [ "$state" = "real_entry" ]; then
      echo "错误: $dest/$SKILL_NAME 是真实目录（非软链），不动它；请手动处理后重试" >&2
      exit 1
    fi
  done

  mkdir -p "$dest"
  if [ "$(entry_state "$dest")" = "linked_here" ]; then
    echo "已挂载: $dest/$SKILL_NAME -> $SKILL_DIR"
    return 0
  fi
  ln -s "$SKILL_DIR" "$dest/$SKILL_NAME"
  echo "挂载完成: $dest/$SKILL_NAME -> $SKILL_DIR"
  echo "提示: skill 列表在会话启动时扫描，新会话生效。"
}

cmd_off() {
  local root dest state removed=0
  for root in zcode claude agents; do
    dest="$(root_path "$root")"
    state="$(entry_state "$dest")"
    case "$state" in
      linked_here)
        rm "$dest/$SKILL_NAME"
        echo "已卸载: $dest/$SKILL_NAME"
        removed=1
        ;;
      linked_elsewhere)
        echo "跳过: $dest/$SKILL_NAME 是指向别处的软链（非本仓库），未动" ;;
      real_entry)
        echo "跳过: $dest/$SKILL_NAME 是真实目录（非软链），未动" ;;
    esac
  done
  [ "$removed" = 1 ] || echo "未发现本技能的挂载。"
}

cmd_status() {
  local root dest state marker
  echo "技能: $SKILL_NAME  ($SKILL_DIR)"
  for root in zcode claude agents; do
    dest="$(root_path "$root")"
    state="$(entry_state "$dest")"
    case "$state" in
      linked_here) marker="✅ 已挂载" ;;
      linked_elsewhere) marker="⚠️  被同名软链占用（指向别处）" ;;
      real_entry) marker="⚠️  被同名真实目录占用" ;;
      missing) marker="— 未挂载" ;;
    esac
    printf "  %-28s %s\n" "$root:" "$marker"
  done
}

case "${1:-}" in
  on) shift; cmd_on "$@" ;;
  off) cmd_off ;;
  status) cmd_status ;;
  *) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
