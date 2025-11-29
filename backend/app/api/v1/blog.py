from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_super_admin, get_current_user
from app.models.blog_post import BlogPost
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime
import re
import os
import uuid

router = APIRouter()


def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from a title."""
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().strip()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


# Pydantic schemas
class BlogPostCreate(BaseModel):
    title: str
    excerpt: str | None = None
    content: str
    thumbnail_url: str | None = None
    is_published: bool = False


class BlogPostUpdate(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    thumbnail_url: str | None = None
    is_published: bool | None = None


class BlogPostResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str | None
    content: str
    thumbnail_url: str | None
    is_published: bool
    published_at: datetime | None
    created_by_id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class BlogPostListResponse(BaseModel):
    """Lightweight response for listing blog posts."""
    id: int
    title: str
    slug: str
    excerpt: str | None
    thumbnail_url: str | None
    is_published: bool
    published_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


# Public endpoints
@router.get("/blog/public", response_model=List[BlogPostListResponse])
def list_published_posts(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List published blog posts (Public endpoint for front page)"""
    posts = db.query(BlogPost).filter(
        BlogPost.is_published == True
    ).order_by(
        BlogPost.published_at.desc()
    ).offset(offset).limit(limit).all()
    return posts


@router.get("/blog/public/{slug}", response_model=BlogPostResponse)
def get_published_post_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get a published blog post by slug (Public endpoint)"""
    post = db.query(BlogPost).filter(
        BlogPost.slug == slug,
        BlogPost.is_published == True
    ).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


# Admin endpoints (Super Admin only)
@router.get("/blog", response_model=List[BlogPostListResponse])
def list_all_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """List all blog posts including drafts (Super Admin only)"""
    posts = db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()
    return posts


@router.get("/blog/{post_id}", response_model=BlogPostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Get a specific blog post (Super Admin only)"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


@router.post("/blog", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: BlogPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Create a new blog post (Super Admin only)"""
    # Generate slug from title
    base_slug = generate_slug(post_data.title)
    slug = base_slug

    # Ensure slug is unique
    counter = 1
    while db.query(BlogPost).filter(BlogPost.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    new_post = BlogPost(
        title=post_data.title,
        slug=slug,
        excerpt=post_data.excerpt,
        content=post_data.content,
        thumbnail_url=post_data.thumbnail_url,
        is_published=post_data.is_published,
        published_at=datetime.utcnow() if post_data.is_published else None,
        created_by_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/blog/{post_id}", response_model=BlogPostResponse)
def update_post(
    post_id: int,
    post_data: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Update a blog post (Super Admin only)"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Update fields
    update_data = post_data.model_dump(exclude_unset=True)

    # If title is being updated, update slug too
    if 'title' in update_data:
        base_slug = generate_slug(update_data['title'])
        slug = base_slug
        counter = 1
        while db.query(BlogPost).filter(BlogPost.slug == slug, BlogPost.id != post_id).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        update_data['slug'] = slug

    # If publishing for the first time, set published_at
    if 'is_published' in update_data and update_data['is_published'] and not post.published_at:
        update_data['published_at'] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(post, field, value)

    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)

    return post


@router.delete("/blog/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Delete a blog post (Super Admin only)"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    db.delete(post)
    db.commit()

    return None


@router.post("/blog/{post_id}/publish", response_model=BlogPostResponse)
def publish_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Publish a blog post (Super Admin only)"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    post.is_published = True
    if not post.published_at:
        post.published_at = datetime.utcnow()
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)

    return post


@router.post("/blog/{post_id}/unpublish", response_model=BlogPostResponse)
def unpublish_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Unpublish a blog post (Super Admin only)"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    post.is_published = False
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)

    return post


@router.post("/blog/upload-image")
async def upload_blog_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_super_admin)
):
    """Upload an image for blog posts (Super Admin only)"""
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: JPEG, PNG, GIF, WebP"
        )

    # Create upload directory if it doesn't exist
    upload_dir = "uploads/blog"
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Save file
    contents = await file.read()
    with open(file_path, 'wb') as f:
        f.write(contents)

    # Return the URL
    return {"url": f"/uploads/blog/{unique_filename}"}
