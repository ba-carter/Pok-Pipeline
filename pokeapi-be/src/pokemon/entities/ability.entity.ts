import { Field, ID, ObjectType } from '@nestjs/graphql';

import { Column, Entity, ManyToMany, PrimaryColumn } from 'typeorm';

import { Pokemon } from './pokemon.entity';

@ObjectType()
@Entity({ name: 'abilities' })
export class Ability {
  @Field(() => ID)
  @PrimaryColumn({ name: 'ability_id' })
  abilityId: number;

  @Field()
  @Column({ name: 'ability_name', unique: true })
  abilityName: string;

  @Field(() => [Pokemon])
  @ManyToMany(() => Pokemon, (pokemon) => pokemon.abilities)
  pokemons: Pokemon[];
}
