import nltk
import os

# Create the directory structure if it doesn't exist
os.makedirs(os.path.expanduser('~/nltk_data/tokenizers'), exist_ok=True)

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Verify the downloads
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    print("NLTK data successfully downloaded and verified!")
except LookupError as e:
    print(f"Error: {e}") 