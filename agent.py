from LLM import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from tools import calculator


class Agent:

    def run(self, user_input: str) -> str:

        # Load memory
        memory = load_memory()

        # First conversation (tool detection)
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        # First LLM response
        llm_response = chat(messages)

        # Check if a tool is requested
        tool_request = parse_tool_call(llm_response)

        # No tool required
        if tool_request is None:

            memory.append({
                "role": "user",
                "content": user_input
            })

            memory.append({
                "role": "assistant",
                "content": llm_response
            })

            save_memory(memory)

            return llm_response

        print("Tool Requested")

        # Execute tool
        tool_name = tool_request.get("tool")

        if tool_name == "calculator":

            expression = tool_request.get("expression", "")

            try:
                tool_result = calculator(expression)
            except Exception as e:
                tool_result = f"Calculator Error: {e}"

        else:
            tool_result = "Unknown tool."

        print("Observation:", tool_result)

        # Second conversation (final answer)
        final_messages = [
            {
                "role": "system",
                "content": """
You are a helpful AI assistant.

The calculator has already executed.

DO NOT call the calculator again.

DO NOT output JSON.

Use the calculator result to answer the user's original question naturally.

Example:

User:
What is 7*7?

Calculator Result:
49

Assistant:
The answer is 49.
"""
            },
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": f"Calculator Result: {tool_result}"
            }
        ]

        final_response = chat(final_messages)

        # Save memory
        memory.append({
            "role": "user",
            "content": user_input
        })

        memory.append({
            "role": "assistant",
            "content": final_response
        })

        save_memory(memory)

        return final_response