from typing import List
from app import schemas
def test_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    print(res.json())
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200