#!/usr/bin/env node
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
const root=resolve(process.cwd());
async function patch(path,fn){
 const src=await readFile(path,"utf8"),next=fn(src);
 if(next!==src)await writeFile(path,next);
 console.log(next!==src?`patched ${path}`:`unchanged ${path}`);
}
await patch(resolve(root,"motifs.mjs"),source=>{
 if(!source.includes("renderFundamentalStructure"))
   source=`import { renderFundamentalStructure } from "./src/fundamental-structure-motif.mjs";\n${source}`;
 if(!source.includes('"fundamental-structure": renderFundamentalStructure'))
   source=source.replace("export const motifs = {",'export const motifs = {\n  "fundamental-structure": renderFundamentalStructure,');
 return source;
});
