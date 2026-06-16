from app.models.document import Document


def create_document(
    db,
    file_name,
    file_path,
    uploaded_by
):
    document = Document(
        file_name=file_name,
        file_path=file_path,
        uploaded_by=uploaded_by
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document