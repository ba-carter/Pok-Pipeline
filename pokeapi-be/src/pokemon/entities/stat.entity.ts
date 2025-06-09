import { forwardRef } from '@nestjs/common';
import { Field, ID, Int, ObjectType } from '@nestjs/graphql';

import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from 'typeorm';

import { Pokemon } from './pokemon.entity';

@ObjectType()
@Entity({ name: 'pokemon_stats' })
export class Stat {
  @Field(() => ID)
  @PrimaryGeneratedColumn({ name: 'stat_id' })
  statId: number;

  @Field()
  @Column({ name: 'stat_name' })
  statName: string;

  @Field(() => Int)
  @Column({ name: 'base_stat' })
  baseStat: number;

  @Field(() => Int)
  @Column()
  effort: number;

  @Field(() => Pokemon)
  @ManyToOne('Pokemon', 'stats')
  @JoinColumn({ name: 'pokemon_id', referencedColumnName: 'pokemonId' })
  pokemon: Pokemon;

  @Column({ name: 'pokemon_id' })
  pokemonId: number;
}
