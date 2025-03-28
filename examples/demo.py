from qr_nlp import (
    read_qr_from_image,
    generate_qr_code,
    process_qr_content
)
import os

def main():
    # Create sample QR code
    sample_text = "QR NLP is awesome! It combines QR detection with NLP processing."
    qr_path = "sample_qr.png"
    generate_qr_code(sample_text, qr_path)
    
    # Read and process the QR code
    if os.path.exists(qr_path):
        print("\n=== QR Code Detection ===")
        qr_text = read_qr_from_image(qr_path)
        print(f"Decoded Text: {qr_text}")
        
        print("\n=== NLP Processing ===")
        results = process_qr_content(qr_text)
        print(f"Language: {results['language']}")
        print(f"Sentiment: {results['sentiment']}")
        print(f"Keywords: {results['keywords']}")
        print(f"Summary: {results['summary']}")
        
        # Clean up
        os.remove(qr_path)
    else:
        print("Error: Failed to generate QR code")

if __name__ == "__main__":
    main()