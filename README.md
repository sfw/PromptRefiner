# PromptRefiner Library

This Python library provides a modular approach to **iterative prompt refinement** using a chatbot-like flow. It supports two main components:

1. **`PromptRefiner` class**: A reusable class that manages a conversation with an OpenAI-like client, refining a user's prompt through iterative Q&A.
2. **`add_prompt_refinement_modal()`**: A Gradio-based function that adds a "Refine Prompt" button and a modal UI, allowing users to chat with the AI refiner directly in your Gradio app.

## Features

- **Iterative Prompt Refinement**: The user can refine their prompt by conversing with the AI, receiving clarifying questions, suggestions, and improvements.
- **Chatbot Integration**: Manages conversation state, automatically building Chatbot pairs for Gradio’s UI.
- **Easy Integration**: Just call `add_prompt_refinement_modal()` in your Gradio `Blocks`, pass it an OpenAI-like client, and bind to a prompt Textbox.
- **Configurable**: Customize system instructions, model, temperature, label text, etc.

---

## Installation

1. **Clone or Download** this repository.
2. Ensure you have the required dependencies (see [Dependencies](#dependencies)).
3. Place `prompt_refine_lib.py` in your project or install as a local package:

   ```
   pip install -e .
   ```
   (if you have a proper setup.py or if you organize this as a local library.)

## Usage

1. PromptRefiner Class
  Constructor:
    ```
    PromptRefiner(
      openai_client,
      system_instructions=None,
      model="o1-mini",
      temperature=1
    )
    ```

      - openai_client: An OpenAI-like client with a .chat.completions.create method.
      - system_instructions: Optional system message that sets the AI’s context.
      - model: Model name (e.g., "o1-mini").
      - temperature: Sampling temperature.

    Methods:
    - start_refinement(prompt_text): Clears old conversation and starts a new round with prompt_text. Returns Chatbot pairs for a Gradio Chatbot.
    - continue_refinement(user_message): Adds a user message, calls AI, returns updated Chatbot pairs.
    - finalize_refinement(): Tells AI we’re done refining; AI returns the final refined prompt.
    
    Attributes:
    - conversation: A list of dicts ({"role": "user"/"assistant", "content": ...}) capturing the entire chat.

2. add_prompt_refinement_modal() Function

    Simplifies embedding a “Refine Prompt” button & modal-based Chat UI in your Gradio app. It:
     1. Creates a PromptRefiner instance internally.
     2. Adds a Button labeled something like “Refine Prompt”.
     3. On click, spawns a Modal UI with a Chatbot, user input box, and “Send” / “Done” buttons.
     4. Finally overwrites the main prompt Textbox with the user’s final refined prompt.
  
    Signature:
    ```
    add_prompt_refinement_modal(
        blocks: gr.Blocks,
        openai_client,
        main_prompt_textbox: name_of_gr.Textbox,
        system_instructions=None,
        model="o1-mini",
        temperature=1,
        refine_button_label="Refine Prompt"
    )
    ```
  
    Returns:
    - refine_btn: the Gradio Button object
    - components_dict: a dictionary of references to the modal’s internal components (chatbot, send_btn, etc.) if needed

## Examples

1.	Basic Usage:
    ```
    import gradio as gr
    from openai import OpenAI
    from prompt_refine_lib import add_prompt_refinement_modal
    
    openai_client = OpenAI(api_key="YOUR_API_KEY_HERE")
    
    with gr.Blocks() as demo:
        # Some main prompt
        main_prompt_text = gr.Textbox(label="Main Prompt", lines=4)
        
        # Add the refinement button & modal
        refine_btn, comps = add_prompt_refinement_modal(
            blocks=demo,
            openai_client=openai_client,
            main_prompt_textbox=main_prompt_text,
            system_instructions="You help refine user's prompts. Keep it short.",
            model="o1-mini",
            temperature=1,
            refine_button_label="Refine This Prompt"
        )
    
        # Launch
        demo.launch()
    ```

2.	Refine Multiple Prompts:

  You can add multiple refinement modals for multiple prompt textboxes. Just call add_prompt_refinement_modal() for each, passing a different main_prompt_textbox.

## Dependencies
  - gradio
  - gradio_modal
  - openai (or similar client supporting .chat.completions.create)


## License

  This library is provided under an MIT License (or your chosen license). See LICENSE file for details.

