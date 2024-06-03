# SolventGPT

Agent-based backend for SolventGPT. Includes a prototype Gradio UI.

## Install and run

Create a new python environment and install poetry.

```shell
python -m pip install poetry
```

Then install the required packaged with poetry

```shell
poetry install
```

Review the settings in `solventgpt/config.py` and/or export the relevant env variables.

Start the UI with the command

```shell
python -m solventgpt.app 
```

Start the fastapi server.

```shell
uvicorn solventgpt.app:app --host 0.0.0.0 --port 8080 --reload
```


