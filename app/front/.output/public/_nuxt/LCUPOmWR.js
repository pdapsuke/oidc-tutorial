import{aT as i,m as s,aU as c}from"./Qr9SC23P.js";import{u}from"./D7BPSamN.js";import{u as l}from"./D0DvQDKK.js";const f=()=>({async validateAccessToken(){return l().get("validateAccessToken","/login/")}}),p=i(async(d,m)=>{let t,a;if(u().getToken("access")==null)return s("/login");let e;async function n(){const{data:r,error:o}=await f().validateAccessToken();!r.value||o.value?(console.error(o.value),e=!1):e=!0}if([t,a]=c(()=>n()),await t,a(),e==!1)return s("/login")});export{p as default};
