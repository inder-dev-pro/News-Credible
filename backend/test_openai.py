import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    print("API Key found, testing connection...")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, API test successful!' if you can read this."}
            ],
            temperature=0.3
        )
        
        # Print the response
        print("\nAPI Response:")
        print(response.choices[0].message.content)
        print("\nAPI test completed successfully!")
        
    except Exception as e:
        print(f"\nError testing API: {str(e)}")

if __name__ == "__main__":
    test_openai_api() 