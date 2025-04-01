{{ config(materialized='view') }}

SELECT
    rank,
    date,
    username,
    max(level) AS level,
    floor(max(xp)) as xp
FROM (
    SELECT
        rank,
        DATE_TRUNC('day', inserted_at) AS date,
        username,
        level,
        value/10 as xp
    FROM {{ ref('total_levels_overview') }}
    WHERE rank <= 100
) t
GROUP BY rank, date, username