import hashlib, json
from . import db, models, schemas, llm_utils

DB = db.init_db()

def fetch_html(url):
    import requests
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text

def extract_article(html, url):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', id='firstHeading')
    title = title.get_text(strip=True) if title else url
    p = soup.select_one('#mw-content-text p')
    summary = p.get_text(strip=True) if p else ''
    sections = [h.get_text(strip=True) for h in soup.select('#mw-content-text h2 .mw-headline')]
    return {'title': title, 'summary': summary, 'sections': sections, 'raw_html': html}

def process_url(url):
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    existing = DB.query(models.QuizRecord).filter_by(url_hash=url_hash).first()
    if existing:
        return schemas.QuizRecordOut.from_orm(existing)
    html = fetch_html(url)
    article = extract_article(html, url)
    quiz, related = llm_utils.generate_quiz_and_topics(article['title'], article['summary'] + '\\n' + article['raw_html'])
    rec = models.QuizRecord(url=url, url_hash=url_hash, title=article['title'], summary=article['summary'],
                            sections="|".join(article['sections']), quiz_json=json.dumps(quiz), related_json=json.dumps(related),
                            raw_html=article['raw_html'])
    DB.add(rec); DB.commit(); DB.refresh(rec)
    return schemas.QuizRecordOut.from_orm(rec)

def list_history():
    rows = DB.query(models.QuizRecord).order_by(models.QuizRecord.created_at.desc()).all()
    return [schemas.QuizRecordList.from_orm(r) for r in rows]

def get_record(record_id:int):
    r = DB.query(models.QuizRecord).filter_by(id=record_id).first()
    if not r:
        return None
    return schemas.QuizRecordOut.from_orm(r)
