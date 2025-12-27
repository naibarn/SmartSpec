/* IMPORT */
import { parse } from 'grammex';
/* MAIN */
const identity = (value) => {
    return value;
};
const makeParser = (grammar) => {
    return (input) => {
        return parse(input, grammar, { memoization: false }).join('');
    };
};
const memoize = (fn) => {
    const cache = {};
    return (arg) => {
        return cache[arg] ?? (cache[arg] = fn(arg));
    };
};
/* EXPORT */
export { identity, makeParser, memoize };
