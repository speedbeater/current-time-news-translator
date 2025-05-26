from flask import Flask, render_template, request, redirect, url_for
from currenttime_report import fetch_currenttime_headlines, translate_to_english, create_news_report
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch and translate headlines
        russian_headlines = fetch_currenttime_headlines()
        english_headlines = translate_to_english(russian_headlines)
        report = create_news_report(russian_headlines, english_headlines)
        
        return render_template('index.html', 
                            report=report,
                            show_results=True)
    
    return render_template('index.html', show_results=False)

if __name__ == '__main__':
    app.run(debug=True)