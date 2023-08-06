#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from optparse import Option
from pprint import pprint
from typing import List, Optional, Union

import yaml
from dateutil.relativedelta import relativedelta
from loguru import logger
from pe_accounting_python_api import PeRestClient
from pydantic import BaseModel, Field


class PeCredentials(BaseModel):
    company_id: str
    api_access_token: str


class EmploymentContract(BaseModel):
    class Config:
        extra = "allow"

    user: dict
    ssn: str
    monthly_salary: int = Field(..., alias="monthly-salary")
    employment_start_date: Optional[date] = Field(..., alias="employment-start-date")
    manager_user: Optional[dict] = Field(None, alias="manager-user")
    monthly_salary_start_date: Optional[date] = Field(None, alias="monthly-salary-start-date")
    vacation_entitlements: Optional[dict] = Field(None, alias="vacation-entitlements")
    zip_code: Optional[str] = Field(None, alias="zip-code")
    address2: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None


class PeUser(BaseModel):

    """Represents a user in PE Accounting."""

    class Config:
        arbitrary_types_allowed = True

    _pe_rest_client: Optional[PeRestClient] = None
    pe_credentials: Optional[PeCredentials] = None

    index: int = 1
    active: bool
    contract: EmploymentContract
    dimension_entry: dict = Field(..., alias="dimension-entry")
    dimensions: dict
    email: str
    id: int
    internal_id: int = Field(..., alias="internal-id")
    name: str

    @classmethod
    def pe_rest_client(cls) -> Optional[PeRestClient]:
        """Lazy create PeRestClient. Store in class attrib."""
        if not hasattr(cls, "pe_credentials"):
            raise Exception("self.pe_credentials has to be set before using this class.")
        if not cls._pe_rest_client and cls.pe_credentials:
            cls._pe_rest_client = PeRestClient(**cls.pe_credentials.dict())
        return cls._pe_rest_client

    @property
    def manager(self):
        if self.contract.manager_user:
            return self.users_dict[self.contract.manager_user["id"]]

    @property
    def years_employed(self) -> str:
        delta = relativedelta(date.today(), self.contract.employment_start_date)
        return f"{delta.years} år, {delta.months} mån"

    def days_to_birthday(self, from_date=date.today()) -> int:
        return (self.next_birthday(from_date=from_date) - from_date).days

    def next_birthday(self, from_date=date.today()) -> date:
        next_birthday = datetime.strptime(self.contract.ssn.split("-")[0], "%Y%m%d").replace(year=from_date.year).date()
        days_remaining = (next_birthday - from_date).days
        if days_remaining < 0:
            next_birthday = next_birthday.replace(year=from_date.year + 1)
        return next_birthday

    def years_next_birthday(self, from_date: date = date.today()) -> int:
        return self.next_birthday().year - datetime.strptime(self.contract.ssn.split("-")[0], "%Y%m%d").year

    @property
    def latest_salary_revision(self) -> Optional[date]:
        return self.contract.monthly_salary_start_date

    @property
    def vacation_entitlement(self) -> Optional[List[dict]]:
        if (
            self.contract
            and self.contract.vacation_entitlements
            and self.contract.vacation_entitlements.get("vacation-entitlements")
        ):
            return self.contract.vacation_entitlements["vacation-entitlements"]
        return None

    @property
    def future_vacation_entitlement_change(self) -> Optional[date]:
        """Is there any configured future vacation entitlement change."""
        if self.vacation_entitlement:
            last = self.vacation_entitlement[-1]
            change_date = date.fromisoformat(last["start-date"])
            if date.today() < change_date:
                return change_date
        return None

    @property
    def postaladdress(self) -> str:
        address = f"{self.contract.address2}, {self.contract.zip_code}, {self.contract.state}"
        return address

    @property
    def phone_nr(self) -> Optional[str]:
        return self.contract.phone

    @property
    def yaml_notes(self) -> Optional[Union[dict, list]]:
        """If yaml is kept in the Notes for a contract, parse and return dict."""
        try:
            return yaml.safe_load(user.contract.notes) if user.contract.notes else None
        except:
            return None

    @property
    def notes(slef) -> Optinal[str]:
        """Raw data from the `notes` field in a employee contract."""
        return user.contract.notes

    def __str__(self):
        return f"{self.name} ({self.email})"

    @classmethod
    def users_on_manager(cls, sort_key="name"):
        manager_dict = defaultdict(list)
        for user in cls.users_dict.values():
            if user.manager is None:
                continue
            manager_dict[user.manager.name].append(user)
        manager_dict = dict(sorted(manager_dict.items()))
        for k, v in manager_dict.items():
            manager_dict[k] = sorted(v, key=lambda user: getattr(user.contract, sort_key))
        return manager_dict

    @classmethod
    def all_users(cls, sort_key="employment_start_date") -> List[PeUser]:
        """
        Get all users, returns list of `PeUser`.

        Note:
          * We want users to have employment contract, fetch contracts and match to users.
          * After sorting, add an index, its nice to have.
          * Also store a dict on the class, so we can fetch all the users without HTTP roundtrip.
        """
        users_dicts = cls.pe_rest_client().users()
        contracts_dict: dict = cls.pe_rest_client().employment_contracts(as_dict=True)

        users = []
        for user in users_dicts:
            if user["id"] in contracts_dict:
                user["contract"] = contracts_dict[user["id"]]
                u = cls(**user)
                users.append(u)

        users = sorted(users, key=lambda user: (getattr(user.contract, sort_key), user.name))
        cls.add_index(users)
        cls.users_dict: dict[int, PeUser] = {user.id: user for user in users}
        return users

    @staticmethod
    def add_index(iterable):
        i = 1
        for item in iterable:
            item.index = i
            i += 1


if __name__ == "__main__":
    """Local testing"""
    import os
    from pprint import pprint

    credentials = PeCredentials(company_id=os.getenv("COMPANY"), api_access_token=os.getenv("API"))
    PeUser.pe_credentials = credentials

    for user in PeUser.all_users():
        print(user.name)
