from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# 1. Load the Model
MODEL_NAME = "ProsusAI/finbert"
print(f"--- Loading AI Model: {MODEL_NAME} ---")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

print(f"Model Label Map: {model.config.id2label}") 
# This tells us if 0 is Positive or Negative (Crucial for debugging!)

def analyze_sentiment(headline):
    try:
        # 2. Tokenize
        inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # 3. Predict
        with torch.no_grad():
            outputs = model(**inputs)
            
        # 4. Get Probabilities
        probs = F.softmax(outputs.logits, dim=-1)
        
        # 5. Print Detailed Debugging Info
        print(f"\nAnalyzing: '{headline}'")
        labels = model.config.id2label
        
        # Loop through all 3 classes (Positive, Negative, Neutral)
        for i in range(len(labels)):
            label_name = labels[i]
            score = probs[0][i].item()
            print(f"  {label_name.upper()}: {score:.4f} ({score*100:.1f}%)")
            
        # Return the winner
        winner_idx = torch.argmax(probs).item()
        if score < 0.60:      # If the AI is less than 60% sure...
            label = "neutral" # Force it to be Neutral
        return labels[winner_idx], probs[0][winner_idx].item()

    except Exception as e:
        print(f"Error: {e}")
        return "Error", 0.0

if __name__ == "__main__":
    test_headlines = [
        "NVIDIA stocks are soaring as demand for AI chips explodes!",
        "NVIDIA profit rose by 50% this quarter.",  # SIMPLER positive sentence
        "The company reported a massive loss.",
    ]
    
    for text in test_headlines:
        analyze_sentiment(text)