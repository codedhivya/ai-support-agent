from sqlalchemy import text

def search_similar_chunks(
    db,
    query_embedding,
    limit=5
):

    query = text("""
        SELECT
            d.file_name,
            dc.chunk_index,
            dc.content
        FROM document_embeddings de
        JOIN document_chunks dc
            ON de.document_id = dc.document_id
            AND de.chunk_index = dc.chunk_index
        JOIN documents d
            ON d.id = de.document_id
        ORDER BY de.embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        query,
        {
            "embedding": str(query_embedding),
            "limit": limit
        }
    )

    return result.fetchall()