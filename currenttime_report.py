import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator

def fetch_currenttime_headlines():
    """Fetch Russian headlines from Current Time website"""
    url = "https://www.currenttime.tv/"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # These selectors might need adjustment as website structure changes
        headlines = []
        for item in soup.select('.main-news__item, .news-feed__item'):
            title = item.get_text(strip=True)
            if title and len(title) > 10:  # Basic filter for actual headlines
                headlines.append(title)
        return headlines[:10]  # Return top 10 headlines
    except Exception as e:
        print(f"Error fetching headlines: {e}")
        return []

def translate_to_english(texts, src_lang='ru'):
    """Translate Russian text to English"""
    translator = Translator()
    translations = []
    for text in texts:
        try:
            translated = translator.translate(text, src=src_lang, dest='en')
            # Make translation sound more like broadcast English
            polished = polished_translation(translated.text)
            translations.append(polished)
        except Exception as e:
            print(f"Error translating '{text}': {e}")
            translations.append(text)  # Fallback to original if translation fails
    return translations

def polished_translation(text):
    """Improve machine translation to sound more like broadcast news"""
    replacements = {
        "Russian Federation": "Russia",
        "Ukrainian conflict": "Ukraine war",
        "According to reports": "Reports indicate",
        "It was reported": "Sources report",
        "Ministry of Defense": "Defense Ministry"
    }
    for rus, eng in replacements.items():
        text = text.replace(rus, eng)
    return text

def create_news_report(original_headlines, translated_headlines):
    """Format the translated headlines into a professional report"""
    report = "CURRENT TIME NEWS REPORT\n"
    report += "="*40 + "\n\n"
    report += "Latest Headlines (Translated from Russian)\n\n"
    
    for i, (orig, trans) in enumerate(zip(original_headlines, translated_headlines), 1):
        report += f"{i}. {trans}\n"
        report += f"   [Original: {orig}]\n\n"
    
    report += "\nReport generated automatically. For informational purposes only.\n"
    return report

def send_email(report, recipient, subject="Current Time News Report"):
    """Simulate sending email (would need real credentials to work)"""
    print(f"\nEmail would be sent to: {recipient}")
    print(f"Subject: {subject}")
    print("\nEmail content:\n")
    print(report)
    print("\n[Email sending would require proper SMTP configuration]")

def main():
    print("Fetching headlines from Current Time...")
    russian_headlines = fetch_currenttime_headlines()
    
    print("\nTranslating headlines to English...")
    english_headlines = translate_to_english(russian_headlines)
    
    print("\nGenerating news report...")
    report = create_news_report(russian_headlines, english_headlines)
    
    print("\n=== CURRENT TIME NEWS REPORT ===\n")
    print(report)
    
    # Simulate email sending
    recipient = "user@example.com"  # This would be provided by user input
    send_email(report, recipient)

if __name__ == "__main__":
    main()