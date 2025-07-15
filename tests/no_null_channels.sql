-- Returns rows if there are messages with NULL channel_id
SELECT *
FROM {{ ref('fct_messages') }}
WHERE channel_id IS NULL
