from llama_extract import LlamaExtract
from dotenv import load_dotenv
import os

def test_api_connection():
    print("Testing Llama Extract API Connection...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    try:
        # Try getting agent by name
        print("\nTesting agent access by name...")
        extractor = LlamaExtract(api_key=api_key)
        agent = extractor.get_agent(name="sp termsheet")
        print("Agent details:", agent)
        
        if agent:
            print("\nTrying to list available agents...")
            agents = extractor.list_agents()
            print("Available agents:", agents)
        
    except Exception as e:
        print(f"Error accessing agent: {e}")

if __name__ == "__main__":
    test_api_connection() 