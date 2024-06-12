import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
    # print(list(posts_map))
    
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200
    
    
def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 401
    
def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_get_one_unexisting_post(authorized_client):
    response = authorized_client.get("/posts/88888")
    assert response.status_code == 404
    
def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [("1st new title", "1st new content", True),
                                                       ("2nd new title", "2nd new content", True),
                                                       ("3rd new title", "3rd new content", False),])   
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
def test_create_post_default_published_true(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={"title": "random test title", "content": "random test content"})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "random test title"
    assert created_post.content == "random test content"
    assert created_post.owner_id == test_user['id']
    
def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={"title": "random test title", "content": "random test content"})
    assert response.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_delete_post_success(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204
    
def test_delete_post_non_exist(authorized_client):
    response = authorized_client.delete(f"/posts/9876564321")
    assert response.status_code == 404

    
def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403
    
    
def test_update_post(authorized_client, test_posts):
    data = {"title": "updated title",
            "content": "updated content",
            "id": test_posts[0].id}
    
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    
def test_update_other_user_post(authorized_client, test_posts):
    data = {"title": "updated title",
            "content": "updated content",
            "id": test_posts[3].id}
    
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403
    
def test_unauthorized_user_update_post(client, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_update_post_non_exist(authorized_client, test_posts):
    data = {"title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id}
    response = authorized_client.put(f"/posts/9876564321", json=data)
    assert response.status_code == 404