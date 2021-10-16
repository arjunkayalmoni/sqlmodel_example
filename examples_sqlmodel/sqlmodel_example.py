from operator import or_
from typing import List, Optional

from sqlmodel import create_engine, Field, Relationship, Session, SQLModel, col, or_, select


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heroes: List['Hero'] = Relationship(back_populates='team')


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key='team.id')
    team: Optional[Team] = Relationship(back_populates='heroes')


sql_filename = 'superheroe.db'
sql_uri = f'sqlite:///{sql_filename}'

engine = create_engine(sql_uri, echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def create_teams():
    with Session(engine) as session:
        team_a = Team(name="Team Alpha", headquarters="Sharp Tower")
        team_b = Team(name="Team Beta", headquarters="Aqua World")
        teams = [team_a, team_b]
        for team in teams:
            session.add(team)
        session.commit()
        for team in teams:
            session.refresh(team)

    return {'team_a': team_a, 'team_b': team_b}


def create_heroes():
    # h1 = Hero(name='Spiderman', secret_name='Peter Parker', age=19)
    # h2 = Hero(name='Ironman', secret_name='Tony Stark')
    teams = create_teams()
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson",
                  team_id=teams['team_a'].id)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador",
                  team_id=teams['team_b'].id)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48,
                  team_id=teams['team_a'].id)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32,
                  team_id=teams['team_b'].id)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35,
                  team_id=teams['team_b'].id)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America",
                  secret_name="Esteban Rogelios", age=93)
    hero_6.team = teams.get('team_a')
    # hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    # hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    # hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    # hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    # hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    # hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    # hero_7 = Hero(name="Captain North America",
    #               secret_name="Esteban Rogelios", age=93)

    heroes = [hero_1, hero_2, hero_3, hero_4, hero_5, hero_6, hero_7]

    with Session(engine) as session:

        for hero in heroes:
            session.add(hero)
        session.commit()

        for hero in heroes:
            session.refresh(hero)

        for hero in heroes:
            print({f'{hero.id}': hero})


def create_heroes_with_relationship_attributes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(
            name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def select_team_heroes():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        result = session.exec(statement)
        team_preventers = result.one()

        print("Preventers heroes:", team_preventers.heroes)


def update_hero_team():
    with Session(engine) as session:
        hero = session.exec(
            # select(Hero).where(
            #     Hero.id == 4
            # )
            select(Hero).where(
                Hero.name == 'Dr. Weird'
            )
        ).one_or_none()
        print({'hero': hero, 'team': hero.team, 'team_id': hero.team_id})
        hero.team = None
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print({'hero': hero, 'team': hero.team, 'team_id': hero.team_id})


def select_heroes():
    with Session(engine) as session:
        # statement = select(Hero)
        # results = session.exec(statement)
        # # for hero in results:
        # #     print(hero)
        # heroes = results.all()

        heroes = session.exec(select(Hero)).all()
        print({'heroes': heroes})


def select_heroes_with_teams():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.id == Team.id)
        # heroes_with_teams = session.exec(statement).all()
        # print({'heroes_with_teams': heroes_with_teams})
        results = session.exec(statement)
        for hero, team in results:
            print({'hero': hero, 'team': team})


def select_heroes_with_teams_using_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
        # heroes_with_teams = session.exec(statement).all()
        # print({'heroes_with_teams': heroes_with_teams})
        results = session.exec(statement)
        for hero, team in results:
            print({'hero': hero, 'team': team})


def select_heroes_teams_using_left_outer_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print({'hero': hero, 'team': team})


def select_heroes_from_aqua():
    with Session(engine) as session:
        statement = select(Hero, Team).join(
            Team).where(Team.headquarters == "Aqua World")
        results = session.exec(statement)
        for hero, team in results:
            print({'hero': hero, 'team': team})


def select_hereos_where():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == 'Deadpond')
        results = session.exec(statement)
        for hero in results:
            print(hero)


def select_senior_heroes():
    with Session(engine) as session:
        # can use col to avoid getting linter warnings about optional[int] that could have a None value
        statement = select(Hero).where(col(Hero.age) >= 35)
        results = session.exec(statement)

        for hero in results:
            print(hero)


def select_junior_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age < 35)
        results = session.exec(statement)

        for hero in results:
            print(hero)


def select_young_heroes():
    with Session(engine) as session:
        # statement = select(Hero).where(Hero.age >= 35).where(Hero.age < 40)
        statement = select(Hero).where(Hero.age >= 35, Hero.age < 40)
        results = session.exec(statement)

        for hero in results:
            print(hero)


def select_youngest_or_oldest_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(
            or_(
                Hero.age <= 35, Hero.age > 90
            )
        )
        results = session.exec(statement)

        for hero in results:
            print(hero)


def select_one_resulting_hero():
    with Session(engine) as session:
        statement = select(Hero).where(
            col(Hero.age) == 35
        )
        result = session.exec(statement)
        hero = result.first()
        print({"hero": hero})


def select_hero_with_session_get():
    with Session(engine) as session:
        hero = session.get(Hero, 1)
        print({'hero': hero})


def limit_heros_rows():
    with Session(engine) as session:
        statement = select(Hero).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)


def limit_heroes_rows_with_where():
    with Session(engine) as session:
        statement = select(Hero).where(
            col(Hero.age) > 32
        ).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print({'heroes': heroes})


def offset_and_limit_heroes_rows():
    with Session(engine) as session:
        statement = select(Hero).offset(6).limit(3)
        results = session.exec(statement).all()
        print(results)


def update_hero():
    with Session(engine) as session:
        statement = select(Hero).where(
            col(Hero.name) == 'Spider-Boy'
        )
        results = session.exec(statement)
        hero = results.one()
        print({'hero': hero})

        hero.age = 45
        session.add(hero)

        statement = select(Hero).where(
            col(Hero.name) == 'Rusty-Man'
        )
        results = session.exec(statement)
        hero_2 = results.one()
        print({'hero_2': hero_2})

        hero_2.age = 50

        session.add(hero_2)

        session.commit()
        session.refresh(hero)
        session.refresh(hero_2)

        print({'hero': hero, 'hero_2': hero_2})


def delete_hero():
    with Session(engine) as session:
        statement = select(Hero).where(
            col(Hero.name) == 'Dr. Weird'
        )
        results = session.exec(statement)
        hero = results.one()
        print({'hero': hero})

        session.delete(hero)
        session.commit()
        print({'hero': hero, 'status': 'deleted'})
        statement = select(Hero).where(Hero.name == "Dr. Weird")
        results = session.exec(statement)
        hero = results.first()
        print({'hero': hero})


def create_team_with_heroes():
    with Session(engine) as session:
        hero_black_lion = Hero(
            name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")

        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        hero_tarantula = Hero(
            name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(
            name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_wakaland.heroes.append(hero_tarantula)
        team_wakaland.heroes.append(hero_dr_weird)
        team_wakaland.heroes.append(hero_cap)

        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)

        print("Team Wakaland:", team_wakaland)
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)


def main():
    # create_db_tables()
    # create_heroes()
    # create_team_with_heroes()
    # create_heroes_with_relationship_attributes()
    # create_heroes_with_relationship_attributes()
    # select_team_heroes()
    update_hero_team()
    # select_heroes()
    # select_hereos_where()
    # select_senior_heroes()
    # select_junior_heroes()
    # select_young_heroes()
    # select_youngest_or_oldest_heroes()
    # select_one_resulting_hero()
    # select_hero_with_session_get()
    # limit_heros_rows()
    # offset_and_limit_heroes_rows()
    # limit_heroes_rows_with_where()
    # update_hero()
    # delete_hero()
    # select_heroes_with_teams()
    # select_heroes_with_teams_using_join()
    # select_heroes_teams_using_left_outer_join()
    # select_heroes_from_aqua()


if __name__ == '__main__':
    main()
