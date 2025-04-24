from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Missing 'company' parameter"}), 400

    # Format search query
    query = quote(f"{company} ESG sustainability controversy site:news.google.com")
    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = [h.get_text() for h in soup.select("h3")][:5]
    except Exception as e:
        headlines = [f"Error fetching headlines: {e}"]

    # Wikipedia Snippet
    wiki_query = quote(f"{company} site:en.wikipedia.org")
    wiki_url = f"https://www.google.com/search?q={wiki_query}"

    try:
        wiki_response = requests.get(wiki_url, headers=headers)
        wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
        snippets = [span.get_text() for span in wiki_soup.select("span") if company.lower() in span.get_text().lower()]
        summary = snippets[0] if snippets else "No Wikipedia summary found."
    except Exception as e:
        summary = f"Error fetching summary: {e}"

    return jsonify({
        "company": company,
        "summary": summary,
        "headlines": headlines,
        "positives": [
            f"{company} may have net-zero targets or ESG disclosures",
            f"{company} may publish annual sustainability reports"
        ],
        "red_flags": [
            f"{company} may have faced controversy, lawsuits or greenwashing accusations"
        ]
    })
