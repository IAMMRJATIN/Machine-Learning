from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'd6d0c51a5c663528df34c1789a96675e'  # Necessary for session management

# Configure the Gemini API
genai.configure(api_key="AIzaSyB2UMm-eoesafVu6dJFRGoSGLQKkP-HSc8")
model = genai.GenerativeModel("gemini-pro")

# Dummy user data for authentication (replace this with a database or other secure storage in production)
users = {
    "testuser": "password123"  # Example username and password
}

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            flash("Login successful!", "success")  # Flash a success message
            return redirect(url_for('home'))  # Redirect to the homepage
        else:
            flash("Invalid username or password", "danger")  # Flash an error message

    return render_template('login.html')

# Route to handle the form submission via POST request
@app.route('/generate', methods=['POST'])
def generate_text():
    prompt = request.form['prompt']  # Get the prompt from the form
    response = model.generate_content(prompt)  # Generate text using Gemini model
    return jsonify({'response': response.text})  # Return the generated text as JSON

if __name__ == '__main__':
    app.run(debug=True)
