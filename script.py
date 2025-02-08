from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
  base_url = "https://infer.e2enetworks.net/project/p-4817/genai/deepseek_r1/v1"
)

completion = client.chat.completions.create(
    model='deepseek_v3',
    messages=[{"role":"user","content":"Can you write a poem about open source machine learning?"}],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=1,
    stream=True
  )
    
for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


