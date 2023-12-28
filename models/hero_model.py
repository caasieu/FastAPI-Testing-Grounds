from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
  from team_model import Team, TeamRead

# Use BaseModel
class HeroBase(SQLModel):
  name: str = Field(index=True)
  secret_name: str
  age: Optional[int] = Field(default=None, index=True)

  team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  team: Optional["Team"] = Relationship(back_populates="heroes")


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

# Hero With Teams to prevent infinite recursion
class HeroReadWithTeam(HeroRead):
  team: Optional["TeamRead"] = None


