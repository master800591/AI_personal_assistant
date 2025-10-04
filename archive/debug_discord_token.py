#!/usr/bin/env python3
"""
Discord Token Debug Script
Debug exactly what token is being loaded and used
"""

import os
from dotenv import load_dotenv

def debug_discord_token():
    """Debug Discord token loading and validation"""
    print("🔍 DISCORD TOKEN DEBUG ANALYSIS")
    print("=" * 50)
    
    # Load .env file
    print("📁 Loading .env file...")
    load_dotenv()
    print("✅ .env file loaded")
    
    # Check environment variable
    token_from_env = os.getenv('DISCORD_BOT_TOKEN')
    print(f"\n🔑 Token from environment:")
    print(f"   Raw value: {repr(token_from_env)}")
    print(f"   Length: {len(token_from_env) if token_from_env else 'None'}")
    print(f"   Type: {type(token_from_env)}")
    
    if token_from_env:
        print(f"   First 10 chars: {token_from_env[:10]}...")
        print(f"   Last 10 chars: ...{token_from_env[-10:]}")
        print(f"   Contains dots: {token_from_env.count('.')}")
        print(f"   Has whitespace: {' ' in token_from_env or '\\t' in token_from_env or '\\n' in token_from_env}")
        
        # Check for common issues
        if token_from_env.startswith(' ') or token_from_env.endswith(' '):
            print("⚠️  WARNING: Token has leading/trailing whitespace!")
            
        if '\\n' in token_from_env or '\\r' in token_from_env:
            print("⚠️  WARNING: Token contains newline characters!")
            
        # Expected Discord token format
        parts = token_from_env.split('.')
        print(f"\n🔍 Token structure analysis:")
        print(f"   Parts (should be 3): {len(parts)}")
        if len(parts) >= 1:
            print(f"   Part 1 length: {len(parts[0])} (should be ~24)")
        if len(parts) >= 2:
            print(f"   Part 2 length: {len(parts[1])} (should be ~6)")
        if len(parts) >= 3:
            print(f"   Part 3 length: {len(parts[2])} (should be ~27)")
            
    else:
        print("❌ No token found in environment!")
        
    # Check .env file directly
    print(f"\n📄 Reading .env file directly:")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if 'DISCORD_BOT_TOKEN' in line:
                    print(f"   Line {i}: {repr(line)}")
                    if '=' in line:
                        key, value = line.split('=', 1)
                        value = value.strip()
                        print(f"   Parsed key: {repr(key)}")
                        print(f"   Parsed value: {repr(value)}")
                        print(f"   Parsed value length: {len(value)}")
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        
    print("\n" + "=" * 50)

if __name__ == "__main__":
    debug_discord_token()