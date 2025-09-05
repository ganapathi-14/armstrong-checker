from flask import Flask, request, redirect, url_for, session, render_template_string
import math

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Utility functions
def is_armstrong(number):
    digits = str(number)
    n = len(digits)
    return sum(int(d)**n for d in digits) == number

def is_even(number):
    return number % 2 == 0

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number))+1):
        if number % i == 0:
            return False
    return True

def is_palindrome(number):
    return str(number) == str(number)[::-1]

def factorial(number):
    return math.factorial(number)

def sum_digits(number):
    return sum(int(d) for d in str(number))

def reverse_number(number):
    return int(str(number)[::-1])

def square(number):
    return number**2

def cube(number):
    return number**3

def count_digits(number):
    return len(str(number))

# Templates
home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
    <style>
        body {
            background-color: #0288d1;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background-color: #003f7f;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
            text-align: center;
            color: white;
        }
        input, button {
            padding: 10px;
            margin-top: 20px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        }
        input {
            width: 250px;
        }
        button {
            background-color: #ff9800;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #e68900;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Enter Your Name</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Your Name" required><br>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
"""

menu_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Menu</title>
    <style>
        body {
            background-color: #0288d1;
            font-family: Arial, sans-serif;
            text-align: center;
            color: white;
        }
        .container {
            margin-top: 50px;
        }
        .button {
            background-color: #003f7f;
            color: white;
            padding: 15px 25px;
            margin: 10px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #002f5c;
        }
        form input {
            padding: 10px;
            width: 300px;
            border-radius: 5px;
            border: none;
            margin-top: 20px;
        }
        form button {
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            background-color: #ff9800;
            color: white;
            margin-left: 10px;
            cursor: pointer;
        }
        form button:hover {
            background-color: #e68900;
        }
        a.exit {
            color: white;
            display: block;
            margin-top: 30px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>Hello {{ username }}! Welcome to this page Created by Sai Ganapathi</h1>
    <div class="container">
        {% for func, label in functions.items() %}
            <a href="{{ url_for('check', function_name=func) }}"><button class="button">{{ label }}</button></a>
        {% endfor %}
    </div>
    <form action="mailto:saiganapathiasodu2@gmail.com" method="get">
        <input type="text" name="body" placeholder="Enter feedback here..." required>
        <button type="submit">Submit Feedback</button>
    </form>
    <a class="exit" href="{{ url_for('logout') }}">Exit</a>
</body>
</html>
"""

check_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ function_name }}</title>
    <style>
        body {
            background-color: #0288d1;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background-color: #003f7f;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
            text-align: center;
            color: white;
            width: 400px;
        }
        input, button {
            padding: 10px;
            margin-top: 20px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        }
        input {
            width: 250px;
        }
        button {
            background-color: #ff9800;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #e68900;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .success { color: #4caf50; }
        .fail { color: #f44336; }
        a { color: white; display: block; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ function_name.replace("_"," ").title() }}</h1>
        <form method="POST">
            <input type="number" name="number" placeholder="Enter number" required>
            <button type="submit">Check</button>
        </form>
        {% if result is not none %}
            <div class="result {% if 'NOT' in result or 'Not' in result %}fail{% else %}success{% endif %}">
                Result: {{ result }}
            </div>
        {% endif %}
        <a href="{{ url_for('menu') }}">← Back to Menu</a>
    </div>
</body>
</html>
"""

functions_dict = {
    "armstrong": "Check Armstrong",
    "evenodd": "Even or Odd",
    "prime": "Check Prime",
    "palindrome": "Check Palindrome",
    "factorial": "Factorial",
    "sumdigits": "Sum of Digits",
    "reverse": "Reverse Number",
    "square": "Square",
    "cube": "Cube",
    "countdigits": "Count Digits"
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('menu'))
    return render_template_string(home_template)

@app.route("/menu")
def menu():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template_string(menu_template, username=session['username'], functions=functions_dict)

@app.route("/check/<function_name>", methods=["GET", "POST"])
def check(function_name):
    if 'username' not in session:
        return redirect(url_for('home'))

    result = None
    if request.method == "POST":
        number = int(request.form['number'])
        if function_name == "armstrong":
            result = f"{number} is {'an Armstrong number' if is_armstrong(number) else 'NOT an Armstrong number'}"
        elif function_name == "evenodd":
            result = f"{number} is {'Even' if is_even(number) else 'Odd'}"
        elif function_name == "prime":
            result = f"{number} is {'Prime' if is_prime(number) else 'Not Prime'}"
        elif function_name == "palindrome":
            result = f"{number} is {'Palindrome' if is_palindrome(number) else 'Not Palindrome'}"
        elif function_name == "factorial":
            result = f"Factorial of {number} is {factorial(number)}"
        elif function_name == "sumdigits":
            result = f"Sum of digits of {number} is {sum_digits(number)}"
        elif function_name == "reverse":
            result = f"Reverse of {number} is {reverse_number(number)}"
        elif function_name == "square":
            result = f"Square of {number} is {square(number)}"
        elif function_name == "cube":
            result = f"Cube of {number} is {cube(number)}"
        elif function_name == "countdigits":
            result = f"{number} has {count_digits(number)} digits"

    return render_template_string(check_template, function_name=function_name, result=result)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
