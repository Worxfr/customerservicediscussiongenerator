#!/usr/bin/env python3
import argparse
import json
import random
import time
import uuid
import boto3
import os
import subprocess
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate customer service discussions using AWS services')
    parser.add_argument('--language', type=str, required=True, help='Language code (e.g., en-US, nl-NL, fr-FR)')
    parser.add_argument('--num_files', type=int, required=True, help='Number of discussion files to generate')
    parser.add_argument('--output_dir', type=str, default='./generated_conversations', help='Output directory for generated files')
    parser.add_argument('--profile', type=str, default='default', help='AWS profile name to use')
    parser.add_argument('--sentiment', type=str, choices=['neutral', 'angry', 'frustrated', 'excited', 'happy', 'sad', 'disappointed', 'confused'], 
                        help='Customer sentiment for the conversation')
    return parser.parse_args()

def get_domain_topics():
    return {
        "technical_support": [
            "network connectivity issues", 
            "device setup assistance", 
            "software updates", 
            "account access problems",
            "mobile app troubleshooting"
        ],
        "billing_inquiries": [
            "unexpected charges", 
            "payment methods", 
            "plan changes", 
            "billing cycle questions",
            "disputing fees"
        ],
        "plan_upgrades": [
            "data plan options", 
            "international roaming", 
            "family plan setup", 
            "promotional offers",
            "device upgrade eligibility"
        ],
        "account_management": [
            "adding new lines", 
            "changing personal information", 
            "account security", 
            "cancellation requests",
            "switching to paperless billing"
        ],
        "general_inquiries": [
            "store locations", 
            "coverage area questions", 
            "new customer onboarding", 
            "warranty information",
            "device trade-in process"
        ]
    }

def generate_prompt(domain, topic, language, customer_sentiment):
    """Generate a prompt for the conversation based on domain, topic, and language"""
    
    # Define language-specific prompts
    if language.startswith("en"):
        agent_label = "Agent"
        customer_label = "Customer"
        language_name = "English"
    elif language.startswith("fr"):
        agent_label = "Agent"
        customer_label = "Client"
        language_name = "French"
    elif language.startswith("de"):
        agent_label = "Agent"
        customer_label = "Kunde"
        language_name = "German"
    elif language.startswith("nl"):
        agent_label = "Agent"
        customer_label = "Klant"
        language_name = "Dutch"
    elif language.startswith("it"):
        agent_label = "Agente"
        customer_label = "Cliente"
        language_name = "Italian"
    elif language.startswith("es"):
        agent_label = "Agente"
        customer_label = "Cliente"
        language_name = "Spanish"
    elif language.startswith("pt"):
        agent_label = "Agente"
        customer_label = "Cliente"
        language_name = "Portuguese"
    elif language.startswith("ro"):
        agent_label = "Agent"
        customer_label = "Client"
        language_name = "Romanian"
    elif language.startswith("ja"):
        agent_label = "担当者"
        customer_label = "顧客"
        language_name = "Japanese"
    elif language.startswith("da"):
        agent_label = "Agent"
        customer_label = "Kunde"
        language_name = "Danish"
    elif language.startswith("fi"):
        agent_label = "Asiakaspalvelija"
        customer_label = "Asiakas"
        language_name = "Finnish"
    elif language.startswith("is"):
        agent_label = "Þjónustufulltrúi"
        customer_label = "Viðskiptavinur"
        language_name = "Icelandic"
    elif language.startswith("nb"):
        agent_label = "Agent"
        customer_label = "Kunde"
        language_name = "Norwegian"
    elif language.startswith("sv"):
        agent_label = "Agent"
        customer_label = "Kund"
        language_name = "Swedish"
    elif language.startswith("pl"):
        agent_label = "Agent"
        customer_label = "Klient"
        language_name = "Polish"
    elif language.startswith("cy"):
        agent_label = "Asiant"
        customer_label = "Cwsmer"
        language_name = "Welsh"
    else:
        agent_label = "Agent"
        customer_label = "Customer"
        language_name = "English"
    
    # Define sentiment instructions
    sentiment_instructions = ""
    if customer_sentiment == "angry":
        sentiment_instructions = f"The {customer_label} is angry and frustrated about their issue."
    elif customer_sentiment == "frustrated":
        sentiment_instructions = f"The {customer_label} is frustrated but trying to remain calm."
    elif customer_sentiment == "excited":
        sentiment_instructions = f"The {customer_label} is excited and enthusiastic, even when discussing issues."
    elif customer_sentiment == "happy":
        sentiment_instructions = f"The {customer_label} is happy and pleasant throughout the conversation."
    elif customer_sentiment == "sad":
        sentiment_instructions = f"The {customer_label} is sad and disappointed about their situation."
    elif customer_sentiment == "disappointed":
        sentiment_instructions = f"The {customer_label} is disappointed with the service they've received."
    elif customer_sentiment == "confused":
        sentiment_instructions = f"The {customer_label} is confused and needs extra explanation."
    else:
        sentiment_instructions = f"The {customer_label} has a neutral tone."
    
    # Create the prompt
    prompt = f"""
Create a realistic customer service conversation in {language_name} between a mobile company {agent_label} and a {customer_label} about {topic}.
The conversation should be between 60-600 seconds when spoken.
{sentiment_instructions}
Format the conversation as follows:
{agent_label}: [Agent's dialogue]
{customer_label}: [Customer's dialogue]
"""
    
    return prompt

def invoke_bedrock(prompt, language, profile_name):
    """Invoke AWS Bedrock to generate the conversation"""
    session = boto3.Session(profile_name=profile_name)
    bedrock = session.client('bedrock-runtime')
    
    # Define model parameters based on language
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # Prepare the request
    request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    # Invoke the model
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(request)
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        conversation = response_body['content'][0]['text']
        
        return conversation
    except Exception as e:
        raise Exception(f"Error invoking Bedrock: {str(e)}")

def get_available_voices(language, profile_name):
    """Get available voices for the specified language"""
    session = boto3.Session(profile_name=profile_name)
    polly = session.client('polly')
    
    try:
        response = polly.describe_voices(LanguageCode=language)
        
        # Group voices by gender
        male_voices = []
        female_voices = []
        
        for voice in response['Voices']:
            if voice['Gender'] == 'Male':
                male_voices.append(voice['Id'])
            else:
                female_voices.append(voice['Id'])
        
        return {
            'male': male_voices,
            'female': female_voices
        }
    except Exception as e:
        print(f"Error getting voices: {str(e)}")
        # Return some default voices as fallback
        return {
            'male': ['Matthew', 'Ruben', 'Remi'],
            'female': ['Joanna', 'Lotte', 'Celine']
        }

def parse_conversation(conversation):
    """Parse the conversation into agent and customer parts with improved handling"""
    agent_parts = []
    customer_parts = []
    
    lines = conversation.strip().split('\n')
    
    # Determine the labels used in this conversation
    agent_label = None
    customer_label = None
    
    # First pass: identify the labels used in the conversation
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for common agent patterns
        if line.startswith("Agent:"):
            agent_label = "Agent:"
            break
        elif line.startswith("Agente:"):
            agent_label = "Agente:"
            break
        elif line.startswith("担当者:"):
            agent_label = "担当者:"
            break
        elif line.startswith("代理店:"):
            agent_label = "代理店:"
            break
        elif line.startswith("Asiakaspalvelija:"):
            agent_label = "Asiakaspalvelija:"
            break
        elif line.startswith("Þjónustufulltrúi:"):
            agent_label = "Þjónustufulltrúi:"
            break
        elif line.startswith("Asiant:"):
            agent_label = "Asiant:"
            break
    
    # Second pass: identify customer label based on the conversation
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for common customer patterns
        if line.startswith("Customer:"):
            customer_label = "Customer:"
            break
        elif line.startswith("Client:"):
            customer_label = "Client:"
            break
        elif line.startswith("Cliente:"):
            customer_label = "Cliente:"
            break
        elif line.startswith("Kunde:"):
            customer_label = "Kunde:"
            break
        elif line.startswith("Klant:"):
            customer_label = "Klant:"
            break
        elif line.startswith("顧客:"):
            customer_label = "顧客:"
            break
        elif line.startswith("Asiakas:"):
            customer_label = "Asiakas:"
            break
        elif line.startswith("Viðskiptavinur:"):
            customer_label = "Viðskiptavinur:"
            break
        elif line.startswith("Cwsmer:"):
            customer_label = "Cwsmer:"
            break
    
    # If we couldn't determine the labels, try to infer them from the conversation structure
    if not agent_label or not customer_label:
        print("Warning: Could not determine conversation labels directly, trying to infer them")
        
        # Look for alternating patterns of speakers
        speaker_lines = []
        current_speaker = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts a new speaker turn
            colon_pos = line.find(':')
            if colon_pos > 0:
                potential_speaker = line[:colon_pos+1]
                if potential_speaker != current_speaker:
                    current_speaker = potential_speaker
                    speaker_lines.append(potential_speaker)
        
        # Count occurrences of each speaker label
        speaker_counts = {}
        for speaker in speaker_lines:
            if speaker not in speaker_counts:
                speaker_counts[speaker] = 0
            speaker_counts[speaker] += 1
        
        # Find the two most common speakers
        sorted_speakers = sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_speakers) >= 2:
            # Determine which is agent and which is customer based on common patterns
            speaker1, speaker2 = sorted_speakers[0][0], sorted_speakers[1][0]
            
            if "agent" in speaker1.lower() or "agente" in speaker1.lower():
                agent_label = speaker1
                customer_label = speaker2
            elif "customer" in speaker1.lower() or "client" in speaker1.lower() or "cliente" in speaker1.lower() or "klant" in speaker1.lower():
                customer_label = speaker1
                agent_label = speaker2
            else:
                # Default assumption: first speaker is agent
                agent_label = speaker1
                customer_label = speaker2
    
    # If we still couldn't determine the labels, use defaults
    if not agent_label:
        agent_label = "Agent:"
    if not customer_label:
        customer_label = "Client:" if "Client:" in conversation else "Customer:"
    
    print(f"Using labels: '{agent_label}' for agent and '{customer_label}' for customer")
    
    # Process the conversation line by line
    current_speaker = None
    current_text = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            # Add a space for empty lines if we're collecting text
            if current_speaker:
                current_text += "\n"
            continue
            
        # Check for speaker change
        if line.startswith(agent_label):
            # If we were collecting text for previous speaker, save it
            if current_speaker == "Customer" and current_text:
                customer_parts.append(current_text.strip())
                current_text = ""
            
            # Start collecting for agent
            current_speaker = "Agent"
            current_text = line.replace(agent_label, "").strip() + " "
        
        elif line.startswith(customer_label):
            # If we were collecting text for previous speaker, save it
            if current_speaker == "Agent" and current_text:
                agent_parts.append(current_text.strip())
                current_text = ""
            
            # Start collecting for customer
            current_speaker = "Customer"
            current_text = line.replace(customer_label, "").strip() + " "
        
        else:
            # Continue with current speaker
            if current_speaker:
                current_text += line + " "
    
    # Don't forget the last part
    if current_speaker == "Agent" and current_text:
        agent_parts.append(current_text.strip())
    elif current_speaker == "Customer" and current_text:
        customer_parts.append(current_text.strip())
    
    print(f"Parsed {len(agent_parts)} agent parts and {len(customer_parts)} customer parts")
    return agent_parts, customer_parts

def generate_speech(text, language, voice_id, output_file, profile_name, emotion=None):
    """Generate speech for a single part without SSML emotion tags"""
    session = boto3.Session(profile_name=profile_name)
    polly = session.client('polly')
    
    # Always use plain text, no SSML
    text_type = "text"
    
    try:
        # Try neural engine first for better quality
        try:
            response = polly.synthesize_speech(
                Engine='neural',
                LanguageCode=language,
                OutputFormat='mp3',
                Text=text,
                VoiceId=voice_id,
                TextType=text_type
            )
            
            # Save the audio stream directly to a local file
            if "AudioStream" in response:
                with open(output_file, 'wb') as file:
                    file.write(response['AudioStream'].read())
                return True
        except Exception as e:
            print(f"Neural engine failed for voice {voice_id}: {str(e)}")
            print("Trying standard engine...")
            
            # Try standard engine if neural failed
            response = polly.synthesize_speech(
                Engine='standard',
                LanguageCode=language,
                OutputFormat='mp3',
                Text=text,
                VoiceId=voice_id,
                TextType=text_type
            )
            
            # Save the audio stream directly to a local file
            if "AudioStream" in response:
                with open(output_file, 'wb') as file:
                    file.write(response['AudioStream'].read())
                return True
    except Exception as e:
        print(f"Error generating speech with voice {voice_id}: {str(e)}")
        return False

def create_conversation_audio_files(agent_parts, customer_parts, language, base_output_file, profile_name, customer_sentiment=None):
    """Create conversation audio by properly interleaving agent and customer parts"""
    # Get available voices for this language
    available_voices = get_available_voices(language, profile_name)
    
    # Randomly select different voices for agent and customer
    agent_gender = random.choice(['male', 'female'])
    customer_gender = 'female' if agent_gender == 'male' else 'male'
    
    # Make sure we have voices available
    if not available_voices[agent_gender] or not available_voices[customer_gender]:
        # If one gender has no voices, use different voices from the same gender
        if available_voices['male']:
            all_voices = available_voices['male']
        else:
            all_voices = available_voices['female']
            
        if len(all_voices) < 2:
            # If we have only one voice, duplicate it (not ideal but prevents errors)
            all_voices = all_voices * 2
            
        agent_voice = random.choice(all_voices)
        # Remove the agent voice from the list to ensure customer gets a different one
        remaining_voices = [v for v in all_voices if v != agent_voice]
        customer_voice = random.choice(remaining_voices)
    else:
        # Normal case: select from different gender pools
        agent_voice = random.choice(available_voices[agent_gender])
        customer_voice = random.choice(available_voices[customer_gender])
    
    print(f"Using voice {agent_voice} for agent and {customer_voice} for customer")
    
    # Map sentiment to emotion for speech synthesis
    customer_emotion = None
    if customer_sentiment:
        if customer_sentiment in ["angry", "frustrated"]:
            customer_emotion = "angry"
        elif customer_sentiment in ["excited", "happy"]:
            customer_emotion = "excited"
        elif customer_sentiment in ["sad", "disappointed"]:
            customer_emotion = "sad"
        print(f"Customer sentiment: {customer_sentiment}, mapped to emotion: {customer_emotion}")
    
    # Create temp directory for parts
    temp_dir = os.path.join(os.path.dirname(base_output_file), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Check if we have any parts to process
    if not agent_parts or not customer_parts:
        print("Warning: No conversation parts found to process")
        return False
    
    # Generate audio for each agent part (neutral)
    agent_audio_files = []
    for i, text in enumerate(agent_parts):
        if not text.strip():
            continue
        output_file = os.path.join(temp_dir, f"agent_{i}.mp3")
        if generate_speech(text, language, agent_voice, output_file, profile_name):
            print(f"Generated agent part {i+1}/{len(agent_parts)}")
            agent_audio_files.append(output_file)
    
    # Generate audio for each customer part (with emotion)
    customer_audio_files = []
    for i, text in enumerate(customer_parts):
        if not text.strip():
            continue
        output_file = os.path.join(temp_dir, f"customer_{i}.mp3")
        if generate_speech(text, language, customer_voice, output_file, profile_name, customer_emotion):
            emotion_text = f" with {customer_emotion} emotion" if customer_emotion else ""
            print(f"Generated customer part {i+1}/{len(customer_parts)}{emotion_text}")
            customer_audio_files.append(output_file)
    
    try:
        # Create a short silence file
        silence_file = os.path.join(temp_dir, "silence.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.5", "-q:a", "9", "-acodec", "libmp3lame", silence_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        
        # Directly concatenate the files using ffmpeg
        combined_file = base_output_file
        
        # Create a list of files to concatenate
        concat_files = []
        for i in range(max(len(agent_audio_files), len(customer_audio_files))):
            if i < len(agent_audio_files):
                concat_files.append(agent_audio_files[i])
                concat_files.append(silence_file)
            if i < len(customer_audio_files):
                concat_files.append(customer_audio_files[i])
                concat_files.append(silence_file)
        
        # Use ffmpeg to concatenate the files directly
        cmd = ["ffmpeg", "-y"]
        for file in concat_files:
            cmd.extend(["-i", file])
        
        # Add the filter complex to concatenate all inputs
        filter_complex = ""
        for i in range(len(concat_files)):
            filter_complex += f"[{i}:0]"
        filter_complex += f"concat=n={len(concat_files)}:v=0:a=1[out]"
        
        cmd.extend(["-filter_complex", filter_complex, "-map", "[out]", combined_file])
        
        # Execute the command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        print(f"Combined audio saved to: {combined_file}")
        
        # Clean up temp files
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        
        return True
    except Exception as e:
        print(f"Error combining audio files: {str(e)}")
        return False

def main():
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    audio_dir = os.path.join(args.output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    # Set customer sentiment
    customer_sentiment = args.sentiment
    if not customer_sentiment:
        # If not specified, randomly select one
        customer_sentiments = ["neutral", "angry", "frustrated", "excited", "happy", "sad", "disappointed", "confused"]
        customer_sentiment = random.choice(customer_sentiments)
    
    domain_topics = get_domain_topics()
    domains = list(domain_topics.keys())
    
    # Add delay between files to avoid throttling
    delay_between_files = 5  # seconds
    
    try:
        for i in range(args.num_files):
            # Add delay between files (except for the first one)
            if i > 0:
                print(f"Waiting {delay_between_files} seconds before generating next conversation...")
                time.sleep(delay_between_files)
                
            # Select random domain and topic
            domain = random.choice(domains)
            topic = random.choice(domain_topics[domain])
            
            # Generate random duration between 60 and 600 seconds
            target_duration = random.randint(60, 600)
            
            print(f"Generating discussion {i+1}/{args.num_files}: {domain} - {topic} (target duration: {target_duration}s)")
            print(f"Customer sentiment: {customer_sentiment}")
            
            # Generate the conversation
            try:
                prompt = generate_prompt(domain, topic, args.language, customer_sentiment)
                conversation = invoke_bedrock(prompt, args.language, args.profile)
                
                # Create unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_id = str(uuid.uuid4())[:8]
                base_filename = f"{args.language}_{domain}_{customer_sentiment}_{timestamp}_{file_id}"
                
                # Save text version
                text_filename = os.path.join(args.output_dir, f"{base_filename}.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(conversation)
                
                print(f"Text saved to: {text_filename}")
                
                # Parse conversation into agent and customer parts
                agent_parts, customer_parts = parse_conversation(conversation)
                
                # Generate conversation audio with alternating voices
                audio_filename = os.path.join(audio_dir, f"{base_filename}.mp3")
                try:
                    if create_conversation_audio_files(agent_parts, customer_parts, args.language, audio_filename, args.profile, customer_sentiment):
                        print(f"Conversation audio saved to: {audio_filename}")
                    else:
                        print(f"Failed to create conversation audio")
                except Exception as e:
                    print(f"Error creating conversation audio: {str(e)}")
            except Exception as e:
                print(f"Error generating conversation: {str(e)}")
                continue
            
            # Add some delay between requests to avoid rate limiting
            time.sleep(1)
        
        print(f"Generated {args.num_files} discussion files in {args.output_dir}")
        print(f"Text files are in: {args.output_dir}")
        print(f"Audio files are in: {audio_dir}")
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user. Partial results may have been saved.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
