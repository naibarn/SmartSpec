import { I as IfBoundedRecord } from './IfBoundedRecord-WIX9x_oz.cjs';

type ExactRecord<Key extends PropertyKey, Value> = IfBoundedRecord<Record<Key, Value>, Partial<Record<Key, Value>>, Record<Key, Value>>;

export type { ExactRecord as E };
