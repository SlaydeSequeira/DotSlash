import torch
from datasets import load_dataset
from transformers import MistralTokenizer, MistralForCausalLM, Trainer, TrainingArguments

# Load dataset
dataset = load_dataset('health_dataset')  # Replace with actual health-related dataset

# Tokenizer initialization
tokenizer = MistralTokenizer.from_pretrained("mistral_model_checkpoint")

def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# Tokenize dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Model initialization
model = MistralForCausalLM.from_pretrained("mistral_model_checkpoint")

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    tokenizer=tokenizer,
)

# Start fine-tuning
trainer.train()

# Save fine-tuned model
model.save_pretrained('./fine_tuned_mistral_model')
tokenizer.save_pretrained('./fine_tuned_mistral_model')

# Evaluate the model
results = trainer.evaluate(tokenized_datasets['test'])
print(results)
