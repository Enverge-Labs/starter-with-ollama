import marimo

__generated_with = "0.14.7"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# Welcome to the Enverge""")
    return


@app.cell
def _():
    import base64
    from pathlib import Path
    gif = Path("./public/enable-ollama.gif").read_bytes()
    gif_base64 = base64.b64encode(gif).decode("utf-8")
    gif_url = f"data:image/gif;base64,{gif_base64}"
    return (gif_url,)


@app.cell(hide_code=True)
def _(mo, gif_url):
    mo.md(
        rf"""
    # Step 1.
    Enable the Ollama extension inside Enverge Lab. Here's how: 

    ![Enable Extension]({gif_url})
    """
    )
    return


@app.cell
def _():
    model_name = "llama3.2"
    return (model_name,)


@app.cell
def _(mo, model_name):
    # Taken from: https://github.com/ollama/ollama-python/blob/main/examples/pull.py
    from ollama import pull

    bars, completed_amounts = {}, {}

    for progress in pull(model_name, stream=True):
      digest = progress.get('digest', '')

      if not digest:
        continue

      if digest not in bars and (total := progress.get('total')):
        bars[digest] = mo.status.progress_bar(total=total).__enter__()
        completed_amounts[digest] = 0

      if completed := progress.get('completed'):
        # Calculate the increment since last update
        last_completed = completed_amounts.get(digest, 0)
        increment = completed - last_completed
        if increment > 0:
            bars[digest].update(increment=increment)
            completed_amounts[digest] = completed

    # Clean up progress bars
    for bar in bars.values():
        try:
            bar.__exit__(None, None, None)
        except:
            pass
    return


@app.cell
def _(model_name):
    from ollama import chat

    messages = [
      {
        'role': 'user',
        'content': 'Why is the sky blue?',
      },
    ]

    response = chat(model_name, messages=messages)
    print(response['message']['content'])
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
