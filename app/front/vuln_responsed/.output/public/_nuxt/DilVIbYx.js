import{V as r,_ as c}from"./jeNWWo_C.js";import{u as l}from"./0_FZVDJP.js";import{u as i}from"./GpHrVUqc.js";import{d as u,r as m,o as _,m as a,L as f,A as p,t as d,z as h,x as k}from"./DAGB_px-.js";import"./ZTTGoMqa.js";const g=k("div",null,"Please wait...",-1),B=u({__name:"callback",setup(x){const s=m(null),t=l(),o=i("keycloak");return _(()=>{new Promise(e=>{t.login(o.value.token||"",o.value.refreshToken||""),e()}).then(()=>{console.log(t.authenticated("access")),setTimeout(()=>{a("/")},2e3)}).catch(e=>{console.error(e),setTimeout(()=>{a("/login")},2e3)})}),(e,v)=>{const n=c;return d(),f(r,{class:"py-8 px-6 fillheight",fluid:""},{default:p(()=>[h(n,{ref_key:"alert",ref:s},null,512),g]),_:1})}}});export{B as default};
