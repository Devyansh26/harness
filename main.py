from utils.llm_client import client
import config
import json

from agent.loop import TOOLS, execute_tool

# response = client.responses.create(
#     model=config.deployment_name,
#     input="How to make maggi. give detailed steps.",
#     stream = True
# )

# for event in response:
#     if event.type == "response.output_text.delta":
#         print(event.delta, end="", flush=True)
# print()


MAX_STEPS = 10

def run_agent_loop(prompt : str) -> None:
    input_items = [{"role": "user", "content": prompt}]

    for step in range(MAX_STEPS):
        print(f"Step {step + 1}/{MAX_STEPS}")

        completed_response = None

        response = client.responses.create(
            model=config.deployment_name,
            input=input_items,
            tools=TOOLS,
            stream=True
        )

        for event in response:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            elif event.type == "response.completed":
                completed_response = event.response

        if completed_response is None:
            raise RuntimeError("No completed response received from the model.")

        input_items.extend(completed_response.output)

        tool_call = [
            item for item in completed_response.output if item.type == "function_call"
        ]

        if not tool_call :
            print()
            return

        print("tool calling starting...")

        for call in tool_call:
            print(f"tool called: {call.name}")
            
            arguments = json.loads(call.arguments)
            result = execute_tool(
                call.name,
                arguments
            )

            print(result)

            input_items.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result
            })  

    print("Maximum steps reached. Exiting the loop.")


if __name__ == "__main__":
    while True:

        prompt = input("Enter your prompt (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            break

        if not prompt.strip():
            print("Prompt cannot be empty. Please enter a valid prompt.")
            continue

        try:
            run_agent_loop(prompt)
        except Exception as e:
            print(f"An error occurred: {e}")
            