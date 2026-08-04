from transformers import pipeline
generator = pipeline("text-generation", model="qwen2.5-0.5b-Instruct"
)
message =[
    {
    "role":"user",
    "content":"""Classify the sentiment.
    Examples:
    sentences i love coorg!
    sent iment:POSITTVE
    sentences I hate flood in coorg!
    Sentiment:NEGATIVE
    Sentence: The cit is okay.
    Sentiment:NEUTRAL
    Now classify:
    Fentence: The pork in coorg is fantastic
    Sentiment:"""
    }
]
result = generator(
    message,
    max_new_tokens=20
)
print(result[0]["generated_text"][-1])