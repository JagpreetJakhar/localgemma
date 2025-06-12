set -e
# Install uv (Python package manager from Astral)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Ollama (for running local language models)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the Gemma 3 4B model
ollama pull gemma3:4b

# Pull the BGE M3 567M embedding model
ollama pull bge-m3:567m

# Sync Python dependencies (requires uv project set up with pyproject.toml)
uv sync

