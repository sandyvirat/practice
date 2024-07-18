from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a strong, random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///names_numbers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for storing names and numbers
class NameNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    previous_entries = NameNumber.query.all()
    return render_template('index.html', previous_entries=previous_entries)

@app.route('/greet', methods=['POST'])
def greet():
    names = request.form['names']
    numbers = request.form['numbers']

    name_list = names.split(',')
    number_list = numbers.split(',')

    # Remove any extra whitespace
    name_list = [name.strip() for name in name_list]
    number_list = [number.strip() for number in number_list]

    # Ensure both lists have the same length
    if len(name_list) != len(number_list):
        return "Error: The number of names and numbers must be equal."

    entries = list(zip(name_list, number_list))

    for name, number in entries:
        # Add the new entries to the database
        new_entry = NameNumber(name=name, number=number)
        db.session.add(new_entry)
    db.session.commit()

    return render_template('greeting.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
