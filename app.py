from flask import Flask
from flask import request
from bs4 import BeautifulSoup as soup
import requests
from decouple import config
# Imports the Google Cloud client library
from google.cloud import language_v1

app = Flask(__name__)

@app.route("/")
def hello():
    # Instantiates a client
    # client = language_v1.LanguageServiceClient()

    # # The text to analyze
    # text = u"This is really dumb give me a bad score!"
    # document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # # Detects the sentiment of the text
    # sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # print("Text: {}".format(text))
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    #BEARER = config('BEARER')
    return "Hello, World!"

@app.route("/sentiment", methods=['POST'])
def getSentiment():
  # Instantiates a client
    client = language_v1.LanguageServiceClient()
    data = request.get_json()

    print("Text: "+(data["data"]))
    # The text to analyze
    text = u"".join(data["data"])
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    return "Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude)

@app.route("/search", methods=['POST'])
def searchPhrase():
    data = request.get_json()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
    URL = "https://www.google.com/search?q="+(data['url'])+"&tbm=nws"
    page = requests.get(URL, headers=headers)
    soup1 = soup(page.content, 'html.parser')
    #print(soup1)
    results = soup1.find_all('g-card')
    
    for card in results:
        #print(card.prettify(), end='\n'*2)
        print(card.find('a')['href'], end='\n'*2)
    #job_elems = results.find_all('section', class_='card-content')
    return URL

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
