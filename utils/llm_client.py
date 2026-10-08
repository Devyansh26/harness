from openai import OpenAI
import config

endpoint = config.base_url

client = OpenAI(
    base_url=endpoint,
    api_key=config.api_key
)


