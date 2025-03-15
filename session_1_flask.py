from flask import Flask

# Create Flask app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Runs the app in debug mode
