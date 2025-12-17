# AuthFastApi
Authentication microservice, the goal of this project is to learn Python and FastApi, it will be updated as new versions of these tools are released.

It is a microservice for user administration and authenication, using JWT tokens and encrypting the information within it, different approaches are used, that is why there may be different implementations performing the same functions.

## Requirements
- Python 3.12+
- FastApi 0.117+

## Installing
1. Create a virtual environment
```bash
python -m venv .venv
```
2. Activate it (Linux, macOS)
```bash
source .venv/bin/activate
```
   Activate it (Windows PowerShell)
```bash
.venv\Scripts\Activate.ps1
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Generate the RSA keys files and name them as 'private_key.pem' and 'public_key.pem', and place them in the project's root folder
```bash
openssl genrsa -out private_key.pem 2048
```
```bash
chmod 0400 private.pem
```
Use the private key file to extract the public key in PEM format
```bash
openssl rsa -in private_key.pem -pubout -out public_key.pem
```
5. Set configurations files (.env, config.ini) for different purposes (mongodb, JWT, CORS, logs)

The microservice uses mongoDB as its database, so the connection string and other configurations must be included in the configuration files

6. Run local development server
```bash
uvicorn src.main:app --reload
```
7. Open the next url in a browser to see the Swagger UI
```bash
http://127.0.0.1:8000/docs
```

> [!NOTE]
> Since the project is used for learning, it does not strictly follow the concept of microservices, where each microservice should have its own realm of responsability
