from streamlit import session_state as ss
import streamlit as st
from streamlit_msal import Msal
import requests
import os
from PIL import Image
from io import BytesIO
import base64

# This MSAL implementation based on the code published at the following GitHub repo:
# https://github.com/WilianZilv/streamlit_msal
# In this app the folder streamlit_msal contains a fork of this Github 
# repo with some modifications to the embedded React.js Code

# For a deployed app, place these variables in an environment variable
client_id = "ca67cffb-9893-4d3e-8ac7-6e2a5e126bee"
#client_id = "b36caaf1-4542-46cf-bae3-db5d7e6a239e"
tenant_id = "3e0d2f7b-8d5d-44ff-9a55-490d31bbdfb9"


# Define the Images logos path
path = 'images/logos/'
logo_url = 'MozaTech.png'  

# Initialize the Msal object
auth_data = Msal.initialize(
    client_id=f"{client_id}",
    authority=f"https://login.microsoftonline.com/{tenant_id}",
    scopes=["User.Read"],  # Ask for a basic profile user info claim
)

# Get user info from Graph API    
def get_user_info(access_token):
    """Get user information from Microsoft Graph API."""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me?$select=displayName,jobTitle,companyName,mail,userPrincipalName,officeLocation,state,givenName',
        headers=headers
    )
    if response.status_code == 200:
        return response.json()        
    return None

def get_user_photo(access_token):
    """Get user profile photo from Microsoft Graph API."""
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(
            'https://graph.microsoft.com/v1.0/me/photo/$value',
            headers=headers
        )
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        return None

# Only show authentication buttons if user is not signed in
if not auth_data:
    #st.write("Please sign in to access the portal")
    st.title("Welcome to the Sales Analytics Portal")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign in"):
            Msal.sign_in() # Show popup to select account
    
    with col2:
        #if st.button("Refresh Token"):
        #    Msal.revalidate() # refresh the accessToken
        st.write("You are not signed in")
else:
    # User is authenticated - show sign out button in sidebar or at bottom
    access_token = auth_data["accessToken"]
    user_info = get_user_info(access_token)
    user_photo = get_user_photo(access_token)
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("👤 User Profile")
        
        # Display user photo
        if user_photo:
            st.write(f"Hi {user_info.get('givenName', 'N/A')}")
            try:
                img = Image.open(BytesIO(user_photo))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_b64 = base64.b64encode(buffered.getvalue()).decode()
                img_html = f"""
                    <img src="data:image/png;base64,{img_b64}" 
                        style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:2px solid #ddd;" />
                """
                st.markdown(img_html, unsafe_allow_html=True)
            except Exception as e:
                    st.write("📷 Photo unavailable")
        else:
            st.write("📷 No photo available")
            
        st.write("**Account Options**")
        if st.button("Sign out"):
            Msal.sign_out() # Clears auth_data
        
        if st.button("Refresh Token"):
            Msal.revalidate() # refresh the accessToken

def display_user_info(user_info, logo_url):
    """Display user information and organization logo."""
    st.title("Welcome to " + user_info.get('companyName') + " Sales Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("User Details")
        st.write(f"**Name:** {user_info.get('displayName', 'N/A')}")
        st.write(f"**Job Title:** {user_info.get('jobTitle', 'N/A')}")
        st.write(f"**Email:** {user_info.get('mail', user_info.get('userPrincipalName', 'N/A'))}")
        #   st.write(f"**Organization:** {user_info.get('companyName', 'N/A')}")
    
    with col2:
        if logo_url:
            try:
                # Assuming logo_url is a local file path like "Images/logos/your_logo.png"
                # Make sure the 'Images/logos' directory is accessible from where your Streamlit app runs
                if os.path.exists(path + logo_url):
                    st.subheader("")
                    #img = Image.open(path + logo_url)
                    img = Image.open(path + "MozaTech.png")
                    st.image(img, caption="", use_container_width=True)
                    st.write(f"**Location:** {user_info.get('officeLocation', 'N/A')}, {user_info.get('state', 'N/A')}")
                else:
                    st.error(f"Local logo file not found: {logo_url}")
            except Exception as e:
                st.error(f"Error loading local logo: {str(e)}")
                st.write("Expected Local Logo Path:", path + logo_url)
        else:
            st.info("No logo available for your organization")


if not auth_data:
    st.write("")
else:
    # Getting useful information
    access_token = auth_data["accessToken"]

    #account = auth_data["account"]
    #name = account["name"]
    #username = account["username"]
    #account_id = account["localAccountId"]
    
    # Call get_user_info and display the result
    user_info = get_user_info(access_token)
    if user_info:
        #st.write("User info from Microsoft Graph:")
        #st.json(user_info)
        display_user_info(user_info, logo_url)
        
    else:
        st.write("Could not fetch user info from Microsoft Graph.")

    # Display information
    #st.write(f"Hello {name}!")
    #st.write(f"Your username is: {username}")
    
    #st.write(f"Your account id is: {account_id}")
    #st.write("Your access token is:")
    #st.code(access_token)
    #st.write("Auth data:")
    #st.json(auth_data)
