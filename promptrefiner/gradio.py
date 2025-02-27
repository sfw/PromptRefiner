import gradio as gr
from gradio_modal import Modal

def add_prompt_refinement_modal(
    openai_client,
    main_prompt_textbox: gr.Textbox,
    system_instructions=None,
    model="o1-mini",
    temperature=1,
    refine_button_label="Refine Prompt"
):
    """
    Adds a 'Refine Prompt' button and modal chatbot to a Gradio interface.
    Must be called within a `with gr.Blocks():` context.

    Args:
        openai_client: OpenAI-like client with .chat.completions.create
        main_prompt_textbox: Gradio Textbox to refine and update
        system_instructions: Optional system message for the refiner
        model: Model name (default: "o1-mini")
        temperature: Model temperature (default: 1)
        refine_button_label: Label for the refine button (default: "Refine Prompt")

    Returns:
        tuple: (refine_btn, components_dict) where components_dict contains UI elements
    """
    from .refiner import PromptRefiner

    refiner = PromptRefiner(
        openai_client=openai_client,
        system_instructions=system_instructions,
        model=model,
        temperature=temperature
    )

    refine_btn = gr.Button(refine_button_label)

    with gr.Modal(visible=False, allow_user_close=True) as modal:
        gr.Markdown("### Prompt Refinement Chat")
        with gr.Column() as refine_chat_container:
            chatbot = gr.Chatbot(label="Refinement Chat")
            user_input = gr.Textbox(label="Your Message", lines=3)
            send_btn = gr.Button("Send")
            done_btn = gr.Button("Done Refining")

    # Start refinement when button is clicked
    def on_refine_click(prompt_text):
        chat_pairs = refiner.start_refinement(prompt_text)
        return chat_pairs

    refine_btn.click(fn=on_refine_click, inputs=main_prompt_textbox, outputs=chatbot)
    refine_btn.click(fn=lambda: gr.Modal(visible=True), inputs=None, outputs=modal)

    # Handle user message submission
    def on_user_send(user_msg):
        new_pairs = refiner.continue_refinement(user_msg)
        return "", new_pairs

    send_btn.click(fn=on_user_send, inputs=user_input, outputs=[user_input, chatbot])

    # Finalize refinement and update main prompt
    def on_done_refining():
        final_prompt = refiner.finalize_refinement()
        return final_prompt

    done_btn.click(fn=on_done_refining, inputs=None, outputs=main_prompt_textbox)
    done_btn.click(fn=lambda: gr.Modal(visible=False), inputs=None, outputs=modal)

    return refine_btn, {
        "modal": modal,
        "chat_container": refine_chat_container,
        "chatbot": chatbot,
        "send_btn": send_btn,
        "done_btn": done_btn,
        "refiner_instance": refiner
    }