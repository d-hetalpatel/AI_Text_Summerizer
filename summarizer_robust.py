# summarizer_robust.py
from transformers import BartTokenizer, BartForConditionalGeneration
import textstat
import torch

print("⏳ Loading summarization model... please wait.")
tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")#("facebook/bart-large-cnn")#
model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")#("facebook/bart-large-cnn")#
print("✅ Model loaded successfully!")

MAX_TOKENS = 1024  # BART-large max tokens

def chunk_text_by_tokens(text, max_tokens=MAX_TOKENS):
    """Split text into chunks that fit the model token limit."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_len = 0

    for word in words:
        token_len = len(tokenizer.encode(word, add_special_tokens=False))
        if current_len + token_len > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_len = token_len
        else:
            current_chunk.append(word)
            current_len += token_len
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_text(text, max_words=130):
    if not text.strip():
        return {"error": "⚠️ Empty text provided!"}

    chunks = chunk_text_by_tokens(text)
    summaries = []

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=MAX_TOKENS)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=int(max_words * 1.3),
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary_text)

    final_summary = " ".join(summaries)

    return {
        "summary": final_summary,
        "original_length": len(text.split()),
        "summary_length": len(final_summary.split()),
        "readability": round(textstat.flesch_reading_ease(final_summary), 2)
    }

if __name__ == "__main__":
    sample_text = "Your very long text goes here..."
    result = summarize_text(sample_text)
    print("\n🧠 Summary:\n", result["summary"])
    print(f"\n📊 Original length: {result['original_length']} | Summary length: {result['summary_length']} | Readability: {result['readability']}")



