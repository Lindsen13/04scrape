WITH api_data AS (
    {% set start_rank = 21 %}
    {% set increment = 21 %}
    {% set iterations = 10 %}

    {% for i in range(iterations) %}
    {% if not loop.first %}
    UNION ALL
    {% endif %}

    SELECT *
    FROM read_json_auto('https://2004.lostcity.rs/api/hiscores/category/0?rank={{ start_rank + (i * increment) }}')

    {% endfor %}
)

SELECT *
FROM api_data