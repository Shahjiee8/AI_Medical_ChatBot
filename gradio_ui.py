import gradio as gr
from Brain import generate_stt_and_images, generate_response, generate_followup_response, query_func
from report import generate_report
from Database import login_auth, register
from ui_config import theme, landing_page_text, css, js_func


def login_success(is_logged_in):
    """
    Handles the UI after a user logs in or logs out.

    If the user is logged in, it clears all the UI elements and shows the
    UI for a logged-in user. If the user is not logged in, it clears all
    the UI elements and shows the login section.

    Args:
        is_logged_in (bool): Whether the user is logged in or not.

    Returns:
        A list of UI elements to update.
    """
    if is_logged_in:
        # Show the UI for a logged-in user
        return clear_all() + view_with_login()
    else:
        # Show the login section
        return clear_all() + toggle_sections(login=True)


def clear_all():
    """
    Resets all UI elements and states to their initial values.

    Returns:
        tuple: A tuple containing initial values for various UI components
        and states, including:
            - stt_output (str): Empty string for speech-to-text output.
            - generated_image (None): Placeholder for generated image.
            - response_audio (None): Placeholder for response audio.
            - response_output (str): Empty string for response text output.
            - in_main (gr.update): Visibility control for main UI section.
            - stt_state (None): Initial state for speech-to-text.
            - enc_img_state (None): Initial state for encoded image.
            - img_url_state (None): Initial state for image URL.
            - followup_history (list): Empty list for follow-up conversation history.
    """
    return (
        "",  # stt_output
        None,  # generated_image
        None,  # response_audio
        "",  # response_output
        gr.update(visible=False),  # in_main
        None,  # stt_state
        None,  # enc_img_state
        None,  # img_url_state
        [],    # followup_history
    )


def toggle_sections(landing=False, login=False, sidebar=False, main=False, followup=False,
                    signup=False, signup_main=False, report=False):
    """
    Toggles the visibility of various sections in the UI.

    Args:
        landing (bool): Visibility for the landing section.
        login (bool): Visibility for the login section.
        sidebar (bool): Visibility for the sidebar.
        main (bool): Visibility for the main content area.
        followup (bool): Visibility for the follow-up section.
        signup (bool): Visibility for the signup section.
        signup_main (bool): Visibility for the main signup area.
        report (bool): Visibility for the report section.

    Returns:
        tuple: A tuple of gr.update objects that set the visibility of each section.
    """
    return (
        gr.update(visible=landing),  # Update visibility for landing section
        gr.update(visible=login),    # Update visibility for login section
        gr.update(visible=sidebar),  # Update visibility for sidebar
        gr.update(visible=main),     # Update visibility for main section
        gr.update(visible=followup),  # Update visibility for follow-up section
        gr.update(visible=signup),   # Update visibility for signup section
        gr.update(visible=signup_main),  # Update visibility for main signup section
        gr.update(visible=report)    # Update visibility for report section
    )


def show_login_page():
    """
    Toggles the visibility of the login section.
    Returns:
        tuple: A tuple of gr.update objects that sets the visibility of the login section.
    """
    return toggle_sections(login=True)


def no_login_view():
    """
    Toggles the visibility of the main content area and the signup section.
    Returns:
        tuple: A tuple of gr.update objects that sets the visibility of the main content area and the signup section.
    """
    return toggle_sections(main=True, signup_main=True)


def view_with_login():
    """
    Toggles the visibility of the sidebar, main content area, follow-up section, and report section.
    Returns:
        tuple: A tuple of gr.update objects that sets the visibility of the sidebar,
               main content area, follow-up section, and report section.
    """
    return toggle_sections(sidebar=True, main=True, followup=True, report=True)


def go_to_signup():
    """
    Toggles the visibility of the signup section.
    Returns:
        tuple: A tuple of gr.update objects that sets the visibility of the signup section.
    """
    return toggle_sections(signup=True)


def continue_as_guest():
    """
    Clears all sections and shows the login section.
    Returns:
        tuple: A tuple of gr.update objects that clears all sections and shows the login section.
    """
    return clear_all() + no_login_view()


def back_to_login():
    """
    Clears all sections and shows the login section.
    Returns:
        tuple: A tuple of gr.update objects that clears all sections and shows the login section.
    """
    return clear_all() + show_login_page()


# Create a gradio interface with a theme, CSS styling, and custom JS to switch themes
with gr.Blocks(theme=theme, css=css, js=js_func) as demo:
    # Create the landing section
    with gr.Column(elem_id="landing-section", elem_classes="section-container") as landing_section:
        # Add a header with the Dr. Chat logo and tagline
        gr.HTML("""<h1><center>Welcome to Dr. Chat</center></h1>""")
        # Add a row of whitespace
        gr.Row(2)
        # Create a row with two columns, one for text and one for the image
        with gr.Row(equal_height=True):
            # Create a column for the text
            with gr.Column(scale=3):
                # Add the landing page text from the ui_config.py file
                gr.HTML(landing_page_text)
                # Add a button to get started
                get_started_btn = gr.Button("Get Started", variant="primary")
            # Create a column for the image
            with gr.Column(scale=2):
                # Add the landing page image
                gr.Image("landing_page_image.jpg", show_label=False, container=False, show_download_button=False,
                         interactive=False, show_fullscreen_button=False)

    # Create the login section with a title and input fields for email and password
    with gr.Column(visible=False, elem_id="login-section", elem_classes="section-container") as login_section:
        # Add a title for the login section
        gr.HTML("<h1><center>Login or continue as guest</center></h1>")
        # Input field for user email
        login_email = gr.Textbox(placeholder="Email...", type="email", container=False)
        # Input field for user password
        login_password = gr.Textbox(placeholder="Password...", type="password", container=False)
        # Create a row for the login and register buttons
        with gr.Row():
            # Button to login
            login_btn = gr.Button("Login", variant="primary")
            # Button to register a new account
            register_button = gr.Button("Register", variant="primary")
        # Button to continue as a guest without logging in
        continue_btn = gr.Button("Continue as guest")

    # Create a sidebar with a title and a link to the user's report history
    with gr.Sidebar(visible=False, open=False) as side_bar:
        # Add a title for the sidebar
        gr.HTML("<center><h2>Reports History</h2></center><hr>")
        # The link to the user's report history
        report_link_display = gr.HTML()
        # Button to logout
        logout_button = gr.Button("Logout")

    with gr.Column(visible=False) as main_section:
        # A row with a column and a button to register
        with gr.Row():
            gr.Column(scale=10)
            with gr.Column():
                signup_main_btn = gr.Button("Register", size="md", visible=False, variant="primary")
        # A header with Dr. Chat logo and tagline
        gr.Markdown("""<center><h1>Dr. Chat</h1></center><br>
                    <center><h2>Your AI powered health assistant</h2></center>""")
        with gr.Tab("Main"):
            # A group containing the main content
            with gr.Group(visible=False) as in_main:
                # A row with two columns, one for the input and one for the output
                with gr.Row(equal_height=True):
                    # The column for the input
                    with gr.Column(scale=3):
                        # The text area where the user can write a query
                        stt_output = gr.TextArea(placeholder="Your query appears here", interactive=False,
                                                 show_label=False)
                        # The image area where the generated image is displayed
                        generated_image = gr.Image(placeholder="Image of your query appears here", interactive=False,
                                                   format="pil", show_label=False)
                    # The column for the output
                    with gr.Column(scale=3):
                        # The audio area where the diagnosis audio is played
                        response_audio = gr.Audio(label="Diagnosis Voice", interactive=False,
                                                  type="filepath", autoplay=True)
                        # The text area where the diagnosis text is displayed
                        response_output = gr.TextArea(placeholder="Diagnosis appears here", interactive=False,
                                                      show_label=False)
            # The multimodal input box
            query_input = gr.MultimodalTextbox(
                sources=["microphone", "upload"], placeholder="How can I help!", show_label=False,
                interactive=True, file_types=[".mp3", ".wav", ".jpg", ".jpeg", ".png", "image", "audio", "text"])
            # The clear button
            clear_btn = gr.Button("Clear", size="md")

        # The Follow-Up tab is used to ask follow-up questions to the AI
        with gr.Tab("Follow Up", visible=False) as followup_section:
            with gr.Column():
                # The doctor's response is displayed here
                with gr.Row():
                    followup_output = gr.Textbox(label="Doctor's Response", interactive=False)
                # The user can input a follow-up question or statement
                followup_input = gr.MultimodalTextbox(
                    sources=["microphone"], placeholder="What can I do to assist you?", show_label=False,
                    interactive=True, file_types=[".mp3", ".wav", "audio", "text"]
                )
                # The generate report button is displayed here
                with gr.Row():
                    gr.Column(scale=12)
                    with gr.Column():
                        report_btn = gr.Button("Generate Medical Report", variant='primary', size="md")

        # The Report tab is used to preview and download the medical report
        with gr.Tab("Report", visible=False) as report_section:
            with gr.Column():
                # The report preview is displayed here
                report_preview = gr.HTML(label="Report Preview")
                # The download PDF button is displayed here
                download_pdf = gr.HTML(label="Download PDF")

    # The Signup section is used for registering new users
    with gr.Column(visible=False, elem_classes="section-container") as signup_section:
        with gr.Row():
            with gr.Column():
                # The back button is used to return to the login section
                home_btn = gr.Button("Back to Login")
            gr.Column(scale=12)  # empty column to center the signup form
        with gr.Column(elem_id="signup-section"):
            # The signup form
            gr.HTML("""<center><h2>SignUp</h2></center>""")
            # The username input box
            user_name = gr.Textbox(show_label=False, placeholder="Username...", container=False)
            # The email input box
            signup_email = gr.Textbox(show_label=False, type='email', placeholder="Email...", container=False)
            # The password input box
            signup_password = gr.Textbox(show_label=False, type='password', placeholder="Password...",
                                         container=False)
            # The password confirmation input box
            confirm_password = gr.Textbox(show_label=False, type='password', placeholder="Confirm Password...",
                                          container=False)
            with gr.Row():
                # The signup button
                signup_sec_btn = gr.Button("Signup", variant="primary")

            stt_state = gr.State()  # The state of the speech-to-text output
            enc_img_state = gr.State()  # The state of the encoded image
            img_url_state = gr.State()  # The state of the image URL
            generated_img_state = gr.State()  # The state of the generated image
            login_status = gr.State()  # The state of the login status
            followup_history = gr.State([])  # The state of the follow-up conversation history
            name_state = gr.State()  # The state of the user's name
            email_state = gr.State()  # The state of the user's email

            # When the get started button is clicked, show the login page
            get_started_btn.click(
                show_login_page,
                outputs=[landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            )

            # When the register button is clicked, show the signup page
            register_button.click(
                go_to_signup,
                outputs=[landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            )

            # When the back button is clicked, go back to the login page
            home_btn.click(
                fn=back_to_login,
                outputs=[stt_output, generated_image, response_audio, response_output,
                         in_main, stt_state, enc_img_state, img_url_state, followup_history,
                         landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            )

            # When the continue button is clicked, continue as a guest
            continue_btn.click(
                continue_as_guest,
                outputs=[stt_output, generated_image, response_audio, response_output,
                         in_main, stt_state, enc_img_state, img_url_state, followup_history,
                         landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            )

            # When the clear button is clicked, clear all the UI elements
            clear_btn.click(
                clear_all,
                outputs=[stt_output, generated_image, response_audio, response_output, in_main,
                         stt_state, enc_img_state, img_url_state, followup_history]
            )

            # When the signup main button is clicked, clear all the UI elements and go to the signup page
            signup_main_btn.click(
                clear_all,
                outputs=[stt_output, generated_image, response_audio, response_output, in_main,
                         stt_state, enc_img_state, img_url_state, followup_history]
            ).then(
                go_to_signup,
                outputs=[landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            )

            # When the user submits a query, generate the speech-to-text and image encodings
            query_input.submit(
                fn=generate_stt_and_images,
                inputs=[query_input],
                outputs=[stt_state, enc_img_state, img_url_state]
            ).then(
                # Then, update the UI to show the main section
                lambda: gr.update(visible=True), None, [in_main]
            ).then(
                # Clear the query input and set it to interactive=False
                lambda: gr.MultimodalTextbox(value="", interactive=False), None, [query_input]
            ).then(
                # Updates the gr.state variables
                fn=query_func,
                inputs=[stt_state, enc_img_state, img_url_state],
                outputs=[stt_output, generated_image, generated_img_state]
            ).then(
                # Generate the response to the query
                fn=generate_response,
                inputs=[stt_state, enc_img_state],
                outputs=[response_audio, response_output, followup_history]
            ).then(
                # Then, set the query input back to interactive=True
                lambda: gr.MultimodalTextbox(interactive=True), None, [query_input]
            )

            # When the user submits a follow-up query, generate the response to the follow-up query
            followup_input.submit(
                fn=generate_followup_response,
                inputs=[followup_input, followup_history],
                outputs=[followup_history, followup_output]
            ).then(
                # Then, clear the follow-up input and set it to interactive=False
                lambda: gr.MultimodalTextbox(value="", interactive=False), None, [followup_input]
            ).then(
                # Then, set the follow-up input back to interactive=True
                lambda: gr.MultimodalTextbox(interactive=True), None, [followup_input]
            )

            # When the report button is clicked, generate the report
            report_btn.click(
                fn=generate_report,
                inputs=[followup_history, name_state, email_state, generated_img_state],
                outputs=[report_preview, download_pdf]
            )

            # When the logout button is clicked, go back to the login page
            logout_button.click(
                fn=back_to_login,
                outputs=[stt_output, generated_image, response_audio, response_output,
                         in_main, stt_state, enc_img_state, img_url_state, followup_history,
                         landing_section, login_section, side_bar, main_section,
                         followup_section, signup_section, signup_main_btn, report_section]
            ).then(
                # Then, clear the follow-up output and report preview
                lambda: (None, None, None), None, [followup_output, report_preview, download_pdf]
            )

        # When the login button is clicked, attempt to log in with the provided email and password
        login_btn.click(
            fn=login_auth,
            inputs=[login_email, login_password],
            outputs=[login_status, email_state, name_state, report_link_display]
        ).then(
            # Then, clear the login inputs
            lambda: ("", ""), None, [login_email, login_password]
        ).then(
            # If the login is successful, update the UI to show the main section
            fn=login_success,
            inputs=[login_status],
            outputs=[stt_output, generated_image, response_audio, response_output,
                     in_main, stt_state, enc_img_state, img_url_state, followup_history,
                     landing_section, login_section, side_bar, main_section,
                     followup_section, signup_section, signup_main_btn, report_section]
        )

        # When the signup button is clicked, attempt to register a new user with the provided name, email, and password.
        signup_sec_btn.click(
            fn=register,
            inputs=[user_name, signup_email, signup_password, confirm_password],
            outputs=[name_state, email_state]
        ).then(
            # Then, clear the signup inputs
            lambda: ("", "", "", ""), None, [user_name, signup_email, signup_password, confirm_password]
        )

# Launch the Gradio demo interface
# 'debug=True' enables debug mode for more verbose output
# 'inbrowser=True' opens the demo in the default web browser
demo.launch(debug=True, inbrowser=True)
