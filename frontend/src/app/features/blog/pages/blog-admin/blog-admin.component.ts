import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { BlogService, BlogPost, BlogPostList, BlogPostCreate, BlogPostUpdate } from '../../services/blog.service';

@Component({
  selector: 'app-blog-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, MatSnackBarModule],
  templateUrl: './blog-admin.component.html',
  styleUrls: ['./blog-admin.component.scss']
})
export class BlogAdminComponent implements OnInit {
  posts: BlogPostList[] = [];
  isLoading = false;
  showEditor = false;
  isEditing = false;
  editingPostId: number | null = null;

  // Form fields
  postTitle = '';
  postExcerpt = '';
  postContent = '';
  postThumbnailUrl = '';
  postIsPublished = false;

  constructor(
    private blogService: BlogService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadPosts();
  }

  loadPosts(): void {
    this.isLoading = true;
    this.blogService.getAllPosts().subscribe({
      next: (posts) => {
        this.posts = posts;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading posts:', error);
        this.snackBar.open('Failed to load posts', 'Close', { duration: 3000 });
        this.isLoading = false;
      }
    });
  }

  openNewPost(): void {
    this.resetForm();
    this.showEditor = true;
    this.isEditing = false;
  }

  editPost(post: BlogPostList): void {
    this.isLoading = true;
    this.blogService.getPost(post.id).subscribe({
      next: (fullPost) => {
        this.postTitle = fullPost.title;
        this.postExcerpt = fullPost.excerpt || '';
        this.postContent = fullPost.content;
        this.postThumbnailUrl = fullPost.thumbnail_url || '';
        this.postIsPublished = fullPost.is_published;
        this.editingPostId = fullPost.id;
        this.showEditor = true;
        this.isEditing = true;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading post:', error);
        this.snackBar.open('Failed to load post', 'Close', { duration: 3000 });
        this.isLoading = false;
      }
    });
  }

  savePost(): void {
    if (!this.postTitle.trim() || !this.postContent.trim()) {
      this.snackBar.open('Title and content are required', 'Close', { duration: 3000 });
      return;
    }

    this.isLoading = true;

    if (this.isEditing && this.editingPostId) {
      const updateData: BlogPostUpdate = {
        title: this.postTitle,
        excerpt: this.postExcerpt || null,
        content: this.postContent,
        thumbnail_url: this.postThumbnailUrl || null,
        is_published: this.postIsPublished
      };

      this.blogService.updatePost(this.editingPostId, updateData).subscribe({
        next: () => {
          this.snackBar.open('Post updated successfully', 'Close', { duration: 3000 });
          this.closeEditor();
          this.loadPosts();
        },
        error: (error) => {
          console.error('Error updating post:', error);
          this.snackBar.open('Failed to update post', 'Close', { duration: 3000 });
          this.isLoading = false;
        }
      });
    } else {
      const createData: BlogPostCreate = {
        title: this.postTitle,
        excerpt: this.postExcerpt || null,
        content: this.postContent,
        thumbnail_url: this.postThumbnailUrl || null,
        is_published: this.postIsPublished
      };

      this.blogService.createPost(createData).subscribe({
        next: () => {
          this.snackBar.open('Post created successfully', 'Close', { duration: 3000 });
          this.closeEditor();
          this.loadPosts();
        },
        error: (error) => {
          console.error('Error creating post:', error);
          this.snackBar.open('Failed to create post', 'Close', { duration: 3000 });
          this.isLoading = false;
        }
      });
    }
  }

  togglePublish(post: BlogPostList): void {
    if (post.is_published) {
      this.blogService.unpublishPost(post.id).subscribe({
        next: () => {
          this.snackBar.open('Post unpublished', 'Close', { duration: 3000 });
          this.loadPosts();
        },
        error: (error) => {
          console.error('Error unpublishing:', error);
          this.snackBar.open('Failed to unpublish', 'Close', { duration: 3000 });
        }
      });
    } else {
      this.blogService.publishPost(post.id).subscribe({
        next: () => {
          this.snackBar.open('Post published', 'Close', { duration: 3000 });
          this.loadPosts();
        },
        error: (error) => {
          console.error('Error publishing:', error);
          this.snackBar.open('Failed to publish', 'Close', { duration: 3000 });
        }
      });
    }
  }

  deletePost(post: BlogPostList): void {
    if (!confirm(`Are you sure you want to delete "${post.title}"?`)) {
      return;
    }

    this.blogService.deletePost(post.id).subscribe({
      next: () => {
        this.snackBar.open('Post deleted', 'Close', { duration: 3000 });
        this.loadPosts();
      },
      error: (error) => {
        console.error('Error deleting:', error);
        this.snackBar.open('Failed to delete post', 'Close', { duration: 3000 });
      }
    });
  }

  uploadImage(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    this.isLoading = true;

    this.blogService.uploadImage(file).subscribe({
      next: (response) => {
        this.postThumbnailUrl = response.url;
        this.snackBar.open('Image uploaded', 'Close', { duration: 3000 });
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error uploading:', error);
        this.snackBar.open('Failed to upload image', 'Close', { duration: 3000 });
        this.isLoading = false;
      }
    });
  }

  closeEditor(): void {
    this.showEditor = false;
    this.resetForm();
    this.isLoading = false;
  }

  private resetForm(): void {
    this.postTitle = '';
    this.postExcerpt = '';
    this.postContent = '';
    this.postThumbnailUrl = '';
    this.postIsPublished = false;
    this.editingPostId = null;
    this.isEditing = false;
  }

  formatDate(dateStr: string | null): string {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  }
}
