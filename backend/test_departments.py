"""
Test script for department and job title functionality.

This script tests:
1. User creation with departments and job titles
2. Task creation with allocated departments
3. Permission logic (can_see_task method)
4. Database integrity
"""

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.models.user import User, UserRole, Department, JobTitle
from app.models.task import Task
from app.models.category import Category
from app.models.organization import Organization
from app.core.database import Base

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:changeme@localhost:5432/zynthio")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def print_test(test_name):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)

def print_success(message):
    """Print success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print error message."""
    print(f"❌ {message}")

def test_database_schema():
    """Test that database schema includes new columns."""
    print_test("Database Schema Verification")

    db = SessionLocal()
    try:
        # Check if department and job_title columns exist in users table
        result = db.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name IN ('department', 'job_title')")
        columns = [row[0] for row in result]

        if 'department' in columns and 'job_title' in columns:
            print_success("Users table has department and job_title columns")
        else:
            print_error(f"Missing columns. Found: {columns}")
            return False

        # Check if allocated_departments column exists in tasks table
        result = db.execute("SELECT column_name FROM information_schema.columns WHERE table_name='tasks' AND column_name='allocated_departments'")
        columns = [row[0] for row in result]

        if 'allocated_departments' in columns:
            print_success("Tasks table has allocated_departments column")
        else:
            print_error("Tasks table missing allocated_departments column")
            return False

        # Check enum types exist
        result = db.execute("SELECT typname FROM pg_type WHERE typname IN ('department', 'jobtitle')")
        types = [row[0] for row in result]

        if 'department' in types and 'jobtitle' in types:
            print_success("Department and JobTitle enum types exist")
        else:
            print_error(f"Missing enum types. Found: {types}")
            return False

        return True
    except Exception as e:
        print_error(f"Schema test failed: {str(e)}")
        return False
    finally:
        db.close()

def test_user_creation_with_departments():
    """Test creating users with departments and job titles."""
    print_test("User Creation with Departments")

    db = SessionLocal()
    try:
        # Get an organization for testing
        org = db.query(Organization).first()
        if not org:
            print_error("No organization found for testing")
            return False

        # Test 1: Create General Manager (Management)
        gm_email = f"test_gm_{os.getpid()}@test.com"
        gm = User(
            email=gm_email,
            hashed_password="test123",
            first_name="General",
            last_name="Manager",
            role=UserRole.SITE_USER,
            department=Department.MANAGEMENT,
            job_title=JobTitle.GENERAL_MANAGER,
            organization_id=org.id
        )
        db.add(gm)
        db.commit()
        db.refresh(gm)

        if gm.department == Department.MANAGEMENT and gm.job_title == JobTitle.GENERAL_MANAGER:
            print_success(f"Created General Manager: {gm.email}")
            print(f"   Department: {gm.department.value}, Job Title: {gm.job_title.value}")
            print(f"   Is Management Level: {gm.is_management_level}")
        else:
            print_error("General Manager creation failed")
            return False

        # Test 2: Create BOH Team Member
        boh_email = f"test_boh_{os.getpid()}@test.com"
        boh_member = User(
            email=boh_email,
            hashed_password="test123",
            first_name="Kitchen",
            last_name="Staff",
            role=UserRole.SITE_USER,
            department=Department.BOH,
            job_title=JobTitle.TEAM_MEMBER,
            organization_id=org.id
        )
        db.add(boh_member)
        db.commit()
        db.refresh(boh_member)

        if boh_member.department == Department.BOH and boh_member.job_title == JobTitle.TEAM_MEMBER:
            print_success(f"Created BOH Team Member: {boh_member.email}")
            print(f"   Department: {boh_member.department.value}, Job Title: {boh_member.job_title.value}")
            print(f"   Is Management Level: {boh_member.is_management_level}")
        else:
            print_error("BOH Team Member creation failed")
            return False

        # Test 3: Create FOH Team Member
        foh_email = f"test_foh_{os.getpid()}@test.com"
        foh_member = User(
            email=foh_email,
            hashed_password="test123",
            first_name="Front",
            last_name="Staff",
            role=UserRole.SITE_USER,
            department=Department.FOH,
            job_title=JobTitle.TEAM_MEMBER,
            organization_id=org.id
        )
        db.add(foh_member)
        db.commit()
        db.refresh(foh_member)

        if foh_member.department == Department.FOH and foh_member.job_title == JobTitle.TEAM_MEMBER:
            print_success(f"Created FOH Team Member: {foh_member.email}")
            print(f"   Department: {foh_member.department.value}, Job Title: {foh_member.job_title.value}")
            print(f"   Is Management Level: {foh_member.is_management_level}")
        else:
            print_error("FOH Team Member creation failed")
            return False

        # Test 4: Create Head Chef (Management)
        chef_email = f"test_chef_{os.getpid()}@test.com"
        chef = User(
            email=chef_email,
            hashed_password="test123",
            first_name="Head",
            last_name="Chef",
            role=UserRole.SITE_USER,
            department=Department.BOH,
            job_title=JobTitle.HEAD_CHEF,
            organization_id=org.id
        )
        db.add(chef)
        db.commit()
        db.refresh(chef)

        if chef.department == Department.BOH and chef.job_title == JobTitle.HEAD_CHEF:
            print_success(f"Created Head Chef: {chef.email}")
            print(f"   Department: {chef.department.value}, Job Title: {chef.job_title.value}")
            print(f"   Is Management Level: {chef.is_management_level}")
        else:
            print_error("Head Chef creation failed")
            return False

        return True
    except Exception as e:
        print_error(f"User creation test failed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def test_task_creation_with_departments():
    """Test creating tasks with allocated departments."""
    print_test("Task Creation with Department Allocation")

    db = SessionLocal()
    try:
        # Get a category for testing
        category = db.query(Category).first()
        if not category:
            print_error("No category found for testing")
            return False

        # Test 1: Create task for BOH only
        boh_task = Task(
            name=f"Kitchen Cleaning {os.getpid()}",
            description="Clean all kitchen surfaces",
            category_id=category.id,
            allocated_departments=['boh']
        )
        db.add(boh_task)
        db.commit()
        db.refresh(boh_task)

        if boh_task.allocated_departments == ['boh']:
            print_success(f"Created BOH-only task: {boh_task.name}")
            print(f"   Allocated to: {boh_task.allocated_departments}")
        else:
            print_error("BOH task creation failed")
            return False

        # Test 2: Create task for FOH only
        foh_task = Task(
            name=f"Dining Area Setup {os.getpid()}",
            description="Set up tables and chairs",
            category_id=category.id,
            allocated_departments=['foh']
        )
        db.add(foh_task)
        db.commit()
        db.refresh(foh_task)

        if foh_task.allocated_departments == ['foh']:
            print_success(f"Created FOH-only task: {foh_task.name}")
            print(f"   Allocated to: {foh_task.allocated_departments}")
        else:
            print_error("FOH task creation failed")
            return False

        # Test 3: Create task for both BOH and FOH
        multi_task = Task(
            name=f"Safety Briefing {os.getpid()}",
            description="Attend daily safety briefing",
            category_id=category.id,
            allocated_departments=['boh', 'foh']
        )
        db.add(multi_task)
        db.commit()
        db.refresh(multi_task)

        if multi_task.allocated_departments == ['boh', 'foh']:
            print_success(f"Created multi-department task: {multi_task.name}")
            print(f"   Allocated to: {multi_task.allocated_departments}")
        else:
            print_error("Multi-department task creation failed")
            return False

        # Test 4: Create task visible to all (no department restriction)
        all_task = Task(
            name=f"General Announcement {os.getpid()}",
            description="Read company announcement",
            category_id=category.id,
            allocated_departments=None
        )
        db.add(all_task)
        db.commit()
        db.refresh(all_task)

        if all_task.allocated_departments is None:
            print_success(f"Created task visible to all: {all_task.name}")
            print(f"   Allocated to: Everyone (no restrictions)")
        else:
            print_error("All-users task creation failed")
            return False

        return True
    except Exception as e:
        print_error(f"Task creation test failed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def test_permission_logic():
    """Test the can_see_task permission logic."""
    print_test("Permission Logic Testing")

    db = SessionLocal()
    try:
        # Get test users and tasks
        org = db.query(Organization).first()

        # Create test users
        gm = User(
            email=f"perm_test_gm_{os.getpid()}@test.com",
            hashed_password="test",
            first_name="Test",
            last_name="GM",
            role=UserRole.SITE_USER,
            department=Department.MANAGEMENT,
            job_title=JobTitle.GENERAL_MANAGER,
            organization_id=org.id
        )

        boh_staff = User(
            email=f"perm_test_boh_{os.getpid()}@test.com",
            hashed_password="test",
            first_name="Test",
            last_name="BOH",
            role=UserRole.SITE_USER,
            department=Department.BOH,
            job_title=JobTitle.TEAM_MEMBER,
            organization_id=org.id
        )

        foh_staff = User(
            email=f"perm_test_foh_{os.getpid()}@test.com",
            hashed_password="test",
            first_name="Test",
            last_name="FOH",
            role=UserRole.SITE_USER,
            department=Department.FOH,
            job_title=JobTitle.TEAM_MEMBER,
            organization_id=org.id
        )

        db.add_all([gm, boh_staff, foh_staff])
        db.commit()

        # Test scenarios
        print("\n--- Test Scenario 1: BOH-only task ---")
        boh_task_deps = ['boh']

        gm_can_see = gm.can_see_task(boh_task_deps)
        boh_can_see = boh_staff.can_see_task(boh_task_deps)
        foh_can_see = foh_staff.can_see_task(boh_task_deps)

        print(f"General Manager (Management) can see BOH task: {gm_can_see}")
        print(f"BOH Team Member can see BOH task: {boh_can_see}")
        print(f"FOH Team Member can see BOH task: {foh_can_see}")

        if gm_can_see and boh_can_see and not foh_can_see:
            print_success("BOH-only task permissions correct")
        else:
            print_error("BOH-only task permissions incorrect")
            return False

        print("\n--- Test Scenario 2: FOH-only task ---")
        foh_task_deps = ['foh']

        gm_can_see = gm.can_see_task(foh_task_deps)
        boh_can_see = boh_staff.can_see_task(foh_task_deps)
        foh_can_see = foh_staff.can_see_task(foh_task_deps)

        print(f"General Manager (Management) can see FOH task: {gm_can_see}")
        print(f"BOH Team Member can see FOH task: {boh_can_see}")
        print(f"FOH Team Member can see FOH task: {foh_can_see}")

        if gm_can_see and not boh_can_see and foh_can_see:
            print_success("FOH-only task permissions correct")
        else:
            print_error("FOH-only task permissions incorrect")
            return False

        print("\n--- Test Scenario 3: Task visible to all (no restrictions) ---")
        all_task_deps = None

        gm_can_see = gm.can_see_task(all_task_deps)
        boh_can_see = boh_staff.can_see_task(all_task_deps)
        foh_can_see = foh_staff.can_see_task(all_task_deps)

        print(f"General Manager can see unrestricted task: {gm_can_see}")
        print(f"BOH Team Member can see unrestricted task: {boh_can_see}")
        print(f"FOH Team Member can see unrestricted task: {foh_can_see}")

        if gm_can_see and boh_can_see and foh_can_see:
            print_success("Unrestricted task permissions correct")
        else:
            print_error("Unrestricted task permissions incorrect")
            return False

        print("\n--- Test Scenario 4: Multi-department task ---")
        multi_deps = ['boh', 'foh']

        gm_can_see = gm.can_see_task(multi_deps)
        boh_can_see = boh_staff.can_see_task(multi_deps)
        foh_can_see = foh_staff.can_see_task(multi_deps)

        print(f"General Manager can see multi-department task: {gm_can_see}")
        print(f"BOH Team Member can see multi-department task: {boh_can_see}")
        print(f"FOH Team Member can see multi-department task: {foh_can_see}")

        if gm_can_see and boh_can_see and foh_can_see:
            print_success("Multi-department task permissions correct")
        else:
            print_error("Multi-department task permissions incorrect")
            return False

        return True
    except Exception as e:
        print_error(f"Permission logic test failed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("DEPARTMENT & JOB TITLE FUNCTIONALITY TEST SUITE")
    print("="*60)

    results = []

    # Run tests
    results.append(("Database Schema", test_database_schema()))
    results.append(("User Creation", test_user_creation_with_departments()))
    results.append(("Task Creation", test_task_creation_with_departments()))
    results.append(("Permission Logic", test_permission_logic()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*60)

    return all(result for _, result in results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
