import { Field, ID, ObjectType } from '@nestjs/graphql';

import { Column, Entity, ManyToMany, PrimaryColumn, PrimaryGeneratedColumn } from 'typeorm';

import { Pokemon } from './pokemon.entity';

@ObjectType()
@Entity({ name: 'types' })
export class Type {
  @PrimaryGeneratedColumn({ name: 'type_id' })
  typeId: number;

  @Field()
  @Column({ name: 'type_name', unique: true })
  typeName: string;

  @Field(() => [Pokemon])
  @ManyToMany(() => Pokemon, (pokemon) => pokemon.types)
  pokemons: Pokemon[];
}
