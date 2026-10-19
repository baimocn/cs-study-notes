#!/usr/bin/env python3
"""
Hermes Memory System - 安装脚本
自动将 hooks、MCP server、配置部署到 ~/.claude/ 目录。

用法:
  python install.py              # 安装到默认位置 (~/.claude/)
  python install.py --dry-run    # 预览安装内容，不实际写入
  python install.py --uninstall  # 卸载
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# Windows console encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
MEMORY_DIR = CLAUDE_DIR / "memory"
MCP_DIR = CLAUDE_DIR / "mcp-servers"
HOOKS_DIR = CLAUDE_DIR / "hooks"
VMEM_DIR = MCP_DIR / "vmem"

# 源文件映射
VMEM_FILES = ["store.py", "migrations.py", "backfill.py", "__init__.py", "config.py"]
HOOK_FILES = [
    "hermes-error-hook.py",
    "hermes-preference-hook.py",
    "hermes-profile-session-hook.py",
    "hermes-recall-hook.py",
    "hermes-introspect-hook.py",
    "hermes-review-hook.py",
    "_helper.py",
]
SERVER_FILE = "vmem-server.py"


def ensure_dirs():
    """创建必要目录。"""
    for d in [MEMORY_DIR, MCP_DIR, HOOKS_DIR, VMEM_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}")


def copy_vmem(src_dir: Path, dry_run: bool = False):
    """复制 vmem 核心模块。"""
    print(f"\n📦 安装 vmem 模块到 {VMEM_DIR}")
    for fname in VMEM_FILES:
        src = src_dir / "vmem" / fname
        dst = VMEM_DIR / fname
        if src.exists():
            if not dry_run:
                shutil.copy2(src, dst)
            print(f"  {'📋' if not dry_run else '📄'} {fname}")


def copy_server(src_dir: Path, dry_run: bool = False):
    """复制 MCP server。"""
    print(f"\n🔌 安装 MCP Server 到 {MCP_DIR}")
    src = src_dir / "server" / SERVER_FILE
    dst = MCP_DIR / SERVER_FILE
    if src.exists():
        if not dry_run:
            shutil.copy2(src, dst)
        print(f"  {'📋' if not dry_run else '📄'} {SERVER_FILE}")


def copy_hooks(src_dir: Path, dry_run: bool = False):
    """复制 hooks。"""
    print(f"\n🪝 安装 Hooks 到 {HOOKS_DIR}")
    for fname in HOOK_FILES:
        src = src_dir / "hooks" / fname
        dst = HOOKS_DIR / fname
        if src.exists():
            if not dry_run:
                shutil.copy2(src, dst)
            print(f"  {'📋' if not dry_run else '📄'} {fname}")


def update_mcp_config(dry_run: bool = False):
    """更新 .mcp.json 添加 vmem server。"""
    config_path = CLAUDE_DIR / ".mcp.json"
    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    servers = config.get("mcpServers", {})
    vmem_entry = {
        "command": "python",
        "args": [str(MCP_DIR / SERVER_FILE).replace("\\", "/")],
        "env": {},
    }

    if servers.get("vmem") == vmem_entry:
        print(f"\n✅ .mcp.json 已配置 vmem server")
        return

    servers["vmem"] = vmem_entry
    config["mcpServers"] = servers

    if not dry_run:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n{'📝' if not dry_run else '📄'} 更新 .mcp.json — 添加 vmem server")


def update_settings_hooks(dry_run: bool = False):
    """更新 settings.json 添加 Hermes hooks。"""
    settings_path = CLAUDE_DIR / "settings.json"
    if not settings_path.exists():
        print(f"\n⚠️  settings.json 不存在 — 跳过 hook 注册")
        print(f"   请手动在 Claude Code settings 中添加 hooks")
        return

    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    hooks = settings.get("hooks", {})

    # SessionStart hook
    session_start = hooks.get("SessionStart", [])
    profile_hook_cmd = f"python {str(HOOKS_DIR / 'hermes-profile-session-hook.py').replace(chr(92), '/')}"
    has_profile = any(
        profile_hook_cmd in str(entry) for entry in session_start
    )
    if not has_profile:
        session_start.append({
            "hooks": [{"async": True, "command": profile_hook_cmd, "shell": "powershell", "timeout": 5, "type": "command"}],
            "matcher": ""
        })
        hooks["SessionStart"] = session_start

    # SessionEnd hook
    session_end = hooks.get("SessionEnd", [])
    introspect_hook_cmd = f"python {str(HOOKS_DIR / 'hermes-introspect-hook.py').replace(chr(92), '/')}"
    has_introspect = any(
        introspect_hook_cmd in str(entry) for entry in session_end
    )
    if not has_introspect:
        session_end.append({
            "hooks": [{"async": True, "command": introspect_hook_cmd, "shell": "powershell", "timeout": 5, "type": "command"}],
            "matcher": ""
        })
        hooks["SessionEnd"] = session_end

    # UserPromptSubmit hook (preference)
    prompt_submit = hooks.get("UserPromptSubmit", [])
    pref_hook_cmd = f"python {str(HOOKS_DIR / 'hermes-preference-hook.py').replace(chr(92), '/')}"
    has_pref = any(pref_hook_cmd in str(entry) for entry in prompt_submit)
    if not has_pref:
        prompt_submit.append({
            "hooks": [{"async": True, "command": pref_hook_cmd, "shell": "powershell", "timeout": 5, "type": "command"}],
            "matcher": ""
        })
        hooks["UserPromptSubmit"] = prompt_submit

    # UserPromptSubmit hook (recall — auto-search related memories)
    recall_hook_cmd = f"python {str(HOOKS_DIR / 'hermes-recall-hook.py').replace(chr(92), '/')}"
    has_recall = any(recall_hook_cmd in str(entry) for entry in prompt_submit)
    if not has_recall:
        prompt_submit.append({
            "hooks": [{"async": True, "command": recall_hook_cmd, "shell": "powershell", "timeout": 5, "type": "command"}],
            "matcher": ""
        })
        hooks["UserPromptSubmit"] = prompt_submit

    settings["hooks"] = hooks

    if not dry_run:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    print(f"{'📝' if not dry_run else '📄'} 更新 settings.json — 注册 Hermes hooks")


def uninstall():
    """卸载 Hermes Memory System。"""
    print("🗑️  卸载 Hermes Memory System")
    for f in [VMEM_DIR / fn for fn in VMEM_FILES]:
        if f.exists():
            f.unlink()
            print(f"  删除 {f}")
    if VMEM_DIR.exists() and not any(VMEM_DIR.iterdir()):
        VMEM_DIR.rmdir()
    for f in [MCP_DIR / SERVER_FILE]:
        if f.exists():
            f.unlink()
            print(f"  删除 {f}")
    for f in [HOOKS_DIR / fn for fn in HOOK_FILES]:
        if f.exists():
            f.unlink()
            print(f"  删除 {f}")
    print("\n⚠️  .mcp.json 和 settings.json 中的配置未自动清理，请手动编辑")


def main():
    parser = argparse.ArgumentParser(description="Hermes Memory System 安装脚本")
    parser.add_argument("--dry-run", action="store_true", help="预览安装内容")
    parser.add_argument("--uninstall", action="store_true", help="卸载")
    args = parser.parse_args()

    src_dir = Path(__file__).parent

    if args.uninstall:
        uninstall()
        return

    print("🚀 Hermes Memory System 安装器")
    print(f"   目标: {CLAUDE_DIR}")

    ensure_dirs()
    copy_vmem(src_dir, args.dry_run)
    copy_server(src_dir, args.dry_run)
    copy_hooks(src_dir, args.dry_run)
    update_mcp_config(args.dry_run)
    update_settings_hooks(args.dry_run)

    if args.dry_run:
        print("\n📋 预览完成（未写入任何文件）")
    else:
        print("\n✅ 安装完成！")
        print("   请重启 Claude Code 以加载 MCP server 和 hooks")
        print(f"   数据库: {MEMORY_DIR / 'vmem.db'}")
        print(f"   模型: {HOME / 'bge-small-zh-v1.5'} (需自行下载)")


if __name__ == "__main__":
    main()
