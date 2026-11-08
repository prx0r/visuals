#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
const root=resolve(process.argv[2]??".");
const analysis=JSON.parse(await readFile(resolve(root,"analysis.json"),"utf8"));
const pack=JSON.parse(await readFile(resolve(root,"MOTHERFUCKER/packs/fundamental-structure.template.json"),"utf8"));
const errors=[];
if(analysis.staticBeats.length!==13)errors.push("expected 13 static beats");
if(analysis.dynamicBeats.length!==14)errors.push("expected 14 dynamic beats");
if(pack.scenes.length!==27)errors.push("expected 27 scenes");
const ops=new Set(pack.scenes.map(s=>s.params.operation));
for(const op of ["klein-four","recursive-grid","group-action","zeno-series","perspective-switch","winner-selection"])
 if(!ops.has(op))errors.push(`missing ${op}`);
if(errors.length){console.error(errors.join("\n"));process.exit(1);}
console.log("Fundamental Structure pack: valid");
