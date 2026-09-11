from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        print("=== Shift Handoff Brief CLI ===")
        print(self.command_help())

    def command_help(self):
        return (
            "Available commands:\n"
            "  - brief <shift notes>\n"
            "  - revise <feedback>\n"
            "  - history\n"
            "  - reset\n"
            "  - help\n"
            "  - exit / quit"
        )

    def handle_command(self, raw_input):
        if not raw_input or not raw_input.strip():
            return "Input Error: Command cannot be blank."

        parts = raw_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        payload = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "brief":
                if not payload.strip():
                    return "Input Error: Shift notes cannot be empty."
                return self.brief_builder.create_brief(self.ai_client, payload)
            
            elif cmd == "revise":
                if not payload.strip():
                    return "Input Error: Revision feedback cannot be empty."
                return self.brief_builder.revise_brief(self.ai_client, payload)
            
            elif cmd == "history":
                count = self.ai_client.message_count()
                return f"Conversation messages count: {count}"
            
            elif cmd == "reset":
                self.ai_client.reset()
                return "Conversation history reset."
            
            elif cmd == "help":
                return self.command_help()
            
            elif cmd in ("exit", "quit"):
                self.running = False
                return "Goodbye!"
            
            else:
                return f"Input Error: Unknown command '{cmd}'. Type 'help' for guidance."

        except ValueError as e:
            return f"Input Error: {e}"
        except RuntimeError as e:
            return f"Service Error: {e}"

    def run(self):
        self.display_welcome()
        while self.running:
            try:
                user_input = input("\nshift-brief> ")
                response = self.handle_command(user_input)
                if response:
                    print(response)
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()