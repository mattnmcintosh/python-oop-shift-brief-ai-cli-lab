import ollama
import copy

class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        cleaned_prompt = prompt.strip()
        user_message = {"role": "user", "content": cleaned_prompt}
        self.history.append(user_message)

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            
            # Extract content supporting both dictionary and object formats
            if isinstance(response, dict):
                message = response.get("message", {})
                if isinstance(message, dict):
                    content = message.get("content")
                else:
                    content = getattr(message, "content", None)
            else:
                message = getattr(response, "message", None)
                if isinstance(message, dict):
                    content = message.get("content")
                else:
                    content = getattr(message, "content", None)

            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("AI service request failed: empty content returned.")

            assistant_content = content.strip()
            self.history.append({"role": "assistant", "content": assistant_content})
            return assistant_content

        except Exception as e:
            if self.history and self.history[-1] == user_message:
                self.history.pop()
            raise RuntimeError(f"AI service request failed: {e}")

    def reset(self):
        self.history = []

    def message_count(self):
        return len(self.history)

    def get_transcript(self):
        return copy.deepcopy(self.history)