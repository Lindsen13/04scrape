{{ config(materialized='view') }}

SELECT
    rank,
    date,
    username,
    level,
    xp
FROM (
    SELECT
        rank,
        DATE_TRUNC('day', inserted_at) AS date,
        inserted_at,
        username,
        level,
        value/10 as xp,
        row_number() OVER(PARTITION BY DATE_TRUNC('day', inserted_at), rank ORDER BY inserted_at desc) as row_nr
    FROM {{ ref('total_levels_overview') }}
    where rank <= 100
) a
WHERE row_nr = 1