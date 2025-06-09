import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';

import { CustomCache } from 'src/cache/custom-cache.decorator';
import { IGetData, RepoQuery } from 'src/common/graphql/types';

import { Ability } from './entities/ability.entity';
import { Pokemon } from './entities/pokemon.entity';
import { Stat } from './entities/stat.entity';
import { Type } from './entities/type.entity';
import {
  CreatePokemonInput,
  GetPokemonListInput,
  PokemonList,
  UpdatePokemonInput,
} from './inputs/pokemon.input';
import { AbilityRepository } from './repositories/ability.repository';
import { PokemonRepository } from './repositories/pokemon.repository';
import { StatRepository } from './repositories/stat.repository';
import { TypeRepository } from './repositories/type.repository';

@Injectable()
export class PokemonService {
  constructor(
    @InjectRepository(PokemonRepository)
    private pokemonRepository: PokemonRepository,
    @InjectRepository(TypeRepository)
    private typeRepository: TypeRepository,
    @InjectRepository(AbilityRepository)
    private abilityRepository: AbilityRepository,
    @InjectRepository(StatRepository)
    private statRepository: StatRepository,
  ) {}

  @CustomCache({ ttl: 300 })
  async getMany(option?: RepoQuery<Pokemon>): Promise<Pokemon[]> {
    const result: IGetData<Pokemon> =
      await this.pokemonRepository.getMany(option);
    return result.data;
  }

  async getOne(option: any): Promise<Pokemon> {
    return this.pokemonRepository.getOne(option);
  }

  async getById(id: number): Promise<Pokemon> {
    return this.pokemonRepository.getPokemonWithRelations(id);
  }

  async getByType(type: string): Promise<Pokemon[]> {
    return this.pokemonRepository.getPokemonByType(type);
  }

  async getPaginated(options: GetPokemonListInput): Promise<PokemonList> {
    return this.pokemonRepository.getPaginatedPokemon(options);
  }

  async create(input: CreatePokemonInput): Promise<Pokemon> {
    const pokemon = this.pokemonRepository.create(input);
    return this.pokemonRepository.save(pokemon);
  }

  async update(id: number, input: UpdatePokemonInput): Promise<Pokemon> {
    await this.pokemonRepository.update({ pokemonId: id }, input);
    return this.getById(id);
  }

  async delete(id: number): Promise<boolean> {
    const result = await this.pokemonRepository.delete({ pokemonId: id });
    return result.affected > 0;
  }

  async getAllTypes(): Promise<Type[]> {
    return this.typeRepository.find();
  }

  async getAllAbilities(): Promise<Ability[]> {
    return this.abilityRepository.find();
  }

  async getStatsForPokemon(pokemonId: number): Promise<Stat[]> {
    return this.statRepository.find({ where: { pokemonId } });
  }
}
