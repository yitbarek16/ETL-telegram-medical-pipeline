-- models/staging/stg_telegram_messages.sql

with source as (
    select * from "telegram_db"."raw"."telegram_messages"
),

renamed as (
    select
        id::bigint as message_id,
        channel::text as channel_name,
        date::timestamp as message_date,
        message::text as message_text,
        has_media::boolean,
        media_type::text,
        image_path::text
    from source
)

select * from renamed