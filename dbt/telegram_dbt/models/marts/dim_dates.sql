-- models/marts/dim_dates.sql

with dates as (
    select
        generate_series(
            date '2022-01-01',
            current_date,
            interval '1 day'
        )::date as date_day
),

dim_dates as (
    select
        date_day,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        extract(day from date_day) as day,
        to_char(date_day, 'Day') as weekday
    from dates
)

select * from dim_dates
