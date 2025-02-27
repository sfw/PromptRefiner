# PromptRefiner

PromptRefiner is a Python library designed to help users refine their prompts through iterative feedback from an AI model. It integrates seamlessly with [Gradio](https://gradio.app), providing a user-friendly modal interface for the refinement process. Whether you're crafting prompts for creative writing, technical queries, or any other purpose, PromptRefiner enhances clarity and effectiveness.

The library is compatible with any client that provides an interface similar to OpenAI's chat completions (e.g., with a `.chat.completions.create` method), offering flexibility in choosing your preferred AI model.

## Installation

To install PromptRefiner, you need Python 3.6 or higher and Gradio 3.0 or higher (due to the `Modal` component). Install it using pip:

```bash
pip install PromptRefiner
```

**Note**: The OpenAI client (or your preferred AI client) is not bundled with PromptRefiner and must be installed separately. For example:

```bash
pip install openai
```

## Usage

Here’s how to integrate PromptRefiner into your Gradio application:

1. **Import the necessary components**:

```python
import gradio as gr
from promptrefiner import add_prompt_refinement_modal
from openai import OpenAI  # or your preferred client
```

2. **Initialize your AI client** (e.g., OpenAI):

```python
openai_client = OpenAI(api_key="your_api_key_here")
```

3. **Set up your Gradio interface with the refinement modal**:

```python
with gr.Blocks() as demo:
    main_prompt = gr.Textbox(label="Enter your prompt here")
    components = add_prompt_refinement_modal(
        openai_client=openai_client,
        main_prompt_textbox=main_prompt,
        system_instructions="You are a helpful assistant that refines prompts.",
        model="01-mini",
        temperature=1
    )
    submit_btn = gr.Button("Submit")
    output = gr.Textbox(label="Output")
    submit_btn.click(fn=lambda x: f"Processed: {x}", inputs=main_prompt, outputs=output)

demo.launch()
```

This creates a Gradio interface with:
- A textbox for your initial prompt.
- A "Refine Prompt" button that opens a modal chat interface to refine the prompt with the AI.
- A "Submit" button to process the refined prompt (here, it simply echoes the result).

When you click "Refine Prompt," a modal opens for AI interaction. Clicking "Done Refining" updates the main textbox with the refined prompt.

### Configuration Options

Customize PromptRefiner via the `add_prompt_refinement_modal` function:

- **`openai_client`**: Your AI client instance (must have a `.chat.completions.create` method).
- **`main_prompt_textbox`**: The Gradio Textbox component for the initial prompt.
- **`system_instructions`**: Optional AI behavior instructions (e.g., "You are a concise editor"). **Note**: For models without `'system'` role support, these are merged into the first user message.
- **`model`**: The AI model (default: `'o1-mini'`). Check your client for supported models.
- **`temperature`**: Controls response randomness (default: `1`, range: 0–2). Lower values yield more predictable outputs.
- **`refine_button_label`**: Custom label for the refine button (default: `'Refine Prompt'`).

## Features

- **Iterative Refinement**: Refine prompts step-by-step via a conversational AI interface.
- **Gradio Integration**: Adds a modal chat interface to Gradio apps for seamless editing.
- **Model Flexibility**: Automatically adapts to models lacking `'system'` message support.
- **Conversation Context**: Maintains history for coherent multi-turn refinements.
- **User-Friendly**: Accessible to non-technical users through an intuitive chat interface.

## Model Compatibility

While optimized for OpenAI models, PromptRefiner works with any similar API client. For models that don’t support `'system'` messages (e.g., "o1-mini"), the library automatically merges system instructions into the user message, ensuring compatibility without extra effort.

## Troubleshooting

- **BadRequestError for `'system'` roles**: The library now handles this automatically. If issues persist, verify your model name and API key.
- **Debugging Tips**:
  - Ensure the model is accessible via your client.
  - Check your API key configuration.
  - Review console output for errors.

## License

PromptRefiner is released under the [MIT License](https://github.com/sfw/PromptRefiner/blob/main/LICENSE).

## Contributing

We welcome contributions! Here’s how to get involved:

- **Report Issues**: Open an issue on the [GitHub repository](https://github.com/sfw/PromptRefiner/issues).
- **Submit Pull Requests**: Fork the repo, make changes, and submit a pull request.

Your input helps improve PromptRefiner for everyone.

## Links

- **GitHub Repository**: [https://github.com/sfw/PromptRefiner](https://github.com/sfw/PromptRefiner)
- **Issue Tracker**: [https://github.com/sfw/PromptRefiner/issues](https://github.com/sfw/PromptRefiner/issues)
- **Documentation**: [https://github.com/sfw/PromptRefiner/wiki](https://github.com/sfw/PromptRefiner/wiki) (if available)

---

**Note**: PromptRefiner is in early development (version 0.1.0). Check the repository for updates or contribute to its growth.

---

**Created by**: Scott Francis Winder ([scott@hackedpodcast.com](mailto:scott@hackedpodcast.com))

---
