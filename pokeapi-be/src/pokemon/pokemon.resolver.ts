import { Args, Int, Mutation, Query, Resolver } from '@nestjs/graphql';

import { CustomCache } from 'src/cache/custom-cache.decorator';
import { UseAuthGuard } from 'src/common/decorators/auth-guard.decorator';
import { UseRepositoryInterceptor } from 'src/common/decorators/repository-interceptor.decorator';

import { Ability } from './entities/ability.entity';
import { Pokemon } from './entities/pokemon.entity';
import { Type } from './entities/type.entity';
import {
  CreatePokemonInput,
  GetPokemonListInput,
  PokemonIdInput,
  PokemonList,
  UpdatePokemonInput,
} from './inputs/pokemon.input';
import { PokemonService } from './pokemon.service';

@Resolver(() => Pokemon)
export class PokemonResolver {
  constructor(private readonly pokemonService: PokemonService) {}

  @Query(() => PokemonList, { name: 'pokemons' })
  @CustomCache({ ttl: 300 })
  async getPaginatedPokemon(
    @Args('input') options: GetPokemonListInput,
  ): Promise<PokemonList> {
    return this.pokemonService.getPaginated(options);
  }

  //   @Query(() => Pokemon, { name: 'pokemon' })
  //   @UseRepositoryInterceptor(Pokemon)
  //   async getPokemonById(
  //     @Args() input: PokemonIdInput,
  //   ): Promise<Pokemon> {
  //     return this.pokemonService.getById(input.id);
  //   }

  @Query(() => Pokemon, { name: 'pokemon' })
  async getPokemonById(
    @Args('id', { type: () => Int }) id: number,
  ): Promise<Pokemon> {
    return this.pokemonService.getById(id);
  }
  @Query(() => [Pokemon], { name: 'pokemonByType' })
  async getPokemonByType(@Args('type') type: string): Promise<Pokemon[]> {
    return this.pokemonService.getByType(type);
  }

  @Query(() => [Type], { name: 'pokemonTypes' })
  @CustomCache({ ttl: 3600 })
  async getAllTypes(): Promise<Type[]> {
    return this.pokemonService.getAllTypes();
  }

  @Query(() => [Ability], { name: 'pokemonAbilities' })
  @CustomCache({ ttl: 3600 })
  async getAllAbilities(): Promise<Ability[]> {
    return this.pokemonService.getAllAbilities();
  }

  @Mutation(() => Pokemon, { name: 'createPokemon' })
  async createPokemon(
    @Args('input') input: CreatePokemonInput,
  ): Promise<Pokemon> {
    return this.pokemonService.create(input);
  }

  @Mutation(() => Pokemon, { name: 'updatePokemon' })
  async updatePokemon(
    @Args('id', { type: () => Int }) id: number,
    @Args('input') input: UpdatePokemonInput,
  ): Promise<Pokemon> {
    return this.pokemonService.update(id, input);
  }

  @Mutation(() => Boolean, { name: 'deletePokemon' })
  async deletePokemon(
    @Args('id', { type: () => Int }) id: number,
  ): Promise<boolean> {
    return this.pokemonService.delete(id);
  }
}
