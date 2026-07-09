# Sync `.ai` To Other Repositories

## Vietnamese User Summary

Lệnh `ai-agent-sync` dùng `.ai` trong repo framework hiện tại làm nguồn chuẩn, rồi copy/đồng bộ sang repo khác.

## Usage

From any target repository:

```bash
ai-agent-sync
```

By default, this syncs `.ai`, checks all required tools, installs missing tools, and runs repo-local initialization when an init command is configured.
It also writes `.ai/runtime/mcp-servers.json` with MCP server commands scoped to the target repository.

To sync `.ai`, initialize tools, and generate native instructions plus Agent Skills for one agent in the current repository, pass the agent shortcut as the first argument:

```bash
ai-agent-sync cline
ai-agent-sync codex
ai-agent-sync cursor
ai-agent-sync copilot
ai-agent-sync claude
ai-agent-sync agy
```

`agy`, `ag`, `anti`, `antigravity`, `aantigravity`, and `gemini` all target Google Antigravity. `clause` is accepted as an alias for `claude`.

If you need to sync into a repository path whose folder name is the same as an agent shortcut, pass an explicit path such as `./cline` or `/path/to/cline`.

## Required Pre-Task MCP Memory Init

Created on: `2026-06-20`.

Agents must initialize MCP Memory before any coding, documentation, debugging, review, refactor, commit, or analysis task when the target repository does not already have `.ai/runtime/memory/memory.jsonl` and `.ai/runtime/mcp-servers.json`.

Preferred command from the target repository root:

```bash
ai-agent-sync --install-tools --yes
```

Fallback when `ai-agent-sync` is not in `PATH`:

```bash
bin/ai-agent-sync --install-tools --yes
```

The default MCP Memory init command in `.ai/registry/tool-bootstrap.json` creates:

```text
.ai/runtime/memory/memory.jsonl
```

The generated MCP runtime config must include an `mcp-memory` server with `MEMORY_FILE_PATH` scoped to that repo-local file. This prevents agents from accidentally using the package-global memory file.

Or pass a repository path:

```bash
ai-agent-sync /path/to/target-repo
```

Preview before writing:

```bash
ai-agent-sync /path/to/target-repo --dry-run
```

Only sync `.ai` and skip tool bootstrap:

```bash
ai-agent-sync /path/to/target-repo --no-tools
```

Merge without deleting extra files already in the target `.ai`:

```bash
ai-agent-sync /path/to/target-repo --no-delete
```

Check tools required by the synced framework:

```bash
ai-agent-sync --check-tools
```

Check tools for one skill:

```bash
ai-agent-sync --check-tools maintaining-existing-apis
```

Sync `.ai` and install missing tools for all skills:

```bash
ai-agent-sync /path/to/target-repo --install-tools --yes
```

Sync `.ai`, initialize tools, and generate native agent instruction files plus Agent Skills:

```bash
ai-agent-sync /path/to/target-repo --install-tools --yes --generate-adapters
```

Equivalent current-repo shortcut examples:

```bash
ai-agent-sync cline
ai-agent-sync copilot
ai-agent-sync agy
```

Sync `.ai` and install missing tools for one skill:

```bash
ai-agent-sync /path/to/target-repo --install-tools maintaining-existing-apis --yes
```

Install only CodeGraph for one skill:

```bash
ai-agent-sync /path/to/target-repo --install-tools maintaining-existing-apis --tool codegraph --yes
```

## Behavior

- Source defaults to this framework repo's `.ai` directory.
- Target defaults to the current working directory.
- Default mode is mirror sync: target `.ai` becomes an exact copy of the source `.ai`.
- If target `.ai` already exists, the command creates `.ai.backup.<timestamp>` before replacing it.
- Normal sync does not bootstrap tools. Use `--check-tools` or `--install-tools` explicitly.
- After an explicit successful tool detection/install, the command writes `.ai/runtime/mcp-servers.json`.
- For an explicit MCP Memory installation, the command creates `.ai/runtime/memory/memory.jsonl` and configures `MEMORY_FILE_PATH` in `.ai/runtime/mcp-servers.json`.
- Run `ai-agent-adapter-sync` after this command when you want native instruction files and Agent Skills for Codex, Cursor, Copilot, Claude, Cline, Antigravity, and cross-tool `AGENTS.md` consumers.
- Use `--no-delete` when a repo intentionally keeps local-only files inside `.ai`.
- Use `--no-tools` to suppress tool operations when composing commands that may otherwise include explicit tool options.
- Use `--no-tool-init` to install missing tools but skip repo-local initialization.
- `--check-tools` scans skill/workflow/rule text and reports missing runtime tools.
- `--install-tools` explicitly runs configured install commands for missing tools. Normal sync and agent shortcuts do not install or initialize tools automatically.
- `--tool <id>` limits check/install to a specific tool. It can be repeated.
- `--generate-adapters` runs `ai-agent-adapter-sync` after `.ai` sync and any explicitly requested tool operation, including native Agent Skills unless `ai-agent-adapter-sync --no-skills` is run separately.
- `--adapter-agent <id>` limits generated native instruction files to one agent target. It can be repeated.
- `--force-adapters` lets generated adapter files overwrite existing user-authored instruction files.

## Tool Install Configuration

The framework includes default npm installers in `.ai/registry/tool-bootstrap.json`:

- CodeGraph: `npm install -g @astudioplus/codegraph-mcp`
- MCP Memory: `npm install -g @modelcontextprotocol/server-memory`
- MCP Filesystem: `npm install -g @modelcontextprotocol/server-filesystem`
- MCP Git: `npm install -g @cyanheads/git-mcp-server`

You can override these defaults with environment variables or by editing `.ai/registry/tool-bootstrap.json`.

Configure install commands with environment variables:

```bash
export AI_CODEGRAPH_INSTALL_COMMAND='<your CodeGraph install command>'
export AI_MCP_MEMORY_INSTALL_COMMAND='<your MCP Memory install command>'
export AI_MCP_FILESYSTEM_INSTALL_COMMAND='<your MCP Filesystem install command>'
export AI_MCP_GIT_INSTALL_COMMAND='<your MCP Git install command>'
```

Or configure persistent commands in `.ai/registry/tool-bootstrap.json`. This file is synced to every target repo with the framework:

```json
{
  "codegraph": {
    "commands": ["codegraph", "codegraph-mcp", "codegraph-cli", "codegraph-daemon"],
    "install_command": "npm install -g @astudioplus/codegraph-mcp",
    "init_command": ""
  }
}
```

Configure per-repository initialization commands when a tool needs them:

```bash
export AI_CODEGRAPH_INIT_COMMAND='<your CodeGraph init/index command>'
export AI_MCP_MEMORY_INIT_COMMAND='<your MCP Memory repo bootstrap command>'
export AI_MCP_FILESYSTEM_INIT_COMMAND='<your MCP Filesystem repo bootstrap command>'
export AI_MCP_GIT_INIT_COMMAND='<your MCP Git repo bootstrap command>'
```

Example flow:

```bash
export AI_CODEGRAPH_INSTALL_COMMAND='npm install -g <your-codegraph-package>'
export AI_CODEGRAPH_INIT_COMMAND='codegraph-mcp --workspace {repo} --graph-only --run-tool codegraph_index_directory --tool-args {repo_tool_args}'
ai-agent-sync /path/to/target-repo
```

For the default `@astudioplus/codegraph-mcp` package, `ai-agent-sync` runs a one-shot `codegraph_index_directory` command to warm up CodeGraph for the target repo.

Supported init command placeholders:

- `{repo}`: shell-quoted absolute repository path.
- `{repo_json}`: JSON string of the absolute repository path.
- `{repo_tool_args}`: shell-quoted JSON object in the shape `{"path": "/path/to/repo"}`.

Supported tool checks:

- `codegraph`: checks `codegraph`, `codegraph-mcp`, `codegraph-cli`, or `codegraph-daemon` in `PATH`; installs default CodeGraph MCP when missing; initializes only when an init command is configured or a known CLI default exists.
- `mcp-memory`: checks `mcp-server-memory`; installs default MCP Memory server when missing; initializes repo-local memory at `.ai/runtime/memory/memory.jsonl`.
- `mcp-filesystem`: checks `mcp-server-filesystem`; installs default MCP Filesystem server when missing.
- `mcp-git`: checks `git-mcp-server`; installs default MCP Git server when missing.

## MCP Runtime Config

After tool bootstrap, `ai-agent-sync` writes:

```text
.ai/runtime/mcp-servers.json
```

This file contains MCP server commands for the synced repo. Example shape:

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "codegraph-mcp",
      "args": ["--workspace", "/path/to/repo"]
    },
    "mcp-filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["/path/to/repo"]
    },
    "mcp-memory": {
      "command": "mcp-server-memory",
      "args": [],
      "env": {
        "MEMORY_FILE_PATH": "/path/to/repo/.ai/runtime/memory/memory.jsonl"
      }
    }
  }
}
```

Use this file as the source for Codex/Cline/Cursor/Claude MCP configuration when the tool supports importing or copying MCP server entries.

## Global Command Setup

Preferred setup:

```bash
bin/ai-agent-sync --install-global
```

This creates symlinks for both commands:

```text
~/.local/bin/ai-agent-sync
~/.local/bin/ai-agent-adapter-sync
```

Use a custom bin directory when needed:

```bash
bin/ai-agent-sync --install-global --global-bin-dir /usr/local/bin
```

Create a symlink from this repo's script to a directory in `PATH`:

```bash
mkdir -p ~/.local/bin
ln -sf /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-sync ~/.local/bin/ai-agent-sync
ln -sf /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-adapter-sync ~/.local/bin/ai-agent-adapter-sync
```

Make sure `~/.local/bin` is in `PATH`.
