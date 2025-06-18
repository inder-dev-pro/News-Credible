import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        return
    
    print("API Key found, testing connection...")
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Make a simple API call
        response = model.generate_content(
            "Say 'Hello, Gemini API test successful!' if you can read this."
        )
        
        # Print the response
        print("\nAPI Response:")
        print(response.text)
        print("\nAPI test completed successfully!")
        
    except Exception as e:
        print(f"\nError testing API: {str(e)}")

if __name__ == "__main__":
    test_gemini_api() 