Below is a comprehensive `README.md` file for your `PromptRefiner` library, crafted based on the details provided in the `setup.py` file. This README includes an introduction, installation instructions, usage examples, configuration options, features, license information, contribution guidelines, and relevant links. It is designed to be clear, informative, and user-friendly, ensuring that both new and experienced users can understand and utilize the library effectively.

---

# PromptRefiner

PromptRefiner is a Python library designed to help users refine their prompts through iterative feedback from an AI model. It integrates seamlessly with [Gradio](https://gradio.app), providing a user-friendly modal interface for the refinement process. Whether you're crafting prompts for creative writing, technical queries, or any other purpose, PromptRefiner can assist in enhancing clarity and effectiveness.

The library is compatible with any client that provides an interface similar to OpenAI's chat completions (e.g., with a `.chat.completions.create` method), allowing flexibility in choosing your preferred AI model.

## Installation

To install PromptRefiner, you need Python 3.6 or higher. Install it using pip:

```bash
pip install PromptRefiner
```

This command will also install the required dependencies, including Gradio (version 3.0 or higher).

## Usage

To integrate PromptRefiner into your Gradio application, follow these steps:

1. **Import the necessary components**:

```python
import gradio as gr
from gradio_modal import Modal
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
    refine_btn, components = add_prompt_refinement_modal(
        openai_client=openai_client,
        main_prompt_textbox=main_prompt,
        system_instructions="You are a helpful assistant that refines prompts.",
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    submit_btn = gr.Button("Submit")
    output = gr.Textbox(label="Output")
    submit_btn.click(fn=lambda x: f"Processed: {x}", inputs=main_prompt, outputs=output)

demo.launch()
```

This example creates a Gradio interface with:
- A textbox for entering your initial prompt.
- A "Refine Prompt" button that opens a modal chat interface to refine the prompt with the AI.
- A "Submit" button to process the refined prompt (in this case, simply echoing it to an output textbox).

When you click "Refine Prompt," a modal opens where you can interact with the AI. Once satisfied, clicking "Done Refining" updates the main prompt textbox with the refined version.

### Configuration Options

Customize PromptRefiner by passing parameters to the `add_prompt_refinement_modal` function:

- **`openai_client`**: Your AI client instance (must have a `.chat.completions.create` method).
- **`main_prompt_textbox`**: The Gradio Textbox component for the initial prompt.
- **`system_instructions`**: Optional custom instructions for the AI (e.g., "You are a concise editor").
- **`model`**: The AI model to use (default: `'o1-mini'`).
- **`temperature`**: Controls the randomness of the AI's responses (default: `1`, range: 0–2).
- **`refine_button_label`**: Custom label for the refine button (default: `'Refine Prompt'`).

## Features

- **Iterative Refinement**: Refine prompts step-by-step through a conversational AI interface.
- **Gradio Integration**: Adds a modal chat interface to Gradio apps for seamless prompt editing.
- **Flexible Configuration**: Supports custom AI models, system instructions, and response settings.
- **Conversation History**: Automatically manages context for coherent AI responses.
- **Simple API**: Easy to integrate into existing Gradio projects.

## License

PromptRefiner is released under the [MIT License](https://github.com/sfw/PromptRefiner/blob/main/LICENSE). See the LICENSE file in the repository for details.

## Contributing

We welcome contributions to PromptRefiner! To get involved:

- **Report Issues**: Encounter a bug or have a suggestion? Open an issue on the [GitHub repository](https://github.com/sfw/PromptRefiner/issues).
- **Submit Pull Requests**: Want to improve the code? Fork the repo, make your changes, and submit a pull request.

Your feedback and contributions help make PromptRefiner better for everyone.

## Links

- **GitHub Repository**: [https://github.com/sfw/PromptRefiner](https://github.com/sfw/PromptRefiner)
- **Issue Tracker**: [https://github.com/sfw/PromptRefiner/issues](https://github.com/sfw/PromptRefiner/issues)
- **Documentation**: [https://github.com/sfw/PromptRefiner/wiki](https://github.com/sfw/PromptRefiner/wiki) (if available)

---

**Note**: PromptRefiner is in early development (version 0.1.0). While functional, future updates may introduce changes. Check the repository for the latest information.

---

**Created by**: Scott Francis Winder ([scott@hackedpodcast.com](mailto:scott@hackedpodcast.com))

---