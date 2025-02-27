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
    from .refiner import PromptRefiner  # Adjust import based on your file structure

    refiner = PromptRefiner(
        openai_client=openai_client,
        system_instructions=system_instructions,
        model=model,
        temperature=temperature
    )

    refine_btn = gr.Button(refine_button_label)
    with Modal(visible=False, allow_user_close=True) as modal:
        gr.Markdown("### Prompt Refinement Chat")
        with gr.Column() as refine_chat_container:
            chatbot = gr.Chatbot(label="Refinement Chat", type="messages")
            user_input = gr.Textbox(label="Your Message", lines=3)
            send_btn = gr.Button("Send")
            done_btn = gr.Button("Done Refining")

    def on_refine_click(prompt_text):
        chat_messages = refiner.start_refinement(prompt_text)
        return gr.update(visible=True), chat_messages

    refine_btn.click(
        fn=on_refine_click,
        inputs=main_prompt_textbox,
        outputs=[modal, chatbot]
    )

    def on_user_send(user_msg):
        new_messages = refiner.continue_refinement(user_msg)
        return "", new_messages

    send_btn.click(
        fn=on_user_send,
        inputs=user_input,
        outputs=[user_input, chatbot]
    )

    def on_done_refining():
        final_prompt = refiner.finalize_refinement()
        return gr.update(visible=False), final_prompt

    done_btn.click(
        fn=on_done_refining,
        inputs=None,
        outputs=[modal, main_prompt_textbox]
    )

    return {
        "modal": modal,
        "chat_container": refine_chat_container,
        "chatbot": chatbot,
        "send_btn": send_btn,
        "done_btn": done_btn,
        "refiner_instance": refiner
    }