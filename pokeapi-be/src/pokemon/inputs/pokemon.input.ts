import { Field, InputType, Int, ObjectType } from '@nestjs/graphql';

import { IsBoolean, IsNumber, IsOptional, IsString } from 'class-validator';

import { Pokemon } from '../entities/pokemon.entity';

@InputType()
export class CreatePokemonInput implements Partial<Pokemon> {
  @Field(() => Int)
  @IsNumber()
  pokemonId: number;

  @Field()
  @IsString()
  name: string;

  @Field(() => Int)
  @IsNumber()
  height: number;

  @Field(() => Int)
  @IsNumber()
  weight: number;

  @Field(() => Int)
  @IsNumber()
  baseExperience: number;

  @Field(() => Boolean)
  @IsBoolean()
  isDefault: boolean;
}

@InputType()
export class UpdatePokemonInput implements Partial<Pokemon> {
  @Field(() => Int, { nullable: true })
  @IsNumber()
  @IsOptional()
  pokemonId?: number;

  @Field({ nullable: true })
  @IsString()
  @IsOptional()
  name?: string;

  @Field(() => Int, { nullable: true })
  @IsNumber()
  @IsOptional()
  height?: number;

  @Field(() => Int, { nullable: true })
  @IsNumber()
  @IsOptional()
  weight?: number;

  @Field(() => Int, { nullable: true })
  @IsNumber()
  @IsOptional()
  baseExperience?: number;

  @Field(() => Boolean, { nullable: true })
  @IsBoolean()
  @IsOptional()
  isDefault?: boolean;
}

@InputType()
export class PokemonIdInput {
  @Field(() => Int)
  @IsNumber()
  id: number;
}

@InputType()
export class GetPokemonListInput {
  @Field(() => Int, { nullable: true })
  @IsOptional()
  @IsNumber()
  limit?: number;

  @Field(() => Int, { nullable: true })
  @IsOptional()
  @IsNumber()
  offset?: number;

  @Field({ nullable: true })
  @IsOptional()
  @IsString()
  type?: string;
}

@ObjectType()
export class PokemonList {
  @Field(() => [Pokemon])
  items: Pokemon[];

  @Field(() => Int)
  total: number;
}
