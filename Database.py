import os
import gradio as gr
from firebase_admin import firestore
from API_Config import auth, db


def register(name, email, password, verify_pass):
    """
    Registers a new user with the provided name, email, and password.

    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password for the user account.
        verify_pass (str): The password verification to ensure it matches the password.

    Returns:
        tuple: A tuple containing the user's name and email if registration is successful.

    Raises:
        gr.Error: If the passwords do not match, if the email is already registered,
                  or if registration fails for any other reason.
    """
    try:
        # Check if password verification matches
        if verify_pass == password:
            # Create a new user with email and password
            user = auth.create_user_with_email_and_password(email, password)

            # Firestore: Create user document using email as document ID
            user_doc_name = email.replace(".com", "").lower()
            db.collection("Patients").document(user_doc_name).set({
                'name': name,
                'email': email
            })

            # Inform user of successful registration
            gr.Info("Account registered, Login to continue.")
            return name, email
        else:
            # Raise error if passwords do not match
            raise gr.Error("Password mismatch.")
    except Exception as e:
        error_str = str(e)
        # Check if email is already registered
        if "EMAIL_EXISTS" in error_str:
            raise gr.Error("This email is already registered.")
        else:
            # Raise a generic error for any other registration failure
            raise gr.Error("Registration failed. Please try again.")


# Step 4: Login Function
def login_auth(email=None, password=None):
    """
    Logs in an existing user with the provided email and password.

    Args:
        email (str): The email of the user.
        password (str): The password for the user account.

    Returns:
        boolean: True if login is successful, False otherwise.
        tuple: A tuple containing the user's name and email if login is successful.
        list: A list of report links for the user.

    Raises:
        gr.Error: If the login fails for any reason.
    """

    # Perform login with Firebase
    try:
        user = auth.sign_in_with_email_and_password(email, password)

        # Inform user of successful login
        gr.Info("Login successful.")

        # Firestore: Get user document using email as document ID
        user_doc_name = email.replace(".com", "").lower()
        user_ref = db.collection("Patients").document(user_doc_name)

        # Get user data (name + email)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            name = user_data.get('name', '')
        else:
            raise gr.Error("User data not found in Firestore. Please contact support.")

        # Get latest 5 reports ordered by Firestore's document ID (timestamp part)
        reports_ref = user_ref.collection("Reports").order_by("date", direction=firestore.Query.DESCENDING).limit(5)
        reports = reports_ref.stream()

        # Build a list of report links
        links_html = ""
        report_list = []
        for r in reports:
            report_data = r.to_dict()
            report_list.append(report_data.get("report_link", ""))

        # Handle no reports
        if not report_list:
            links_html = "<p>No reports available.</p>"
        else:
            # Build a list of report links
            for link_html in report_list:
                links_html += f"{link_html}<br><hr>"

        # Return True, email, name, and list of latest 5 reports
        return True, email, name, links_html
    except Exception as e:
        error_str = str(e)
        # Handle invalid password or email
        if "INVALID_PASSWORD" in error_str or "EMAIL_NOT_FOUND" in error_str:
            raise gr.Error("Invalid email or password.")
        else:
            # Raise a generic error for any other login failure
            raise gr.Error("Login failed. Please try again.")
