# EHO Global Categories and Tasks - Base Seed Data

This document describes the base global categories and tasks for the AetherCore FSM system.

## Overview

The following 16 EHO-compliant categories (IDs 126-141) serve as the **base global seed data** for all organizations. These categories and their associated tasks are based on UK Environmental Health Officer (EHO) food safety compliance requirements.

## Global Categories

### Daily Checklists (8 categories)
1. **Temperature Control (AM)** - Morning temperature checks for fridges, freezers, hot holding
2. **Temperature Control (PM)** - Afternoon temperature checks
3. **Personal Hygiene** - Hand washing, uniform cleanliness, illness reporting
4. **Cleaning and Disinfection** - Daily cleaning schedules and sanitization
5. **Food Storage and Handling** - Proper storage temperatures, FIFO, labeling
6. **Cross-Contamination Prevention** - Separate equipment, color coding, allergen control
7. **Waste Management** - Waste disposal, bin maintenance
8. **Water Supply and Drainage** - Water safety, drainage checks

### Weekly Checklists (4 categories)
9. **Allergen Management** - Allergen matrix updates, staff training
10. **Equipment Maintenance** - Equipment checks, calibration
11. **Pest Control** - Pest activity monitoring, proofing checks
12. **Documentation and Record Keeping** - Record reviews, documentation updates

### Monthly Checklists (3 categories)
13. **Food Safety Management System (HACCP)** - HACCP review, critical control points
14. **Training Records** - Staff training completion, competency assessments
15. **Structure and Facilities** - Building maintenance, repair needs

### Quarterly Checklists (1 category)
16. **Supplier and Traceability** - Supplier audits, traceability verification

## Database Schema

- **Categories**: category IDs 126-141
- **Tasks**: 27 total tasks across all categories
- **Frequency types**: DAILY, WEEKLY, MONTHLY, QUARTERLY

## Usage for New Organizations

When a new organization is created, these global categories and tasks should be:
1. Available for assignment to their sites
2. Cloneable/customizable per organization if needed
3. Used as templates for organization-specific variations

## Future Expansion

As the system grows, additional categories can be added:
- **Six Monthly** checks (HVAC, deep cleaning)
- **Annual** compliance (licenses, insurance, audits)
- Industry-specific categories (retail, manufacturing, healthcare)

## Technical Notes

- Categories are marked with `is_global = true` in the database
- Tasks are active by default (`is_active = true`)
- Each task has an `order_index` for consistent display
- Tasks support dynamic forms via `has_dynamic_form` and `form_config`

## Seed Scripts

- `seed_eho_categories.py` - Creates the 16 base categories
- `seed_eho_tasks.py` - Creates all associated tasks
- `generate_eho_checklists.py` - Generates daily/weekly/monthly/quarterly checklists

## Last Updated

2025-11-20 - Initial EHO base categories established
