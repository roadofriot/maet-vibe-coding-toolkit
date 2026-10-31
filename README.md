# MindSparQ AI Engineering System (MAET v2.0) — Complete Universal IDE Package

**One-Time Installation. Automatically Active Across Antigravity, VS Code, VSCodium, Cursor & Gemini CLI.**

## Why v2.0 Works Automatically Without Manual Calling
When you run `./install-ubuntu.sh` (or `.\install-windows.ps1`), `maet.py` automatically wires your entire computer at the OS and IDE level:
1. **Global IDE Prompt Injection (`applyTo: "**"` & `alwaysApply: true`):**
   Installs `maet-global.instructions.md` directly into the global `User/prompts/` folder and patches `User/settings.json` for **Google Antigravity**, **VS Code**, **VSCodium**, and **Cursor IDE**. Every chat or coding session in any workspace automatically loads the framework.
2. **Home-Directory Root Inheritance:**
   Installs `~/AGENTS.md`, `~/CLAUDE.md`, `~/.cursorrules`, `~/.windsurfrules`, `~/.gemini/GEMINI.md`, `~/.gemini/antigravity/AGENTS.md`, and `~/.cursor/rules/maet-global.mdc`. Any project inside your home folder automatically inherits the rules.
3. **Complete 35 Skills + 5 Virtual Agents + 3 Native Antigravity Plugins:**
   Installs all 20 Essential Skills, 15 Advanced Skills, 5 Specialist Agent personas, and 3 native Antigravity plugin bundles into `~/.maet/` and `~/.gemini/antigravity/plugins/`.
4. **Zero-Touch MCP Auto-Configuration:**
   Automatically merges **Context7** and **Playwright MCP** into `~/.gemini/config/mcp_config.json`, `~/.gemini/antigravity/mcp_config.json`, and `~/.cursor/mcp.json`.

---

## One-Time Installation Commands

### Ubuntu Linux
```bash
unzip MAET-MindSparQ-AI-Engineering-Toolkit-v2.zip
cd MAET-MindSparQ-AI-Engineering-Toolkit-v2
chmod +x install-ubuntu.sh
./install-ubuntu.sh
```
*(Optional: Run `./install-ubuntu.sh --with-external` to also clone `obra/superpowers`, `stitch-skills`, `gemini-skills`, and `supabase-plugin` into `~/.maet/external/`.)*

### Windows 10 / 11 (PowerShell)
```powershell
Expand-Archive .\MAET-MindSparQ-AI-Engineering-Toolkit-v2.zip -DestinationPath .
cd .\MAET-MindSparQ-AI-Engineering-Toolkit-v2
.\install-windows.ps1
```
