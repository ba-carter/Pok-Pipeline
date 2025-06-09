import { CustomRepository } from 'src/common/decorators/typeorm.decorator';
import { ExtendedRepository } from 'src/common/graphql/customExtended';

import { Stat } from '../entities/stat.entity';

@CustomRepository(Stat)
export class StatRepository extends ExtendedRepository<Stat> {}
