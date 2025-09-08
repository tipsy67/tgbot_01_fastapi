
def update_model_from_pydantic(db_model, pydantic_model, exclude: set = None):
    """Обновляет модель БД из Pydantic модели"""
    if exclude is None:
        exclude = set()

    update_data = pydantic_model.model_dump(exclude_unset=True, exclude=exclude)
    for key, value in update_data.items():
        setattr(db_model, key, value)
    return db_model
