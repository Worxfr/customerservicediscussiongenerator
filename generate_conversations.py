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

def generate_prompt(domain, topic, language, customer_sentiment=None):
    # Add customer sentiment to the prompt if specified
    sentiment_instruction = ""
    if customer_sentiment:
        sentiment_instruction = f"The customer should express a {customer_sentiment} sentiment throughout the conversation. "
    
    # Adjust prompt based on language
    if language.startswith('ja-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (担当者: for agent and 顧客: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "担当者:" or "代理店:".
        """
    elif language.startswith('zh-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (客服: for agent and 客户: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "客服:".
        """
    elif language.startswith('ko-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (상담원: for agent and 고객: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "상담원:".
        """
    elif language.startswith('ar-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (الوكيل: for agent and العميل: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "الوكيل:".
        """
    elif language.startswith('de-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: for agent and Kunde: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:".
        """
    elif language.startswith('it-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agente: for agent and Cliente: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agente:".
        """
    elif language.startswith('es-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agente: for agent and Cliente: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agente:".
        """
    elif language.startswith('pt-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agente: for agent and Cliente: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agente:".
        """
    elif language.startswith('sv-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: for agent and Kund: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:".
        """
    elif language.startswith('da-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: for agent and Kunde: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:".
        """
    elif language.startswith('fi-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Asiakaspalvelija: for agent and Asiakas: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Asiakaspalvelija:".
        """
    elif language.startswith('nb-') or language.startswith('no-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: for agent and Kunde: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:".
        """
    elif language.startswith('pl-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: for agent and Klient: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:".
        """
    elif language.startswith('is-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Þjónustufulltrúi: for agent and Viðskiptavinur: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Þjónustufulltrúi:".
        """
    elif language.startswith('cy-'):
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Asiant: for agent and Cwsmer: for customer).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Asiant:".
        """
    else:
        base_prompt = f"""
        Create a realistic conversation between a mobile phone company customer service agent and a customer discussing {topic} in the domain of {domain}.
        The conversation should be natural, include typical greetings and closings, and demonstrate how the agent helps resolve the customer's issue.
        Format the conversation as a dialogue with clear speaker labels (Agent: and Customer:).
        The conversation should be in {language} language.
        Include some back-and-forth exchanges with the agent asking clarifying questions.
        Make the conversation between 60 and 600 seconds long if it were spoken aloud.
        {sentiment_instruction}
        DO NOT include any introductory text, metadata, or explanations before the conversation - start directly with "Agent:" or the equivalent in the target language.
        """
    return base_prompt

def invoke_bedrock(prompt, language, profile_name):
    session = boto3.Session(profile_name=profile_name)
    bedrock_runtime = session.client('bedrock-runtime')
    
    # Choose the appropriate model based on language
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response['body'].read().decode('utf-8'))
    return response_body['content'][0]['text']

def get_available_voices(language, profile_name):
    """Get all available voices for a language"""
    session = boto3.Session(profile_name=profile_name)
    polly = session.client('polly')
    
    # Map language codes to compatible Polly language codes
    language_map = {
        'zh-CN': 'cmn-CN',  # Map Chinese to Mandarin Chinese
        'ar-SA': 'arb',     # Map Arabic to Modern Standard Arabic
    }
    
    # Use mapped language code if available
    polly_language = language_map.get(language, language)
    
    try:
        response = polly.describe_voices(LanguageCode=polly_language)
        voices = response['Voices']
        
        # Separate male and female voices
        male_voices = [v['Id'] for v in voices if v['Gender'] == 'Male']
        female_voices = [v['Id'] for v in voices if v['Gender'] == 'Female']
        
        return {
            'male': male_voices if male_voices else ['Matthew'],  # Default if no male voices
            'female': female_voices if female_voices else ['Joanna']  # Default if no female voices
        }
    except Exception as e:
        print(f"Error getting voices for language {language}: {str(e)}")
        # Return default voices
        return {
            'male': ['Matthew'],
            'female': ['Joanna']
        }

def parse_conversation(text):
    """Parse conversation into agent and customer parts"""
    agent_parts = []
    customer_parts = []
    
    # Skip any metadata or introductory text before the actual conversation
    lines = text.split('\n')
    conversation_started = False
    actual_conversation_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is the start of the actual conversation
        if line.startswith("Agent:") or line.startswith("Customer:") or \
           line.startswith("Klant:") or line.startswith("Client:") or \
           line.startswith("Cliente:") or line.startswith("担当者:") or \
           line.startswith("顧客:") or line.startswith("고객:") or \
           line.startswith("상담원:") or line.startswith("客户:") or \
           line.startswith("客服:") or line.startswith("العميل:") or \
           line.startswith("الوكيل:") or line.startswith("代理店:") or \
           line.startswith("Kunde:") or line.startswith("Agente:") or \
           line.startswith("Kund:") or line.startswith("Klient:") or \
           line.startswith("Asiakaspalvelija:") or line.startswith("Asiakas:") or \
           line.startswith("Þjónustufulltrúi:") or line.startswith("Viðskiptavinur:") or \
           line.startswith("Agens:") or line.startswith("Pelanggan:") or \
           line.startswith("Asiant:") or line.startswith("Cwsmer:"):
            conversation_started = True
            
        if conversation_started:
            actual_conversation_lines.append(line)
    
    # Now process the actual conversation
    current_speaker = None
    current_text = ""
    
    # Identify the agent and customer labels based on the first few lines
    agent_label = "Agent:"
    customer_label = "Customer:"
    
    for line in actual_conversation_lines[:5]:  # Check first few lines
        if line.startswith("Klant:"):
            customer_label = "Klant:"
            agent_label = "Agent:"
        elif line.startswith("Client:"):
            customer_label = "Client:"
            agent_label = "Agent:"
        elif line.startswith("Cliente:"):
            customer_label = "Cliente:"
            agent_label = "Agent:"
        elif line.startswith("担当者:"):
            agent_label = "担当者:"
            customer_label = "顧客:"
        elif line.startswith("代理店:"):
            agent_label = "代理店:"
            customer_label = "顧客:"
        elif line.startswith("상담원:"):
            agent_label = "상담원:"
            customer_label = "고객:"
        elif line.startswith("客服:"):
            agent_label = "客服:"
            customer_label = "客户:"
        elif line.startswith("الوكيل:"):
            agent_label = "الوكيل:"
            customer_label = "العميل:"
        elif line.startswith("Kunde:"):
            customer_label = "Kunde:"
            agent_label = "Agent:"
        elif line.startswith("Agente:"):
            agent_label = "Agente:"
            customer_label = "Cliente:"
        elif line.startswith("Kund:"):
            customer_label = "Kund:"
            agent_label = "Agent:"
        elif line.startswith("Klient:"):
            customer_label = "Klient:"
            agent_label = "Agent:"
        elif line.startswith("Asiakaspalvelija:"):
            agent_label = "Asiakaspalvelija:"
            customer_label = "Asiakas:"
        elif line.startswith("Þjónustufulltrúi:"):
            agent_label = "Þjónustufulltrúi:"
            customer_label = "Viðskiptavinur:"
        elif line.startswith("Agens:"):
            agent_label = "Agens:"
            customer_label = "Pelanggan:"
        elif line.startswith("Asiant:"):
            agent_label = "Asiant:"
            customer_label = "Cwsmer:"
    
    for line in actual_conversation_lines:
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
    """Create separate audio files for agent and customer parts"""
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
    
    # Combine the parts using cat command for simplicity
    try:
        # Create a list of files in order
        files = []
        for i in range(max(len(agent_audio_files), len(customer_audio_files))):
            if i < len(agent_audio_files):
                files.append(agent_audio_files[i])
            if i < len(customer_audio_files):
                files.append(customer_audio_files[i])
        
        # Use cat to concatenate the files
        cmd = ["cat"] + files
        
        with open(base_output_file, 'wb') as outfile:
            subprocess.run(cmd, stdout=outfile, check=True)
        
        print(f"Combined audio saved to: {base_output_file}")
        
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
    
    try:
        for i in range(args.num_files):
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
                base_filename = f"{args.language}_{domain}_{timestamp}_{file_id}"
                
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
