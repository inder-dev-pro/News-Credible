"""
Test script for ContentAnalyzer to verify initialization and basic functionality.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.content_analyzer import ContentAnalyzer

async def test_content_analyzer():
    """Test the ContentAnalyzer initialization and basic functionality"""
    
    print("Testing ContentAnalyzer initialization...")
    
    try:
        # Initialize the content analyzer
        analyzer = ContentAnalyzer()
        print("✓ ContentAnalyzer initialized successfully")
        
        # Check if TensorFlow model is available
        if analyzer.is_model_available():
            print("✓ TensorFlow model is available")
        else:
            print("⚠ TensorFlow model is not available, using Gemini-only mode")
        
        # Test retry functionality if model is not available
        if not analyzer.is_model_available():
            print("Attempting to retry model loading...")
            if analyzer.retry_model_loading():
                print("✓ Model loaded successfully on retry")
            else:
                print("⚠ Model loading failed on retry, continuing with Gemini-only mode")
        
        print("\nContentAnalyzer test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error during ContentAnalyzer test: {str(e)}")
        return False

def main():
    """Main test function"""
    print("ContentAnalyzer Test")
    print("=" * 30)
    
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("⚠ Warning: GOOGLE_API_KEY not found in environment variables")
        print("   The analyzer will still initialize but Gemini features may not work")
    
    # Run the test
    success = asyncio.run(test_content_analyzer())
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 