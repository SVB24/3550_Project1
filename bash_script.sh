# Clone the repository (if applicable) or create a new directory
mkdir jwks_server
cd jwks_server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Create `requirements.txt`
echo "
fastapi
uvicorn
pyjwt
cryptography
pytest
pytest-cov
requests
" > requirements.txt

# Install dependencies
pip install -r requirements.txt
