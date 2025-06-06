
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import nltk
nltk.download('punkt')

app = Flask(__name__)

def calculate_similarity(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')

    similarity = calculate_similarity(text1, text2)
    sentiment1 = TextBlob(text1).sentiment
    sentiment2 = TextBlob(text2).sentiment

    return jsonify({
        "similarity": round(similarity * 100, 2),
        "sentiment1": {
            "polarity": sentiment1.polarity,
            "subjectivity": sentiment1.subjectivity
        },
        "sentiment2": {
            "polarity": sentiment2.polarity,
            "subjectivity": sentiment2.subjectivity
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
