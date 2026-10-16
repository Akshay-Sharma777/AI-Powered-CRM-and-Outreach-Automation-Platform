-- Reusable Query: sample_leads_filter.sql
-- Filter leads by score band, status, and source with pagination and joins
-- Usage in leads_repo.py via parameterised execution

SELECT 
    o.id,
    org.name AS organization_name,
    o.title,
    o.type AS opportunity_type,
    s.name AS source_name,
    o.source_url,
    o.experience_min,
    o.experience_max,
    o.salary_text,
    o.location,
    o.status,
    COALESCE(dqs.score, 0) AS score,
    COALESCE(dqs.band, 'low') AS score_band,
    u.full_name AS assigned_user_name,
    o.discovered_at
FROM opportunities o
JOIN organizations org ON o.organization_id = org.id
JOIN sources s ON o.source_id = s.id
LEFT JOIN users u ON o.assigned_to = u.id
LEFT JOIN LATERAL (
    SELECT score, band 
    FROM data_quality_scores 
    WHERE opportunity_id = o.id 
    ORDER BY scored_at DESC 
    LIMIT 1
) dqs ON TRUE
WHERE 
    (%s IS NULL OR o.status = %s)
    AND (%s IS NULL OR s.id = %s)
    AND (%s IS NULL OR dqs.band = %s)
    AND (%s IS NULL OR o.experience_max <= %s)
    AND (%s IS NULL OR o.title ILIKE %s OR org.name ILIKE %s)
ORDER BY o.discovered_at DESC
LIMIT %s OFFSET %s;
