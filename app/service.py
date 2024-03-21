"""
Service layer for managing articles.

This module provides functions to interact with articles in the application.
It utilizes the database session (`session`) from `app.db` and the `Article` model from `app.model`.
"""
import logging
from typing import List
from app.model import Article
from app import db
from sqlalchemy import or_
from app.news import check_url
logger = logging.getLogger(__name__)


def get_articles_with_keywords(keywords: List[str]) -> List[Article]:
    """
    Fetches articles containing at least one keyword from the database.

    This function searches for articles whose headers contain at least one of the provided keywords.
    Articles are retrieved in descending order of their timestamps (newest first).

    Args:
      keywords: A list of keywords to search for.

    Returns:
        A list of articles matching the criteria.
        If no keywords are provided, an empty list is returned.
    """
    if not keywords: 
        return []
    
    conditions = [Article.header.like(f"%{keyword}%") for keyword in keywords]  
    query = db.session.query(Article).order_by(Article.timestamp.desc()).filter(or_(*conditions))    
    return query.all()


def save_article_if_new(article: Article) -> None:    
    """
    Saves an article if it's not already in the database based on URL.

    This function checks if the article already exists in the database based on its URL.
    If the article is new (has a URL and a header), it's added to the database.

    Args:
        article: The article object to save.
    """
    if not article.url or not article.header:
        return   
    
    if check_url(article.url)!=True:
        return

    try:                
        existing_article = db.session.query(Article).filter_by(url=article.url).first()

        if not existing_article:
            new_article = Article(header=article.header, url=article.url)
            db.session.add(new_article)
            db.session.commit()
    except Exception as e:
        logger.error(f"Error saving article: {e}")
        
        db.session.close()