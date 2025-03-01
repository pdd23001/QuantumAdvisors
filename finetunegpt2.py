import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset

def fine_tune_gpt2(model_name="gpt2", dataset_name="wikitext", subset="wikitext-2-raw-v1", output_dir="./gpt2_finetuned"):
    # Load tokenizer and dataset
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token to EOS token

    dataset = load_dataset(dataset_name, subset)

    # Tokenization function
    def tokenize_function(examples):
        inputs = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
        inputs["labels"] = inputs["input_ids"].copy()  # Labels must match input_ids for causal LM
        return inputs

    # Apply tokenization
    tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

    # Load GPT-2 model for causal language modeling
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Resize token embeddings (important if pad token is added)
    model.resize_token_embeddings(len(tokenizer))

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=1,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        save_total_limit=2,
        load_best_model_at_end=True
    )

    # Trainer setup
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
    )

    # Train the model
    trainer.train()

    # Save final model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(f"Model fine-tuned and saved to {output_dir}")

# Run fine-tuning
fine_tune_gpt2()
print("fine tuning done!!")