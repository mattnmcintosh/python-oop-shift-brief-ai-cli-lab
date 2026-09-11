class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError("Shift notes cannot be empty.")

        sections_str = "\n".join([f"- {sec}" for sec in self.REQUIRED_SECTIONS])
        return (
            "Generate a shift handoff brief based on these notes.\n\n"
            f"Notes:\n{notes.strip()}\n\n"
            "Requirements:\n"
            "- Do not invent details not provided.\n"
            "- Use 'Unknown' for missing information.\n"
            f"Include these sections:\n{sections_str}"
        )

    def build_revision_prompt(self, feedback):
        if not isinstance(feedback, str) or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty.")

        sections_str = "\n".join([f"- {sec}" for sec in self.REQUIRED_SECTIONS])
        return (
            "Revise the previous shift handoff brief based on earlier conversation and this feedback:\n\n"
            f"Feedback:\n{feedback.strip()}\n\n"
            "Requirements:\n"
            "- Do not invent details.\n"
            f"Include these sections:\n{sections_str}"
        )

    def is_usable_brief(self, response_text):
        if not isinstance(response_text, str) or not response_text.strip():
            return False
        return all(section in response_text for section in self.REQUIRED_SECTIONS)

    def format_brief(self, response_text, is_revision=False):
        prefix = "\nRevised Shift Handoff Brief" if is_revision else "\nShift Handoff Brief"
        cleaned = response_text.strip()
        if cleaned.startswith("Shift Handoff Brief") or cleaned.startswith("Revised Shift Handoff Brief"):
            return f"\n{cleaned}"
        return f"{prefix}\n{cleaned}"

    def create_brief(self, ai_client, notes):
        prompt = self.build_brief_prompt(notes)
        response_text = ai_client.send(prompt)

        if not self.is_usable_brief(response_text):
            raise RuntimeError("AI response did not include required sections.")

        return self.format_brief(response_text, is_revision=False)

    def revise_brief(self, ai_client, feedback):
        prompt = self.build_revision_prompt(feedback)
        response_text = ai_client.send(prompt)

        if not self.is_usable_brief(response_text):
            raise RuntimeError("AI response did not include required sections.")

        return self.format_brief(response_text, is_revision=True)