from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# Take input from user
sentence = input("The food was amazing and the service was excellent! I will definitely come back again. ")

prompt = f"""
Classify the sentiment of the following sentence as Positive, Neutral, or Negative.

Sentence: {sentence}
Sentiment:
"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=5)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\nPredicted Sentiment:", result)


