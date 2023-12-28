from typing import TYPE_CHECKING, List, Optional

from sqlmodel import SQLModel, Field, Relationship



class TeamBase(SQLModel):
  name: str = Field(index=True)
  headquarters: str

class Team(TeamBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  heroes: List["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
  pass

class TeamRead(TeamBase):
  id: int

class TeamUpdate(SQLModel):
  name: Optional[str] = None
  headquarters: Optional[str] = None






# Use BaseModel
class HeroBase(SQLModel):
  name: str = Field(index=True)
  secret_name: str
  age: Optional[int] = Field(default=None, index=True)

  team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  team: Optional[Team] = Relationship(back_populates="heroes")


# These are only Pydantic Data Models
# Multiple Data Models for the API without the "table=True"
class HeroCreate(HeroBase):
  pass

class HeroRead(HeroBase):
  id: int

# With all optional Values
class HeroUpdate(SQLModel):
  name: Optional[str] = None
  secret_name: Optional[str] = None 
  age: Optional[int] = None
  team_id: Optional[int] = None


# Team with Heroes to prevent infite recursion
class TeamReadWithHeroes(TeamRead):
  heroes: List[HeroRead] = []

# Hero With Teams to prevent infinite recursion
class HeroReadWithTeam(HeroRead):
  team: Optional[TeamRead] = None


