from app import db, service
from app.model import Article
from unittest.mock import patch
from app.tests.config import session, clear_data


def test_save_article_with_invalid_field(session, clear_data):
    article = Article(header="", url="https://example.com/empty-header-article")
    service.save_article_if_new(article)
    saved_article = db.session.query(Article).filter_by(url=article.url).first()
    assert saved_article is None, "Article with empty header should not be saved"
    
    article = Article(header="New header", url="")
    saved_article = db.session.query(Article).filter_by(url=article.url).first()
    service.save_article_if_new(article)
    assert saved_article is None, "Article with empty URL should not be saved"
    
    article = Article(header="Nový titulek", url="invalid_url")
    service.save_article_if_new(article)
    saved_article = db.session.query(Article).filter_by(url=article.url).first()
    assert saved_article is None, "Article with invalid URL should not be saved"

    article = Article(header="Nový titulek", url="https://invalid_url")
    service.save_article_if_new(article)
    saved_article = db.session.query(Article).filter_by(url=article.url).first()
    assert saved_article is None, "Article with invalid URL should not be saved" 


def test_save_new_article(session, clear_data):
    article = Article(header="New header", url="https://example.com/new-article")
    service.save_article_if_new(article)
    saved_article = db.session.query(Article).filter_by(url=article.url).first()

    assert saved_article is not None, "New article should be saved"
    assert saved_article.header == article.header, "New article should be saved"  


def test_save_existing_article(session, clear_data):
    existing_article = Article(header="Existing header", url="https://example.com/existing-article")
    db.session.add(existing_article)
    db.session.commit()    
    new_article = Article(header="New header", url="https://example.com/existing-article")
    service.save_article_if_new(new_article)
    saved_article = db.session.query(Article).filter_by(url=new_article.url).first()

    assert saved_article.header == existing_article.header, "Article with existing URL should not be saved"


def test_save_article_with_duplicate_title_but_different_url(session, clear_data):

    existing_article = Article(header="New header", url="https://example.com/existing-article")
    db.session.add(existing_article)
    db.session.commit()

    new_article = Article(header="New header", url="https://example.com/new-article-2")
    service.save_article_if_new(new_article)

    saved_articles = db.session.query(Article).filter_by(header="New header").all()
    assert len(saved_articles) == 2
    assert saved_articles[0].url == "https://example.com/existing-article", "Article with non-existent URL should be saved"
    assert saved_articles[1].url == "https://example.com/new-article-2", "Article with non-existent URL should be saved"


def test_save_article_add_db_error(session, clear_data):

    article = Article(header="Error header", url="https://example.com/error-article")
    with patch('app.db.session.add') as mock_add:
        mock_add.side_effect = Exception("Chyba databáze")
        service.save_article_if_new(article)

    saved_article = db.session.query(Article).filter_by(url=article.url).first()
    assert saved_article is None, "With DB error article should not be saved"


def test_get_articles_with_keywords(session, clear_data):
    db.session.add(Article(header='a b c', url=''))
    db.session.add(Article(header='b c d', url=''))
    db.session.add(Article(header='x y z', url=''))
    db.session.commit()

    assert service.get_articles_with_keywords(keywords=['aaa']) == [], "No match keyword should return []"
    assert service.get_articles_with_keywords(keywords=[]) == [], "Empty keywords list should return []"

    assert service.get_articles_with_keywords(keywords=['a'])[0].header == 'a b c'
    assert service.get_articles_with_keywords(keywords=['d'])[0].header == 'b c d'
    assert service.get_articles_with_keywords(keywords=['y'])[0].header == 'x y z'
    assert len(service.get_articles_with_keywords(keywords=['a'])) == 1
    assert len(service.get_articles_with_keywords(keywords=['b'])) == 2
    
    assert len(service.get_articles_with_keywords(keywords=['b','c'])) == 2
    assert 'a b c' in [a.header for a in service.get_articles_with_keywords(keywords=['b', 'c'])]
    assert 'b c d' in [a.header for a in service.get_articles_with_keywords(keywords=['b', 'c'])] 
    db.session.query(Article).delete()
    db.session.commit()