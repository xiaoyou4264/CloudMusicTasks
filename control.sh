#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
用法：./control.sh <命令>

  start           启动后台调度器，首次启动时创建容器
  stop            停止后台调度器
  restart         重启后台调度器，容器不存在时创建并启动
  status          查看调度容器状态（含已停止）
  logs [--follow] 查看最近 100 行调度日志，可持续跟踪
  run             手动执行一轮已启用的账号任务，并按配置发送推送
  help            显示帮助

run 使用一次性容器，调度器停止时也能执行。请避开定时任务执行时段。
EOF
}

invalid_usage() {
    usage >&2
    exit 2
}

command_name=${1:-help}
case "$command_name" in
    help|-h|--help)
        [[ $# -le 1 ]] || invalid_usage
        usage
        exit 0
        ;;
    logs)
        [[ $# -eq 1 || ( $# -eq 2 && $2 == --follow ) ]] || invalid_usage
        ;;
    start|stop|restart|status|run)
        [[ $# -eq 1 ]] || invalid_usage
        ;;
    *)
        invalid_usage
        ;;
esac
shift

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
compose=(docker compose -f compose.yaml)
service=cloudmusictasks

case "$command_name" in
    start)
        exec "${compose[@]}" up -d "$service"
        ;;
    stop)
        exec "${compose[@]}" stop "$service"
        ;;
    restart)
        container_id=$("${compose[@]}" ps --all --quiet "$service")
        if [[ -z $container_id ]]; then
            exec "${compose[@]}" up -d "$service"
        fi
        exec "${compose[@]}" restart "$service"
        ;;
    status)
        exec "${compose[@]}" ps --all "$service"
        ;;
    logs)
        exec "${compose[@]}" logs --tail=100 "$@" "$service"
        ;;
    run)
        exec "${compose[@]}" run --rm --no-deps -T "$service" python index.py
        ;;
esac
