import pytest
from app.api import app
from app import api


def test_find_articles_invalid_data():
    pass
    


    #json 
    """
    1. Valid Request with Articles:
    2. Invalid Request (Missing Keywords):
    3. Invalid Request (Non-JSON Format):
    4. Mocked Error from get_articles_with_keywords (Optional):
    invalid keyword types
    Consider testing edge cases (e.g., empty keyword lists).
    Adapt the tests and assertions to match your expected response structure and error messages.
 
    """

from pytest import fixture  # Assuming you haven't imported it already

@pytest.fixture
def client():
    # Create a test client for your Flask app
    """
    app.run(debug=True)
    with app.find_articles() as client:
        yield client
    """

def test_find_articles_valid_request(client):
  """Tests finding articles with valid keywords."""
    
  data = {'keywords': ['politics', 'technology']}
  #response = client.post('/articles/find', json=data)
  #assert response.status_code == 200
  #assert response.json['articles']  # Check if 'articles' key exists
