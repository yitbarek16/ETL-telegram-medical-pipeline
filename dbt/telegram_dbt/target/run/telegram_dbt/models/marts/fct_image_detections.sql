
      
  
    

  create  table "telegram_db"."raw_analytics"."fct_image_detections__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    d.id AS detection_id,
    d.message_id,
    m.channel_id,
    m.date_day AS date,
    d.object_class,
    d.confidence
FROM "telegram_db"."raw"."image_detections" d
LEFT JOIN "telegram_db"."raw_analytics"."fct_messages" m
    ON d.message_id = m.message_id


  );
  
  