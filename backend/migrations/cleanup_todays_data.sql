-- Clean up today's checklists and responses for fresh testing
-- Keeps all task definitions, categories, users, and sites

-- Delete task field responses for today's checklist items
DELETE FROM task_field_responses
WHERE checklist_item_id IN (
    SELECT ci.id
    FROM checklist_items ci
    JOIN checklists c ON ci.checklist_id = c.id
    WHERE c.checklist_date = CURRENT_DATE
);

-- Delete checklist items for today's checklists
DELETE FROM checklist_items
WHERE checklist_id IN (
    SELECT id FROM checklists WHERE checklist_date = CURRENT_DATE
);

-- Delete today's checklists
DELETE FROM checklists WHERE checklist_date = CURRENT_DATE;

-- Show summary
SELECT 'Cleanup completed - today''s checklists and responses deleted' AS result;
SELECT 'Task definitions, categories, users, and sites preserved' AS preserved;
