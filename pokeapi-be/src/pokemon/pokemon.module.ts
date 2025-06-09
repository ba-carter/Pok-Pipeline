import { Module } from '@nestjs/common';

import { TypeOrmExModule } from 'src/common/modules/typeorm.module';

import { PokemonResolver } from './pokemon.resolver';
import { PokemonService } from './pokemon.service';
import { AbilityRepository } from './repositories/ability.repository';
import { PokemonRepository } from './repositories/pokemon.repository';
import { StatRepository } from './repositories/stat.repository';
import { TypeRepository } from './repositories/type.repository';

@Module({
  imports: [
    TypeOrmExModule.forCustomRepository([
      PokemonRepository,
      TypeRepository,
      AbilityRepository,
      StatRepository,
    ]),
  ],
  providers: [PokemonResolver, PokemonService],
  exports: [PokemonService],
})
export class PokemonModule {}
