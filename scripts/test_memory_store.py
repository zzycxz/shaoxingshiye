#!/usr/bin/env python3
"""memory_store.py 冒烟测试：临时目录跑完整生命周期，无需第三方依赖。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "memory_store.py"


def run(*args: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, check=False,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {"raw": proc.stdout}
    return proc.returncode, payload


def check(name: str, cond: bool) -> None:
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        raise SystemExit(f"FAILED: {name}")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        env_note = f"SHAOXINGSHIYE_MEMORY_DIR={tmp}"
        os.environ["SHAOXINGSHIYE_MEMORY_DIR"] = tmp
        print(f"冒烟测试（{env_note}）:")

        code, out = run("status")
        check("未启用时 status 报不存在", code == 0 and out.get("exists") is False)

        code, out = run("apply", "--json", json.dumps(
            {"scope": "leader", "subject_id": "张总", "field": "风格", "value": "强势",
             "source_type": "user_report"}))
        check("未同意时写入被拒（NOT_INITIALIZED）", code == 1 and out["error"]["code"] == "NOT_INITIALIZED")

        code, _ = run("enable", "--confirm")
        check("enable --confirm 成功", code == 0)

        code, out = run("apply", "--json", json.dumps(
            {"scope": "leader", "subject_id": "张总", "field": "汇报偏好", "value": "结论先行",
             "source_type": "user_report"}))
        check("合法 leader 写入成功", code == 0 and out.get("ok") is True)

        code, out = run("apply", "--json", json.dumps(
            {"scope": "leader", "subject_id": "张总", "field": "风格", "value": "群里看着强势",
             "source_type": "records"}))
        check("来源门禁：records 不能进 leader（SOURCE_NOT_ELIGIBLE）",
              code == 1 and out["error"]["code"] == "SOURCE_NOT_ELIGIBLE")

        code, out = run("apply", "--json", json.dumps(
            {"scope": "event", "subject_id": "张总", "field": "猜测", "value": "他讨厌这个方案",
             "source_type": "assistant_inference"}))
        check("来源门禁：推断不能进 event", code == 1 and out["error"]["code"] == "SOURCE_NOT_ELIGIBLE")

        code, out = run("context", "--subject-id", "张总")
        check("context 返回已写入条目", code == 0 and out.get("count", 0) >= 1)

        code, out = run("undo")
        check("undo 成功", code == 0 and out.get("ok") is True)

        code, out = run("apply", "--json", json.dumps(
            {"scope": "leader", "subject_id": "张总", "field": "雷区", "value": "周五下午别找",
             "source_type": "user_report"}))
        check("重新写入一条用于失效测试", code == 0 and out.get("ok") is True)

        code, out = run("deactivate", "张总", "--confirm")
        check("deactivate 标注失效成功", code == 0 and out.get("ok") is True)
        code, out = run("show", "--subject-id", "张总")
        active = out.get("count", 0)
        code, out = run("show", "--subject-id", "张总", "--all")
        check("失效标注后 active 减少、--all 可见", active == 0 and out.get("count", 0) >= 1)

        code, out = run("forget-person", "张总", "--confirm")
        check("forget-person 成功", code == 0 and out.get("ok") is True)

        code, out = run("revoke", "--delete", "--confirm")
        check("revoke --delete 清库成功", code == 0 and out.get("deleted") is True)
        code, out = run("status")
        check("清库后 status 回到不存在", out.get("exists") is False)

    print("memory_store 冒烟测试全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
