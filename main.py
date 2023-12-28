from contextlib import asynccontextmanager

from typing import List
from fastapi import Depends ,FastAPI, HTTPException, Query
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from model import Team, TeamCreate, TeamRead, TeamUpdate, TeamReadWithHeroes, Hero, HeroCreate, HeroRead, HeroUpdate, HeroReadWithTeam
#from models.hero_model import Hero, HeroCreate, HeroRead, HeroUpdate, HeroReadWithTeam
#from models.team_model import Team, TeamCreate, TeamRead, TeamUpdate, TeamReadWithHeroes

from utils import get_session






# Execute on startup
@asynccontextmanager
async def lifespan(app: FastAPI):

  print("| STARTING |") 
  create_db_and_tables()
  yield # Executes the code before itself
  

  print("| Exiting |")

app = FastAPI(lifespan=lifespan)



# Create the hero and commit him to the database

# UPDATE: Now i'm using FastAPI dependecy "Depends" which pretty much embeds the request into a session as well here
# UPDATE: The value of a dependency will only be used for one request
# UPDATE: FastAPI will call it right before calling your code and will give you the value from that dependency.

@app.post('/heroes/', response_model=HeroRead)
def create_heroes(*, session: Session = Depends(get_session), hero: HeroCreate):  
  db_hero = Hero.model_validate(hero)
  session.add(db_hero)
  session.commit()
  session.refresh(db_hero)
  return db_hero


# Read a hero by its id and verify if exists
@app.get('/heroes/{hero_id}', response_model=HeroReadWithTeam)
def get_hero(*, session: Session = Depends(get_session) , hero_id: int):
  hero = session.get(Hero, hero_id) # get by id
  if not hero:
    raise HTTPException(status_code=404, detail="Hero Not Found")
  return hero


# PATH: localhost://limit/?offset=1&limit=100
# Read a limited number of heroes
@app.get('/limit/', response_model=List[HeroRead])
def limit_heroes(*, session: Session = Depends(get_session) ,offset: int = 0, limit: int = Query(default=100, le=100)):  
  heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
  return heroes


# Read All Heroes
@app.get('/heroes/', response_model=List[HeroRead])
def read_heroes(*, session: Session = Depends(get_session)):
  heroes = session.exec(select(Hero)).all()
  return heroes


# Update partially the values of a hero us patch
@app.patch('/update/{hero_id}', response_model=HeroRead)
def update_hero(*, session: Session = Depends(get_session), hero_id:int, hero: HeroUpdate):
  db_hero = session.get(Hero, hero_id)
  if not db_hero:
    raise HTTPException(status_code=404, detail="Hero not found")
  hero_data = hero.model_dump(exclude_unset=True) # Ignore valores que o client não incluiu, assim se enviar {} a base de dados vai apenas ignorar e manter os dados correntes

  for key, value in hero_data.items():
    setattr(db_hero, key, value)
  session.add(db_hero)
  session.commit()
  session.refresh(db_hero)

  return db_hero


# Delete a hero using delete
@app.delete('/delete/{hero_id}')
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
  hero = session.get(Hero, hero_id)
  if not hero:
    raise HTTPException(status_code=404, detail="Hero Not Found Bro!")
  session.delete(hero)
  session.commit()

  return {"deleted": True}
    














'''  PATH OPERATIONS FOR TEAMS  '''
# Create a Team on the database
@app.post('/teams/', response_model=TeamRead)
def create_teams(*, session: Session = Depends(get_session), team: TeamCreate):
  db_team = Team.model_validate(team)  
  session.add(db_team)
  session.commit()
  session.refresh(db_team)
  return db_team

# Get all the Teams
@app.get('/teams/', response_model=List[TeamRead])
def read_teams(*, session: Session = Depends(get_session)):
  teams = session.exec(select(Team)).all()
  return teams

# Get a specific team based on its id
@app.get('/teams/{team_id}', response_model=TeamReadWithHeroes)
def read_team(*, session: Session = Depends(get_session), team_id: int):
  team = session.get(Team, team_id)
  if not team:
    raise HTTPException(status_code=404 ,detail="Team não encontrado!")
  return team

# Update a team based on the id
@app.patch('/teams/{team_id}', response_model=TeamRead)
def update_team(*, session: Session = Depends(get_session), team_id: int, team: TeamUpdate):
  db_team = session.get(Team, team_id)
  if not db_team:
    raise HTTPException(status_code=404 ,detail="Team não encontrado!")
  
  team_data = team.model_dump(exclude_unset=True) # Ignore valores que o client não incluiu, assim se enviar {} a base de dados vai apenas ignorar e manter os dados correntes
  for key, value in team_data.items():
    setattr(db_team, key, value)
  session.add(db_team)
  session.commit()
  session.refresh(db_team)
  return db_team

# Delete a team based on its id
@app.delete('/teams/{team_id}')
def delete_team(*, session: Session = Depends(get_session), team_id: int):
  db_team = session.get(Team, team_id)
  if not db_team:
    raise HTTPException(status_code=404, detail="Sem Team Para Apagar!")
  session.delete(db_team)
  session.commit()

  return {"Deleted": True}






# Index Page
@app.get('/')
def index():
  return {"Index": 1}




# create_db_and_tables()
