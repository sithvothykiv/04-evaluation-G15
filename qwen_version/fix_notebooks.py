import json
import glob
import os

key = "sk-ws-H.DDLHEXI.SR82.MEYCIQCBSGAps6xCs3yyu7H1VMvOUNsD9FfYYx5bT-bIK7wfGgIhAL6jYaXGbSFx4q2WkO5cF4SwilWUnlmrSU3Jknvw8LKK"
new_client_str = f"openai_client = OpenAI(base_url='https://dashscope-intl.aliyuncs.com/compatible-mode/v1', api_key='{key}')\n"

for nb_path in glob.glob("/Users/kivsithvothy/Downloads/04-evaluation-G15/code/qwen_version/*.ipynb"):
    with open(nb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for cell in data.get("cells", []):
        if cell.get("cell_type") == "code":
            new_source = []
            for line in cell.get("source", []):
                # Swap model names
                line = line.replace("gpt-5.4-mini", "qwen-max")
                line = line.replace("qwen3.8-max", "qwen-max")
                
                # Replace empty OpenAI client with DashScope client
                if line.strip() == "openai_client = OpenAI()":
                    line = line.replace("openai_client = OpenAI()", new_client_str)
                
                # Fix the manual parse cell in 01-data-gen
                if "response = openai_client.responses.parse(" in line:
                    line = line.replace("openai_client.responses.parse(", "openai_client.chat.completions.create(")
                if 'input=messages' in line:
                    line = line.replace("input=messages", "messages=messages")
                if 'text_format=Questions' in line:
                    line = line.replace("text_format=Questions", "response_format={'type': 'json_object'}")
                if "response.output_parsed.questions" in line:
                    line = "import json\njson.loads(response.choices[0].message.content)['questions']\n"
                    
                new_source.append(line)
            cell["source"] = new_source

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)

print("Notebooks updated successfully!")
