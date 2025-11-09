# Aider Setup for New Repository

Step-by-step guide to configure Aider with Ollama for a new git repository.

## Prerequisites

- Ollama installed and running
- Model pulled: `ollama pull starcoder2:instruct` (or your preferred model)
- Aider installed: [install aider](https://aider.chat/docs/install.html)
- Git repository initialized

## Step 1: Navigate to Your Repository

```bash
cd /path/to/your/repo
```

## Step 2: Create `.aider.model.settings.yml`

This file controls Ollama's context window size (how much code/conversation it can remember).

Create the file in your repository root:

```yaml
- name: ollama_chat/starcoder2:instruct
  extra_params:
    num_ctx: 32768
```

**Explanation:**
- `num_ctx: 32768` = 32K token context window
- Higher = more memory, but your hardware (64GB RAM, 16GB VRAM) can handle it
- Adjust based on your model's max context (check with `ollama show starcoder2:instruct`)

## Step 3: Create `.aider.model.metadata.json`

This tells Aider about your model's capabilities.

```json
{
  "ollama_chat/starcoder2:instruct": {
    "max_tokens": 32768,
    "max_input_tokens": 32768,
    "max_output_tokens": 4096,
    "litellm_provider": "ollama_chat",
    "mode": "chat"
  }
}
```

**Explanation:**
- `max_input_tokens`: Must match `num_ctx` from settings file
- `max_output_tokens`: How long the model's responses can be (4K is standard)
- Change the model name if using a different model

## Step 4: Create `.aider.conf.yml`

This is the main configuration file that ties everything together.

```yaml
model: ollama_chat/starcoder2:instruct
model-metadata-file: .aider.model.metadata.json
model-settings-file: .aider.model.settings.yml
edit-format: whole
map-tokens: 4096
```

**Explanation:**
- `model`: Your Ollama model (format: `ollama_chat/model-name`)
- `edit-format: whole`: Replaces entire files (better for small-medium files)
- `map-tokens: 4096`: Repository map size (recommended max, don't increase)

## Step 5: (Optional) Add to `.gitignore`

Decide if you want to commit these configs or keep them local:

```bash
# Option A: Keep configs local (add to .gitignore)
echo ".aider*" >> .gitignore

# Option B: Commit configs (good for team consistency)
git add .aider*
```

## Step 6: Test Your Setup

Run aider:

```bash
aider
```

You should see:

```
Aider v0.86.1
Model: ollama_chat/starcoder2:instruct with whole edit format
Git repo: .git with X files
Repo-map: using 4096 tokens, auto refresh
```

✅ **No warnings** = correctly configured!

## Step 7: Basic Usage

```bash
# Start aider (auto-loads config)
aider

# Add specific files to chat context
/add src/main.py src/utils.py

# Ask aider to make changes
> "Add error handling to the parse_config function"

# See what files are in context
/ls

# Clear context
/clear

# Exit
/exit
```

## Customization Options

### For Different Models

Replace `starcoder2:instruct` with your model name in **all three config files**:
- `.aider.model.settings.yml`
- `.aider.model.metadata.json`
- `.aider.conf.yml`

### Adjusting Context Window

Check your model's max context:
```bash
ollama show your-model-name
```

Then adjust `num_ctx` and `max_input_tokens` to match (common values: 8192, 16384, 32768, 65536).

### Tuning for Speed vs. Context

**More speed, less context:**
```yaml
# In .aider.model.settings.yml
num_ctx: 8192

# In .aider.conf.yml
map-tokens: 2048
```

**More context, slower:**
```yaml
# In .aider.model.settings.yml
num_ctx: 65536

# In .aider.conf.yml
map-tokens: 4096  # Don't go higher!
```

### Edit Formats

In `.aider.conf.yml`, you can change `edit-format`:

- `whole`: Replaces entire files (best for small files, <500 lines)
- `diff`: Shows only changes (better for large files)
- `udiff`: Unified diff format (advanced)

## Troubleshooting

### "Repo-map: using 2048 tokens" (context not applied)

- Check that `.aider.model.settings.yml` exists and has correct `num_ctx`
- Verify all three config files are in the same directory as where you run `aider`
- Restart Ollama: `ollama serve` (in separate terminal)

### "Warning: map-tokens > 4096 is not recommended"

- Reduce `map-tokens` in `.aider.conf.yml` to 4096 or lower
- Higher values confuse the LLM with irrelevant code

### Model not found

- Check model is pulled: `ollama list`
- Verify model name format: `ollama_chat/model-name` (not just `model-name`)

### Slow performance

- Reduce `num_ctx` (try 16384 or 8192)
- Reduce `map-tokens` (try 2048)
- Use smaller model (e.g., `qwen2.5-coder:7b`)

## Recommended Models for Coding

| Model | Size | Context | Speed | Quality |
|-------|------|---------|-------|---------|
| `qwen2.5-coder:7b` | 7B | 32K | Fast | Good |
| `starcoder2:instruct` | 15B | 16K | Medium | Very Good |
| `codellama:34b` | 34B | 16K | Slow | Excellent |
| `deepseek-coder-v2:16b` | 16B | 64K | Medium | Excellent |

## Hardware Requirements (Your System)

- **RAM**: 64GB total (20GB used) = **44GB available** ✅
- **VRAM**: 16GB = Can run up to 34B models comfortably ✅
- **Recommended**: 7B-16B models for best speed/quality balance

## Advanced: Per-Project Model Selection

You can use different models for different repos by having different configs:

```bash
# Repo A: Fast model for quick edits
cd ~/repo-a
# .aider.conf.yml → qwen2.5-coder:7b

# Repo B: Powerful model for complex refactoring
cd ~/repo-b
# .aider.conf.yml → deepseek-coder-v2:16b
```

## Resources

- [Aider Documentation](https://aider.chat/docs/)
- [Ollama Models](https://ollama.com/library)
- [Aider GitHub](https://github.com/paul-gauthier/aider)

---

**Quick Reference:**

```bash
# Three config files needed:
.aider.conf.yml              # Main config
.aider.model.settings.yml    # Ollama context window
.aider.model.metadata.json   # Model capabilities

# Start aider:
aider

# Common commands:
/add <file>      # Add file to context
/drop <file>     # Remove file
/ls              # List files in context
/clear           # Clear all files
/help            # Show all commands
/exit            # Quit
```
