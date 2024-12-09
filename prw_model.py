from typing import List
from datetime import date, time
from sqlalchemy.orm import registry
from sqlmodel import Field, Relationship
from .prw_meta_model import PrwMetaModel, PrwMeta, PrwSourcesMeta


class PrwModel(PrwMetaModel, registry=registry()):
    pass


class PrwPatient(PrwModel, table=True):
    __tablename__ = "prw_patients"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(
        unique=True,
        index=True,
        max_length=24,
        description="ID hash from unique salt and row ID",
    )
    sex: str = Field(regex="^[MFO]$")
    age: int | None = Field(description="Age in years")
    age_mo: int | None = Field(description="Age in months if <2yo")
    city: str | None = None
    state: str | None = None
    pcp: str | None = None

    encounters: List["PrwEncounter"] = Relationship(back_populates="patient")


class PrwEncounter(PrwModel, table=True):
    __tablename__ = "prw_encounters"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(max_length=24, foreign_key="prw_patients.prw_id")
    location: str
    dept: str
    encounter_date: date
    encounter_time: time
    encounter_age: int | None = Field(description="Age in years at encounter")
    encounter_age_mo: int | None = Field(description="Age in months at encounter if <2yo")
    encounter_type: str
    service_provider: str | None = None
    billing_provider: str | None = None
    with_pcp: bool | None = None
    appt_status: str | None = None
    diagnoses: str | None = None
    level_of_service: str | None = None

    patient: PrwPatient | None = Relationship(back_populates="encounters")
