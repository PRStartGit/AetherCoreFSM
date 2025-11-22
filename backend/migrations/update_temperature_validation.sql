-- Update temperature validation rules to match legal food safety limits
-- Fridges: 1-5°C (UK/EU food safety regulations)
-- Freezers: -18°C or colder (typically -18 to -25°C)

-- Update AM Fridge Temperature Checks (Task ID: 77)
UPDATE task_fields
SET validation_rules = jsonb_build_object(
    'repeat_count_field_id', 206,
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
WHERE task_id = 77 AND field_label = 'Fridge Temperature Readings';

-- Update AM Freezer Temperature Checks (Task ID: 78)
UPDATE task_fields
SET validation_rules = jsonb_build_object(
    'repeat_count_field_id', 208,
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
WHERE task_id = 78 AND field_label = 'Freezer Temperature Readings';

-- Update PM Fridge Temperature Checks (Task ID: 80)
UPDATE task_fields
SET validation_rules = jsonb_build_object(
    'repeat_count_field_id', 213,
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
WHERE task_id = 80 AND field_label = 'Fridge Temperature Readings';

-- Update PM Freezer Temperature Checks (Task ID: 81)
UPDATE task_fields
SET validation_rules = jsonb_build_object(
    'repeat_count_field_id', 215,
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
WHERE task_id = 81 AND field_label = 'Freezer Temperature Readings';
