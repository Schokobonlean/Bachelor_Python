from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def main():
    return "worked", 200