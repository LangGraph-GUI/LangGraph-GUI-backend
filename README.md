# LangGraph-GUI-backend

The backend supports running LangGraph-GUI workflow json using localLLM such ollama.

For more infomation, please see official site: [LangGraph-GUI.github.io](https://LangGraph-GUI.github.io)

## Environment Setup

To install the required dependencies for LangGraph and server, run:
```bash
pip install -r requirements.txt
```

## Running the server

To run a local language model, first start Ollama in a separate terminal:
```bash
ollama serve
```

At another thread, up the server
```bash
mkdir src/workspace
cd src/workspace
python ../server.py
```
