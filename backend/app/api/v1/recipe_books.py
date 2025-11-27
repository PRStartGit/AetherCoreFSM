from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.recipe_permissions import has_recipe_access, has_recipe_crud
from app.models.user import User
from app.models.site import Site
from app.models.recipe_book import RecipeBook, RecipeBookRecipe
from app.models.recipe import Recipe
from app.schemas.recipe_book import (
    RecipeBookCreate,
    RecipeBookUpdate,
    RecipeBookResponse,
    RecipeBookWithRecipes,
    RecipeInBook,
    AddRecipeToBook,
    RemoveRecipeFromBook,
    SiteInfo
)

router = APIRouter()


def _build_book_response(book: RecipeBook) -> RecipeBookResponse:
    """Build RecipeBookResponse with sites info"""
    sites_info = [SiteInfo(id=site.id, name=site.name) for site in book.sites] if book.sites else []

    return RecipeBookResponse(
        id=book.id,
        organization_id=book.organization_id,
        title=book.title,
        description=book.description,
        site_id=book.site_id,
        sites=sites_info,
        is_active=book.is_active,
        created_by_user_id=book.created_by_user_id,
        created_at=book.created_at,
        updated_at=book.updated_at
    )


@router.post("", response_model=RecipeBookResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_book(
    book: RecipeBookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe book (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create recipe books"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Use user's organization
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    # Create recipe book
    new_book = RecipeBook(
        organization_id=current_user.organization_id,
        site_id=book.site_id,  # Legacy support
        title=book.title,
        description=book.description,
        is_active=book.is_active,
        created_by_user_id=current_user.id
    )

    db.add(new_book)
    db.flush()  # Get the ID

    # Handle multi-site assignment
    if book.site_ids:
        sites = db.query(Site).filter(Site.id.in_(book.site_ids)).all()
        new_book.sites = sites

    db.commit()
    db.refresh(new_book)

    # Build response with sites
    return _build_book_response(new_book)


@router.get("", response_model=List[RecipeBookResponse])
def get_recipe_books(
    site_id: Optional[int] = Query(None, description="Filter by site (NULL = organization-global)"),
    include_inactive: bool = Query(False, description="Include inactive recipe books"),
    organization_id: Optional[int] = Query(None, description="Filter by organization (super admin only)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe books for user's organization (super admin can see all)"""
    from app.models.user import UserRole

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    query = db.query(RecipeBook).options(joinedload(RecipeBook.sites))

    # Super admin can see all recipe books or filter by organization
    if current_user.role == UserRole.SUPER_ADMIN:
        if organization_id is not None:
            query = query.filter(RecipeBook.organization_id == organization_id)
        # If no organization_id, show all
    else:
        # Non-super admins can only see their own organization
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization"
            )
        query = query.filter(RecipeBook.organization_id == current_user.organization_id)

    # Filter by site if specified (check both legacy site_id and multi-site)
    if site_id is not None:
        from app.models.recipe_book import recipe_book_sites
        query = query.filter(
            (RecipeBook.site_id == site_id) |
            RecipeBook.sites.any(Site.id == site_id)
        )

    # Filter by active status
    if not include_inactive:
        query = query.filter(RecipeBook.is_active == True)

    books = query.offset(skip).limit(limit).all()
    return [_build_book_response(book) for book in books]


@router.get("/{book_id}", response_model=RecipeBookWithRecipes)
def get_recipe_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe book by ID with its recipes"""
    from app.models.user import UserRole

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    book = db.query(RecipeBook).options(joinedload(RecipeBook.sites)).filter(RecipeBook.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe book not found"
        )

    # Super admin can view any book; others must match organization
    if current_user.role != UserRole.SUPER_ADMIN:
        if book.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Recipe book belongs to a different organization"
            )

    # Get recipes in this book
    recipe_assignments = db.query(RecipeBookRecipe).filter(
        RecipeBookRecipe.recipe_book_id == book_id
    ).order_by(RecipeBookRecipe.order_index).all()

    recipes = []
    for assignment in recipe_assignments:
        recipe = assignment.recipe
        recipes.append(RecipeInBook(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            photo_url=recipe.photo_url,
            category_id=recipe.category_id,
            order_index=assignment.order_index,
            added_at=assignment.added_at
        ))

    # Build response with sites
    book_response = _build_book_response(book)
    return RecipeBookWithRecipes(
        **book_response.model_dump(),
        recipes=recipes,
        recipe_count=len(recipes)
    )


@router.put("/{book_id}", response_model=RecipeBookResponse)
def update_recipe_book(
    book_id: int,
    book: RecipeBookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe book (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit recipe books"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check book exists
    db_book = db.query(RecipeBook).options(joinedload(RecipeBook.sites)).filter(RecipeBook.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe book not found"
        )

    # Check organization match
    if db_book.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe book belongs to a different organization"
        )

    # Update fields (excluding site_ids which needs special handling)
    update_data = book.model_dump(exclude_unset=True, exclude={'site_ids'})
    for field, value in update_data.items():
        setattr(db_book, field, value)

    # Handle multi-site assignment
    if book.site_ids is not None:
        sites = db.query(Site).filter(Site.id.in_(book.site_ids)).all() if book.site_ids else []
        db_book.sites = sites

    db.commit()
    db.refresh(db_book)

    return _build_book_response(db_book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a recipe book (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete recipe books"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check book exists
    db_book = db.query(RecipeBook).filter(RecipeBook.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe book not found"
        )

    # Check organization match
    if db_book.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe book belongs to a different organization"
        )

    db.delete(db_book)
    db.commit()


@router.post("/{book_id}/recipes", status_code=status.HTTP_201_CREATED)
def add_recipe_to_book(
    book_id: int,
    recipe_data: AddRecipeToBook,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a recipe to a book (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify recipe books"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check book exists
    book = db.query(RecipeBook).filter(RecipeBook.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe book not found"
        )

    # Check organization match
    if book.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe book belongs to a different organization"
        )

    # Check recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_data.recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Check recipe organization match
    if recipe.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe belongs to a different organization"
        )

    # Check if recipe is already in the book
    existing = db.query(RecipeBookRecipe).filter(
        RecipeBookRecipe.recipe_book_id == book_id,
        RecipeBookRecipe.recipe_id == recipe_data.recipe_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe is already in this book"
        )

    # Add recipe to book
    assignment = RecipeBookRecipe(
        recipe_book_id=book_id,
        recipe_id=recipe_data.recipe_id,
        order_index=recipe_data.order_index or 0
    )

    db.add(assignment)
    db.commit()

    return {"message": "Recipe added to book successfully"}


@router.delete("/{book_id}/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recipe_from_book(
    book_id: int,
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a recipe from a book (CRUD roles only)"""
    # Check CRUD permission
    if not has_recipe_crud(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify recipe books"
        )

    # Check access permission
    if not has_recipe_access(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to the Recipe Book module"
        )

    # Check book exists
    book = db.query(RecipeBook).filter(RecipeBook.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe book not found"
        )

    # Check organization match
    if book.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recipe book belongs to a different organization"
        )

    # Find assignment
    assignment = db.query(RecipeBookRecipe).filter(
        RecipeBookRecipe.recipe_book_id == book_id,
        RecipeBookRecipe.recipe_id == recipe_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found in this book"
        )

    db.delete(assignment)
    db.commit()
