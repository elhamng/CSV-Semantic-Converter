
Installation and version check<img width="121" height="100" alt="image" src="https://github.com/user-attachments/assets/5baab378-dbe5-494a-a64a-d9eef39c7a7e" />
Step 1: Make sure Python is installed
          python --version
Step 2: Install pip (Python’s package manager)           
        pip --version
        python -m ensurepip –upgrade
   Step 3: Create and activate a virtual environment (recommended)
 python -m venv myenv
Activate it:
On Windows:
myenv\Scripts\activate
On Bash: 
source myenv/Scripts/activate
<img width="121" height="100" alt="image" src="https://github.com/user-attachments/assets/04660bc5-9e0e-4c76-a5dc-27bc39583ce6" />
python 

pip install pandas

Then run Python and test:
import pandas
print(pandas.__version__)
<img width="121" height="100" alt="image" src="https://github.com/user-attachments/assets/33382c62-fd45-470e-8010-fbad865ddaac" />
To deactivate:
      deactivate
<img width="121" height="100" alt="image" src="https://github.com/user-attachments/assets/6acc330b-7f76-4aed-8635-9d4e463ea633" />

