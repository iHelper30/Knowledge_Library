# Natural Language Processing Basics

## Introduction

This tutorial introduces you to Natural Language Processing (NLP), covering fundamental concepts and practical implementations using Python.

## Prerequisites

- Python 3.8+
- Basic understanding of machine learning concepts
- Familiarity with Python programming

## Setup

1. Install required packages:
```bash
pip install nltk spacy transformers pandas numpy
```

2. Download required NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

## Core NLP Concepts

### 1. Text Preprocessing

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Sample text
text = "Natural Language Processing (NLP) is a branch of artificial intelligence that helps computers understand human language."

# Tokenization
tokens = word_tokenize(text)
print("Tokens:", tokens)

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
print("Filtered tokens:", filtered_tokens)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(token) for token in filtered_tokens]
print("Lemmatized:", lemmatized)
```

### 2. Part-of-Speech Tagging

```python
from nltk import pos_tag

# Tag parts of speech
tagged = pos_tag(tokens)
print("POS Tags:", tagged)
```

### 3. Named Entity Recognition (NER)

```python
import spacy

# Load English language model
nlp = spacy.load('en_core_web_sm')

# Process text
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")
```

## Advanced Topics

### 1. Text Classification

```python
from transformers import pipeline

# Load text classification pipeline
classifier = pipeline('sentiment-analysis')

# Analyze sentiment
text = "I love learning about NLP!"
result = classifier(text)
print(f"Sentiment: {result[0]['label']}, Score: {result[0]['score']:.2f}")
```

### 2. Text Generation

```python
from transformers import pipeline

# Load text generation pipeline
generator = pipeline('text-generation')

# Generate text
prompt = "Natural Language Processing is"
result = generator(prompt, max_length=50, num_return_sequences=1)
print("Generated text:", result[0]['generated_text'])
```

### 3. Text Summarization

```python
from transformers import pipeline

# Load summarization pipeline
summarizer = pipeline('summarization')

# Summarize text
long_text = """
[Your long text here...]
"""
summary = summarizer(long_text, max_length=130, min_length=30)
print("Summary:", summary[0]['summary_text'])
```

## Practical Applications

### 1. Building a Simple Chatbot

```python
def simple_chatbot(user_input):
    # Convert to lowercase
    user_input = user_input.lower()
    
    # Define simple responses
    responses = {
        'hello': 'Hi there! How can I help you?',
        'how are you': 'I\'m doing well, thank you!',
        'bye': 'Goodbye! Have a great day!',
        'default': 'I\'m not sure how to respond to that.'
    }
    
    # Return appropriate response
    for key in responses:
        if key in user_input:
            return responses[key]
    return responses['default']

# Test the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = simple_chatbot(user_input)
    print("Bot:", response)
```

### 2. Text Analysis Tool

```python
def analyze_text(text):
    # Process with spaCy
    doc = nlp(text)
    
    # Extract basic statistics
    stats = {
        'word_count': len([token for token in doc if not token.is_punct]),
        'sentence_count': len(list(doc.sents)),
        'entities': [(ent.text, ent.label_) for ent in doc.ents],
        'pos_tags': [(token.text, token.pos_) for token in doc]
    }
    
    return stats

# Example usage
text = "Apple Inc. is planning to release new iPhone models next year. The company's CEO, Tim Cook, made the announcement."
analysis = analyze_text(text)
print("Analysis Results:", analysis)
```

## Best Practices

1. Text Preprocessing
   - Always clean and normalize text
   - Handle special characters appropriately
   - Consider domain-specific requirements

2. Model Selection
   - Choose appropriate models for your task
   - Consider computational resources
   - Balance accuracy vs. speed

3. Evaluation
   - Use appropriate metrics
   - Consider multiple evaluation methods
   - Test with diverse data

## Exercises

1. Build a simple text classifier
2. Implement a basic text summarizer
3. Create a named entity extractor
4. Develop a keyword extraction tool

## Resources

- [NLTK Documentation](https://www.nltk.org/)
- [spaCy Documentation](https://spacy.io/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Stanford NLP Course](https://web.stanford.edu/class/cs224n/)

## Next Steps

1. Explore advanced NLP concepts:
   - Word embeddings
   - Attention mechanisms
   - Transfer learning

2. Practice with real-world projects:
   - Build a document classifier
   - Create a language translator
   - Develop a question-answering system

3. Study advanced frameworks:
   - PyTorch
   - TensorFlow
   - JAX
