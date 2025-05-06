from llama_extract import LlamaExtract
from pydantic import BaseModel, Field
import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize client
api_key = os.getenv("LLAMA_CLOUD_API_KEY")
try:
    extractor = LlamaExtract(api_key=api_key)
except Exception as e:
    print(f"Error initializing LlamaExtract: {e}")
    extractor = LlamaExtract()

def extract_termsheet(file_path):
    # Use existing agent "sp termsheet"
    try:
        agent = extractor.get_agent(name="sp termsheet")
        
        # Extract data from document
        result = agent.extract(file_path)
        return result.data
    except Exception as e:
        print(f"Extraction error: {e}")
        raise e

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            result = extract_termsheet(file_path)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            agents = extractor.list_agents()
            print("Available agents:", agents)
        except Exception as e:
            print(f"Error listing agents: {e}")
        print("Please provide a file path as a command line argument.")
        print("Example: python extract.py termsheet.pdf") 