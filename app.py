from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a strong, random key

# In-memory storage for names and numbers
entries = []

@app.route('/')
def index():
    return render_template('index.html', previous_entries=entries)

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

    global entries
    entries = list(zip(name_list, number_list))

    return render_template('greeting.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
