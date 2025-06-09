import { CustomRepository } from 'src/common/decorators/typeorm.decorator';
import { ExtendedRepository } from 'src/common/graphql/customExtended';

import { Ability } from '../entities/ability.entity';

@CustomRepository(Ability)
export class AbilityRepository extends ExtendedRepository<Ability> {}
