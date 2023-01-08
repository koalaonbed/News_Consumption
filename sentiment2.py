import argparse
import os
from google.cloud import language_v1
import csv


credential_path = 'My_First_Project-a54e1af6d90b.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

"""
def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    result = []
    
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        result.append(
            "Sentence {} has a sentiment score of {}".format(index, sentence_sentiment)
        )
    

    result.append(
        "Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude)
    )
    

    result.extend(
        [score, magnitude]
    )
    print(score,magnitude)
    return result

"""

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    #language = "en"
    document = {"content": text_content, "type_": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )

    return response.document_sentiment.score, response.document_sentiment.magnitude

    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))
    


def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    #client = language_v1.LanguageServiceClient()

    with open(movie_review_filename, "r",encoding="utf-8") as review_file: 
        # Instantiates a plain text document.
        rows = csv.reader(review_file)
        #content = review_file.read()
        for i,row in enumerate(rows):
            if i==0:
                with open("sentiment_coding/1108_1129_sent.csv", 'a', newline='', encoding="utf-8-sig") as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                continue
            """
            data = []
            data.append(row[0])
            data.append(row[1])
            """
            if row[9]!="-1":
                #document = language_v1.Document(content=row[9], type_=language_v1.Document.Type.PLAIN_TEXT)
                #annotations = client.analyze_sentiment(request={'document': document, 'encoding_type' : language_v1.EncodingType.UTF8})
                row.extend(sample_analyze_sentiment(row[9]))
            else:
                row.extend([-99,-99])

            if row[17]!="-1":
                print(row[17])
                #document = language_v1.Document(content=row[16], type_=language_v1.Document.Type.PLAIN_TEXT)
                #annotations = client.analyze_sentiment(request={'document': document, 'encoding_type' : language_v1.EncodingType.UTF8})
                row.extend(sample_analyze_sentiment(row[17]))
            else:
                row.extend([-99,-99])
            """
            if row[41]!="-1":
                document = language_v1.Document(content=row[41], type_=language_v1.Document.Type.PLAIN_TEXT)
                annotations = client.analyze_sentiment(request={'document': document})
                row.extend(print_result(annotations))
            else:
                row.extend([-99,-99])
            """
            with open("sentiment_coding/1108_1129_sent.csv", 'a', newline='', encoding="utf-8-sig") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)




if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "filename",
        help="The filename of the movie review you'd like to analyze.",
    )
    args = parser.parse_args()
    '''

    # the file consists of sentences which you want to analyze
    # analyze(args.movie_review_filename)

    analyze("sentiment_coding/1108_1129.csv")






