from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class Statute(BaseModel):
    act_name: str = Field(..., min_length=3, max_length=200)
    year: int = Field(..., ge=1963, le=2026)
    section_number: str = Field(..., pattern=r"^\d+[A-Z]?$")
    title: str = Field(..., min_length=5)
    text: str = Field(..., min_length=50)
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("act_name")
    @classmethod
    def act_name_must_be_title_case(cls, v: str) -> str:
        if v != v.title():
            raise ValueError("Act name must be in title case")
        return v

    @field_validator("text")
    @classmethod
    def text_must_not_be_whitespace(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Text cannot be whitespace only")
        return v


def demo_valid():
    print("\n=== VALID STATUTE ===")
    statute = Statute(
        act_name="Data Protection Act",
        year=2019,
        section_number="4",
        title="Principles of data protection",
        text="Every data controller shall ensure that personal data is processed lawfully and in a manner that ensures appropriate security.",
    )
    print(statute)
    print("\nAs dict:")
    print(statute.model_dump())


def demo_invalid():
    print("\n=== INVALID STATUTE ===")
    try:
        Statute(
            act_name="data protection act",
            year=1800,
            section_number="4B",
            title="x",
            text="",
        )
    except ValidationError as e:
        print(f"Validation failed with {e.error_count()} errors:")
        for err in e.errors():
            print(f"  - {err['loc'][0]}: {err['msg']}")


def demo_from_dict():
    print("\n=== VALIDATE FROM RAW DICT ===")
    raw = {
        "act_name": "Computer Misuse And Cybercrimes Act",
        "year": 2018,
        "section_number": "12",
        "title": "Unauthorized access to computer systems",
        "text": "A person who causes a computer system to perform a function with intent to secure unauthorized access commits an offence.",
    }
    statute = Statute.model_validate(raw)
    print(f"Parsed: {statute.act_name} Section {statute.section_number}")


if __name__ == "__main__":
    demo_valid()
    demo_invalid()
    demo_from_dict()