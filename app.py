from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from gtts import gTTS
from PIL import Image
import os
import tempfile
from gemini_helper import analyze_image, generate_story  # Assuming these are your helper functions

# Initialize Flask app
app = Flask(__name__)

# Configure upload and audio folders
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files.get('file')
        genre = request.form.get('genre')

        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Debug: print the image path
            print(f"Image saved at: {image_path}")

            # Open image and pass it to analysis function
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                image = Image.open(image_path)
                image.save(tmp.name)

                # Analyze the image and generate the story
                analysis = analyze_image(tmp.name)
                story = generate_story(analysis, genre)

                # Generate audio for the story
                audio_filename = f"{os.path.splitext(filename)[0]}_{genre}.mp3"
                audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
                tts = gTTS(text=story, lang='en')
                tts.save(audio_path)

                # Render the result page with the generated story and audio
                return render_template(
                    'index.html',
                    image_path=filename,
                    story=story,
                    genre=genre,
                    audio_path=audio_filename
                )

    return render_template('index.html', image_path=None, story=None, audio_path=None)

if __name__ == "__main__":
    app.run(debug=True)
