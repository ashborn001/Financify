# Financify
 Financify is an agent based on Langchain framework equipped with two tools which retrieves financial data and news based on input ticker symbol using APIs.

## Setup
1. Clone this repository.
   ```
   git clone https://github.com/ashborn001/Financify
   ```
2. Setup a Virtual Environment and install all the dependencies
   ```
   cd Financify
   ```
   ```
   python -m venv venv
   ```

   ```
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
   
   ```
   pip install -r requirements.txt
   ```

4. Create your NEWS_API_KEY
   Visit this website and sign in to generate your own API Key
   ```
   https://newsapi.org/
   ```
   Create a .env file and enter NEWS_API_KEY="YOUR_API_KEY"

5. Run main.py in terminal
   ```
   python main.py
   ```
