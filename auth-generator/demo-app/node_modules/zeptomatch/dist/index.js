/* IMPORT */
import convert from './convert/parser.js';
import normalize from './normalize/parser.js';
import { memoize } from './utils.js';
/* MAIN */
const zeptomatch = (glob, path) => {
    if (Array.isArray(glob)) {
        const res = glob.map(zeptomatch.compile);
        const isMatch = res.some(re => re.test(path));
        return isMatch;
    }
    else {
        const re = zeptomatch.compile(glob);
        const isMatch = re.test(path);
        return isMatch;
    }
};
/* UTILITIES */
zeptomatch.compile = memoize((glob) => {
    return new RegExp(`^${convert(normalize(glob))}[\\\\/]?$`, 's');
});
/* EXPORT */
export default zeptomatch;
