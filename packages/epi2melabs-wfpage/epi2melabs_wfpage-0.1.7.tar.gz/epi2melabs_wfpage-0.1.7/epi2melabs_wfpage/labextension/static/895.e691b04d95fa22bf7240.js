"use strict";(self.webpackChunk_epi2melabs_epi2melabs_wfpage=self.webpackChunk_epi2melabs_epi2melabs_wfpage||[]).push([[895],{2895:(e,t,n)=>{n.r(t),n.d(t,{default:()=>Q});var a=n(4674),o=n(6468),r=n(6148),l=n(2581);const i=new(n(9381).LabIcon)({name:"ui-components:labs",svgstr:'\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="42" height="51" viewBox="0 0 42 51">\n    <defs>\n        <filter id="Rectangle_1" x="0" y="0" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_2" x="0" y="24" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_3" x="0" y="12" width="28" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n    </defs>\n    <g id="Component_2_1" data-name="Component 2 – 1" transform="translate(9 6)">\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="24" height="9" rx="1" transform="translate(9 6)" fill="#08bbb2"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="24" height="9" rx="1" transform="translate(9 30)" fill="#0179a4"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="10" height="9" rx="1" transform="translate(9 18)" fill="#fccb10"/>\n        </g>\n    </g>\n  </svg>\n'});var s=n(6271),c=n.n(s),d=n(974),p=n(3839),m=n.n(p);const u={UNKNOWN:{name:"UNKNOWN",className:"grey"},LAUNCHED:{name:"LAUNCHED",className:"blue"},ENCOUNTERED_ERROR:{name:"ENCOUNTERED_ERROR",className:"orange"},COMPLETED_SUCCESSFULLY:{name:"COMPLETED_SUCCESSFULLY",className:"green"},TERMINATED:{name:"TERMINATED",className:"black"}},f=m()((({status:e,className:t})=>c().createElement("div",{className:`status-indicator ${t}`},c().createElement("div",{className:u[e].className}))))`
  > div {
    width: 18px;
    height: 18px;
    padding: 0;
    border-radius: 100%;
    line-height: 18px;
    text-align: center;
    font-size: 10px;
    color: white;
  }

  .blue {
    cursor: pointer;
    background-color: #005c75;
    box-shadow: 0 0 0 rgba(204, 169, 44, 0.4);
    animation: pulse-blue 2s infinite;
  }

  @keyframes pulse-blue {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
    }
  }

  .orange {
    cursor: pointer;
    background-color: #e34040;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-orange 2s infinite;
  }

  @keyframes pulse-orange {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
    }
  }

  .green {
    cursor: pointer;
    background-color: #17bb75;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-green 2s infinite;
  }

  @keyframes pulse-green {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
    }
  }

  .grey {
    background-color: #707070;
  }

  .black {
    background-color: black;
  }
`,g=m()((({className:e})=>c().createElement("span",{className:e},c().createElement("div",{className:"lds-ellipsis"},c().createElement("div",null),c().createElement("div",null),c().createElement("div",null),c().createElement("div",null)))))`
  display: flex;
  align-items: center;

  .lds-ellipsis {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 20px;
  }
  .lds-ellipsis div {
    position: absolute;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.1);
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
  }
  .lds-ellipsis div:nth-child(1) {
    left: 8px;
    animation: lds-ellipsis1 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(2) {
    left: 8px;
    animation: lds-ellipsis2 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(3) {
    left: 32px;
    animation: lds-ellipsis2 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(4) {
    left: 56px;
    animation: lds-ellipsis3 0.6s infinite;
  }
  @keyframes lds-ellipsis1 {
    0% {
      transform: scale(0);
    }
    100% {
      transform: scale(1);
    }
  }
  @keyframes lds-ellipsis3 {
    0% {
      transform: scale(1);
    }
    100% {
      transform: scale(0);
    }
  }
  @keyframes lds-ellipsis2 {
    0% {
      transform: translate(0, 0);
    }
    100% {
      transform: translate(24px, 0);
    }
  }
`;var b=n(6077),h=n(4982);async function x(e="",t={}){const n=h.ServerConnection.makeSettings(),a=b.URLExt.join(n.baseUrl,"epi2melabs-wfpage",e);let o;try{o=await h.ServerConnection.makeRequest(a,t,n)}catch(e){throw new h.ServerConnection.NetworkError(e)}let r=await o.text();if(r.length>0)try{r=JSON.parse(r)}catch(e){console.log("Not a JSON response body.",o)}if(!o.ok)throw new h.ServerConnection.ResponseError(o,r.message||r);return r}const w=m()((({className:e,docTrack:t,app:n})=>{const a=(0,d.useNavigate)(),o=(0,d.useParams)(),[r,l]=(0,s.useState)(""),[i,p]=(0,s.useState)(null),[m,u]=(0,s.useState)([]),[b,h]=(0,s.useState)(null),[w,E]=(0,s.useState)(null),[v,k]=(0,s.useState)("nextflow.stdout"),y=async e=>{const{curr_dir:t,base_dir:n}=await x("cwd");return`${n.replace(t,"").replace(/^\//,"")}/instances/${e.path.split("/").reverse()[0]}`},N=async()=>{const e=await x(`instances/${o.id}`);return p(e),l(e.status),e};(0,s.useEffect)((()=>{(async()=>{const e=await N();C(e),O(e,v)})();const e=setInterval((()=>N()),5e3);return()=>{clearInterval(e)}}),[]);const C=async e=>{if(e){const t=encodeURIComponent(`${e.path}/params.json`),{contents:n}=await x(`file/${t}?contents=true`);null!==n&&h(n)}},O=async(e,t)=>{if(e){const n=encodeURIComponent(`${e.path}/${t}`),{contents:a}=await x(`file/${n}?contents=true`);null!==a&&E(a)}},j=async e=>{if(e){const n=`${await y(e)}/output`;try{const e=await(await t.services.contents.get(n)).content.filter((e=>"directory"!==e.type));u(e)}catch(e){console.log("Instance outputs not available yet")}}},S=e=>{t.open(e)},R=e=>{e!==v&&(E(null),k(e))};(0,s.useEffect)((()=>{if(j(i),O(i,v),!["COMPLETED_SUCCESSFULLY","TERMINATED","ENCOUNTERED_ERROR"].includes(r)){const e=setInterval((()=>j(i)),1e4),t=setInterval((()=>O(i,v)),7500);return()=>{O(i,v),j(i),clearInterval(e),clearInterval(t)}}}),[r,v]);const z=async e=>{const t=await x(`instances/${o.id}`,{method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify({delete:e})});e&&t.deleted&&a("/workflows")};if(!i)return c().createElement("div",{className:`instance ${e}`},c().createElement("div",{className:"loading-screen"},c().createElement("p",null,"Instance data is loading... (If this screen persists, check connection to jupyterlab server and/or labslauncher)"),c().createElement(g,null)));const _=["LAUNCHED"].includes(r),I=(e=>{let t=null;return m.length&&m.forEach((n=>{n.name===`${e.workflow}-report.html`&&(t=n)})),t})(i);return c().createElement("div",{className:`instance ${e}`},c().createElement("div",{className:"instance-container"},c().createElement("div",{className:"instance-section instance-header"},c().createElement("div",{className:"instance-header-top"},c().createElement("h2",{className:"instance-workflow"},"Workflow: ",i.workflow),_?c().createElement("button",{onClick:()=>z(!1)},"Stop Instance"):""),c().createElement("h1",null,i.name),c().createElement("div",{className:"instance-details"},c().createElement("div",{className:"instance-status"},c().createElement(f,{status:r||"UNKNOWN"}),c().createElement("p",null,r)),c().createElement("p",null,"Created: ",i.created_at),c().createElement("p",null,"Updated: ",i.updated_at),c().createElement("p",null,"ID: ",o.id))),c().createElement("div",{className:"instance-section instance-params"},c().createElement("div",{className:"instance-section-header"},c().createElement("h2",null,"Instance params"),c().createElement("div",{className:"instance-section-header-controls"},c().createElement("button",{onClick:()=>{i&&a(`/workflows/${i.workflow}/${i.id}`)}},"Configure and rerun"))),c().createElement("div",{className:"instance-section-contents"},b&&b.length?c().createElement("ul",null,b.map((e=>c().createElement("li",null,c().createElement("span",null,e))))):c().createElement("div",null,c().createElement(g,null)))),c().createElement("div",{className:"instance-section instance-logs"},c().createElement("div",{className:"instance-section-header"},c().createElement("h2",null,"Instance logs"),c().createElement("div",{className:"instance-section-header-controls"},c().createElement("button",{onClick:()=>R("nextflow.stdout")},"Nextflow"),c().createElement("button",{onClick:()=>R("invoke.stdout")},"Invoke"))),c().createElement("div",{className:"instance-section-contents"},w&&w.length?c().createElement("ul",null,w.map((e=>c().createElement("li",null,c().createElement("span",null,e))))):c().createElement("div",null,c().createElement(g,null)))),c().createElement("div",{className:"instance-section instance-outputs"},c().createElement("div",{className:"instance-section-header"},c().createElement("h2",null,"Output files"),c().createElement("div",{className:"instance-section-header-controls"},I?c().createElement("button",{onClick:()=>S(I.path)},"Open report"):"",c().createElement("button",{onClick:()=>i?(async e=>{const t=await y(e);n.commands.execute("filebrowser:go-to-path",{path:t})})(i):""},"Open folder"))),c().createElement("div",{className:"instance-section-contents"},m.length?c().createElement("ul",null,m.map((e=>c().createElement("li",null,c().createElement("button",{onClick:()=>S(e.path)},e.name))))):c().createElement("div",{className:"instance-section-contents"},"No outputs yet..."))),c().createElement("div",{className:"instance-section instance-delete"},c().createElement("div",{className:"instance-section-header"},c().createElement("h2",null,"Danger zone")),c().createElement("div",{className:"instance-section-contents"},c().createElement("div",{className:_?"inactive":"active"},c().createElement("button",{onClick:()=>_?null:z(!0)},"Delete Instance"))))))}))`
  background-color: #f6f6f6;

  .loading-screen {
    display: flex;
    justify-content: center;
    min-height: calc(100vh - 100px);
    align-items: center;
    flex-direction: column;
  }

  .loading-screen p {
    text-align: center;
    max-width: 600px;
    padding-bottom: 15px;
  }

  .instance-container {
    padding: 50px 0 100px 0 !important;
  }

  .instance-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .instance-section-header {
    padding-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-section-header-controls button {
    cursor: pointer;
    padding: 10px 15px;
    margin-left: 10px;
    border: none;
    color: rgba(0, 0, 0, 0.3);
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: rgb(239, 239, 239);
  }

  .instance-section-header-controls button:hover {
    color: #005c75;
  }

  .instance-section-contents {
    padding: 15px;
    border-radius: 4px;
  }

  .instance-header-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  .instance-header-top button {
    cursor: pointer;
    padding: 8px 15px;
    border: 1px solid #e34040;
    color: #e34040;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .instance-header-top button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-outputs .instance-section-contents,
  .instance-params .instance-section-contents,
  .instance-logs .instance-section-contents {
    background-color: #f6f6f6;
    font-size: 12px;
    font-family: monospace;
    overflow: auto;
    text-overflow: initial;
    max-height: 500px;
    white-space: pre;
    color: black;
    border-radius: 4px;
  }

  .instance-outputs .instance-section-contents button,
  .instance-params .instance-section-contents span,
  .instance-logs .instance-section-contents span {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-outputs li {
    margin: 0 0 5px 0;
    display: flex;
    background-color: #f6f6f6;
  }

  .instance-outputs .instance-section-contents button {
    width: 100%;
    text-align: left;
    padding: 5px 0 10px 0;
    font-size: 12px;
    font-family: monospace;
    border: none;
    outline: none;
    background: transparent;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    cursor: pointer;
  }

  .instance-outputs .instance-section-contents > ul > li:last-child button {
    border-bottom: none;
    padding-bottom: 0;
  }

  .instance-outputs .instance-section-contents button:hover {
    color: #005c75;
  }

  .instance-delete .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-delete button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }
  .instance-delete .active button {
    border: 1px solid #e34040;
    color: #e34040;
  }
  .instance-delete .active button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }
`;var E=n(7118),v=n.n(E),k=n(1735),y=n(1956),N=n(7646),C=n(1054);const O=m()((({id:e,label:t,format:n,description:a,defaultValue:o,error:r,onChange:l,className:i})=>{const[d,p]=(0,s.useState)(o);return c().createElement("div",{className:`BooleanInput ${i} ${d?"checked":"unchecked"}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,className:"boolInput",type:"checkbox",defaultChecked:o,onChange:t=>{p(!!t.target.checked),l(e,n,!!t.target.checked)}}),c().createElement("span",null,c().createElement(y.FontAwesomeIcon,{icon:d?C.faCheck:C.faTimes}))),r.length?c().createElement("div",{className:"error"},r.map((e=>c().createElement("p",null,"Error: ",e)))):"")}))`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  label {
    position: relative;
    display: inline-block;
  }

  label span {
    box-sizing: border-box;
    min-width: 75px;
    margin: 0;
    padding: 15px 25px;
    display: block;

    text-align: center;
    font-size: 16px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    cursor: pointer;
    transition: 0.2s ease-in-out all;
    -moz-appearance: textfield;
  }

  input {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  label span:hover {
    border: 1px solid #005c75;
  }

  input:checked + span {
    background-color: #005c75;
    color: white;
  }
`,j=m()((({id:e,label:t,format:n,description:a,defaultValue:o,choices:r,error:l,onChange:i,className:s})=>c().createElement("div",{className:`SelectInput ${s}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("select",{id:e,onChange:t=>i(e,n,t.target.value)},o?"":c().createElement("option",{className:"placeholder",selected:!0,disabled:!0,hidden:!0,value:"Select an option"},"Select an option"),r.map((e=>c().createElement("option",{key:e.label,selected:!(e.value!==o),value:e.value},e.label))))),l.length?c().createElement("div",{className:"error"},l.map((e=>c().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  label {
    display: flex;
  }

  select {
    margin: 0;
    min-width: 50%;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  select:hover {
    border: 1px solid #005c75;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,S=m()((({id:e,label:t,format:n,description:a,defaultValue:o,minLength:r,maxLength:l,pattern:i,error:s,onChange:d,className:p})=>c().createElement("div",{className:`TextInput ${p}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,type:"text",placeholder:"Enter a value",defaultValue:o,pattern:i,minLength:r,maxLength:l,onChange:t=>d(e,n,t.target.value)})),s.length?c().createElement("div",{className:"error"},s.map((e=>c().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  label {
    display: flex;
  }

  input {
    margin: 0;
    min-width: 50%;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  input:hover {
    border: 1px solid #005c75;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,R=e=>{let t;switch(e){case"file-path":t="file";break;case"directory-path":t="directory";break;default:t="path"}return t},z=m()((({id:e,label:t,format:n,description:a,defaultValue:o,pattern:r,error:l,onChange:i,className:d})=>{const[p,m]=(0,s.useState)(""),[u,f]=(0,s.useState)(null),[g,b]=(0,s.useState)("/"),[h,w]=(0,s.useState)([]),[E,v]=(0,s.useState)(!1),k=(0,s.useRef)(null),N=R(n);let O=[];l.length&&(O=[...l]),u&&(O=[u,...O]),(0,s.useEffect)((()=>{(async()=>{const e=await(async e=>{const t=encodeURIComponent(e);return(await x(`directory/${t}?contents=true`,{method:"GET"})).contents})(g);e&&w(e.filter((e=>!("directory"===N&&!e.isdir))).sort(((e,t)=>e.name.localeCompare(t.name))))})()}),[g]);return c().createElement("div",{id:e,className:`FileInput ${d}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("div",{className:"file-input-container"},c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,ref:k,type:"text",placeholder:"Enter a value",defaultValue:o,pattern:r,onChange:t=>{(async(t,n)=>{if([/http:\/\//,/https:\/\//,/^$/,/s3:\/\//].some((e=>e.test(t))))return f(null),void i(e,n,t);const a=encodeURIComponent(t),o=await x(`${n}/${a}`,{method:"GET"});if(!o.exists)return f(o.error),void i(e,n,"");f(null),i(e,n,t)})(t.target.value,R(n))}})),c().createElement("button",{className:"file-browser-toggle",onClick:()=>v(!E)},"Browse")),E?c().createElement("div",{className:"file-browser"},c().createElement("div",{className:"file-browser-contents"},c().createElement("div",{className:"file-browser-path file-browser-close"},c().createElement("button",{onClick:()=>v(!1)},c().createElement(y.FontAwesomeIcon,{icon:C.faTimes}),"Close")),c().createElement("ul",null,"/"!==g?c().createElement("li",{className:"file-browser-path file-browser-back"},c().createElement("button",{onClick:()=>b((e=>{const t=e.split("/").slice(0,-1).join("/");return""===t?"/":t})(g))},c().createElement(y.FontAwesomeIcon,{icon:C.faLevelUpAlt}),"Go Up")):"",h.map((e=>c().createElement("li",{className:"file-browser-path "+(p===e.path?"selected":"")},c().createElement("button",{onClick:()=>((e,t,n)=>{if(e===p)return;if(!t&&"directory"===N)return;if(t&&"file"===N)return;m(e);const a=n.current;if(a){((e,t)=>{var n,a;const o=null===(n=Object.getOwnPropertyDescriptor(e,"value"))||void 0===n?void 0:n.set,r=Object.getPrototypeOf(e),l=null===(a=Object.getOwnPropertyDescriptor(r,"value"))||void 0===a?void 0:a.set;o&&o!==l?null==l||l.call(e,t):null==o||o.call(e,t)})(a,e);const t=new Event("input",{bubbles:!0});a.dispatchEvent(t)}})(e.path,e.isdir,k),onDoubleClick:()=>{return t=e.path,void(e.isdir&&b(t));var t}},c().createElement(y.FontAwesomeIcon,{icon:e.isdir?C.faFolder:C.faFile}),e.name))))))):"",O.length?c().createElement("div",{className:"error"},O.map((e=>c().createElement("p",null,"Error: ",e)))):"")}))`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  .file-input-container {
    max-width: 700px;
    display: flex;
    border: 1px solid transparent;
    border-radius: 4px;
  }

  .file-input-container:hover {
    border: 1px solid #005c75;
  }

  label {
    width: 100%;
    display: flex;
  }

  input {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  input,
  .file-browser-toggle {
    margin: 0;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    color: black;
    border: 0;
    background-color: #f3f3f3;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .file-browser-toggle {
    line-height: 1.2em;
    border-radius: 0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    border-left: 1px solid #ccc;
    cursor: pointer;
  }

  .file-browser-toggle:hover {
    background-color: #005c75;
    color: white;
  }

  .file-browser {
    position: fixed;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    top: 0px;
    left: 0px;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.35);
    /* max-height: 300px; */
    /* margin: 10px 0 0 0; */
    /* border-radius: 4px; */
    /* background-color: #f3f3f3; */
    /* overflow-y: auto; */
  }

  .file-browser-contents {
    width: 900px;
    /* max-height: 500px; */
    border-radius: 4px;
    overflow-y: auto;
    /* background-color: #f3f3f3; */
    background-color: rgba(255, 255, 255, 0.6);
  }

  .file-browser-contents > ul {
    max-height: 500px;
    overflow-y: auto;
  }

  .file-browser-path button {
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;
    display: flex;
    align-items: center;
    text-align: left;
    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    outline: none;
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #f4f4f4;
    cursor: pointer;
  }

  .file-browser-path:nth-child(even) button {
    background-color: #f2f2f2;
  }

  .file-browser-path:last-child button {
    border-bottom: none;
  }

  .file-browser-path button:hover {
    color: #005c75;
  }

  .file-browser-path.selected button {
    background-color: #005c75;
    color: white;
  }

  .file-browser-path.selected button:hover {
    color: white;
  }

  .file-browser-back {
    font-style: italic;
    background-color: rgba(0, 0, 0, 0.1);
  }

  .file-browser-close {
    background-color: transparent;
  }

  .file-browser-path.file-browser-close button {
    display: flex;
    justify-content: end;
    border-radius: 0;
    border-bottom: 2px solid #ccc;
    color: #333;
  }

  .file-browser-path.file-browser-close:hover button {
    background-color: #f2f2f2;
    color: #333;
  }

  .file-browser-path button svg {
    padding: 0 10px 0 0;
    color: lightgray;
    font-size: 1.5em;
  }

  .file-browser-path button:hover svg {
    color: #005c75;
  }

  .file-browser-path.selected button:hover svg {
    color: lightgray;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,_=m()((({id:e,label:t,format:n,description:a,defaultValue:o,min:r,max:l,error:i,onChange:s,className:d})=>c().createElement("div",{className:`NumInput ${d}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,type:"number",defaultValue:o,min:r,max:l,onChange:t=>s(e,n,Number(t.target.value))})),i.length?c().createElement("div",{className:"error"},i.map((e=>c().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    color: black;
  }

  p {
    padding: 0 0 10px 0;
    font-size: 13px;
    color: #333;
  }

  label {
    display: flex;
  }

  input {
    margin: 0;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  input:hover {
    border: 1px solid #005c75;
  }

  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }
`,I=(e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}),$=m()((({id:e,schema:t,error:n,onChange:a,className:o})=>c().createElement("div",{className:`parameter ${o}`},((e,t,n,a)=>(e=>"boolean"===e.type)(t)?c().createElement(O,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}))(e,t),{error:n,onChange:a})):(e=>!!e.enum)(t)?c().createElement(j,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,choices:t.enum.map((e=>({value:e,label:e})))}))(e,t),{error:n,onChange:a})):(e=>!("string"!==e.type||!["file-path","directory-path","path"].includes(e.format)))(t)?c().createElement(z,Object.assign({},I(e,t),{error:n,onChange:a})):(e=>"string"===e.type&&!e.enum)(t)?c().createElement(S,Object.assign({},I(e,t),{error:n,onChange:a})):(e=>!!["integer","number"].includes(e.type))(t)?c().createElement(_,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,min:t.minimum,max:t.maximum}))(e,t),{error:n,onChange:a})):c().createElement(S,Object.assign({},I(e,t),{error:n,onChange:a})))(e,t,n,a))))`
  padding: 25px 0;
  border-top: 1px solid #e5e5e5;
`,L=m()((({title:e,fa_icon:t,properties:n,errors:a,onChange:o,className:r})=>{const[l,i]=(0,s.useState)(!1),d=0===Object.keys(a).length;k.library.add(C.fas,N.fab);const p=null==t?void 0:t.split(" ")[1],m=null==t?void 0:t.split(" ")[0],u=(null==p?void 0:p.startsWith("fa-"))?p.split("fa-")[1]:p;return c().createElement("div",{className:`parameter-section ${r}`},c().createElement("div",{className:"parameter-section-container "+(d?"valid":"")},c().createElement("button",{className:"parameter-section-toggle",onClick:()=>i(!l)},c().createElement("h3",null,"string"==typeof t?c().createElement(y.FontAwesomeIcon,{icon:[m,u]}):"",e),c().createElement("div",{className:"parameter-section-toggle-controls"},d?c().createElement("div",{className:"parameter-section-toggle-errors valid"},c().createElement(y.FontAwesomeIcon,{icon:C.faCheckCircle})):c().createElement("div",{className:"parameter-section-toggle-errors invalid"},c().createElement("p",null,Object.keys(a).length),c().createElement(y.FontAwesomeIcon,{icon:C.faTimesCircle})),c().createElement(y.FontAwesomeIcon,{icon:l?C.faCaretUp:C.faCaretDown}))),c().createElement("ul",{className:"parameter-section-items "+(l?"open":"closed")},Object.entries(n).map((([e,t])=>c().createElement("li",{className:"parameter"},c().createElement($,{id:e,schema:t,error:a[e]||[],onChange:o})))))))}))`
  .parameter-section-toggle {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    padding: 15px;
    justify-content: space-between;
    align-items: center;
    border: none;
    outline: none;
    background: transparent;
    cursor: pointer;
  }

  .parameter-section-toggle h3 svg {
    margin-right: 15px;
  }

  .parameter-section-toggle h3 {
    font-size: 16px;
    font-weight: normal;
    color: #e34040;
  }

  .parameter-section-container.valid .parameter-section-toggle h3 {
    color: black;
  }

  .parameter-section-toggle-controls {
    display: flex;
  }

  .parameter-section-toggle-errors {
    margin-right: 15px;
    display: flex;
    align-items: center;
  }

  .parameter-section-toggle-errors svg {
    width: 15px;
    height: 15px;
    margin-left: 5px;
  }

  .parameter-section-toggle-errors.valid svg {
    color: #1d9655;
  }

  .parameter-section-toggle-errors.invalid svg {
    color: #e34040;
  }

  .parameter-section-toggle-errors.invalid p {
    font-weight: bold;
    color: #e34040;
  }

  .parameter-section-items {
    display: block;
    padding: 15px 15px 0 15px;
    transition: 0.2s ease-in-out all;
  }

  .parameter-section-items.closed {
    display: none;
  }

  .parameter-section-items.open {
    padding-top: 15px;
    display: block;
  }
`;const T=m()((({className:e})=>{const t=(0,d.useParams)(),n=(0,d.useNavigate)(),[a,o]=(0,s.useState)(),[r,l]=(0,s.useState)({}),[i,p]=(0,s.useState)(!1),[m,u]=(0,s.useState)({}),[f,g]=(0,s.useState)([]),[b,h]=(0,s.useState)(null),[w,E]=(0,s.useState)();(0,s.useEffect)((()=>{(async()=>{const e=await(async()=>await x(`workflows/${t.name}`))();o(e);const n=await(async e=>{if(e){const{path:t}=await x(`instances/${e}`),n=encodeURIComponent(`${t}/params.json`),{exists:a,contents:o}=await x(`file/${n}?contents=true`);return a?JSON.parse(o.join("")):null}})(t.instance_id);l(n||e.defaults);const a=Object.values(e.schema.definitions).map((e=>{return Object.assign(Object.assign({},e),{properties:(t=e.properties,Object.entries(t).filter((([e,t])=>!t.hidden&&"out_dir"!==e)).reduce(((e,t)=>Object.assign({[t[0]]:t[1]},e)),{}))});var t})).filter((e=>0!==Object.keys(e.properties).length));if(n){const e=((e,t)=>e.map((e=>Object.assign(Object.assign({},e),{properties:Object.entries(e.properties).reduce(((e,n)=>Object.assign({[n[0]]:Object.assign(Object.assign({},n[1]),{default:t[n[0]]||n[1].default})},e)),{})}))))(a,n);g(e)}else g(a)})()}),[]);const k=(e,t,n)=>{if(""!==n)l(Object.assign(Object.assign({},r),{[e]:n}));else{const t=r,n=e,a=(t[n],function(e,t){var n={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&t.indexOf(a)<0&&(n[a]=e[a]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var o=0;for(a=Object.getOwnPropertySymbols(e);o<a.length;o++)t.indexOf(a[o])<0&&Object.prototype.propertyIsEnumerable.call(e,a[o])&&(n[a[o]]=e[a[o]])}return n}(t,["symbol"==typeof n?n:n+""]));l(a)}};return(0,s.useEffect)((()=>{if(a){const{valid:e,errors:t}=function(e,t){const n=new(v())({allErrors:!0,strictSchema:!1,verbose:!0}).compile(t);return{valid:n(e),errors:n.errors}}(r,a.schema);u(e?{}:(e=>{const t={};return e.forEach((e=>{Object.values(e.params).forEach((n=>{t[n]=[...t[n]||[],e.message||""]}))})),t})(t)),p(e)}}),[r]),a?c().createElement("div",{className:`workflow ${e}`},c().createElement("div",{className:"workflow-container"},c().createElement("div",{className:"workflow-section workflow-header"},c().createElement("h1",null,"Workflow: ",t.name),c().createElement("div",{className:"workflow-description"},c().createElement("div",null,a.desc)),c().createElement("div",{className:"workflow-details"},c().createElement("div",null,"Version ",a.defaults.wfversion))),c().createElement("div",{className:"workflow-section workflow-name"},c().createElement("h2",null,"1. Name workflow run"),c().createElement("div",{className:"workflow-section-contents"},c().createElement("input",{id:"worflow-name-input",type:"text",placeholder:"E.g. my_experiment (Between 10 and 50 characters).",onChange:e=>{var t;""===(t=e.target.value)||t.length>50||t.length<10?E(null):E(t)},maxLength:50}))),c().createElement("div",{className:"workflow-section workflow-parameter-sections"},c().createElement("h2",null,"2. Choose parameters"),c().createElement("div",{className:"workflow-section-contents"},c().createElement("ul",null,f.map((e=>{return c().createElement("li",null,c().createElement(L,{title:e.title,description:e.description,fa_icon:e.fa_icon,properties:e.properties,errors:(t=e.properties,n=m,Object.keys(t).reduce(((e,t)=>Object.prototype.hasOwnProperty.call(n,t)?Object.assign(Object.assign({},e),{[t]:n[t]}):e),{})),onChange:k}));var t,n}))))),c().createElement("div",{className:"workflow-section workflow-launch-control"},c().createElement("h2",null,"3. Launch workflow"),c().createElement("div",{className:"workflow-section-contents"},c().createElement("div",{className:"launch-control "+(i&&w?"active":"inactive")},c().createElement("button",{onClick:()=>(async()=>{if(!i||!w)return;const{created:e,instance:a,error:o}=await x("instances",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({workflow:t.name,params:r},w?{name:w}:{}))});o&&h(o),e&&n(`/instances/${a.id}`)})()},"Run command"),b?c().createElement("div",{className:"error"},c().createElement("p",null,"Error: ",b)):""))))):c().createElement(c().Fragment,null)}))`
  background-color: #f6f6f6;

  .workflow-container {
    padding: 0 0 100px 0 !important;
  }

  .workflow-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .workflow-section > h2 {
    padding-bottom: 15px;
  }

  .workflow-header {
    width: 100%;
    margin: 0 auto 50px auto;
    max-width: 100%;
    box-shadow: none;
    padding: 75px 0;
    text-align: center;
  }

  .workflow-description div {
    letter-spacing: 0em;
    font-size: 14px;
    text-transform: none;
    padding-bottom: 15px;
    max-width: 700px;
    line-height: 1.4em;
    text-align: center;
    margin: 0 auto;
    color: #a0a0a0;
  }

  .workflow-details div {
    /* color: #333;
    font-weight: normal;
    font-size: 14px; */
    padding-bottom: 5px;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    letter-spacing: 0.05em;
  }

  .workflow-parameter-sections .workflow-section-contents > ul > li {
    background-color: #fafafa;
    padding: 15px;
    margin: 0 0 15px 0;
    border-radius: 4px;
  }

  .workflow-name .workflow-section-contents {
    border-radius: 4px;
    background-color: #f6f6f6;
  }

  .workflow-name input {
    margin: 0;
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .workflow-name input:hover {
    border: 1px solid #005c75;
  }

  .workflow-launch-control .workflow-section-contents {
    padding: 15px;
    border-radius: 4px;
    background-color: #f6f6f6;
  }

  .workflow-launch-control button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .workflow-launch-control .active button {
    border: 1px solid #1d9655;
    color: #1d9655;
  }
  .workflow-launch-control .active button:hover {
    cursor: pointer;
    background-color: #1d9655;
    color: white;
  }
  .workflow-launch-control .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;var U=n(5131),D=n.n(U);const F=m()((({path:e,onClick:t,docTrack:n,buttonText:a,className:o})=>{const[r,l]=(0,s.useState)([]),i=async()=>{l(await d(e,n))};(0,s.useEffect)((()=>{i();const e=e=>{i()},t=n.services.contents.fileChanged;return t.connect(e),()=>{t.disconnect(e)}}),[]);const d=async(e,t)=>(await(async(e,t)=>(await Promise.all((await t.services.contents.get(e)).content.map((e=>"directory"===e.type?null:e)))).filter((e=>!!e)))(e,t)).filter((e=>e.path.endsWith(".ipynb"))).map((e=>({name:e.name,path:e.path,last_modified:e.last_modified})));return 0===r.length?c().createElement("div",{className:`notebooks-list empty ${o}`},c().createElement("div",{className:"empty"},c().createElement(y.FontAwesomeIcon,{icon:C.faBookOpen}),c().createElement("h2",null,"No notebooks to display."))):c().createElement("div",{className:`notebooks-list ${o}`},c().createElement("ul",null,r.map((e=>{return c().createElement("li",null,c().createElement("div",{className:"notebook"},c().createElement("div",null,c().createElement("div",{className:"notebook-header"},c().createElement("span",null,"Last modified: ",(o=e.last_modified,D()(o).format("MMMM Do YYYY, h:mm:ss a"))),c().createElement("h3",null,(e=>e.split("/").reverse()[0].split("_").join(" ").split(".ipynb").join(""))(e.path))),c().createElement("div",{className:"notebook-buttons"},c().createElement("button",{onClick:()=>t(e.path,n)},a)))));var o}))))}))`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  .notebook {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  .notebook span {
    color: #333;
  }
  .notebook-header span {
    letter-spacing: 0.05em;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    padding-bottom: 5px;
  }
  .notebook-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
  }
  .notebook-header h3 {
    font-size: 18px;
    padding: 10px 0 15px 0;
  }
  .notebook-buttons {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .notebook-link {
    color: #1d9655;
  }
  .notebook-buttons button {
    padding: 15px 25px;
    border: 1px solid #1d9655;
    color: #1d9655;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    background-color: transparent;
    transition: 0.2s ease-in-out all;
  }
  .notebook-buttons button:hover {
    background-color: #1d9655;
    color: white;
    cursor: pointer;
  }
`,A=m()((({className:e,docTrack:t,templateDir:n,workDir:a})=>c().createElement("div",{className:`index-panel ${e}`},c().createElement("div",{className:"index-panel-intro"},c().createElement("h1",null,"EPI2ME Labs Notebooks"),c().createElement("p",null,"EPI2ME Labs maintains a growing collection of notebooks on a range of topics from basic quality control to genome assembly. These are free and open to use by anyone. Browse the list below and get started.")),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Recent notebooks"),c().createElement(F,{path:a,onClick:(e,t)=>{t.open(e)},docTrack:t,buttonText:"Open notebook"})),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Available notebooks"),c().createElement(F,{path:n,onClick:async(e,t)=>{await t.copy(e,a).then((n=>{t.open(e)}))},docTrack:t,buttonText:"Copy and open"})))))`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .index-panel-intro {
    padding: 75px 50px 75px 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .index-panel-intro h1 {
    padding: 25px 0;
    text-align: center;
  }

  .index-panel-intro p {
    max-width: 800px;
    text-align: center;
    font-size: 16px;
    line-height: 1.7em;
  }

  .index-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`,P=m()((({className:e})=>{const[t,n]=(0,s.useState)([]);return(0,s.useEffect)((()=>{(async()=>{const e=await x("workflows");n(Object.values(e))})()}),[]),0===t.length?c().createElement("div",{className:`workflows-list empty ${e}`},c().createElement("div",{className:"empty"},c().createElement("h2",null,c().createElement(y.FontAwesomeIcon,{icon:C.faFolderOpen}),"No workflows installed."))):c().createElement("div",{className:`workflows-list ${e}`},c().createElement("ul",null,t.map((e=>c().createElement("li",null,c().createElement("div",{className:"workflow"},c().createElement("div",null,c().createElement("div",{className:"workflow-header"},c().createElement("span",null,"Version ",e.defaults.wfversion),c().createElement("h3",null,e.name)),c().createElement("div",{className:"workflow-buttons"},c().createElement("a",{className:"workflow-url",href:e.url},"Github"),c().createElement(d.Link,{className:"workflow-link",to:`/workflows/${e.name}`},c().createElement("div",null,"Open workflow"))))))))))}))`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  .workflow {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }

  .workflow span {
    color: #333;
  }

  .workflow-header span {
    letter-spacing: 0.05em;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    padding-bottom: 5px;
  }
  .workflow-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
  }
  .workflow-buttons {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .workflow-link {
    color: #1d9655;
  }
  .workflow-buttons div {
    padding: 15px 25px;
    border: 1px solid #1d9655;
    color: #1d9655;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .workflow-buttons div:hover {
    background-color: #1d9655;
    color: white;
  }
`,M=m()((({className:e,onlyTracked:t})=>{const[n,a]=(0,s.useState)([]),[o,r]=(0,s.useState)([]);(0,s.useEffect)((()=>{(async()=>{const e=await x("instances"),t=Object.values(e),n=t.filter((e=>["UNKNOWN","LAUNCHED"].includes(e.status)));a(t),r(n)})()}),[]),(0,s.useEffect)((()=>{const e=setInterval((()=>(async()=>{const e=await Promise.all(o.map((async e=>await x(`instances/${e.id}`,{method:"GET",headers:{"Content-Type":"application/json"}}))));r(e)})()),5e3);return()=>{clearInterval(e)}}),[o]);const l=(t?o:n).sort(((e,t)=>e.created_at<t.created_at?1:e.created_at>t.created_at?-1:0));return 0===l.length?c().createElement("div",{className:`instance-list ${e}`},c().createElement("div",{className:"empty"},c().createElement("div",null,c().createElement("h2",null,c().createElement(y.FontAwesomeIcon,{icon:C.faHistory}),"No workflows instances yet...")))):c().createElement("div",{className:`instance-list ${e}`},c().createElement("ul",null,l.map((e=>c().createElement("li",null,c().createElement("div",{className:"instance"},c().createElement("div",null,c().createElement("div",{className:"instance-header"},c().createElement("h2",null,e.name),c().createElement("span",null,e.workflow," | Created: ",e.created_at)),c().createElement("div",{className:"instance-bar"},c().createElement("div",{className:"instance-status"},c().createElement(f,{status:e.status}),c().createElement("p",null,e.status)),c().createElement(d.Link,{className:"instance-link",to:`/instances/${e.id}`},c().createElement("div",null,"View Instance"))))))))))}))`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .empty p {
    padding-bottom: 10px;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }
  .instance {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }
  .instance span {
    color: #333;
  }
  .instance-header h2 {
    padding: 5px 0;
  }
  .instance-header span {
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    letter-spacing: 0.05em;
  }
  .instance-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
    padding-bottom: 15px;
  }
  .instance-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .instance-status {
    display: flex;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    align-items: center;
  }
  .instance-status p {
    padding-left: 15px;
  }
  .instance-link {
    color: #005c75;
  }
  .instance-link div {
    padding: 15px 25px;
    border: 1px solid #005c75;
    color: #005c75;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .instance-link div:hover {
    background-color: #005c75;
    color: white;
  }
`,G=M,B=m()((({className:e})=>c().createElement("div",{className:`index-panel ${e}`},c().createElement("div",{className:"index-panel-intro"},c().createElement("h1",null,"EPI2ME Labs Workflows"),c().createElement("p",null,"EPI2ME Labs is developing a range of workflows covering a variety of everyday bioinformatics needs. Like the notebooks, these are free and open to use by anyone.")),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Available workflows"),c().createElement(P,null)),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Workflow instances"),c().createElement(G,null)))))`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .index-panel-intro {
    padding: 75px 50px 75px 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .index-panel-intro h1 {
    padding: 25px 0;
    text-align: center;
  }

  .index-panel-intro p {
    max-width: 800px;
    text-align: center;
    font-size: 16px;
    line-height: 1.7em;
  }

  .index-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`,V=()=>{const e=new Blob(['\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="148" height="198" viewBox="0 0 148 198">\n    <defs>\n      <filter id="Rectangle_1" x="0" y="0" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_2" x="0" y="130" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_3" x="0" y="65" width="73" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n    </defs>\n    <g id="Component_1_2" data-name="Component 1 – 2" transform="translate(9 6)">\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="130" height="50" rx="5" transform="translate(9 6)" fill="#08bbb2"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="130" height="50" rx="5" transform="translate(9 136)" fill="#0179a4"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="55" height="50" rx="5" transform="translate(9 71)" fill="#fccb10"/>\n      </g>\n    </g>\n  </svg>\n'],{type:"image/svg+xml"}),t=URL.createObjectURL(e);return c().createElement("div",{className:"labsLogo"},c().createElement("img",{src:t,alt:"The EPI2ME Labs logo"}))},W=m()((({className:e})=>c().createElement("header",{className:`header ${e}`},c().createElement("div",{className:"header-section left-navigation"},c().createElement(d.Link,{to:"/notebooks"},"Notebooks"),c().createElement(d.Link,{to:"/workflows"},"Workflows")),c().createElement("div",{className:"header-section center-navigation"},c().createElement(d.Link,{to:"/"},c().createElement(V,null))),c().createElement("div",{className:"header-section right-navigation"},c().createElement("a",{href:"https://labs.epi2me.io/"},"Labs Blog")))))`
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  background-color: #00485b;
  color: white;

  .labsLogo img {
    width: 25px;
  }

  .header-section {
    width: calc(100% / 3);
    display: flex;
    align-items: center;
  }

  .left-navigation a {
    padding-right: 25px;
  }

  .center-navigation {
    justify-content: center;
  }

  .right-navigation {
    justify-content: right;
  }

  a {
    font-weight: bold;
  }
`,Y=m()((({className:e})=>c().createElement("footer",{className:`footer ${e}`},c().createElement("p",null,"@2008 - ",D()().year()," Oxford Nanopore Technologies. All rights reserved"))))`
  width: 100%;
  padding: 25px;
  text-align: center;
  box-sizing: border-box;
`,H=m().div``;class J extends r.ReactWidget{constructor(e,t,n){super(),this.app=e,this.docTrack=t,this.settings=n,this.addClass("jp-ReactWidget"),this.addClass("epi2melabs-wfpage-widget")}render(){return c().createElement(d.MemoryRouter,null,c().createElement(H,null,c().createElement("main",{style:{position:"relative"}},c().createElement(W,null),c().createElement("div",null,c().createElement(d.Routes,null,c().createElement(d.Route,{path:"/workflows/:name"},c().createElement(d.Route,{path:":instance_id",element:c().createElement(T,null)}),c().createElement(d.Route,{path:"",element:c().createElement(T,null)})),c().createElement(d.Route,{path:"/workflows",element:c().createElement(B,null)}),c().createElement(d.Route,{path:"/instances/:id",element:c().createElement(w,{docTrack:this.docTrack,app:this.app})}),c().createElement(d.Route,{path:"/notebooks",element:c().createElement(A,{docTrack:this.docTrack,templateDir:this.settings.get("template_dir").composite,workDir:this.settings.get("working_dir").composite})}),c().createElement(d.Route,{path:"/",element:c().createElement(A,{docTrack:this.docTrack,templateDir:this.settings.get("template_dir").composite,workDir:this.settings.get("working_dir").composite})}))),c().createElement(Y,null))))}}const K="@epi2melabs/epi2melabs-wfpage:plugin",q="create-epi2me-labs-launcher",Q={id:K,autoStart:!0,requires:[l.ILauncher,a.ISettingRegistry,o.IDocumentManager],activate:(e,t,n,a)=>{const{commands:o,shell:l}=e,s=(t,n,a)=>{const o=new J(e,n,a),l=new r.MainAreaWidget({content:o});l.title.label="EPI2ME Labs",t.add(l,"main")};Promise.all([e.restored,n.load(K)]).then((([,e])=>{o.addCommand(q,{caption:"Create an EPI2ME Labs launcher",label:"EPI2ME Labs",icon:i,execute:()=>s(l,a,e)}),s(l,a,e),t&&t.add({command:q,category:"EPI2ME Labs"})}))}}}}]);