from datetime import datetime
import os
import requests
import json
from PIL import Image
from io import BytesIO
import base64
import gradio as gr
from firebase_admin import firestore
from API_Config import PDF_API_KEY, client, db, template_id


def generate_report(history, name, email, img_input):
    """
    Generate a medical report based on the patient-doctor conversation history.
    1. Symptoms
    2. Observations
    3. Recommendations

    Args:
        history (list): A list of dictionaries containing the conversation history.
            Each dictionary should contain the following keys:
                - role (str): The role of the user (either "user" or "assistant").
                - content (str): The content of the message.
        name (str): The patient's name.
        email (str): The patient's email address.
        img_input (str or bytes): The image input to include in the report.
            If a string, it should be a URL pointing to the image.
            If bytes, it should be the raw image data.

    Returns:
        str: The generated report as a string.
        str: The download link for the generated PDF report.
        error: An error message if the report generation fails.
    """
    try:
        # build the prompt to generate the report
        prompt = """
        You are a medical assistant generating a professional and concise medical report based on the following patient-doctor conversation.

        Please structure the report using the following sections:

        1. Symptoms  
        2. Observations  
        3. Recommendations

        Formatting guidelines:

        - Return ONLY the JSON object with this structure:
          {
            "Symptoms": "",
            "Observations": "",
            "Recommendations": ""
          }
        - Do not include any explanation, commentary, or preamble. ONLY output the JSON.
        - Use HTML formatting for the content of each field (no Markdown).
        - Keep a formal and clinical tone.
        """

        # convert the history to the expected format
        for msg in history:
            if msg["role"] == "user":
                prompt += f"Patient: {msg['content']}\n"
            else:
                prompt += f"Doctor: {msg['content']}\n"

        # generate the report content
        response = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_content = response.choices[0].message.content

        report_json = json.loads(generated_content)

        img_html = ""
        img_base64 = ""
        try:
            # convert the image to base64
            if isinstance(img_input, str):
                if img_input.startswith("http"):
                    img_response = requests.get(img_input)
                    img_response.raise_for_status()
                    image = Image.open(BytesIO(img_response.content))
                else:
                    image_data = base64.b64decode(img_input)
                    image = Image.open(BytesIO(image_data))

                # convert the image to base64
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                # add the image to the report
                img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="max-width:100%; height:auto;"><br>'

        except Exception:
            img_html = "<p><i>Image could not be included in report.</i></p>"
            img_base64 = ""

        # generate the report HTML
        report_html = f"""
                <h2 style="text-align:center">Medical Report</h2>
                <p><b>Name:</b> {name}<br>
                <b>Email:</b> {email}<br>
                <b>Date:</b> {datetime.today().strftime('%B %d, %Y')}</p><br>
                <h2 style="text-align:center">Image</h2>
                <div style="text-align:center">{img_html}</div>
                <h2 style="text-align:center">Diagnosis</h2>
                <h3>Symptoms</h3>{report_json['Symptoms']}
                <h3>Observations</h3>{report_json['Observations']}
                <h3>Recommendations</h3>{report_json['Recommendations']}
                """

        # generate the report PDF
        payload = {
            "name": name,
            "email": email,
            "date": datetime.today().strftime("%B %d, %Y"),
            "Symptoms": report_json["Symptoms"],
            "Observations": report_json["Observations"],
            "Recommendations": report_json["Recommendations"],
            "Image": img_html if img_base64 else ""
        }

        # Post the report data to the PDF API to generate the report PDF
        response = requests.post(
            f"https://rest.apitemplate.io/v2/create-pdf?template_id={template_id}",
            headers={"X-API-KEY": PDF_API_KEY},
            json=payload
        )

        # Check if the API call was successful
        if response.status_code != 200:
            raise Exception(f"PDF API error: {response.text}")

        # Get the download URL for the report
        download_url = response.json().get("download_url")
        if not download_url:
            raise Exception("No download_url in API response")

        # Fetch the PDF file content from the download URL
        file_response = requests.get(download_url)

        # Encode the PDF content into a base64 string
        pdf_base64 = base64.b64encode(file_response.content).decode("utf-8")

        # Generate a timestamp for the report filename
        timestamp = datetime.now().strftime("%d-%m-%Y_%I-%M-%p")
        safe_name = name.replace(" ", "_")
        filename = f"{safe_name}_Report_{timestamp}.pdf"

        # Prepare the user document reference in Firestore
        user_doc_name = email.replace(".com", "").lower()
        user_ref = db.collection("Patients").document(user_doc_name)
        report_id = f"Report_{timestamp}"

        # Create a download link for the PDF report
        download_link = f'<a download="{filename}" href="data:application/pdf;base64,{pdf_base64}" target="_blank">{report_id}</a>'

        # Save the report data to Firestore
        report_data = {
            'report_id': report_id,
            'report_link': download_link,
            'date': datetime.now().isoformat()
        }
        user_ref.collection("Reports").document(report_id).set(report_data)

        # Retrieve all reports and delete any beyond the latest 5
        reports_ref = user_ref.collection("Reports").order_by("date", direction=firestore.Query.DESCENDING)
        reports = reports_ref.stream()

        report_docs = list(reports)
        if len(report_docs) > 5:
            for r in report_docs[5:]:
                r.reference.delete()

        # Return the HTML content and download link for the report
        return report_html, download_link

    except Exception:
        # Handle any exceptions and provide an error message
        return "<p>Error generating report. Please try again later.</p>", ""
