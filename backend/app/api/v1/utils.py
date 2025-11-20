from fastapi import APIRouter, HTTPException, UploadFile, File, status, Depends
from sqlalchemy.orm import Session
import httpx
from app.core.database import get_db
from app.services.storage import storage_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/utils/postcode-lookup/{postcode}")
async def lookup_postcode(postcode: str):
    """
    Proxy endpoint for UK postcode lookup using postcodes.io API.

    This endpoint exists to avoid CORS issues when calling postcodes.io directly from the frontend.
    The frontend HTTP interceptor adds Authorization headers to all requests, which causes
    CORS preflight failures with external APIs.
    """
    # Clean the postcode (remove spaces)
    cleaned_postcode = postcode.replace(" ", "").upper()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.postcodes.io/postcodes/{cleaned_postcode}",
                timeout=10.0
            )

            # Return the response from postcodes.io as-is
            return response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Postcode lookup service timeout"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Postcode lookup service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Postcode lookup failed: {str(e)}"
        )


@router.post("/utils/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a photo file.
    
    This endpoint handles photo uploads for checklist items, defects, etc.
    The file is optimized and stored, and a URL is returned.
    """
    try:
        # Upload and optimize the file
        file_url = await storage_service.upload_file(
            file=file,
            subfolder="photos",
            optimize=True
        )
        
        return {
            "success": True,
            "file_url": file_url,
            "message": "Photo uploaded successfully"
        }
    
    except ValueError as e:
        # Validation errors (file too large, wrong type, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload photo: {str(e)}"
        )


@router.delete("/utils/delete-photo")
async def delete_photo(
    file_url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a photo file.
    
    This endpoint removes a photo from storage.
    """
    try:
        success = storage_service.delete_file(file_url)
        
        if success:
            return {
                "success": True,
                "message": "Photo deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete photo: {str(e)}"
        )
