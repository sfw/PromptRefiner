import openai

class PromptRefiner:
    def __init__(self, openai_client, system_instructions=None, model="o1-mini", temperature=1):
        self.openai_client = openai_client
        self.system_instructions = system_instructions or "You are a helpful assistant tasked with refining prompts."
        self.model = model
        self.temperature = temperature
        self.conversation = []

    def _call_ai(self, user_message=None):
        if user_message:
            self.conversation.append({"role": "user", "content": user_message})

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                temperature=self.temperature
            )
        except openai.BadRequestError as e:
            if "unsupported_value" in str(e) and "system" in str(e):
                # Model doesn’t support 'system' role; merge system message into user message
                system_msg = next((msg for msg in self.conversation if msg["role"] == "system"), None)
                if system_msg:
                    self.conversation = [msg for msg in self.conversation if msg["role"] != "system"]
                    if self.conversation and self.conversation[0]["role"] == "user":
                        self.conversation[0]["content"] = system_msg["content"] + "\n\n" + self.conversation[0]["content"]
                    else:
                        self.conversation.insert(0, {"role": "user", "content": system_msg["content"]})
                # Retry the API call without the system role
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation,
                    temperature=self.temperature
                )
            else:
                raise e  # Re-raise if the error isn’t related to 'system' role

        ai_text = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": ai_text})
        return ai_text

    def start_refinement(self, prompt_text):
        self.conversation = [{"role": "system", "content": self.system_instructions}]
        user_intro = (
            f"I have a prompt I want to refine:\n\n{prompt_text}\n\n"
            "Please ask clarifying questions or suggest improvements. "
            "We'll iterate until I'm satisfied, then produce a final refined prompt. "
            "Please provide the final refined prompt and only the final prompt. "
            "If no feedback or refinements were given, please just send back the original prompt."
        )
        self._call_ai(user_intro)
        return self._to_chatbot_messages()

    def continue_refinement(self, user_message):
        concat_user_message = (user_message + "\n\n" + 
            "If this doesn't appease you, please ask more clarifying questions or suggest improvements. "
            "We'll iterate until I'm satisfied, then you'll produce a final refined prompt. ")
        self._call_ai(user_message)
        return self._to_chatbot_messages()

    def finalize_refinement(self):
        # Extract the final refined prompt from the conversation (customize as needed)
        last_assistant_msg = next((msg for msg in reversed(self.conversation) if msg["role"] == "assistant"), None)
        return last_assistant_msg["content"] if last_assistant_msg else ""

    def _to_chatbot_messages(self):
        # Return messages for Gradio Chatbot with type='messages', excluding 'system'
        return [msg for msg in self.conversation if msg["role"] != "system"]