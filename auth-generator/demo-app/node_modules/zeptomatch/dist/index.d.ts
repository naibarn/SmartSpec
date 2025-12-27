declare const zeptomatch: {
    (glob: string | string[], path: string): boolean;
    compile: (arg: string) => RegExp;
};
export default zeptomatch;
