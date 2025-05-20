#!/usr/bin/env python3
import subprocess
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate customer service discussions in all supported languages')
    parser.add_argument('--profile', type=str, default='default', help='AWS profile name to use')
    parser.add_argument('--output_dir', type=str, default='./generated_conversations', help='Output directory for generated files')
    parser.add_argument('--sentiment', type=str, choices=['neutral', 'angry', 'frustrated', 'excited', 'happy', 'sad', 'disappointed', 'confused'], 
                        help='Customer sentiment for the conversation')
    parser.add_argument('--audio-only', action='store_true', help='Only generate for languages with audio support')
    return parser.parse_args()

def get_supported_languages():
    """Returns a list of supported language codes with their descriptions"""
    # All languages are now fully supported
    supported_languages = {
        # European languages
        'en-GB': 'English (British)',
        'en-US': 'English (American)',
        'nl-NL': 'Dutch',
        'fr-FR': 'French',
        'de-DE': 'German',
        'it-IT': 'Italian',
        'pt-PT': 'Portuguese (European)',
        'es-ES': 'Spanish (European)',
        'da-DK': 'Danish',
        'fi-FI': 'Finnish',
        'is-IS': 'Icelandic',
        'nb-NO': 'Norwegian',
        'sv-SE': 'Swedish',
        'pl-PL': 'Polish',
        'ro-RO': 'Romanian',
        'cy-GB': 'Welsh',
        
        # Asian languages
        'ja-JP': 'Japanese',
    }
    
    return {
        'audio': supported_languages,
        'text': {},  # No text-only languages anymore
        'all': supported_languages
    }

def main():
    args = parse_arguments()
    
    # Get the list of supported languages
    languages = get_supported_languages()
    
    # Determine which languages to use
    if args.audio_only:
        selected_languages = languages['audio']
        print("Generating conversations for languages with audio support")
    else:
        selected_languages = languages['all']
        print("Generating conversations for all supported languages")
    
    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate a discussion for each language
    for lang_code, lang_name in selected_languages.items():
        print(f"\n{'='*50}")
        print(f"Generating discussion for {lang_name} ({lang_code})")
        print(f"{'='*50}")
        
        # Build the command
        cmd = [
            "python", "generate_conversations.py",
            "--language", lang_code,
            "--num_files", "1",
            "--profile", args.profile,
            "--output_dir", f"{args.output_dir}/{lang_code}"
        ]
        
        # Add sentiment if specified
        if args.sentiment:
            cmd.extend(["--sentiment", args.sentiment])
        
        # Execute the command
        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully generated discussion for {lang_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating discussion for {lang_name}: {e}")
    
    print("\nAll language discussions have been generated!")

if __name__ == "__main__":
    main()
