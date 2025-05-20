# Customer Service Discussion Generator

> [!WARNING]  
> ## ⚠️ Important Disclaimer
>
> **This project is for testing and demonstration purposes only.**
>
> Please be aware of the following:
>
> - Security measures may not be comprehensive or up to date.
> - The project may not comply with all best practices or organizational standards.
>
> Before using any part of this project in a production environment:
>
> 1. Thoroughly review and understand all code and configurations.
> 2. Conduct a comprehensive security audit.
> 3. Test extensively in a safe, isolated environment.
> 4. Adapt and modify the code to meet your specific requirements and security standards.
> 5. Ensure compliance with your organization's policies and any relevant regulations.
>
> The maintainers of this project are not responsible for any issues that may arise from the use of this code in production environments.
---

This tool generates realistic customer service discussions between a mobile company agent and a customer across various domains and languages. It uses AWS services to create high-quality content in both text and audio formats.

## Features

- Generate discussions in multiple European languages (including Dutch)
- Customize the number of discussions to generate
- Create conversations with different customer sentiments (angry, excited, sad, etc.)
- Realistic conversations across different customer service domains
- Variable conversation lengths (60-600 seconds)
- Output in both text and audio formats locally on your machine
- Uses AWS Bedrock for natural language generation
- Uses Amazon Polly for high-quality text-to-speech conversion
- Creates audio with different voices for agent and customer

## Prerequisites

- Python 3.6+
- AWS account with appropriate permissions
- AWS CLI configured with credentials
- Required Python packages: `boto3`

## Installation

1. Clone this repository or download the script files
2. Install required dependencies:

```bash
pip install boto3
```

3. Configure your AWS credentials:

```bash
aws configure
```

## Usage

### Generate a single conversation in a specific language:

```bash
python generate_conversations.py --language en-US --num_files 1 --profile your-profile-name
```

### Generate a conversation with a specific customer sentiment:

```bash
python generate_conversations.py --language en-US --num_files 1 --sentiment angry --profile your-profile-name
```

### Generate conversations in all supported languages:

```bash
python generate_all_languages_conversations.py --profile your-profile-name
```

Parameters:

- `--language`: Language code for the discussions (e.g., `en-US`, `nl-NL`, `fr-FR`)
- `--num_files`: Number of discussion files to generate
- `--output_dir`: (Optional) Output directory for generated files (default: `./generated_conversations`)
- `--profile`: (Optional) AWS profile name to use (default: `default`)
- `--sentiment`: (Optional) Customer sentiment for the conversation (choices: `neutral`, `angry`, `frustrated`, `excited`, `happy`, `sad`, `disappointed`, `confused`)

## Supported Languages

The script supports the following languages, with varying levels of compatibility:

### Fully Supported Languages

| Language Code | Description         | Text Generation | Audio Generation | Sentiment Support |
|--------------|---------------------|-----------------|------------------|------------------|
| en-US        | English (American)  | ✅ | ✅ | ✅ Full |
| en-GB        | English (British)   | ✅ | ✅ | ✅ Full |
| fr-FR        | French              | ✅ | ✅ | ✅ Full |
| de-DE        | German              | ✅ | ✅ | ⚠️ Basic |
| nl-NL        | Dutch               | ✅ | ✅ | ⚠️ Basic |
| it-IT        | Italian             | ✅ | ✅ | ⚠️ Basic |
| es-ES        | Spanish (European)  | ✅ | ✅ | ⚠️ Basic |
| pt-PT        | Portuguese (European) | ✅ | ✅ | ⚠️ Basic |
| ro-RO        | Romanian            | ✅ | ✅ | ⚠️ Basic |
| ja-JP        | Japanese            | ✅ | ✅ | ⚠️ Basic |
| da-DK        | Danish              | ✅ | ✅ | ❌ None |
| fi-FI        | Finnish             | ✅ | ✅ | ❌ None |
| is-IS        | Icelandic           | ✅ | ✅ | ❌ None |
| nb-NO        | Norwegian           | ✅ | ✅ | ❌ None |
| sv-SE        | Swedish             | ✅ | ✅ | ❌ None |
| pl-PL        | Polish              | ✅ | ✅ | ❌ None |
| cy-GB        | Welsh               | ✅ | ✅ | ❌ None |

**Sentiment Support Levels:**
- **Full**: Supports all sentiment expressions (angry, excited, sad, etc.) with neural voices
- **Basic**: Supports basic sentiment through text content but limited emotional expression in audio
- **None**: Sentiment is expressed only through text content; audio has no emotional variation

Note: For non-English languages, the script has been specifically optimized to handle the correct speaker labels in each language:
- Japanese: 担当者/顧客 or 代理店/顧客
- German: Agent/Kunde
- Italian: Agente/Cliente
- Spanish: Agente/Cliente
- Portuguese: Agente/Cliente
- Danish: Agent/Kunde
- Finnish: Asiakaspalvelija/Asiakas
- Icelandic: Þjónustufulltrúi/Viðskiptavinur
- Norwegian: Agent/Kunde
- Swedish: Agent/Kund
- Polish: Agent/Klient
- Welsh: Asiant/Cwsmer

## Customer Sentiments

You can generate conversations with different customer sentiments:

- `neutral`: Standard customer interaction
- `angry`: Customer is upset or frustrated
- `frustrated`: Customer is having difficulty resolving an issue
- `excited`: Customer is enthusiastic or happy
- `happy`: Customer is pleased with the service
- `sad`: Customer is disappointed or unhappy
- `disappointed`: Customer expected better service
- `confused`: Customer doesn't understand something

If no sentiment is specified, the script will randomly select one.

## Generated Content

The script generates discussions across the following domains:

1. Technical Support
   - Network connectivity issues
   - Device setup assistance
   - Software updates
   - Account access problems
   - Mobile app troubleshooting

2. Billing Inquiries
   - Unexpected charges
   - Payment methods
   - Plan changes
   - Billing cycle questions
   - Disputing fees

3. Plan Upgrades
   - Data plan options
   - International roaming
   - Family plan setup
   - Promotional offers
   - Device upgrade eligibility

4. Account Management
   - Adding new lines
   - Changing personal information
   - Account security
   - Cancellation requests
   - Switching to paperless billing

5. General Inquiries
   - Store locations
   - Coverage area questions
   - New customer onboarding
   - Warranty information
   - Device trade-in process

## Output Files

For each generated discussion, the script creates:

1. A text file (`.txt`) containing the conversation transcript in the main output directory
2. An audio file (`.mp3`) in the `audio` subdirectory of the output directory

The audio files feature:
- Different voices for the agent and customer
- Natural pauses between turns
- No narration or speaker labels (just the conversation)

File naming convention: `{language}_{domain}_{timestamp}_{uuid}.{extension}`

## AWS Services Used

- **Amazon Bedrock**: Generates natural, contextually relevant conversations with specified customer sentiments
- **Amazon Polly**: Converts text to lifelike speech using different voices for each speaker
- **AWS CLI**: Used for authentication and access to AWS services

## How It Works

1. The script generates a conversation text using Amazon Bedrock with specified customer sentiment
2. It parses the text to separate agent and customer parts
3. It queries Amazon Polly to get available voices for the specified language
4. It randomly selects different voices for the agent and customer (ensuring they're different)
5. It generates audio for each part of the conversation
6. It combines the parts with appropriate pauses to create a natural-sounding conversation
7. The final audio file contains only the conversation, without any narration or speaker labels

## Troubleshooting

Common issues:

1. **AWS credentials not found**: Ensure you've configured AWS CLI with `aws configure`
2. **Permission errors**: Verify your IAM user has permissions for Bedrock, Polly, and S3
3. **Language not supported**: Check the supported language list and use the correct language code
4. **Voice not available**: Some languages have limited voice options; the script will automatically select available voices
5. **Neural engine not supported**: For some voices, the script will automatically fall back to standard engine
## Troubleshooting

If you encounter issues when using the script, here are some common problems and their solutions:

### Audio Generation Issues

1. **No audio file generated**: 
   - Check that you have the necessary permissions for Amazon Polly
   - Verify that the language code is supported (see the Supported Languages section)
   - Ensure your AWS credentials are correctly configured

2. **Incomplete audio files**:
   - This may happen if the conversation parsing fails
   - Check that the conversation format follows the expected pattern
   - Try using a different sentiment or regenerating the conversation

3. **Voice quality issues**:
   - Some languages only support standard voices, not neural voices
   - The script automatically falls back to standard voices when needed
   - For best quality, use languages with neural voice support

### Text Generation Issues

1. **Incorrect language generation**:
   - Verify that AWS Bedrock supports the requested language
   - Check that the language code is correctly formatted (e.g., 'en-US', not 'en_US')
   - Try using a different model if available

2. **Conversation format issues**:
   - The script expects specific speaker labels based on the language
   - If the format is incorrect, try regenerating the conversation
   - For non-European languages, check that the correct speaker labels are used

### AWS Service Issues

1. **AWS credentials not found**:
   - Run `aws configure` to set up your credentials
   - Verify that the profile name is correct if using a non-default profile

2. **Permission errors**:
   - Ensure your IAM user has permissions for Bedrock and Polly
   - Check AWS CloudTrail for specific permission errors

3. **Rate limiting**:
   - If generating many conversations, you might hit AWS service limits
   - Add delays between requests or reduce the number of concurrent requests

## Advanced Usage

### Generating Conversations with Specific Sentiments

You can generate conversations with specific customer sentiments to create more diverse and realistic training data:

```bash
# Generate an angry customer conversation
python generate_conversations.py --language en-US --num_files 1 --sentiment angry --profile your-profile-name

# Generate an excited customer conversation
python generate_conversations.py --language fr-FR --num_files 1 --sentiment excited --profile your-profile-name

# Generate a sad customer conversation
python generate_conversations.py --language ja-JP --num_files 1 --sentiment sad --profile your-profile-name
```

### Batch Generation

To generate multiple conversations at once:

```bash
# Generate 5 conversations in English
python generate_conversations.py --language en-US --num_files 5 --profile your-profile-name

# Generate 3 conversations with different sentiments
python generate_conversations.py --language en-US --num_files 1 --sentiment angry --profile your-profile-name
python generate_conversations.py --language en-US --num_files 1 --sentiment excited --profile your-profile-name
python generate_conversations.py --language en-US --num_files 1 --sentiment sad --profile your-profile-name
```

### Custom Output Directory

You can specify a custom output directory for your generated conversations:

```bash
python generate_conversations.py --language en-US --num_files 1 --output_dir ./my_conversations --profile your-profile-name
```

### Generate Conversations in All Supported Languages

To generate conversations in all supported languages:

```bash
python generate_all_languages_conversations.py --profile your-profile-name
```

You can also specify a sentiment for all generated conversations:

```bash
python generate_all_languages_conversations.py --sentiment excited --profile your-profile-name
```

## Best Practices

1. **Start with a small number of files** to ensure everything is working correctly before generating larger batches.

2. **Test different sentiments** to create a diverse dataset that covers various customer scenarios.

3. **Use appropriate AWS credentials** with the minimum necessary permissions for security.

4. **Monitor your AWS usage** to avoid unexpected charges, especially when generating large numbers of conversations.

5. **Back up your generated conversations** regularly, especially if you're using them for training purposes.

6. **Check the audio quality** of generated conversations to ensure they meet your requirements.

7. **Use the latest version** of the script to benefit from improvements and bug fixes.
