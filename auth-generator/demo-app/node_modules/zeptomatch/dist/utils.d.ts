import type { ExplicitRule } from 'grammex';
declare const identity: <T>(value: T) => T;
declare const makeParser: (grammar: ExplicitRule<string>) => (input: string) => string;
declare const memoize: <T>(fn: (arg: string) => T) => ((arg: string) => T);
export { identity, makeParser, memoize };
