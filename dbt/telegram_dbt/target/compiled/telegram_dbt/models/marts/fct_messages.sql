-- models/marts/fct_messages.sql

with messages as (
    select * from "telegram_db"."raw_staging"."stg_telegram_messages"
),

fct as (
    select
        md5(channel_name) as channel_id,
        message_date::date as date_day,
        message_id,
        length(message_text) as message_length,
        has_media,
        media_type
    from messages
)
 
select * from fct