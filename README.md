Shift Handoff Brief AI Tool
A modular, object-oriented Python command-line interface (CLI) application designed to assist property management and facilities operations teams in generating and revising structured shift handoff briefs using a local LLM via Ollama.
Architecture & Design
This application demonstrates a clean separation of concerns, decoupling user interaction, domain-specific prompt engineering, and external AI service communication across distinct layers:
CLI Presentation Layer (shift_cli.py): Manages the interactive terminal loop, parses user commands, handles input validation errors gracefully, and controls application state.
Domain/Builder Layer (brief_builder.py): Encapsulates business logic, builds structured prompt instructions requiring specific operational sections, and verifies that AI-generated responses meet structural quality standards before presentation.
Reusable AI Service Layer (ai_client.py): Manages API communication, conversation history tracking, response sanitization, and automatic rollback of failed message states on network errors.
Key Features
Modular Design: Fully decoupled components allowing independent unit testing and future reuse (e.g., migrating the AIClient and BriefBuilder to a web framework like Flask or FastAPI).
Required Operational Sections: Automatically enforces structural integrity for five key categories:
Shift Summary:
Open Issues:
Action Items:
Follow-Up Questions:
Risk Notes:
Robust Error Handling & State Recovery: Validates inputs, handles empty/blank queries, catches network outages, and rolls back failed user prompts from history.
Local LLM Integration: Interfaces natively with Ollama (llama3.2) to maintain data privacy and eliminate cloud API dependencies.
Prerequisites & Installation
Ensure Python 3.10+ is installed.
Install and run Ollama locally, ensuring the model is available:
Bash
ollama pull llama3.2
ollama serve




Install the required Python dependencies:
Bash
pip install ollama pytest




Usage & Command Reference
Run the interactive CLI application from your terminal:
Bash
python -m lib.shift_cli

Available Commands
Command
Description
Example
brief <notes>
Generates a new shift handoff brief from raw operational notes.
brief Register 2 froze during closing shift.
revise <feedback>
Modifies and improves the previous brief using manager feedback.
revise Make the action items more specific.
history
Displays the current conversation message count.
history
reset
Clears conversation history and resets context.
reset
help
Displays command guidance and usage instructions.
help
exit / quit
Terminates the CLI session.
exit

Running Tests
Execute the test suite using pytest to verify functionality across models, builders, and the CLI controller:
Bash
pytest

