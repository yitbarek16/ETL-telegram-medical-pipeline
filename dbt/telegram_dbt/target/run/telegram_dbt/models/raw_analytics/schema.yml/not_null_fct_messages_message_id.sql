
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_id
from "telegram_db"."raw_analytics"."fct_messages"
where message_id is null



  
  
      
    ) dbt_internal_test