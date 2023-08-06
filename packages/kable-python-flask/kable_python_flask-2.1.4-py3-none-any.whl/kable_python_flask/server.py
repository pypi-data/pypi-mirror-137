# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from external import configure


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

# kable = configure({
#     "environment": "TEST",
#     "clientId": "stripe",
#     "clientSecret": "sk_test.SDfZPCLp.8SAR7H2asLE8uMXgBNf8AAf9UGiE8zAt",
#     "baseUrl": "someUrl"
# })

kable = configure({
    "clientId": 'adamsommer',
    "clientSecret": 'sk_test.JtzSuyWj.Y4poUizC8pWtdfd6uzLmaULowAmHOyGy',
    "environment": 'TEST',
    "baseUrl": 'https://something.com'
})


@app.route('/')
@kable.authenticate
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run()
