# Termsheet Parser

A powerful Python application for extracting and analyzing financial product term sheets using LlamaExtract and Streamlit. This tool helps financial professionals automate the process of extracting structured data from complex financial product term sheets.

## 🌟 Features

- **Automated Data Extraction**: Extract structured data from PDF term sheets using LlamaExtract
- **Real-time Market Data**: Integration with Yahoo Finance for live market data of underlying assets
- **Interactive Visualizations**: 
  - Candlestick charts for underlying assets
  - Coupon payment schedule visualization
  - Risk analysis dashboard
- **Batch Processing**: Process multiple term sheets at once
- **Modern UI**: Clean and intuitive Streamlit interface
- **Data Export**: Download extracted data in JSON format

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- LlamaExtract API key
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Aary03/Termsheet-parser.git
cd Termsheet-parser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add your LlamaExtract API key:
```
LLAMA_CLOUD_API_KEY=your_api_key_here
```

### Usage

1. **Run the Streamlit App**:
```bash
streamlit run app.py
```

2. **Batch Processing**:
```bash
python batch_process.py path/to/termsheets/directory
```

## 📊 Data Structure

The parser extracts the following information from term sheets:

- Product General Information
  - Product Name
  - Product Type
  - Currency
  - Issue Size
  - Denomination
  - Minimum Investment

- Important Dates
  - Initial Fixing Date
  - Issue Date
  - Final Fixing Date
  - Redemption Date

- Underlying Assets
  - Name
  - Bloomberg Ticker
  - Exchange
  - Reference Currency

- Coupon Information
  - Payment Schedule
  - Rates
  - Payment Dates

- Risk Factors
  - Risk of Loss
  - Issuer Credit Risk
  - Market Risks

## 🛠️ Technical Details

### Components

- `app.py`: Main Streamlit application
- `extract.py`: Core extraction logic using LlamaExtract
- `batch_process.py`: Batch processing functionality
- `test_api.py`: API testing utilities

### Dependencies

- llama-extract: For PDF data extraction
- streamlit: For the web interface
- pandas: For data manipulation
- yfinance: For market data
- plotly: For interactive visualizations
- python-dotenv: For environment variable management

## 🔒 Security

- API keys are stored securely in environment variables
- Sensitive data is excluded via .gitignore
- PDF files are processed locally

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LlamaExtract for providing the extraction API
- Streamlit for the amazing web framework
- Yahoo Finance for market data access

## 📧 Contact

For any queries or support, please reach out to the repository owner.
