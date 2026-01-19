# QR_Indoor_Navigation
The indoor navigation system uses QR code markers at junctions to identify a user's current location within a building. By scanning these markers, the system determines the corresponding graph node and calculates the shortest path to a selected destination. This system provides a web-based solution for indoor navigation within a multi-floor building . 
Use python 3.12.2
use lastes verion of pip

2. Install Python and create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```


5. To Run
   a. First run local Naviagation web app  in the terminal
   ```bash 
   python Navigation.py
      ```
b. Then run the online Naviagation web app  in a different terminal
   ```bash 
python Online_NavgApp.py
   
       ```
