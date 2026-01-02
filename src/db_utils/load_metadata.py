import yaml
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError


class ColumnSchema(BaseModel):
    """Schema for a single column."""
    name: str
    description: str
    tests: Optional[List[Dict[str, Any]]] = None


class TableSchema(BaseModel):
    """Schema for a single table."""
    name: str
    description: str
    columns: List[ColumnSchema]


class Metadata(BaseModel):
    """Root structure for the YAML metadata."""
    version: int
    tables: List[TableSchema]


def load_metadata(file_path):
    # Specify the encoding as 'utf-8' when opening the file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return Metadata.model_validate(data)

if __name__ == "__main__":
    metadata =  load_metadata('/content/metadata.yaml')
    print(metadata)