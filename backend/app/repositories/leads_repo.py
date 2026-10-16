"""
Leads & Opportunities Repository.
Direct parameterised SQL access via psycopg3.
STRICTLY NO ORM.
"""

from typing import List, Optional, Tuple, Dict, Any
from backend.app.core.db import get_conn


def list_leads_raw_sql(
    source_id: Optional[str] = None,
    status: Optional[str] = None,
    band: Optional[str] = None,
    max_experience: Optional[int] = None,
    search_term: Optional[str] = None,
    page: int = 1,
    page_size: int = 25
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Executes parameterised query to fetch paginated leads.
    Page size is capped at 100.
    """
    limit = min(page_size, 100)
    offset = (max(page, 1) - 1) * limit

    search_pattern = f"%{search_term}%" if search_term else None

    query = """
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
    """

    params = (
        status, status,
        source_id, source_id,
        band, band,
        max_experience, max_experience,
        search_pattern, search_pattern, search_pattern,
        limit, offset
    )

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, row)) for row in cur.fetchall()]

            # Count total matching
            count_query = """
                SELECT COUNT(*)
                FROM opportunities o
                JOIN organizations org ON o.organization_id = org.id
                JOIN sources s ON o.source_id = s.id
                LEFT JOIN LATERAL (
                    SELECT band 
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
                    AND (%s IS NULL OR o.title ILIKE %s OR org.name ILIKE %s);
            """
            cur.execute(count_query, params[:-2])
            total = cur.fetchone()[0]

    return rows, total
