from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    pokemon_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    is_default = Column(Boolean)

    # Relationships
    types = relationship("PokemonType", back_populates="pokemon")
    abilities = relationship("PokemonAbility", back_populates="pokemon")
    stats = relationship("PokemonStat", back_populates="pokemon")


class Type(Base):
    __tablename__ = "types"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)

    pokemon = relationship("PokemonType", back_populates="type")


class Ability(Base):
    __tablename__ = "abilities"

    ability_id = Column(Integer, primary_key=True, autoincrement=True)
    ability_name = Column(String(100), unique=True, nullable=False)

    pokemon = relationship("PokemonAbility", back_populates="ability")


class PokemonType(Base):
    __tablename__ = "pokemon_types"

    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), primary_key=True)
    type_id = Column(Integer, ForeignKey("types.type_id"), primary_key=True)

    pokemon = relationship("Pokemon", back_populates="types")
    type = relationship("Type", back_populates="pokemon")


class PokemonAbility(Base):
    __tablename__ = "pokemon_abilities"

    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), primary_key=True)
    ability_id = Column(Integer, ForeignKey("abilities.ability_id"), primary_key=True)

    pokemon = relationship("Pokemon", back_populates="abilities")
    ability = relationship("Ability", back_populates="pokemon")


class PokemonStat(Base):
    __tablename__ = "pokemon_stats"

    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.pokemon_id"), nullable=False)
    stat_name = Column(String(50), nullable=False)
    base_stat = Column(Integer, nullable=False)
    effort = Column(Integer, default=0)

    pokemon = relationship("Pokemon", back_populates="stats")
