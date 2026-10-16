import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export type Station = 'evidence' | 'assembly' | 'dispatch';
export type WorldState = {baseline:boolean;resolved:boolean;proposal:boolean;paused:boolean;station:Station;modalOpen:boolean};
export type Telemetry={x:number;z:number;nearby:Station|null};
export type FactoryController={update:(s:WorldState)=>void;home:()=>void;walk:(enabled:boolean)=>void;move:(key:string,down:boolean)=>void;interact:()=>void;dispose:()=>void};

export function createFactory(container:HTMLElement,onStation:(id:Station)=>void,onReady:()=>void,onTelemetry:(t:Telemetry)=>void,onInteract:(id:Station)=>void):FactoryController {
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0b141c');
 scene.fog=new THREE.FogExp2('#0b141c',.018);
 const camera=new THREE.PerspectiveCamera(37,1,.1,120);camera.position.set(20,21,29);
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'high-performance'});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.8));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.5;
 container.appendChild(renderer.domElement);renderer.domElement.setAttribute('aria-label','Northstar factory. Enter factory to walk with WASD or arrows; drag to look and press E near a station.');renderer.domElement.tabIndex=0;
 const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,1,0);controls.enableDamping=true;controls.enablePan=false;controls.minDistance=16;controls.maxDistance=48;controls.minPolarAngle=.35;controls.maxPolarAngle=1.25;controls.update();
 const geometry:THREE.BufferGeometry[]=[],materials:THREE.Material[]=[],textures:THREE.Texture[]=[];
 const mat=(color:string,metalness=.1,roughness=.6,emissive?:string)=>{const m=new THREE.MeshStandardMaterial({color,metalness,roughness,emissive:emissive||'#000000',emissiveIntensity:emissive?1.2:0});materials.push(m);return m};
 const navy=mat('#21343e'), wall=mat('#334650'), slate=mat('#4e626a'), dark=mat('#111d28'), cream=mat('#e1ddcb'), orange=mat('#ed9a46'), mint=mat('#83efd2'), steel=mat('#8fa5a8',.65,.32), rubber=mat('#101c25'), glow=mat('#8cf9dd',.2,.3,'#63e5ca'), goldGlow=mat('#ffc071',.1,.4,'#ffab48'), blueGlow=mat('#a8ddff',.1,.4,'#65bddd');
 function mesh(g:THREE.BufferGeometry,m:THREE.Material,parent:THREE.Object3D=scene,x=0,y=0,z=0){geometry.push(g);const o=new THREE.Mesh(g,m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
 function box(w:number,h:number,d:number,m:THREE.Material,p:THREE.Object3D=scene,x=0,y=0,z=0,r=.04){return mesh(r?new RoundedBoxGeometry(w,h,d,2,r):new THREE.BoxGeometry(w,h,d),m,p,x,y,z)}
 function cyl(r:number,h:number,m:THREE.Material,p:THREE.Object3D=scene,x=0,y=0,z=0){return mesh(new THREE.CylinderGeometry(r,r,h,16),m,p,x,y,z)}
 function sphere(r:number,m:THREE.Material,p:THREE.Object3D=scene,x=0,y=0,z=0){return mesh(new THREE.SphereGeometry(r,16,12),m,p,x,y,z)}
 function label(text:string,width:number,height:number,p:THREE.Object3D,x:number,y:number,z:number,color='#b9f4e3',bg='#152a34'){
  const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=256;const ctx=canvas.getContext('2d')!;ctx.fillStyle=bg;ctx.fillRect(0,0,1024,256);ctx.strokeStyle=color;ctx.lineWidth=4;ctx.strokeRect(10,10,1004,236);ctx.fillStyle=color;ctx.font='600 72px monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,512,128,950);const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;textures.push(texture);const m=new THREE.MeshBasicMaterial({map:texture});materials.push(m);return mesh(new THREE.PlaneGeometry(width,height),m,p,x,y,z)
 }
 scene.add(new THREE.HemisphereLight('#b9e9ff','#2c3942',2));const sun=new THREE.DirectionalLight('#e8f8ff',3.2);sun.position.set(3,17,12);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-14;sun.shadow.camera.right=14;sun.shadow.camera.top=12;sun.shadow.camera.bottom=-12;sun.shadow.bias=-.0005;sun.shadow.normalBias=.035;scene.add(sun);
 const warmLight=new THREE.PointLight('#ffb766',75,16,2);warmLight.position.set(-5,6,-1);scene.add(warmLight);const coolLight=new THREE.PointLight('#6edbcf',65,15,2);coolLight.position.set(5,5,1);scene.add(coolLight);
 // An open miniature factory stage. All geometry and characters are original.
 box(30,.8,24,navy,scene,0,-.55,3,.2);box(29.7,.15,23.7,slate,scene,0,-.08,3,.05);
 const grid=new THREE.GridHelper(17.4,29,'#758e92','#566d73');grid.position.y=.009;scene.add(grid);
 box(30,3.4,.22,wall,scene,0,1.65,-8.9);box(.22,3.4,24,wall,scene,-14.9,1.65,3);
 // Back-wall windows and luminous roof rails.
 for(let i=0;i<9;i++){box(1.65,1.45,.05,dark,scene,-7.8+i*1.92,2.15,-5.76);box(1.42,1.2,.025,blueGlow,scene,-7.8+i*1.92,2.15,-5.71);box(.045,1.2,.04,steel,scene,-7.8+i*1.92,2.15,-5.67)}
 for(let x=-8;x<=8;x+=4){box(.15,4,.15,steel,scene,x,2,-5.5);box(.18,.15,10.3,navy,scene,x,4,-.5);box(.09,.04,7,blueGlow,scene,x,3.89,-.5)}
 box(17,.15,.18,navy,scene,0,4,-5.45);box(17,.15,.18,navy,scene,0,4,4.55);
 label('NORTHSTAR  /  NIGHT SHIFT',6.3,.7,scene,0,3.12,-5.69,'#c8e6e6');
 // Floor route and caution strips.
 for(let i=0;i<12;i++)box(.65,.02,.09,cream,scene,-7.4+i*1.3,.03,4.5,0);
 for(const z of [-4.6,3.7])box(16,.015,.05,mint,scene,0,.03,z,0);
 const stations:Record<Station,THREE.Group>={evidence:new THREE.Group(),assembly:new THREE.Group(),dispatch:new THREE.Group()};
 Object.entries(stations).forEach(([id,g])=>{g.userData.station=id;scene.add(g)});
 // Evidence workbench: a real reading station with moving technician.
 const desk=stations.evidence;desk.position.set(-5.7,0,.7);
 box(3.4,.2,1.6,cream,desk,0,1.25,0);for(const x of [-1.4,1.4])for(const z of [-.55,.55])box(.12,1.2,.12,steel,desk,x,.6,z);
 const screen=box(1.2,.82,.12,dark,desk,-.6,1.98,-.5);screen.rotation.x=-.1;box(1.03,.62,.025,glow,desk,-.6,2,-.415);box(.12,.35,.12,steel,desk,-.6,1.5,-.5);box(.7,.05,.3,slate,desk,-.6,1.4,-.5);
 for(let i=0;i<5;i++)box(.6,.025,.72,cream,desk,.65,1.38+i*.028,.2);
 box(.5,.04,.15,orange,desk,.7,1.55,.15);cyl(.13,.26,orange,desk,-1.2,1.48,.4);
 box(.85,1.25,.8,navy,desk,1.5,.63,-1.8);for(let i=0;i<3;i++){box(.7,.3,.02,slate,desk,1.5,.3+i*.35,-1.38);box(.2,.04,.04,steel,desk,1.5,.3+i*.35,-1.35)}
 label('01  EVIDENCE',2.65,.55,desk,0,.32,1.05,'#ffcb89');
 // Conveyor line with scanner arch and individually moving bottles.
 const assembly=stations.assembly;assembly.position.set(0,0,-.8);
 box(2.45,.25,7.2,navy,assembly,0,.8,0);box(1.9,.08,7,rubber,assembly,0,.96,0);for(const x of [-1.05,1.05]){box(.12,.15,7.1,steel,assembly,x,1,0);for(const z of [-2.8,0,2.8])box(.15,.8,.15,steel,assembly,x,.4,z)}
 for(let i=0;i<25;i++)box(1.8,.02,.035,slate,assembly,0,1.01,-3.35+i*.28,0);
 for(const x of [-1.12,1.12])box(.24,2.3,.5,orange,assembly,x,1.9,-.6);
 box(2.5,.3,.55,orange,assembly,0,3,-.6);label('N / SCAN',1.8,.3,assembly,0,3.04,-.31,'#132a33','#efb56c');
 const scannerMat=new THREE.MeshBasicMaterial({color:'#78e4cc',transparent:true,opacity:.13,side:THREE.DoubleSide});materials.push(scannerMat);const scanPlane=mesh(new THREE.PlaneGeometry(1.9,1.8),scannerMat,assembly,0,1.92,-.6);
 const bottles:THREE.Group[]=[];for(let i=0;i<10;i++){const g=new THREE.Group();assembly.add(g);cyl(.14,.48,i%3===0?mint:cream,g,0,.29,0);cyl(.08,.12,steel,g,0,.59,0);cyl(.1,.1,orange,g,0,.7,0);g.position.set(i%2===0?-.45:.45,1.04,-3.3+i*.65);bottles.push(g)}
 label('02  ASSEMBLY',2.3,.5,assembly,0,.3,4,'#9bf0da');
 // Dispatch: pallets, containers, and a held shipment with an unresolved beacon.
 const dispatch=stations.dispatch;dispatch.position.set(5.4,0,.4);
 const crates:THREE.Group[]=[];for(let i=0;i<4;i++){const g=new THREE.Group();g.position.set((i%2)*2-1,0,Math.floor(i/2)*2.05-2);dispatch.add(g);for(let j=0;j<3;j++)box(1.65,.1,.18,cream,g,0,.12,-.55+j*.55);for(let j=0;j<2;j++){box(1.45,.58,1.2,i===3?orange:navy,g,0,.45+j*.59,0);box(.12,.59,1.21,cream,g,0,.45+j*.59,0);box(1.46,.08,1.21,slate,g,0,.6+j*.59,0)}label('S'+(i+1),.65,.32,g,0,.77,.616,'#e8e9d0',i===3?'#ac6a32':'#223d46');crates.push(g)}
 const beacon=cyl(.11,.2,goldGlow,dispatch,1,1.75,.05);cyl(.17,.06,steel,dispatch,1,1.62,.05);
 label('03  DISPATCH',2.7,.5,dispatch,0,.31,2,'#ffcb89');
 // Storage rack and wall details.
 for(const x of [3.7,6.7])box(.12,2.4,.12,steel,scene,x,1.2,-4.9);
 for(const y of [.35,1.25,2.15]){box(3.2,.12,.8,navy,scene,5.2,y,-4.9);for(let j=0;j<4;j++)box(.55,.58,.65,j%2?orange:cream,scene,4.05+j*.73,y+.35,-4.9)}
 for(let i=0;i<3;i++){cyl(.4,1.15,navy,scene,-7.5+i*.9,.58,-3.9);cyl(.42,.05,steel,scene,-7.5+i*.9,1.13,-3.9)}

 // Receiving wing, service plant and outbound staging surround the live line.
 for(const x of [-11,11]){
  box(3,.12,7,navy,scene,x,.04,1);
  for(const z of [-1.5,1,3.5]){box(2.5,1.3,1.5,cream,scene,x,.75,z);box(2.52,.15,1.52,orange,scene,x,1.1,z)}
 }
 for(const x of [-11,-7,7,11]){cyl(.8,2.5,steel,scene,x,1.25,-7);cyl(.82,.12,mint,scene,x,2.5,-7)}
 label('RECEIVING / MATERIALS',5,.7,scene,-10,3.2,-8.7);
 label('OUTBOUND / HOLD FOR REVIEW',6,.7,scene,9,3.2,-8.7,'#ffcb89');
 for(const x of [-11,-6,0,6,11]){box(.12,.02,10,cream,scene,x,.03,9,0)}
 for(const z of [6,13])box(27,.02,.1,mint,scene,0,.03,z,0);
 label('PEDESTRIAN ROUTE',4,.5,scene,-5,1,12,'#b9f4e3');
 const obstacles=[[-7.6,-3.7,-1.6,1.6],[-1.6,1.6,-4.8,3], [3.1,7.7,-2.7,1.7], [3.3,7.2,-5.6,-4.2],[-8,-5,-4.6,-3.2],[-12.6,-9.4,-2.6,4.6],[9.4,12.6,-2.6,4.6],...[-11,-7,7,11].map(x=>[x-1.1,x+1.1,-8.1,-5.9])];
 const blocked=(x:number,z:number)=>Math.abs(x)>14.2||z< -8.2||z>14.2||obstacles.some(([a,b,c,d])=>x>a-.3&&x<b+.3&&z>c-.3&&z<d+.3);
 // Little forklift, with a properly articulated driver.
 const lift=new THREE.Group();scene.add(lift);box(1.25,.55,1.6,orange,lift,0,.65,0);box(.75,.15,.8,dark,lift,0,1.02,.25);for(const x of [-.58,.58])for(const z of [-.5,.5]){const wheel=cyl(.25,.18,rubber,lift,x,.32,z);wheel.rotation.z=Math.PI/2;cyl(.1,.19,steel,lift,x,.32,z).rotation.z=Math.PI/2}for(const x of [-.5,.5])box(.07,1.2,.07,steel,lift,x,1.35,.55);box(1.2,.08,1.1,navy,lift,0,1.95,.15);for(const x of [-.42,.42]){box(.07,1.7,.1,steel,lift,x,1.1,-.83);box(.15,.07,1.2,steel,lift,x,.3,-1.35)}
 function crew(color:THREE.Material,x:number,z:number,helmetColor=orange){const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);const skin=mat('#b18a71');const body=box(.47,.67,.31,color,g,0,.9,0,.09);box(.49,.11,.33,cream,g,0,.84,0);box(.09,.59,.34,cream,g,-.16,.95,0);box(.09,.59,.34,cream,g,.16,.95,0);sphere(.21,skin,g,0,1.45,0);const helmet=sphere(.24,helmetColor,g,0,1.59,0);helmet.scale.y=.55;box(.55,.055,.43,helmetColor,g,0,1.52,.04);box(.32,.08,.04,dark,g,0,1.46,.19);const arms:THREE.Group[]=[],legs:THREE.Group[]=[];for(const side of [-1,1]){const a=new THREE.Group();a.position.set(side*.3,1.15,0);g.add(a);box(.14,.48,.18,color,a,0,-.21,0,.06);sphere(.085,skin,a,0,-.49,0);arms.push(a);const leg=new THREE.Group();leg.position.set(side*.14,.6,0);g.add(leg);box(.17,.46,.22,navy,leg,0,-.2,0);box(.21,.13,.33,rubber,leg,0,-.45,.05);legs.push(leg)}return {g,body,arms,legs}}
 const mira=crew(mint,-5.65,2.1);mira.g.rotation.y=Math.PI;const clipboard=box(.36,.45,.05,dark,mira.arms[0],0,-.45,.12);clipboard.rotation.x=.2;
 const sol=crew(orange,2.2,-1.4,cream);sol.g.rotation.y=-Math.PI/2;
 const courier=crew(navy,5,3.2);courier.g.scale.setScalar(.9);
 // Pip: original walking inspection robot, with articulated limbs and expressive visor.
 const robot=new THREE.Group();scene.add(robot);robot.position.set(-2.6,0,3.4);
 const torso=box(.6,.55,.44,cream,robot,0,.75,0,.12);box(.35,.18,.025,navy,robot,0,.78,.23);box(.18,.045,.03,glow,robot,0,.79,.25);
 const head=new THREE.Group();head.position.y=1.3;robot.add(head);box(.8,.57,.57,orange,head,0,0,0,.16);box(.66,.35,.055,dark,head,0,0,.29,.11);
 const eyeL=box(.1,.16,.03,glow,head,-.16,.025,.325,.035),eyeR=box(.1,.16,.03,glow,head,.16,.025,.325,.035);
 cyl(.03,.25,steel,head,.23,.38,0);sphere(.06,glow,head,.23,.54,0);
 const robotArms:THREE.Group[]=[],robotLegs:THREE.Group[]=[];for(const side of [-1,1]){const arm=new THREE.Group();arm.position.set(side*.43,.95,0);robot.add(arm);sphere(.11,steel,arm);box(.17,.34,.2,orange,arm,0,-.2,0,.06);sphere(.11,cream,arm,0,-.4,0);robotArms.push(arm);const leg=new THREE.Group();leg.position.set(side*.21,.5,0);robot.add(leg);cyl(.075,.24,steel,leg,0,-.1,0);box(.26,.18,.36,orange,leg,0,-.27,.055,.06);robotLegs.push(leg)}
 const haloMat=new THREE.MeshBasicMaterial({color:'#93f4d2',transparent:true,opacity:.5,side:THREE.DoubleSide});materials.push(haloMat);const halo=mesh(new THREE.RingGeometry(.52,.57,48),haloMat,robot,0,.025,0);halo.rotation.x=-Math.PI/2;
 // Courier drone and slow-moving airborne flecks.
 const drone=new THREE.Group();scene.add(drone);sphere(.22,cream,drone);box(.24,.08,.08,glow,drone,0,0,.2);const rotor=cyl(.5,.025,steel,drone,0,.3,0);rotor.scale.z=.12;
 const dots=new Float32Array(80*3);for(let i=0;i<80;i++){dots[i*3]=Math.sin(i*41.4)*10;dots[i*3+1]=1+(i%17)/3;dots[i*3+2]=Math.cos(i*57.2)*7}const particleGeometry=new THREE.BufferGeometry();particleGeometry.setAttribute('position',new THREE.BufferAttribute(dots,3));geometry.push(particleGeometry);const particleMat=new THREE.PointsMaterial({color:'#b3d9c9',size:.035,transparent:true,opacity:.35});materials.push(particleMat);const particles=new THREE.Points(particleGeometry,particleMat);scene.add(particles);
 const stationRings:Record<Station,THREE.Mesh>={} as Record<Station,THREE.Mesh>;for(const [id,g] of Object.entries(stations)){const m=new THREE.MeshBasicMaterial({color:'#89e4cb',transparent:true,opacity:.28,side:THREE.DoubleSide});materials.push(m);const ring=mesh(new THREE.RingGeometry(.35,.4,48),m,g,0,.04,2.2);ring.rotation.x=-Math.PI/2;stationRings[id as Station]=ring}
 let state:WorldState={baseline:false,resolved:false,proposal:false,paused:false,station:'evidence',modalOpen:false};let elapsed=0,last=0,raf=0,disposed=false;const keys=new Set<string>();let walkMode=false,nearby:Station|null=null,lastTelemetry=0;let manualUntil=0;const target=new THREE.Vector3(-3.7,0,2.5);
 const raycaster=new THREE.Raycaster();const pointer=new THREE.Vector2();let downX=0,downY=0;
 const down=(e:PointerEvent)=>{downX=e.clientX;downY=e.clientY};
 const click=(e:PointerEvent)=>{if(Math.abs(e.clientX-downX)+Math.abs(e.clientY-downY)>7)return;const rect=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);const hits=raycaster.intersectObjects(Object.values(stations),true);if(hits.length){let o:THREE.Object3D|null=hits[0].object;while(o&&!o.userData.station)o=o.parent;if(o)onStation(o.userData.station)}};
 const interact=()=>{if(walkMode&&nearby&&!state.paused&&!state.modalOpen)onInteract(nearby)};
 const keydown=(e:KeyboardEvent)=>{if(state.modalOpen)return;if(e.key.toLowerCase()==='e'){e.preventDefault();if(!e.repeat)interact();return;}if(['w','a','s','d','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();keys.add(e.key);manualUntil=elapsed+5}};
 const keyup=(e:KeyboardEvent)=>keys.delete(e.key);const blur=()=>keys.clear();
 renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointerup',click);renderer.domElement.addEventListener('keydown',keydown);renderer.domElement.addEventListener('keyup',keyup);renderer.domElement.addEventListener('blur',blur);
 function resize(){const w=container.clientWidth,h=container.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.zoom=Math.min(1,camera.aspect/1.3);camera.updateProjectionMatrix()}
 const observer=new ResizeObserver(resize);observer.observe(container);resize();
 function animate(ms:number){if(disposed)return;raf=requestAnimationFrame(animate);if(ms-last<1000/30)return;const dt=Math.min((ms-last)/1000,.05);last=ms;if(document.hidden)return;
  const moving=!state.paused&&!state.modalOpen; if(moving)elapsed+=dt;const t=elapsed;
  if(moving){
   bottles.forEach((g,i)=>{g.position.z=-3.3+((t*.38+i*.65)%6.5)});scanPlane.position.y=1.9+Math.sin(t*2)*.12;
   mira.body.rotation.z=Math.sin(t*1.5)*.025;mira.arms[0].rotation.x=-.65+Math.sin(t*1.4)*.16;mira.g.rotation.y=Math.PI+Math.sin(t*.5)*.15;
   sol.arms[0].rotation.x=-.45+Math.sin(t*1.8)*.3;sol.arms[1].rotation.x=.2+Math.sin(t*1.8+1)*.15;sol.g.position.y=Math.sin(t*1.8)*.015;
   courier.g.position.x=4.3+Math.sin(t*.22)*1.3;courier.g.position.z=3.1;courier.g.rotation.y=Math.cos(t*.22)>0?Math.PI/2:-Math.PI/2;courier.legs.forEach((l,i)=>l.rotation.x=Math.sin(t*5+i*Math.PI)*.3);courier.arms.forEach((a,i)=>a.rotation.x=Math.sin(t*5+i*Math.PI)*.2);
   lift.position.set(-4.4+Math.sin(t*.13)*1.3,0,-3.5);lift.rotation.y=Math.PI/2;
   drone.position.set(4+Math.sin(t*.35)*1.2,3.3+Math.sin(t*1.8)*.15,1+Math.cos(t*.35)*1.6);rotor.rotation.y=t*25;drone.rotation.y=-t*.35;
   particles.rotation.y=t*.015;
   const manual=new THREE.Vector3((keys.has('d')||keys.has('ArrowRight')?1:0)-(keys.has('a')||keys.has('ArrowLeft')?1:0),0,(keys.has('s')||keys.has('ArrowDown')?1:0)-(keys.has('w')||keys.has('ArrowUp')?1:0));
   if(walkMode&&manual.lengthSq()){const yaw=Math.atan2(camera.position.x-controls.target.x,camera.position.z-controls.target.z);manual.applyAxisAngle(new THREE.Vector3(0,1,0),yaw)}
   const delta=manual.lengthSq()?manual.normalize():walkMode||elapsed<manualUntil?new THREE.Vector3():target.clone().sub(robot.position).setY(0);const walking=delta.length()>.1;
   if(walking){delta.normalize();const step=dt*(walkMode?3.4:1.5);const nx=robot.position.x+delta.x*step,nz=robot.position.z+delta.z*step;if(!blocked(nx,robot.position.z))robot.position.x=nx;if(!blocked(robot.position.x,nz))robot.position.z=nz;const angle=Math.atan2(delta.x,delta.z);robot.rotation.y+=Math.atan2(Math.sin(angle-robot.rotation.y),Math.cos(angle-robot.rotation.y))*.12}
   robotLegs.forEach((l,i)=>l.rotation.x=walking?Math.sin(t*10+i*Math.PI)*.45:0);robotArms.forEach((a,i)=>a.rotation.x=walking?Math.sin(t*10+i*Math.PI)*.3:Math.sin(t*2+i)*.08);
   head.rotation.z=Math.sin(t*1.4)*.05;head.position.y=1.3+Math.sin(t*2)*.025;torso.position.y=.75+Math.sin(t*2)*.018;const blink=Math.sin(t*1.1)>.992?.1:1;eyeL.scale.y=eyeR.scale.y=blink;halo.rotation.z=t*.2;
   if(state.proposal)robotArms[1].rotation.z=-.9+Math.sin(t*6)*.25;
  }
  beacon.material=state.resolved?glow:goldGlow;beacon.scale.y=state.resolved?1:1+Math.sin(elapsed*2)*.12;
  Object.entries(stationRings).forEach(([id,ring])=>{ring.scale.setScalar(id===state.station?1.4+Math.sin(elapsed*2)*.15:1);(ring.material as THREE.MeshBasicMaterial).opacity=id===state.station?.6:.2});
  if(walkMode){const focus=robot.position.clone().add(new THREE.Vector3(0,1,0));const shift=focus.clone().sub(controls.target);camera.position.add(shift);controls.target.copy(focus)}
  const points:Record<Station,[number,number]>={evidence:[-5.7,2.7],assembly:[2.5,0],dispatch:[5.4,3.3]};
  nearby=(Object.entries(points).find(([,p])=>Math.hypot(robot.position.x-p[0],robot.position.z-p[1])<2)?.[0] as Station)||null;
  if(ms-lastTelemetry>150){lastTelemetry=ms;onTelemetry({x:robot.position.x,z:robot.position.z,nearby})}
  controls.update();renderer.render(scene,camera);
 }
 raf=requestAnimationFrame(animate);onReady();
 return {walk(enabled){walkMode=enabled;keys.clear();controls.minDistance=enabled?3:16;controls.maxDistance=enabled?12:48;controls.maxPolarAngle=enabled?1.48:1.25;controls.target.copy(enabled?robot.position.clone().add(new THREE.Vector3(0,1,0)):new THREE.Vector3(0,1,2));camera.position.copy(controls.target).add(enabled?new THREE.Vector3(0,3,6):new THREE.Vector3(20,21,29));controls.update();renderer.domElement.focus()},move(key,down){if(down)keys.add(key);else keys.delete(key)},interact,update(next){state=next;keys.clear();const pos={evidence:[-3.7,2.7],assembly:[.7,3.5],dispatch:[6,3.7]}[next.station];target.set(pos[0],0,pos[1])},home(){if(walkMode){controls.target.copy(robot.position).add(new THREE.Vector3(0,1,0));camera.position.copy(controls.target).add(new THREE.Vector3(0,3,6))}else{camera.position.set(20,21,29);controls.target.set(0,1,2)}controls.update()},dispose(){disposed=true;cancelAnimationFrame(raf);observer.disconnect();controls.dispose();renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointerup',click);renderer.domElement.removeEventListener('keydown',keydown);renderer.domElement.removeEventListener('keyup',keyup);renderer.domElement.removeEventListener('blur',blur);geometry.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());renderer.dispose();renderer.domElement.remove()}}
}
