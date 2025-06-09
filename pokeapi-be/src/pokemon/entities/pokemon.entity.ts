import { forwardRef } from '@nestjs/common';
import { Field, ID, Int, ObjectType } from '@nestjs/graphql';

import {
  Column,
  CreateDateColumn,
  Entity,
  JoinTable,
  ManyToMany,
  OneToMany,
  PrimaryColumn,
  UpdateDateColumn,
} from 'typeorm';

import { Ability } from './ability.entity';
import { Stat } from './stat.entity';
import { Type } from './type.entity';

@ObjectType()
@Entity({ name: 'pokemon' })
export class Pokemon {
  @Field(() => ID)
  @PrimaryColumn({ name: 'pokemon_id' })
  pokemonId: number;

  @Field()
  @Column()
  name: string;

  @Field(() => Int)
  @Column()
  height: number;

  @Field(() => Int)
  @Column()
  weight: number;

  @Field(() => Int)
  @Column({ name: 'base_experience' })
  baseExperience: number;

  @Field(() => Boolean)
  @Column({ name: 'is_default' })
  isDefault: boolean;

  //   @Field(() => [Type])
  //   @ManyToMany(() => Type, type => type.pokemons)
  //   @JoinTable({
  //     name: 'pokemon_types',
  //     joinColumn: { name: 'pokemon_id' },
  //     inverseJoinColumn: { name: 'type_id' },
  //   })
  //   types: Type[];

  @Field(() => [Type])
  @ManyToMany(() => Type, (type) => type.pokemons)
  @JoinTable({
    name: 'pokemon_types',
    joinColumn: { name: 'pokemon_id', referencedColumnName: 'pokemonId' },
    inverseJoinColumn: { name: 'type_id', referencedColumnName: 'typeId' },
  })
  types: Type[];

  @Field(() => [Ability])
  @ManyToMany(() => Ability, (ability) => ability.pokemons)
  @JoinTable({
    name: 'pokemon_abilities',
    joinColumn: { name: 'pokemon_id', referencedColumnName: 'pokemonId' },
    inverseJoinColumn: {
      name: 'ability_id',
      referencedColumnName: 'abilityId',
    },
  })
  abilities: Ability[];

  @Field(() => Date)
  @CreateDateColumn({ name: 'created_at', type: 'timestamp' })
  createdAt: Date;

  @Field(() => Date)
  @UpdateDateColumn({ name: 'updated_at', type: 'timestamp' })
  updatedAt: Date;
}
