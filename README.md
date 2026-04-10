# AuthFastApi
Authentication microservice, the goal of this project is to learn Python and FastApi, it will be updated as new versions of these tools are released.

It is a microservice for user administration and authenication, using JWT tokens and encrypting the information within it, different approaches are used, that is why there may be different implementations performing the same functions.

## Requirements
- Python 3.12+
- FastApi 0.124+
- Google account and activate [Google cloud](https://console.cloud.google.com) to obtain OAuth2 config values (Optional)

> [!IMPORTANT]
> It is necessary to complete the configuration file(.env), create the PEM files and place them in the root folder

## Installing
1. Create a virtual environment
```bash
python -m venv .venv
```
2. Activate it (Linux, macOS)
```bash
source .venv/bin/activate
```
   (Windows PowerShell)
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
5. Set configuration file (.env)

The microservice uses mongoDB as its database, so the connection string and other configurations (mongodb, JWT, CORS, logs, Google OAuth2) must be included

6. Run local development server
```bash
uvicorn src.main:app --reload
```
7. Open the next url in a browser to see the Swagger UI
```bash
http://127.0.0.1:8000/docs
```

## Using with Docker
1. Create the image
```bash
docker build -t auth-service:latest .
```
   Or download the image hosted in this repository.
```bash
docker pull ghcr.io/ablogo/authfastapi:latest
```
2. Run a container from the image previously created
```bash
docker run -p 8000:80 --env-file .env auth-service:latest
```

## Google OAuth2
To implement this auth system, you need to obtain OAuth 2.0 credentials from the Google API Console.

[Follow the steps on this page to obtain the credentials](https://developers.google.com/identity/protocols/oauth2)

Once you have done this, you must place those values in the .env file.

```bash
GOOGLE_OAUTH_ID=
GOOGLE_OAUTH_CLIENT=
GOOGLE_OAUTH_SECRET=
```

The following values should be customized based on your development, the scopes that you need and the links on your site.

```bash
GOOGLE_OAUTH_REDIRECT_RESPONSE=https://127.0.0.1:8000/auth/google-response
GOOGLE_OAUTH_JS_ORIGINS=http://127.0.0.1:8000,http://localhost:8081
GOOGLE_OAUTH_SCOPES=https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/userinfo.profile,openid
```

> [!NOTE]
> Since the project is used for learning, it does not strictly follow the concept of microservices, where each microservice should have its own realm of responsability and use different approaches.
