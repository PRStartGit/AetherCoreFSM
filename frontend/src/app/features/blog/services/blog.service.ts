import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string | null;
  content: string;
  thumbnail_url: string | null;
  is_published: boolean;
  published_at: string | null;
  created_by_id: number;
  created_at: string;
  updated_at: string | null;
}

export interface BlogPostList {
  id: number;
  title: string;
  slug: string;
  excerpt: string | null;
  thumbnail_url: string | null;
  is_published: boolean;
  published_at: string | null;
  created_at: string;
}

export interface BlogPostCreate {
  title: string;
  excerpt?: string | null;
  content: string;
  thumbnail_url?: string | null;
  is_published?: boolean;
}

export interface BlogPostUpdate {
  title?: string;
  excerpt?: string | null;
  content?: string;
  thumbnail_url?: string | null;
  is_published?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class BlogService {
  private apiUrl = '/api/v1';

  constructor(private http: HttpClient) {}

  // Public endpoints
  getPublishedPosts(limit: number = 10, offset: number = 0): Observable<BlogPostList[]> {
    return this.http.get<BlogPostList[]>(`${this.apiUrl}/blog/public`, {
      params: { limit: limit.toString(), offset: offset.toString() }
    });
  }

  getPublishedPostBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPost>(`${this.apiUrl}/blog/public/${slug}`);
  }

  // Admin endpoints
  getAllPosts(): Observable<BlogPostList[]> {
    return this.http.get<BlogPostList[]>(`${this.apiUrl}/blog`);
  }

  getPost(id: number): Observable<BlogPost> {
    return this.http.get<BlogPost>(`${this.apiUrl}/blog/${id}`);
  }

  createPost(post: BlogPostCreate): Observable<BlogPost> {
    return this.http.post<BlogPost>(`${this.apiUrl}/blog`, post);
  }

  updatePost(id: number, post: BlogPostUpdate): Observable<BlogPost> {
    return this.http.put<BlogPost>(`${this.apiUrl}/blog/${id}`, post);
  }

  deletePost(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/blog/${id}`);
  }

  publishPost(id: number): Observable<BlogPost> {
    return this.http.post<BlogPost>(`${this.apiUrl}/blog/${id}/publish`, {});
  }

  unpublishPost(id: number): Observable<BlogPost> {
    return this.http.post<BlogPost>(`${this.apiUrl}/blog/${id}/unpublish`, {});
  }

  uploadImage(file: File): Observable<{ url: string }> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<{ url: string }>(`${this.apiUrl}/blog/upload-image`, formData);
  }
}
