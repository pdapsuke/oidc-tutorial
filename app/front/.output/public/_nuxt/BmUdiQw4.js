import{V as p,_ as u}from"./C2D9y0U9.js";import{d,r as f,L as _,o as h,m as a,M as m,A as k,q as g,t as w,z as y,x}from"./Qr9SC23P.js";import{u as C}from"./D7BPSamN.js";import"./DsrXlFoV.js";const T=x("div",null,"Please wait...",-1),b=d({__name:"callback",setup($){const r=f(null),c=_().query.code||"";c.toString();async function i(e){const s="http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/token",{clientId:n,redirectUri:l}=g().public,o=new URLSearchParams;o.append("grant_type","authorization_code"),o.append("code",e),o.append("client_id",`${n}`),o.append("redirect_uri",`${l}`);try{const t=await fetch(s,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:o.toString()});if(!t.ok)throw new Error("Failed to fetch access token");return t.json()}catch(t){r.value.error(`Error fetching access token: ${t}`),console.error("Error fetching access token:",t)}}return h(()=>{i(`${c}`).then(e=>{e?(console.log(e),C().login(e.access_token,e.refresh_token),a("/")):setTimeout(()=>{a("/login")},2e3)})}),(e,s)=>{const n=u;return w(),m(p,{class:"py-8 px-6 fillheight",fluid:""},{default:k(()=>[y(n,{ref_key:"alert",ref:r},null,512),T]),_:1})}}});export{b as default};
