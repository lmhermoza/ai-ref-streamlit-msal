# streamlit-login-and-db
# Streamlit Entra ID Organization Portal

This Streamlit application authenticates users with Microsoft Entra ID (formerly Azure AD), retrieves their user details, and displays their organization logo from an Azure SQL database. It uses Azure Key Vault to securely store and retrieve database connection strings.

## Features

- Authentication with Microsoft Entra ID
- Retrieval of user details (name, email, organization)
- Secure connection to Azure SQL database using Azure Key Vault
- Clean UI to display user information and organization logo

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Microsoft Entra ID application registration
- Azure SQL Database
- Azure Key Vault
- ODBC Driver for SQL Server

### Environment Variables

Set the following environment variables:

\`\`\`
ENTRA_CLIENT_ID=your_client_id
ENTRA_TENANT_ID=your_tenant_id
ENTRA_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8501
KEY_VAULT_NAME=your_key_vault_name
DB_CONNECTION_SECRET_NAME=AzureSqlConnectionString
\`\`\`

### Azure Key Vault Setup

1. Create an Azure Key Vault if you don't have one already
2. Add a secret named `AzureSqlConnectionString` with your full database connection string:
   \`\`\`
   DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server.database.windows.net;DATABASE=your_database;UID=your_username;PWD=your_password
   \`\`\`
3. Grant your application or development identity access to the Key Vault with Secret Get permissions

### Installation

1. Clone this repository
2. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
3. Run the database setup script:
   \`\`\`
   python scripts/setup_database.py
   \`\`\`
4. Start the Streamlit app:
   \`\`\`
   streamlit run app.py
   \`\`\`

### Entra ID Application Setup

1. Register a new application in the Microsoft Entra ID admin center
2. Set the redirect URI to `http://localhost:8501` (or your deployed app URL)
3. Grant API permissions for Microsoft Graph User.Read
4. Create a client secret and note it down
5. Update your environment variables with the application details

### Azure Identity Authentication

This application uses DefaultAzureCredential for authentication to Azure Key Vault, which supports:

- Environment variables
- Managed Identity
- Visual Studio Code credentials
- Azure CLI credentials
- Interactive browser authentication

For local development, make sure you're logged in with Azure CLI or have the appropriate environment variables set.

## Database Schema

The application expects an Azure SQL database with an existing table named `BusinessDivisions` with the following structure:

\`\`\`sql
CREATE TABLE BusinessDivisions (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    LogoUrl NVARCHAR(1000) NULL
);
\`\`\`

Note: The application does not create this table - it must already exist in your database.

## Deployment

To deploy this application:

1. Set up the required environment variables in your deployment environment
2. Install the ODBC Driver for SQL Server
3. Deploy the Streamlit application using your preferred method (Streamlit Cloud, Docker, etc.)
4. Update the redirect URI in your Entra ID application registration
5. Ensure your deployed application has proper access to Azure Key Vault

