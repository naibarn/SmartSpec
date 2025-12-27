/* IMPORT */
import { makeParser } from '../utils.js';
import Grammar from './grammar.js';
/* MAIN */
const parser = makeParser(Grammar);
/* EXPORT */
export default parser;
