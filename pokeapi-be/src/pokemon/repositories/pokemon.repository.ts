import { CustomRepository } from 'src/common/decorators/typeorm.decorator';
import { ExtendedRepository } from 'src/common/graphql/customExtended';

import { Pokemon } from '../entities/pokemon.entity';
import { GetPokemonListInput } from '../inputs/pokemon.input';

@CustomRepository(Pokemon)
export class PokemonRepository extends ExtendedRepository<Pokemon> {
  async getPokemonWithRelations(id: number): Promise<Pokemon> {
    return this.createQueryBuilder('pokemon')
      .leftJoinAndSelect('pokemon.types', 'types')
      .leftJoinAndSelect('pokemon.abilities', 'abilities')
      .leftJoinAndSelect('pokemon.stats', 'stats')
      .where('pokemon.pokemon_id = :id', { id })
      .getOne();
  }

  async getPokemonByType(type: string): Promise<Pokemon[]> {
    return this.createQueryBuilder('pokemon')
      .innerJoin('pokemon.types', 'type', 'type.type_name = :type', { type })
      .leftJoinAndSelect('pokemon.types', 'types')
      .leftJoinAndSelect('pokemon.abilities', 'abilities')
      .getMany();
  }

  async getPaginatedPokemon(
    options: GetPokemonListInput,
  ): Promise<{ items: Pokemon[]; total: number }> {
    const { limit = 20, offset = 0, type } = options;

    const query = this.createQueryBuilder('pokemon')
      .leftJoinAndSelect('pokemon.types', 'types')
      .leftJoinAndSelect('pokemon.abilities', 'abilities')
      .leftJoinAndSelect('pokemon.stats', 'stats');

    if (type) {
      query.innerJoin(
        'pokemon.types',
        'filterType',
        'filterType.type_name = :type',
        { type },
      );
    }

    const [items, total] = await query
      .skip(offset)
      .take(limit)
      .getManyAndCount();

    return { items, total };
  }
  async getPaginatedPokemons(
    options: GetPokemonListInput,
  ): Promise<{ items: Pokemon[]; total: number }> {
    const { limit = 20, offset = 0, type } = options;

    const query = this.createQueryBuilder('pokemon')
      .leftJoinAndSelect('pokemon.types', 'types')
      .leftJoinAndSelect('pokemon.abilities', 'abilities')
      .leftJoinAndSelect('pokemon.stats', 'stats');

    if (type) {
      query.where('types.type_name = :type', { type });
    }

    const [items, total] = await query
      .skip(offset)
      .take(limit)
      .getManyAndCount();

    return { items, total };
  }
}
