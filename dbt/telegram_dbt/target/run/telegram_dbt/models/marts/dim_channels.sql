
  
    

  create  table "telegram_db"."raw_analytics"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    -- models/marts/dim_channels.sql

with messages as (
    select * from "telegram_db"."raw_staging"."stg_telegram_messages"
),

dim_channels as (
    select distinct
        channel_name as channel,
        md5(channel_name) as channel_id
    from messages
)

select * from dim_channels
  );
  