class PromptRefiner:
    """
    A reusable class that provides iterative prompt-refinement logic with an OpenAI-like client.
    Stores the conversation and produces Chatbot (user, AI) pairs for display.
    """

    def __init__(self, openai_client, system_instructions=None, model="o1-mini", temperature=1):
        self.openai_client = openai_client
        self.model = model
        self.temperature = temperature
        self.system_instructions = system_instructions or (
            "You are an AI that helps refine the user's prompt. "
            "Ask clarifying questions or suggest improvements until the user is satisfied. "
            "If you want any further information, please ask for it."
        )
        self.conversation = []

    def _call_ai(self, user_message=None):
        """
        Appends an optional user message, calls the AI, appends the AI response, and returns the AI text.
        """
        if user_message:
            self.conversation.append({"role": "user", "content": user_message})
        
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=self.conversation,
            temperature=self.temperature
        )
        ai_text = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": ai_text})
        return ai_text

    def start_refinement(self, prompt_text):
        """
        Starts a new refinement session with the user's prompt.
        Returns the chat as Chatbot pairs.
        """
        self.conversation = [{"role": "system", "content": self.system_instructions}]
        user_intro = (
            f"I have a prompt I want to refine:\n\n{prompt_text}\n\n"
            "Please ask clarifying questions or suggest improvements. "
            "We'll iterate until I'm satisfied, then produce a final refined prompt."
        )
        self._call_ai(user_intro)
        return self._to_chatbot_pairs()

    def continue_refinement(self, user_message):
        """
        Continues refinement with a new user message.
        Returns updated Chatbot pairs.
        """
        self._call_ai(user_message)
        return self._to_chatbot_pairs()

    def finalize_refinement(self):
        """
        Requests the final refined prompt from the AI.
        Returns the prompt text.
        """
        final_req = (
            "I am done refining. Please provide the final refined prompt "
            "and only the final prompt. If no feedback or refinements were given, "
            "please just send back the original prompt."
        )
        reply = self._call_ai(final_req)
        return self._extract_refined_prompt(reply)

    def _extract_refined_prompt(self, ai_text):
        """
        Extracts and returns the final prompt from the AI's response.
        """
        return ai_text

    def _to_chatbot_pairs(self):
        """
        Converts the conversation to a list of (user_text, ai_text) pairs for gr.Chatbot.
        Skips system messages.
        """
        pairs = []
        pending_user = None
        for msg in self.conversation:
            if msg["role"] == "system":
                continue
            elif msg["role"] == "user":
                pending_user = msg["content"]
            elif msg["role"] == "assistant":
                pairs.append((pending_user or "", msg["content"]))
                pending_user = None
        return pairs