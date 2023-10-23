import os
import openai
from typing import Dict
from tqdm import tqdm
import dotenv

from src.logger import get_console_logger
from src.paths import TRAINING_DATA_DIR

logger = get_console_logger()

dotenv.load_dotenv()

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_chat_data(prompt, num_responses=100):
    # Use the chat completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates Q&A datasets."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        n=num_responses,
        max_tokens=1500  # Adjust as necessary
    )
    
    return response.choices

# Construct the prompt for GPT-3.5
prompt = """
I will give you multiple sample prompts with a project section and a context section. Based on these examples, please generate 100 diverse and different examples following the same pattern. Make sure each generated example is unique and tailored to different real estate scenarios. Format the output as a Python list of dictionaries with keys: project and context.

# SAMPLE 1
# PROJECT
I am a real estate developer in California.
I am building a three-story house in the city.
What are the general code regulations for building a house in California?

# CONTEXT
All housing units need to be built with a bathroom.
New constructions in high-risk fire zones must use fire-resistant materials.
Seismic safety regulations require structures to be earthquake-resistant.

# SAMPLE 2
# PROJECT
I am considering renovating a historic building in downtown.
What are the preservation requirements and restrictions?

# CONTEXT
Historic buildings have designated preservation standards.
Any alterations require prior approval from the preservation committee.
Owners can receive tax incentives for maintaining the building's historic integrity.

# SAMPLE 3
# PROJECT
I am a contractor looking to build a commercial complex.
Are there specific zoning laws I should be aware of in California?

# CONTEXT
Zoning laws vary by city and region.
Commercial complexes might require additional parking space provisions.
Environmental impact assessments may be mandatory for large commercial projects.
"""

# Then, follow with the code to generate data and process responses.


#New constructions in high-risk fire zones must use fire-resistant materials.
#Seismic safety regulations require structures to be earthquake-resistant.
#Buildings above two stories need multiple exits for safety.
#Drainage systems must be in place to prevent water pooling on the property.
#Solar panel installations are encouraged with tax incentives for green energy adoption.
# Generate data
responses = generate_chat_data(prompt)

# Extract the generated examples from the response with tqdm progress bar
generated_examples = []
for choice in tqdm(responses, desc="Processing responses"):
    text = choice['message']['content'].strip()

    # Debugging: Print the content
    print(text)

    try:
        # Convert string to Python object (assuming model returns valid Python code)
        examples = eval(text)
        generated_examples.extend(examples)
    except SyntaxError:
        print("There was a syntax error in the model's response. Skipping this response.")

 
# Remove any Ellipsis items from generated_examples
generated_examples = [example for example in generated_examples if example is not Ellipsis]

PROMPT_TEMPLATE = """
You are an expert in California Building Codes and Regulations. I will give you some information about a building project, and you will tell me if it is compliant with the code. If it is not compliant, you will tell me how to make it compliant. If it is compliant, you will tell me how to make it better.

# PROJECT
{PROJECT}

# CONTEXT
{CONTEXT}

Please provide concrete advice in less than 100 tokens, and make sure it is compliant with the code. If you are unsure, please consult the code before answering. If you are still unsure, please ask for clarification.
"""

openai.api_key = os.environ["OPENAI_API_KEY"]

def build_prompt(example: Dict) -> str:

    return PROMPT_TEMPLATE.format(
        PROJECT=example["project"],
        CONTEXT=example['context'],
    )

def run():
   

    output = []
    for example in tqdm(generated_examples):
        
        prompt = build_prompt(example)
        logger.info(f'{prompt=}')

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=100,
        )

        response = response['choices'][0]['text']
        logger.info(f'{response=}')

        output.append({
            **example,
            'response': response
        })

    # save output as json file
    import json
    with open(TRAINING_DATA_DIR / 'training_data.json', 'w') as f:
        json.dump(output, f, indent=4)

if __name__ == '__main__':
    run()