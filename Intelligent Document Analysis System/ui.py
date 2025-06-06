import tkinter as tk
from tkinter import scrolledtext, messagebox
import nltk
import difflib
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def get_similarity(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100

def get_sentiment(text):
    return sia.polarity_scores(text)

def get_grade(score):
    if score >= 90: return "A"
    elif score >= 75: return "B"
    elif score >= 60: return "C"
    elif score >= 45: return "D"
    else: return "F"

def get_feedback(t1, t2):
    diff = difflib.unified_diff(t1.split(), t2.split(), lineterm='')
    return "\n".join(diff)

def export_pdf(report_text, path):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    text_obj = c.beginText(40, height - 50)
    text_obj.setFont("Helvetica", 12)
    for line in report_text.split('\n'):
        if text_obj.getY() < 50:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, height - 50)
            text_obj.setFont("Helvetica", 12)
        text_obj.textLine(line)
    c.drawText(text_obj)
    c.save()

class DocumentAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Intelligent Document Analysis System")
        self.root.geometry("1200x850")
        self.root.configure(bg="#c0f0b3")

        self.canvas = tk.Canvas(root, bg="#c0f0b3")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#c0f0b3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Label(self.scrollable_frame, text="Intelligent Document Analysis System",
                 font=("Helvetica", 24, "bold"), bg="#c0f0b3", fg="white").pack(pady=15)

        tk.Label(self.scrollable_frame, text="Enter Text for Document 1:",
                 font=("Arial", 14, "bold"), bg="#c0f0b3", fg="black").pack(pady=5)
        self.doc1_entry = scrolledtext.ScrolledText(self.scrollable_frame, wrap=tk.WORD, width=130, height=8,
                                                    font=("Consolas", 12), bg="#f8c8dc", fg="black")
        self.doc1_entry.pack(pady=5)

        tk.Label(self.scrollable_frame, text="Enter Text for Document 2:",
                 font=("Arial", 14, "bold"), bg="#c0f0b3", fg="black").pack(pady=5)
        self.doc2_entry = scrolledtext.ScrolledText(self.scrollable_frame, wrap=tk.WORD, width=130, height=8,
                                                    font=("Consolas", 12), bg="#f8c8dc", fg="black")
        self.doc2_entry.pack(pady=5)

        tk.Button(self.scrollable_frame, text="Analyze Documents", command=self.analyze_documents,
                  bg="#f8c8dc", fg="black", font=("Arial", 13, "bold"), width=22).pack(pady=15)

        self.result_box = scrolledtext.ScrolledText(self.scrollable_frame, wrap=tk.WORD, width=130, height=14,
                                                    font=("Consolas", 12), bg="#f8c8dc", fg="black")
        self.result_box.pack(pady=10)

        self.chart_frame = tk.Frame(self.scrollable_frame, bg="#c0f0b3")
        self.chart_frame.pack(pady=10)

        tk.Button(self.scrollable_frame, text="Export Report as PDF", command=self.export_report_pdf,
                  bg="#f8c8dc", fg="black", font=("Arial", 13), width=22).pack(pady=5)

        tk.Button(self.scrollable_frame, text="Clear All", command=self.clear_all,
                  bg="#f8c8dc", fg="black", font=("Arial", 13), width=22).pack(pady=5)

    def analyze_documents(self):
        doc1_text = self.doc1_entry.get(1.0, tk.END).strip()
        doc2_text = self.doc2_entry.get(1.0, tk.END).strip()

        if not doc1_text or not doc2_text:
            messagebox.showerror("Input Missing", "Please input both documents before analyzing.")
            return

        similarity = get_similarity(doc1_text, doc2_text)
        grade = get_grade(similarity)
        sentiment1 = get_sentiment(doc1_text)
        sentiment2 = get_sentiment(doc2_text)
        feedback = get_feedback(doc1_text, doc2_text)

        result_text = (
            f"📌 Similarity Score: {similarity:.2f}%\n\n"
            f"🏷️ Grade for Document 2: {grade}\n\n"
            f"😊 Sentiment Analysis:\n"
            f" - Document 1: Pos {sentiment1['pos']}, Neg {sentiment1['neg']}, Neu {sentiment1['neu']}, Compound {sentiment1['compound']}\n"
            f" - Document 2: Pos {sentiment2['pos']}, Neg {sentiment2['neg']}, Neu {sentiment2['neu']}, Compound {sentiment2['compound']}\n\n"
            f"🧾 Feedback (Differences):\n{feedback}"
        )

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result_text)
        self.draw_sentiment_chart(sentiment1, sentiment2)

    def draw_sentiment_chart(self, s1, s2):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = ['Positive', 'Negative', 'Neutral', 'Compound']
        doc1_scores = [s1['pos'], s1['neg'], s1['neu'], s1['compound']]
        doc2_scores = [s2['pos'], s2['neg'], s2['neu'], s2['compound']]

        fig, ax = plt.subplots(figsize=(8, 3))
        bar_width = 0.35
        indices = range(len(labels))

        ax.bar(indices, doc1_scores, bar_width, label='Document 1', color='#7fc97f')
        ax.bar([i + bar_width for i in indices], doc2_scores, bar_width, label='Document 2', color='#beaed4')

        ax.set_xticks([i + bar_width / 2 for i in indices])
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1)
        ax.set_title("Sentiment Scores Comparison")
        ax.legend()

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def export_report_pdf(self):
        from tkinter import filedialog
        report = self.result_box.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            export_pdf(report, file_path)
            messagebox.showinfo("Success", "Report exported successfully!")

    def clear_all(self):
        self.doc1_entry.delete(1.0, tk.END)
        self.doc2_entry.delete(1.0, tk.END)
        self.result_box.delete(1.0, tk.END)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentAnalyzer(root)
    root.mainloop()
