import subprocess
import time
import json
import sys
import os

# Import urlopen to make requests without installing external libraries like 'requests'
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def run_ngrok():
    output_file = "Navigation_link.txt"
    
    print("Starting ngrok tunnel on port 5000...")
    
    # Start ngrok process in the background
    # stdout/stderr are silenced to keep the console clean for our own output
    try:
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', '5000'], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("Error: 'ngrok' command not found. Make sure it is installed and in your system PATH.")
        return

    # Give ngrok a few seconds to initialize the tunnel
    time.sleep(3)

    try:
        # ngrok exposes a local API at localhost:4040 where we can get tunnel info
        response = urlopen("http://127.0.0.1:4040/api/tunnels")
        data = json.loads(response.read())
        
        # Find the public HTTPS URL in the API response
        public_url = None
        for tunnel in data['tunnels']:
            if tunnel['proto'] == 'https':
                public_url = tunnel['public_url']
                break
        
        if public_url:
            print(f"Tunnel active! Public URL: {public_url}")
            
            # Write to text file (overwrites existing content)
            with open(output_file, "w") as f:
                f.write(public_url)
            print(f"URL successfully saved to {output_file}")
            
            print("\nKeep this script running to keep the tunnel open.")
            print("Press Ctrl+C to stop.")
            
            # Keep the script running to keep the child process (ngrok) alive
            ngrok_process.wait()
        else:
            print("Error: Could not find an HTTPS tunnel. Is ngrok running correctly?")
            ngrok_process.terminate()
            
    except Exception as e:
        print(f"An error occurred: {e}")
        # Ensure we don't leave a zombie ngrok process
        if 'ngrok_process' in locals():
            ngrok_process.terminate()
            
    except KeyboardInterrupt:
        print("\nStopping ngrok...")
        if 'ngrok_process' in locals():
            ngrok_process.terminate()

if __name__ == "__main__":
    run_ngrok()