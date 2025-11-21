from fastapi import APIRouter, HTTPException, UploadFile, File, status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
import os
from app.core.database import get_db
from app.services.storage import storage_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# GetAddress.io API key (free tier: 20 requests/day)
GETADDRESS_API_KEY = os.getenv("GETADDRESS_API_KEY", "")


@router.get("/utils/postcode-lookup/{postcode}")
async def lookup_postcode(postcode: str):
    """
    Get list of addresses for a UK postcode using GetAddress.io API.
    Falls back to postcodes.io for basic location data if no API key.
    """
    cleaned_postcode = postcode.replace(" ", "").upper()

    try:
        async with httpx.AsyncClient() as client:
            # Try GetAddress.io first if API key is configured
            if GETADDRESS_API_KEY:
                response = await client.get(
                    f"https://api.getaddress.io/find/{cleaned_postcode}",
                    params={"api-key": GETADDRESS_API_KEY, "expand": "true"},
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    addresses = data.get("addresses", [])

                    # Format addresses for frontend
                    formatted_addresses = []
                    for addr in addresses:
                        # GetAddress returns: line_1, line_2, line_3, line_4, locality, town_or_city, county
                        formatted_addresses.append({
                            "line_1": addr.get("line_1", ""),
                            "line_2": addr.get("line_2", ""),
                            "line_3": addr.get("line_3", ""),
                            "town_or_city": addr.get("town_or_city", ""),
                            "county": addr.get("county", ""),
                            "country": "UK",
                            "postcode": cleaned_postcode,
                            "formatted": addr.get("formatted_address", [])
                        })

                    return {
                        "status": 200,
                        "addresses": formatted_addresses,
                        "postcode": cleaned_postcode
                    }

            # Fallback to postcodes.io for basic data
            response = await client.get(
                f"https://api.postcodes.io/postcodes/{cleaned_postcode}",
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                return {
                    "status": 200,
                    "addresses": [{
                        "line_1": "",
                        "line_2": "",
                        "line_3": "",
                        "town_or_city": result.get("admin_district", ""),
                        "county": result.get("admin_county", "") or result.get("region", ""),
                        "country": result.get("country", "UK"),
                        "postcode": cleaned_postcode,
                        "formatted": []
                    }],
                    "postcode": cleaned_postcode,
                    "basic_only": True  # Flag that this is basic data only
                }

            return {"status": 404, "error": "Postcode not found"}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Postcode lookup timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Postcode lookup failed: {str(e)}")


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
