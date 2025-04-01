{{ config(materialized='incremental') }}

WITH source_data AS (
    SELECT
        username,
        level,
        value,
        date,
        rank,
        '{{ this.schema }}' AS dbt_run_id,
        CURRENT_TIMESTAMP AS inserted_at
    FROM {{ ref('total_levels') }}
)

SELECT *
FROM source_data

{% if is_incremental() %}
WHERE 1=1
{% endif %}