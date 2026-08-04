from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

messages = [
    {
        "role": "user",
        "content": """
Classify the sentiment.

Examples:
Sentence: I love Coorg!
Sentiment: POSITIVE

Sentence: I hate this product!
Sentiment: NEGATIVE

Sentence: The city is okay.
Sentiment: NEUTRAL

Now classify:

Sentence: The pork in Coorg is fantastic.
Sentiment:
"""
    }
]

result = generator(
    messages,
    max_new_tokens=20,
    do_sample=False
)

print(result[0]["generated_text"][-1]["content"])