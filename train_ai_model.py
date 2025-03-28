"""
AI Model Trainer for QR Code Content Analysis
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
from qr_nlp.exceptions import AIProcessingError

class QRAIModelTrainer:
    """Handles training and evaluation of QR content analysis models"""
    
    def __init__(self, base_model="bert-base-uncased"):
        """Initialize with base model"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(base_model)
            self.model = AutoModelForSequenceClassification.from_pretrained(base_model).to(self.device)
        except Exception as e:
            raise AIProcessingError(f"Model initialization failed: {str(e)}")

    def load_dataset(self, data_path: str):
        """Load and preprocess training data from CSV"""
        try:
            dataset = load_dataset('csv', data_files=data_path)
            return dataset.map(self._preprocess_data, batched=True)
        except Exception as e:
            raise AIProcessingError(f"Dataset loading failed: {str(e)}")

    def _preprocess_data(self, examples):
        """Tokenize text data for model input"""
        return self.tokenizer(examples["text"], truncation=True, padding="max_length")

    def train(self, dataset, epochs=3, batch_size=8, eval_split=0.1):
        """Train model with evaluation"""
        try:
            # Split dataset
            split = dataset["train"].train_test_split(eval_split)
            train_loader = torch.utils.data.DataLoader(split["train"], batch_size=batch_size)
            eval_loader = torch.utils.data.DataLoader(split["test"], batch_size=batch_size)
            
            # Training setup
            optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-5)
            self.model.train()
            
            # Training loop
            for epoch in range(epochs):
                total_loss = 0
                for batch in train_loader:
                    inputs = {k: v.to(self.device) for k, v in batch.items() 
                             if k in ['input_ids', 'attention_mask']}
                    outputs = self.model(**inputs, labels=batch['label'].to(self.device))
                    loss = outputs.loss
                    loss.backward()
                    optimizer.step()
                    optimizer.zero_grad()
                    total_loss += loss.item()
                
                # Evaluation
                eval_results = self.evaluate(eval_loader)
                print(f"Epoch {epoch+1} - Loss: {total_loss/len(train_loader):.4f}")
                print(f"Evaluation: {eval_results}")
            
            return self.model
        except Exception as e:
            raise AIProcessingError(f"Training failed: {str(e)}")

    def evaluate(self, dataloader):
        """Evaluate model performance"""
        self.model.eval()
        total_correct = 0
        total_samples = 0
        
        with torch.no_grad():
            for batch in dataloader:
                inputs = {k: v.to(self.device) for k, v in batch.items() 
                         if k in ['input_ids', 'attention_mask']}
                outputs = self.model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=-1)
                total_correct += (predictions == batch['label'].to(self.device)).sum().item()
                total_samples += len(batch['label'])
        
        return {
            "accuracy": total_correct / total_samples,
            "correct": total_correct,
            "total": total_samples
        }

if __name__ == "__main__":
    # Example usage
    trainer = QRAIModelTrainer()
    dataset = trainer.load_dataset("path/to/your/dataset.csv")
    trained_model = trainer.train(dataset)
    trained_model.save_pretrained("trained_qr_ai_model")