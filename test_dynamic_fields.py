"""
Test script for Dynamic Task Fields API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_task_fields_api():
    print("🧪 Testing Dynamic Task Fields API\n")

    # Step 1: Create task fields for a task (using task_id = 1)
    print("1️⃣ Creating task fields for Task ID 1...")

    bulk_data = {
        "task_id": 1,
        "fields": [
            {
                "field_type": "temperature",
                "field_label": "Fridge Temperature (°C)",
                "field_order": 0,
                "is_required": True,
                "validation_rules": {
                    "min": 0,
                    "max": 8,
                    "create_defect_if": "out_of_range"
                },
                "options": None,
                "show_if": None
            },
            {
                "field_type": "yes_no",
                "field_label": "Is door sealed properly?",
                "field_order": 1,
                "is_required": True,
                "validation_rules": None,
                "options": None,
                "show_if": None
            },
            {
                "field_type": "dropdown",
                "field_label": "Cleanliness Rating",
                "field_order": 2,
                "is_required": True,
                "validation_rules": None,
                "options": ["Excellent", "Good", "Fair", "Poor"],
                "show_if": None
            },
            {
                "field_type": "text",
                "field_label": "Additional Notes",
                "field_order": 3,
                "is_required": False,
                "validation_rules": None,
                "options": None,
                "show_if": None
            }
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/task-fields/bulk",
            json=bulk_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 201:
            fields = response.json()
            print(f"✅ Successfully created {len(fields)} task fields!")
            for field in fields:
                print(f"   - {field['field_label']} ({field['field_type']}) - ID: {field['id']}")

            # Step 2: Retrieve the fields
            print("\n2️⃣ Retrieving task fields...")
            response = requests.get(f"{BASE_URL}/task-fields?task_id=1")

            if response.status_code == 200:
                retrieved_fields = response.json()
                print(f"✅ Retrieved {len(retrieved_fields)} fields")

                # Step 3: Test submitting responses (using checklist_item_id = 1)
                print("\n3️⃣ Submitting field responses...")

                submission = {
                    "checklist_item_id": 1,
                    "responses": [
                        {
                            "task_field_id": fields[0]['id'],
                            "number_value": 4.5  # Temperature
                        },
                        {
                            "task_field_id": fields[1]['id'],
                            "boolean_value": True  # Yes/No
                        },
                        {
                            "task_field_id": fields[2]['id'],
                            "text_value": "Good"  # Dropdown
                        },
                        {
                            "task_field_id": fields[3]['id'],
                            "text_value": "Everything looks great!"  # Notes
                        }
                    ]
                }

                response = requests.post(
                    f"{BASE_URL}/task-field-responses",
                    json=submission,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 201:
                    responses = response.json()
                    print(f"✅ Successfully submitted {len(responses)} responses!")

                    # Step 4: Retrieve responses
                    print("\n4️⃣ Retrieving responses...")
                    response = requests.get(f"{BASE_URL}/task-field-responses?checklist_item_id=1")

                    if response.status_code == 200:
                        retrieved_responses = response.json()
                        print(f"✅ Retrieved {len(retrieved_responses)} responses")
                        for resp in retrieved_responses:
                            value = resp.get('number_value') or resp.get('text_value') or resp.get('boolean_value')
                            print(f"   - Field {resp['task_field_id']}: {value}")

                        print("\n✨ All tests passed! Dynamic fields system is working!")
                    else:
                        print(f"❌ Failed to retrieve responses: {response.status_code}")
                        print(f"   {response.text}")
                else:
                    print(f"❌ Failed to submit responses: {response.status_code}")
                    print(f"   {response.text}")
            else:
                print(f"❌ Failed to retrieve fields: {response.status_code}")
                print(f"   {response.text}")
        else:
            print(f"❌ Failed to create fields: {response.status_code}")
            print(f"   {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_task_fields_api()
