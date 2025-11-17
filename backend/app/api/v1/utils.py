from fastapi import APIRouter, HTTPException, status
import httpx

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
