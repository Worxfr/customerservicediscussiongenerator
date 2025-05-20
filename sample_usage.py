#!/usr/bin/env python3
"""
Sample script demonstrating how to use the Customer Service Discussion Generator.
This script generates a conversation in English with an angry customer sentiment.
"""

import subprocess
import os

def main():
    # Define parameters
    language = "en-US"
    sentiment = "angry"
    output_dir = "./sample_output"
    profile = "default"  # Change this to your AWS profile
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Build the command
    cmd = [
        "python", "generate_conversations.py",
        "--language", language,
        "--num_files", "1",
        "--sentiment", sentiment,
        "--output_dir", output_dir,
        "--profile", profile
    ]
    
    # Execute the command
    try:
        print(f"Generating a sample conversation in {language} with {sentiment} sentiment...")
        subprocess.run(cmd, check=True)
        print(f"Sample conversation generated successfully in {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating conversation: {e}")

if __name__ == "__main__":
    main()
