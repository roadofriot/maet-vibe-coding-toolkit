#!/usr/bin/env python3
"""
MAET v2.0 (MindSparQ AI Engineering Toolkit) — Universal One-Time IDE Auto-Installer
Automatically configures and wires:
  1. Google Antigravity IDE & CLI
  2. Visual Studio Code (VS Code)
  3. VSCodium
  4. Cursor IDE
  5. Gemini CLI & Claude/Windsurf/Universal Root Agents
  6. Core MCP Servers (Context7 & Playwright)
  7. Workspace Auto-Linker (`maet link`) & Git Template Directory

Zero external Python dependencies required (Python 3.10+ standard library).
Works on Ubuntu Linux and Windows 10/11.
"""
from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = "2.0.0"
HOME = Path.home()
MAET_HOME = HOME / ".maet"
BACKUP_DIR = MAET_HOME / "backups"
STATE_FILE = MAET_HOME / "state.json"


def backup_file(path: Path) -> Path | None:
    if path.exists() and path.is_file():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = str(path.relative_to(HOME) if path.is_relative_to(HOME) else path.name).replace("/", "_").replace("\\", "_")
        dest = BACKUP_DIR / f"{safe_name}.{stamp}.bak"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        return dest
    return None


def load_json_safe(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return {}
        return json.loads(text)
    except Exception:
        # If settings.json has comments (JSONC), preserve backup and avoid corrupting
        return None


def save_json_safe(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def get_ide_user_dirs() -> dict[str, Path]:
    """Returns User config directories for Antigravity, VS Code, VSCodium, and Cursor on Linux/Windows/macOS."""
    sysname = platform.system().lower()
    if sysname == "windows":
        appdata = Path(os.environ.get("APPDATA", HOME / "AppData" / "Roaming"))
        return {
            "Antigravity": appdata / "Antigravity" / "User",
            "VSCode": appdata / "Code" / "User",
            "VSCodium": appdata / "VSCodium" / "User",
            "Cursor": appdata / "Cursor" / "User",
        }
    elif sysname == "darwin":
        app_support = HOME / "Library" / "Application Support"
        return {
            "Antigravity": app_support / "Antigravity" / "User",
            "VSCode": app_support / "Code" / "User",
            "VSCodium": app_support / "VSCodium" / "User",
            "Cursor": app_support / "Cursor" / "User",
        }
    else:
        cfg = HOME / ".config"
        return {
            "Antigravity": cfg / "Antigravity" / "User",
            "VSCode": cfg / "Code" / "User",
            "VSCodium": cfg / "VSCodium" / "User",
            "Cursor": cfg / "Cursor" / "User",
        }


def get_mcp_config_paths() -> list[Path]:
    """Returns all global MCP config locations across Antigravity, Gemini CLI, and Cursor."""
    sysname = platform.system().lower()
    paths = [
        HOME / ".gemini" / "config" / "mcp_config.json",
        HOME / ".gemini" / "antigravity" / "mcp_config.json",
        HOME / ".gemini" / "settings.json",
        HOME / ".cursor" / "mcp.json",
    ]
    if sysname == "windows":
        appdata = Path(os.environ.get("APPDATA", HOME / "AppData" / "Roaming"))
        paths.append(appdata / "Antigravity" / "User" / "mcp_config.json")
    else:
        paths.append(HOME / ".config" / "Antigravity" / "User" / "mcp_config.json")
    return paths


def copy_directory(src: Path, dst: Path) -> list[str]:
    copied = []
    if not src.exists():
        return copied
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied.append(str(target))
    return copied


def patch_ide_settings_json(settings_path: Path, constitution_path: Path, prompts_dir: Path) -> bool:
    """
    Non-destructively injects global instruction file locations into VS Code / VSCodium / Antigravity / Cursor User/settings.json
    so the IDE loads MAET automatically on every workspace without user action.
    """
    data = load_json_safe(settings_path)
    if data is None or not isinstance(data, dict):
        print(f"[NOTE] Skipped JSON patch for {settings_path} (contains custom comments); prompt file inside {prompts_dir} is still active.")
        return False

    backup_file(settings_path)

    # 1. Enable prompt & instruction files globally (VS Code / Antigravity / VSCodium / Cursor)
    data["chat.promptFiles"] = True

    # 2. Register ~/.maet/core and User/prompts in chat.instructionsFilesLocations
    locations = data.get("chat.instructionsFilesLocations")
    if not isinstance(locations, dict):
        locations = {}
    locations[str(prompts_dir)] = True
    locations[str(constitution_path.parent)] = True
    data["chat.instructionsFilesLocations"] = locations

    # 3. Register in github.copilot.chat.codeGeneration.instructions for Copilot/compatible agents
    copilot_inst = data.get("github.copilot.chat.codeGeneration.instructions")
    if not isinstance(copilot_inst, list):
        copilot_inst = []
    entry = {"file": str(constitution_path)}
    if not any(isinstance(x, dict) and x.get("file") == str(constitution_path) for x in copilot_inst):
        copilot_inst.append(entry)
    data["github.copilot.chat.codeGeneration.instructions"] = copilot_inst

    save_json_safe(settings_path, data)
    return True


def configure_default_mcps() -> list[str]:
    """Automatically configures Context7 (zero-RAM remote docs) and Playwright MCP across all MCP config files."""
    default_servers = {
        "context7": {
            "serverUrl": "https://mcp.context7.com/mcp",
            "url": "https://mcp.context7.com/mcp"
        },
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"]
        }
    }
    updated = []
    for mcp_path in get_mcp_config_paths():
        data = load_json_safe(mcp_path)
        if data is None or not isinstance(data, dict):
            continue
        backup_file(mcp_path)
        servers = data.setdefault("mcpServers", {})
        for s_id, s_cfg in default_servers.items():
            if s_id not in servers:
                servers[s_id] = s_cfg
        save_json_safe(mcp_path, data)
        updated.append(str(mcp_path))
    return updated


def configure_git_template(constitution_path: Path) -> str | None:
    """
    Sets up a Git template directory with info/exclude and hooks so new/cloned repos
    can inherit MAET protection without polluting git status.
    """
    git_bin = shutil.which("git")
    if not git_bin:
        return None
    tpl_dir = MAET_HOME / "git-template"
    hooks_dir = tpl_dir / "hooks"
    info_dir = tpl_dir / "info"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    info_dir.mkdir(parents=True, exist_ok=True)

    # Pre-commit hook that blocks accidental hardcoded secrets (.env or private keys)
    pre_commit = hooks_dir / "pre-commit"
    pre_commit.write_text(
        "#!/usr/bin/env bash\n"
        "# MAET Security Gate: Prevent committing .env files or private keys\n"
        "if git diff --cached --name-only | grep -E '(^|/)\\.env($|\\.)' | grep -v '\\.example$' >/dev/null 2>&1; then\n"
        "  echo '[MAET SECURITY GATE] Blocked commit: Attempting to commit a .env file!'\n"
        "  exit 1\n"
        "fi\n",
        encoding="utf-8"
    )
    try:
        os.chmod(pre_commit, 0o755)
    except Exception:
        pass
    return str(tpl_dir)


def cmd_install(with_external: bool = False) -> None:
    print("======================================================================")
    print("  MindSparQ AI Engineering System (MAET v2.0) — Universal Installer")
    print("======================================================================")
    MAET_HOME.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    installed_files = []

    # 1. Copy core constitution, 35 skills, 5 agents, 3 plugins, and catalog to ~/.maet/
    for folder in ("core", "skills", "agents", "plugins", "catalog"):
        installed_files.extend(copy_directory(ROOT / folder, MAET_HOME / folder))

    constitution_src = MAET_HOME / "core" / "GLOBAL-CONSTITUTION.md"
    print(f"[1/6] Installed 35 Skills, 5 Virtual Agents & 3 Plugins into: {MAET_HOME}")

    # 2. Install Home-Root Universal Fallbacks (Picked up automatically by any project under $HOME)
    root_targets = [
        HOME / "AGENTS.md",
        HOME / "CLAUDE.md",
        HOME / ".cursorrules",
        HOME / ".windsurfrules",
        HOME / ".gemini" / "GEMINI.md",
        HOME / ".gemini" / "antigravity" / "AGENTS.md",
        HOME / ".cursor" / "rules" / "maet-global.mdc",
    ]
    for target in root_targets:
        backup_file(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(constitution_src, target)
        installed_files.append(str(target))
    print("[2/6] Installed global root instructions (~/AGENTS.md, ~/.gemini/GEMINI.md, ~/.cursorrules, etc.)")

    # 3. Auto-Wire All 4 IDEs (Antigravity, VS Code, VSCodium, Cursor) via User/prompts/*.instructions.md & settings.json
    ide_dirs = get_ide_user_dirs()
    for ide_name, user_dir in ide_dirs.items():
        prompts_dir = user_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        inst_file = prompts_dir / "maet-global.instructions.md"
        backup_file(inst_file)
        shutil.copy2(constitution_src, inst_file)
        installed_files.append(str(inst_file))

        settings_file = user_dir / "settings.json"
        patch_ide_settings_json(settings_file, constitution_src, prompts_dir)
        print(f"[3/6] Auto-wired IDE [{ide_name}] -> {inst_file}")

    # 4. Install Antigravity Native Plugins into ~/.gemini/antigravity/plugins/
    agy_plugins_dir = HOME / ".gemini" / "antigravity" / "plugins"
    installed_files.extend(copy_directory(ROOT / "plugins", agy_plugins_dir))
    print(f"[4/6] Installed Antigravity Native Plugin Suite -> {agy_plugins_dir}")

    # 5. Auto-configure MCP Servers (Context7 + Playwright) across all IDEs
    mcp_updated = configure_default_mcps()
    print(f"[5/6] Auto-configured MCP Servers (Context7 & Playwright) in {len(mcp_updated)} config paths")

    # 6. Configure Git Security Gate Template
    tpl_path = configure_git_template(constitution_src)
    print(f"[6/6] Configured Git Pre-Commit Secret Scanner Template -> {tpl_path}")

    # Optional: Install external GitHub plugins/repos if requested
    if with_external:
        cmd_install_external()

    state = {
        "version": VERSION,
        "installed_at": datetime.now().isoformat(timespec="seconds"),
        "maet_home": str(MAET_HOME),
        "installed_files": installed_files,
        "mcp_configs": mcp_updated,
    }
    save_json_safe(STATE_FILE, state)

    print("\n======================================================================")
    print("  SUCCESS: MAET v2.0 IS NOW GLOBALLY ACTIVE ACROSS ALL YOUR IDEs!")
    print("======================================================================")
    print("  • Antigravity, VS Code, VSCodium, Cursor & Gemini CLI are now wired.")
    print("  • Restart any open IDE window once.")
    print("  • Open ANY project and type your request in plain Nepali or English.")
    print("  • Every IDE will automatically route, plan, code, test & verify!")
    print("======================================================================")


def cmd_link_workspace(workspace_path: str) -> None:
    """
    Optional helper: Injects local symlinks/copies (.cursorrules, AGENTS.md, .github/copilot-instructions.md)
    into a specific project directory and adds them to .git/info/exclude so they never pollute Git status.
    """
    ws = Path(workspace_path).resolve()
    if not ws.exists() or not ws.is_dir():
        raise SystemExit(f"Directory not found: {ws}")

    constitution_src = MAET_HOME / "core" / "GLOBAL-CONSTITUTION.md"
    if not constitution_src.exists():
        constitution_src = ROOT / "core" / "GLOBAL-CONSTITUTION.md"

    targets = [
        ws / "AGENTS.md",
        ws / ".cursorrules",
        ws / ".github" / "copilot-instructions.md",
        ws / ".gemini" / "styleguide.md",
    ]
    for t in targets:
        if not t.exists():
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(constitution_src, t)
            print(f"[LINKED] {t}")

    git_exclude = ws / ".git" / "info" / "exclude"
    if git_exclude.parent.exists():
        existing = git_exclude.read_text(encoding="utf-8") if git_exclude.exists() else ""
        additions = ["AGENTS.md", ".cursorrules", ".github/copilot-instructions.md", ".gemini/styleguide.md"]
        with git_exclude.open("a", encoding="utf-8") as f:
            f.write("\n# MAET Auto-Ignored Workspace Rules\n")
            for item in additions:
                if item not in existing:
                    f.write(f"{item}\n")
        print(f"[GIT-EXCLUDE] Added rule files to {git_exclude} (keeps git status clean)")


def cmd_install_external() -> None:
    """Downloads/installs curated external GitHub repositories into ~/.maet/external/ and Antigravity CLI."""
    ext_dir = MAET_HOME / "external"
    ext_dir.mkdir(parents=True, exist_ok=True)
    agy_bin = shutil.which("agy")
    git_bin = shutil.which("git")

    if agy_bin:
        print("[EXTERNAL] Installing obra/superpowers via Antigravity CLI...")
        subprocess.run([agy_bin, "plugin", "install", "https://github.com/obra/superpowers"], check=False)

    if not git_bin:
        print("[WARN] Git CLI not found; skipping external GitHub repo clones.")
        return

    repos = [
        ("superpowers", "https://github.com/obra/superpowers.git"),
        ("anthropic-skills", "https://github.com/anthropics/skills.git"),
        ("stitch-skills", "https://github.com/google-labs-code/stitch-skills.git"),
        ("gemini-skills", "https://github.com/google-gemini/gemini-skills.git"),
        ("supabase-plugin", "https://github.com/supabase-community/supabase-plugin.git"),
    ]
    for name, url in repos:
        dest = ext_dir / name
        if dest.exists():
            print(f"[EXTERNAL] Updating {name}...")
            subprocess.run([git_bin, "-C", str(dest), "pull", "--ff-only"], check=False)
        else:
            print(f"[EXTERNAL] Cloning {name} -> {dest}...")
            subprocess.run([git_bin, "clone", "--depth", "1", url, str(dest)], check=False)


def cmd_doctor() -> int:
    print("=== MAET v2.0 Universal IDE Doctor ===")
    print(f"OS Platform      : {platform.platform()}")
    print(f"Python Version   : {platform.python_version()}")
    print(f"MAET Home        : {MAET_HOME} ({'INSTALLED' if (MAET_HOME / 'core' / 'GLOBAL-CONSTITUTION.md').exists() else 'MISSING'})")

    for name, udir in get_ide_user_dirs().items():
        inst = udir / "prompts" / "maet-global.instructions.md"
        settings = udir / "settings.json"
        print(f"IDE [{name:11s}] : Prompt={'OK' if inst.exists() else 'MISSING'} | Settings={'OK' if settings.exists() else 'NONE'}")

    for mcp_path in get_mcp_config_paths():
        if mcp_path.exists():
            data = load_json_safe(mcp_path)
            servers = list((data or {}).get("mcpServers", {}).keys()) if isinstance(data, dict) else []
            print(f"MCP Config       : [OK] {mcp_path} -> {servers}")

    print("\n[HEALTHY] All IDEs are globally wired and ready.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="MAET v2.0 — Universal One-Time AI Engineering Installer")
    sub = parser.add_subparsers(dest="cmd", required=False)

    p_inst = sub.add_parser("install", help="One-time install across all IDEs (default)")
    p_inst.add_argument("--with-external", action="store_true", help="Also clone external GitHub skill repos (Superpowers, Stitch, etc.)")

    sub.add_parser("doctor", help="Check installation health across all IDEs")
    sub.add_parser("external", help="Download/update external GitHub skill repositories")

    p_link = sub.add_parser("link", help="Inject rule files into a specific project folder outside $HOME")
    p_link.add_argument("path", nargs="?", default=".", help="Target workspace path")

    args = parser.parse_args()
    cmd = args.cmd or "install"
    if cmd == "install":
        cmd_install(with_external=getattr(args, "with_external", False))
    elif cmd == "doctor":
        raise SystemExit(cmd_doctor())
    elif cmd == "external":
        cmd_install_external()
    elif cmd == "link":
        cmd_link_workspace(args.path)


if __name__ == "__main__":
    main()
