import { CustomRepository } from 'src/common/decorators/typeorm.decorator';
import { ExtendedRepository } from 'src/common/graphql/customExtended';

import { Type } from '../entities/type.entity';

@CustomRepository(Type)
export class TypeRepository extends ExtendedRepository<Type> {}
