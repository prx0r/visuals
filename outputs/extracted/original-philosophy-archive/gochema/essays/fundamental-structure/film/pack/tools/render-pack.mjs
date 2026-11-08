#!/usr/bin/env node
import { readFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { renderVideo, renderContactSheet, validateVideo } from "../MOTHERFUCKER/renderer.mjs";
const packPath=resolve(process.argv[2]??"MOTHERFUCKER/packs/fundamental-structure.json");
const output=resolve(process.argv[3]??"MOTHERFUCKER/build/fundamental-structure/video.mp4");
await mkdir(dirname(output),{recursive:true});
const pack=JSON.parse(await readFile(packPath,"utf8"));
for(const time of [0.08,0.28,0.55,0.82,0.96])
 await renderContactSheet(pack,resolve(`MOTHERFUCKER/build/fundamental-structure/contact-${String(time).replace(".","")}.png`),{columns:4,cellWidth:360,time});
await renderVideo(pack,output);
const result=validateVideo(pack,output);
if(!result.valid)throw new Error(result.errors.join("\n"));
console.log(JSON.stringify(result,null,2));
