import gradio as gr

# ========== LANDING PAGE TEXT ==========
landing_page_text = """
<h3 style="text-align: justify;">
Dr. Chat is your intelligent, voice-driven health companion – always ready to listen, analyze, and assist. 
Whether you’re feeling unwell, curious about a symptom, or simply seeking peace of mind, you can speak naturally 
or upload an image, and Dr. Chat will step in with insightful, informative feedback.<br><br>
Powered by advanced language and vision models, it mimics the clarity and compassion of real healthcare 
professionals, offering a conversational experience that feels both personal and professional.<br><br>
From converting your voice into text, analyzing symptoms, interpreting images, and even generating tailored medical 
reports, Dr. Chat streamlines your journey from concern to clarity. No need for a medical background – everything 
is delivered in an easy-to-understand way, making healthcare more approachable than ever.<br><br>
Whether you’re a student exploring diagnostics, a parent managing family health, or just someone looking for fast 
and reliable insights, Dr. Chat is designed with you in mind. Enjoy smooth, interactive feedback via both text and 
voice, get possible conditions explained clearly, and take the next step with confidence. Accessible, supportive, 
and always learning, Dr. Chat is your smart gateway to better health conversations.<br><br>
Let’s take the guesswork out of wellness – together.
</h3>
"""

# ========== THEME ==========
# Configure the theme using Gradio's Ocean theme with custom hues and styles
theme = gr.themes.Ocean(
    primary_hue="teal",  # Primary color set to teal
    secondary_hue="blue",  # Secondary color set to blue
    neutral_hue="gray",  # Neutral color set to gray
).set(
    background_fill_primary='*neutral_50',  # Primary background color
    background_fill_secondary='white',  # Secondary background color
    block_border_color='*neutral_300',  # Block border color
    block_info_text_color='*neutral_400',  # Info text color
    block_title_text_color='*neutral_900',  # Title text color
    block_title_text_weight='500',  # Title text weight
    input_border_color_focus='*primary_700',  # Input border color on focus
    button_primary_text_color='*neutral_50',  # Primary button text color
    button_secondary_background_fill_hover='*secondary_400',  # Secondary button hover background
    button_secondary_text_color='*neutral_700'  # Secondary button text color
)

# ========== JS STYLING ==========
# JavaScript function to refresh the theme to light mode if not already set
js_func = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.href = url.href;
    }
}
"""

# ========== CSS STYLING ==========
# Custom CSS styling for the Gradio interface
css = """
footer {
    visibility: hidden;  # Hide the footer
}
.gradio-container .fillable {
    width: 95% !important;  # Set fillable width to 95%
    max-width: unset !important;  # Remove max-width constraints
}
.section-container {
    margin: 2rem auto;  # Set margin for section container
    padding: 1.5rem;  # Set padding for section container
    max-width: 1000px;  # Set max width for section container
    width: 90%;  # Set width for section container
    border-radius: 12px;  # Set border radius for section container
    box-sizing: border-box;  # Use border-box sizing
}
"""