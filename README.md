# Intelligent Document Analysis System

An interactive desktop application built with Python and Tkinter for comprehensive document analysis. This tool helps users compare two documents by detecting plagiarism, calculating similarity, providing detailed feedback on differences, analyzing sentiment, and grading content quality.

# Features

- **Plagiarism Detection & Similarity Score**  
  Calculates how similar two documents are, helping identify copied or overlapping content.

- **Difference Feedback**  
  Highlights differences line-by-line between Document 1 and Document 2 with clear, actionable feedback.

- **Sentiment Analysis**  
  Analyzes the sentiment polarity of each document and visualizes results with an embedded bar chart.

- **Content Grading**  
  Provides a simple grade (A-D) based on similarity metrics to assess document quality.

- **User-Friendly GUI**  
  Designed with a modern and appealing interface using pista green and pastel pink colors for a smooth user experience.

# Technologies Used

- Python 3.x  
- Tkinter (GUI)  
- TextBlob (Sentiment Analysis)  
- Matplotlib (Visualization)  
- Difflib (Text similarity)  

# Installation

1. Clone the repository:

git clone https://github.com/YourUsername/intelligent-document-analysis.git

cd intelligent-document-analysis

2. Create and activate a virtual environment:

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:

pip install -r requirements.txt

4. Run the application:

python app.py
