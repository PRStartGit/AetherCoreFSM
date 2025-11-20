"""
File Storage Service
Handles file uploads to local storage or cloud storage (S3, Azure, etc.)
"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import io


class StorageService:
    """
    Storage service that handles file uploads.
    Currently uses local storage, but can be extended to use S3, Azure, etc.
    """
    
    def __init__(self, base_path: str = "/app/uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Image settings
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        self.thumbnail_size = (800, 800)  # Max dimensions for thumbnails
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        return Path(filename).suffix.lower()
    
    def _validate_image(self, file: UploadFile) -> None:
        """Validate uploaded image file"""
        # Check file extension
        ext = self._get_file_extension(file.filename or "")
        if ext not in self.allowed_extensions:
            allowed_types = ", ".join(self.allowed_extensions)
            raise ValueError(
                f"Invalid file type. Allowed types: {allowed_types}"
            )
        
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if size > self.max_image_size:
            max_size_mb = self.max_image_size / 1024 / 1024
            raise ValueError(f"File too large. Maximum size: {max_size_mb}MB")
    
    def _optimize_image(self, image_data: bytes, filename: str) -> bytes:
        """Optimize image size and quality"""
        try:
            # Open image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert RGBA to RGB if needed
            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")
            
            # Resize if too large
            if image.width > self.thumbnail_size[0] or image.height > self.thumbnail_size[1]:
                image.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            output = io.BytesIO()
            ext = self._get_file_extension(filename)
            
            if ext in [".jpg", ".jpeg"]:
                image.save(output, format="JPEG", quality=85, optimize=True)
            elif ext == ".png":
                image.save(output, format="PNG", optimize=True)
            elif ext == ".webp":
                image.save(output, format="WEBP", quality=85)
            else:
                image.save(output, format="JPEG", quality=85, optimize=True)
            
            return output.getvalue()
        except Exception as e:
            # If optimization fails, return original
            print(f"Image optimization failed: {e}")
            return image_data
    
    async def upload_file(
        self,
        file: UploadFile,
        subfolder: str = "photos",
        optimize: bool = True
    ) -> str:
        """
        Upload a file to storage
        
        Args:
            file: The uploaded file
            subfolder: Subfolder to store the file in (e.g., photos, defects)
            optimize: Whether to optimize images
        
        Returns:
            The URL/path to access the uploaded file
        """
        # Validate file
        self._validate_image(file)
        
        # Generate unique filename
        ext = self._get_file_extension(file.filename or "")
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        # Create subfolder
        upload_dir = self.base_path / subfolder
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Full file path
        file_path = upload_dir / unique_filename
        
        # Read file data
        file_data = await file.read()
        
        # Optimize if requested
        if optimize and ext in self.allowed_extensions:
            file_data = self._optimize_image(file_data, file.filename or "")
        
        # Write file
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        # Return relative URL (will be served by FastAPI static files or nginx)
        return f"/uploads/{subfolder}/{unique_filename}"
    
    def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from storage
        
        Args:
            file_url: The URL/path of the file to delete
        
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Extract path from URL
            if file_url.startswith("/uploads/"):
                rel_path = file_url[len("/uploads/"):]
                file_path = self.base_path / rel_path
                
                if file_path.exists():
                    file_path.unlink()
                    return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False


# Global storage service instance
storage_service = StorageService()
