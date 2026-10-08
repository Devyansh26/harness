from utils.llm_client import client
import config

response = client.responses.create(
    model=config.deployment_name,
    input="How to make maggi. give detailed steps.",
    stream = True
)

for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
print()