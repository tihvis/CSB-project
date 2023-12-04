from flask import Flask
from flask import flash, request, render_template, redirect, session

app = Flask(__name__)

import routes