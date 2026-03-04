#!/usr/bin/env python3
"""
Basic usage example of Kimi Authentication Bridge
"""

from kimi_auth_bridge import KimiAuthBridge


def main():
    # Initialize the bridge
    bridge = KimiAuthBridge()
    
    # Check authentication status
    print("🔐 Checking Kimi CLI authentication...")
    
    if bridge.is_authenticated():
        print("✅ Authenticated!")
        
        # Get token info
        token_preview = bridge.get_token_preview()
        print(f"🎫 Token: {token_preview}")
        
        # Get API info
        print(f"🌐 API Base: {bridge.get_api_base()}")
        print(f"🤖 Model: {bridge.get_default_model()}")
        
        # Get headers for API requests
        try:
            headers = bridge.get_auth_headers()
            print(f"📋 Headers ready for API requests")
            
            # Example: Using with requests library
            print("\n📡 Example API call:")
            print(f"""
import requests

response = requests.post(
    "{bridge.get_api_base()}/chat/completions",
    headers=headers,
    json={{
        "model": "{bridge.get_default_model()}",
        "messages": [{{"role": "user", "content": "Hello!"}}]
    }}
)
print(response.json())
""")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        print("❌ Not authenticated!")
        print("💡 Run 'kimi login' to authenticate")


if __name__ == "__main__":
    main()
