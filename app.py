from flask import Flask, jsonify
from flask import request
from bs4 import BeautifulSoup as soup
import requests
from decouple import config
import json
from dotenv import load_dotenv
import os

# Imports the Google Cloud client library
from google.cloud import language_v1
from google.oauth2 import service_account, credentials
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
# privatekey = config('private_key')
# privatekey = privatekey.replace("\\\\", "\\")
# print(privatekey)
creds2 = service_account.Credentials.from_service_account_info({
  "type": config('type'),
  "project_id": config('project_id'),
  "private_key_id": config('private_key_id'),
#   "private_key": r"".join(config('private_key')),
  "private_key": json.loads(os.environ['private_key']),
#   "private_key": (os.environ['private_key']),


  "client_email": config('client_email'),
  "client_id": config('client_id'),
  "auth_uri": config('auth_uri'),
  "token_uri": config('token_uri'),
  "auth_provider_x509_cert_url": config('auth_provider_x509_cert_url'),
  "client_x509_cert_url": config('client_x509_cert_url')
})


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
    client = language_v1.LanguageServiceClient(credentials=creds2)
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
    # return getSentimentFromWeb

# @app.route("/web", methods=['POST'])
def getSentimentFromWeb(description):
  # Instantiates a client
    # data = request.get_json()
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
    # # URL = request.get_json()['url']
    # URL = url
    # page = requests.get(URL, headers=headers)
    # soup1 = soup(page.content, 'html.parser')
    client = language_v1.LanguageServiceClient(credentials=creds2)
    # data = soup1.find('body').text
    # wordlen = len(data)
    # half = int(wordlen / 2)
    # if half > 1000:
    #     half = wordlen - 100
    # data = data[half:]
    # print("Text: "+(data["data"]))
    # The text to analyze
    text = u"".join(description)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # print("Text: {}".format(text))
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    # return "Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude)
    return sentiment.score
    # return data



@app.route("/testEntity", methods=['POST'])
def getEntity():
  # Instantiates a client
    client = language_v1.LanguageServiceClient(credentials=json.dumps(creds))
    data = request.get_json()

    print("Text: "+(data["data"]))
    # The text to analyze
    text = u"".join(data["data"])

    return getTweetEntities(text)

def getTweetEntities(tweetText):
    client = language_v1.LanguageServiceClient(credentials=creds2)

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    #language = "en"
    document = {"content": tweetText, "type_": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})
    output = ""
    tweetEntities = []
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        #print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        # for metadata_name, metadata_value in entity.metadata.items():
        #     print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            if (not mention.text.content in tweetEntities) and (not "http" in mention.text.content) :
                ents = mention.text.content.split(" ")
                for enti in ents:
                    output += "+" 
                    output += enti
                    tweetEntities.append(enti)

            # Get the mention type, e.g. PROPER for proper noun
            # print(
            #     u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            # )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))
    print(output[1:])
    return output[1:]

def calculateSentimentScore(score):
    sentiment = 50
    multiplier = 50*score
    sentiment += multiplier
    return int(sentiment)

def calcSentimentColor(score):
    if score > 40:
        return 2
    elif score > 25:
        return 1
    return 0

@app.route("/search", methods=['POST'])
def searchPhrase():
    data = request.get_json()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
    tweetEnts = getTweetEntities(data['tweet'])
    URL = "https://www.google.com/search?q="+(tweetEnts)+"&tbm=nws"
    page = requests.get(URL, headers=headers)
    soup1 = soup(page.content, 'html.parser')
    #print(soup1)
    results = soup1.find_all('g-card')
    jsonReturn = []
    
    for card in results:
        #print(card.prettify(), end='\n'*2)
        if len(jsonReturn) < 4:
            print(card.find('a')['href'], end='\n'*2)
            print((card.find('a')).find('g-img').find('img')['src'])
            # 'image': str((card.find('a')).find_all('g-img')[-1].find('img')['src'])
            taga = card.find('a')
            url = card.find('a')['href']
            source = taga.find('div',class_="XTjFC WF4CUc").text
            title = ((taga.find('div',class_="hI5pFf")).text)
            description = taga.find('div', class_="Y3v8qd").text
            timestamp = taga.find('span', class_="WG9SHc").text
            title = title.replace(source,"")
            title = title.replace(description,"")
            title = title.replace(timestamp,"")
            title = title.replace("\n","")
            description = description.replace("\n","")
            sentimentScore = calculateSentimentScore(getSentimentFromWeb(description))
            color = calcSentimentColor(sentimentScore)
            # URL = "https://www.google.com/search?q="+(tweetEnts)+"&tbm=nws"
            page = requests.get(url, headers=headers)
            soup2 = soup(page.content, 'html.parser')
            if soup2.find('meta', property="og:image"):
                imgUrl = soup2.find('meta', property="og:image")['content']
            # imgUrl = 
            print(imgUrl)
            tempJson = {
                'url' : url, 
                'source': source,
                'title': title,
                'timestamp': timestamp,
                'description': description,
                'sentimentScore': sentimentScore,
                'color': color,
                'image': imgUrl
                }
            jsonReturn.append(tempJson)
    #job_elems = results.find_all('section', class_='card-content')
    return jsonify(jsonReturn)
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
