from flask import Flask, render_template_string

from backend.template import TEMPLATE

app = Flask(__name__)

# Dummy generative content
def generate_dummy_content():
    categories = ['main', 'sub', 'sport', 'weather', 'humour']
    dummy_content = {}
    for category in categories:
        dummy_content[category] = [{
            'title': 'Lorem Ipsum',
            'subtitle': 'Dolor sit amet',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'image': 'test.png',  # Placeholder image. Make sure to replace with the correct path or URL.
        } for _ in range(3)]  # Generate 3 dummy articles per category
    return dummy_content

@app.route('/')
def home():
    content = generate_dummy_content()
    return render_template_string(TEMPLATE, content=content)

if __name__ == "__main__":
    app.run(debug=True)
