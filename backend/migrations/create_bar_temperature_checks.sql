-- Create BAR temperature control categories and duplicate temperature check tasks

-- Create BAR Temperature Control (AM) category
INSERT INTO categories (name, description, is_active, frequency, opens_at, closes_at, is_global, icon)
VALUES (
    'BAR Temperature Control (AM)',
    'Morning temperature checks for bar fridges and freezers',
    true,
    'daily',
    '08:00:00',
    '12:00:00',
    true,
    '🌡️'
) RETURNING id;

-- Create BAR Temperature Control (PM) category
INSERT INTO categories (name, description, is_active, frequency, opens_at, closes_at, is_global, icon)
VALUES (
    'BAR Temperature Control (PM)',
    'Evening temperature checks for bar fridges and freezers',
    true,
    'daily',
    '17:00:00',
    '23:59:00',
    true,
    '🌡️'
) RETURNING id;

-- Get the new category IDs (will need to run separately to get IDs)
-- For now, assuming they will be 142 and 143 (next available after 141)

-- Create BAR AM Fridge Temperature Checks task
INSERT INTO tasks (name, description, is_active, order_index, has_dynamic_form, category_id, priority)
SELECT
    'BAR AM Fridge Temperature Checks',
    'Check and record all bar fridge temperatures in the morning',
    true,
    1,
    true,
    (SELECT id FROM categories WHERE name = 'BAR Temperature Control (AM)'),
    'high'
WHERE EXISTS (SELECT 1 FROM categories WHERE name = 'BAR Temperature Control (AM)');

-- Create BAR AM Freezer Temperature Checks task
INSERT INTO tasks (name, description, is_active, order_index, has_dynamic_form, category_id, priority)
SELECT
    'BAR AM Freezer Temperature Checks',
    'Check and record all bar freezer temperatures in the morning',
    true,
    2,
    true,
    (SELECT id FROM categories WHERE name = 'BAR Temperature Control (AM)'),
    'high'
WHERE EXISTS (SELECT 1 FROM categories WHERE name = 'BAR Temperature Control (AM)');

-- Create BAR PM Fridge Temperature Checks task
INSERT INTO tasks (name, description, is_active, order_index, has_dynamic_form, category_id, priority)
SELECT
    'BAR PM Fridge Temperature Checks',
    'Check and record all bar fridge temperatures in the evening',
    true,
    1,
    true,
    (SELECT id FROM categories WHERE name = 'BAR Temperature Control (PM)'),
    'high'
WHERE EXISTS (SELECT 1 FROM categories WHERE name = 'BAR Temperature Control (PM)');

-- Create BAR PM Freezer Temperature Checks task
INSERT INTO tasks (name, description, is_active, order_index, has_dynamic_form, category_id, priority)
SELECT
    'BAR PM Freezer Temperature Checks',
    'Check and record all bar freezer temperatures in the evening',
    true,
    2,
    true,
    (SELECT id FROM categories WHERE name = 'BAR Temperature Control (PM)'),
    'high'
WHERE EXISTS (SELECT 1 FROM categories WHERE name = 'BAR Temperature Control (PM)');

-- Now create task fields for each task
-- BAR AM Fridge Temperature Checks fields
INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    (SELECT id FROM tasks WHERE name = 'BAR AM Fridge Temperature Checks'),
    'Number of Fridges',
    'number',
    1,
    true,
    '{"min": 0, "max": 50}'::jsonb
WHERE EXISTS (SELECT 1 FROM tasks WHERE name = 'BAR AM Fridge Temperature Checks');

INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    t.id,
    'Fridge Temperature Readings',
    'repeating_group',
    2,
    false,
    jsonb_build_object(
        'repeat_count_field_id', (SELECT id FROM task_fields WHERE task_id = t.id AND field_label = 'Number of Fridges'),
        'repeat_label', 'Fridge',
        'repeat_template', jsonb_build_array(
            jsonb_build_object(
                'type', 'temperature',
                'label', 'Temperature (°C)',
                'min', 1,
                'max', 5,
                'auto_defect_threshold', 5,
                'auto_defect_operator', '>'
            ),
            jsonb_build_object(
                'type', 'photo',
                'label', 'Photo Evidence (optional)'
            )
        )
    )
FROM tasks t
WHERE t.name = 'BAR AM Fridge Temperature Checks';

-- BAR AM Freezer Temperature Checks fields
INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    (SELECT id FROM tasks WHERE name = 'BAR AM Freezer Temperature Checks'),
    'Number of Freezers',
    'number',
    1,
    true,
    '{"min": 0, "max": 50}'::jsonb
WHERE EXISTS (SELECT 1 FROM tasks WHERE name = 'BAR AM Freezer Temperature Checks');

INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    t.id,
    'Freezer Temperature Readings',
    'repeating_group',
    2,
    false,
    jsonb_build_object(
        'repeat_count_field_id', (SELECT id FROM task_fields WHERE task_id = t.id AND field_label = 'Number of Freezers'),
        'repeat_label', 'Freezer',
        'repeat_template', jsonb_build_array(
            jsonb_build_object(
                'type', 'temperature',
                'label', 'Temperature (°C)',
                'min', -25,
                'max', -18,
                'auto_defect_threshold', -18,
                'auto_defect_operator', '>'
            ),
            jsonb_build_object(
                'type', 'photo',
                'label', 'Photo Evidence (optional)'
            )
        )
    )
FROM tasks t
WHERE t.name = 'BAR AM Freezer Temperature Checks';

-- BAR PM Fridge Temperature Checks fields
INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    (SELECT id FROM tasks WHERE name = 'BAR PM Fridge Temperature Checks'),
    'Number of Fridges',
    'number',
    1,
    true,
    '{"min": 0, "max": 50}'::jsonb
WHERE EXISTS (SELECT 1 FROM tasks WHERE name = 'BAR PM Fridge Temperature Checks');

INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    t.id,
    'Fridge Temperature Readings',
    'repeating_group',
    2,
    false,
    jsonb_build_object(
        'repeat_count_field_id', (SELECT id FROM task_fields WHERE task_id = t.id AND field_label = 'Number of Fridges'),
        'repeat_label', 'Fridge',
        'repeat_template', jsonb_build_array(
            jsonb_build_object(
                'type', 'temperature',
                'label', 'Temperature (°C)',
                'min', 1,
                'max', 5,
                'auto_defect_threshold', 5,
                'auto_defect_operator', '>'
            ),
            jsonb_build_object(
                'type', 'photo',
                'label', 'Photo Evidence (optional)'
            )
        )
    )
FROM tasks t
WHERE t.name = 'BAR PM Fridge Temperature Checks';

-- BAR PM Freezer Temperature Checks fields
INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    (SELECT id FROM tasks WHERE name = 'BAR PM Freezer Temperature Checks'),
    'Number of Freezers',
    'number',
    1,
    true,
    '{"min": 0, "max": 50}'::jsonb
WHERE EXISTS (SELECT 1 FROM tasks WHERE name = 'BAR PM Freezer Temperature Checks');

INSERT INTO task_fields (task_id, field_label, field_type, field_order, is_required, validation_rules)
SELECT
    t.id,
    'Freezer Temperature Readings',
    'repeating_group',
    2,
    false,
    jsonb_build_object(
        'repeat_count_field_id', (SELECT id FROM task_fields WHERE task_id = t.id AND field_label = 'Number of Freezers'),
        'repeat_label', 'Freezer',
        'repeat_template', jsonb_build_array(
            jsonb_build_object(
                'type', 'temperature',
                'label', 'Temperature (°C)',
                'min', -25,
                'max', -18,
                'auto_defect_threshold', -18,
                'auto_defect_operator', '>'
            ),
            jsonb_build_object(
                'type', 'photo',
                'label', 'Photo Evidence (optional)'
            )
        )
    )
FROM tasks t
WHERE t.name = 'BAR PM Freezer Temperature Checks';

-- Display summary
SELECT 'Created BAR temperature control categories and tasks' AS summary;
SELECT id, name FROM categories WHERE name LIKE 'BAR%' ORDER BY id;
SELECT id, name, category_id FROM tasks WHERE name LIKE 'BAR%' ORDER BY category_id, id;
