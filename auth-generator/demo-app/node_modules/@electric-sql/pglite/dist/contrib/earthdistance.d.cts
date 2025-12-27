import { d as PGliteInterface } from '../pglite-BPiZge4p.cjs';

declare const earthdistance: {
    name: string;
    setup: (_pg: PGliteInterface, _emscriptenOpts: any) => Promise<{
        bundlePath: URL;
    }>;
};

export { earthdistance };
