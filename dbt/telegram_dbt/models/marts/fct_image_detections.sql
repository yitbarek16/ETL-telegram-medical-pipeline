{{ config(
    materialized='incremental',
    unique_key='detection_id'
) }}

SELECT
    d.id AS detection_id,
    d.message_id,
    m.channel_id,
    m.date_day AS date,
    d.object_class,
    d.confidence
FROM {{ source('raw', 'image_detections') }} d
LEFT JOIN {{ ref('fct_messages') }} m
    ON d.message_id = m.message_id

{% if is_incremental() %}
WHERE d.id > (SELECT MAX(detection_id) FROM {{ this }})
{% endif %}
