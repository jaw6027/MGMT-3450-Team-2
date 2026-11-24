import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url));
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
const files=walk(root);let json=0,html=0,links=0,modules=0;
for(const file of files){
 if(file.endsWith('.json')){const data=JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));json++;if(Array.isArray(data.ads)){for(const ad of data.ads){if(!fs.existsSync(path.join(path.dirname(file),'assets',ad.image)))throw Error('Missing campaign image '+ad.image);}}}
 if(file.endsWith('.mjs')){const r=spawnSync(process.execPath,['--check',file],{encoding:'utf8'});if(r.status!==0)throw Error(r.stderr);modules++;}
 if(!file.endsWith('.html'))continue;
 const text=fs.readFileSync(file,'utf8');html++;
 for(const match of text.matchAll(/<script>([\s\S]*?)<\/script>/g))new vm.Script(match[1],{filename:file});
 const markup=text.replace(/<script>[\s\S]*?<\/script>/g,'');
 const refs=[...markup.matchAll(/(?:href|src)="([^"]+)"/g)].map(m=>m[1]);
 for(const match of text.matchAll(/"([^"\s]+\.(?:png|jpg|svg))"/g))if(match[1].includes('/'))refs.push(match[1]);
 for(const ref of new Set(refs)){
  if(/^(?:https?:|data:|mailto:|#)/i.test(ref))continue;
  const local=decodeURIComponent(ref.split('#')[0].split('?')[0]);if(!local)continue;
  const target=path.resolve(path.dirname(file),local);
  if(!fs.existsSync(target))throw Error('Broken local reference: '+path.relative(root,file)+' -> '+ref);
  links++;
 }
}
console.log(JSON.stringify({jsonFilesParsed:json,htmlPagesChecked:html,localReferencesChecked:links,sourceModulesSyntaxChecked:modules}));
