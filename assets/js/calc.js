/* Easy.Finance — calculator engine (no dependencies) */
(function(){
  "use strict";
  var CUR = {USD:{l:"en-US",f:1},CAD:{l:"en-CA",f:1},EUR:{l:"de-DE",f:1},GBP:{l:"en-GB",f:1},AUD:{l:"en-AU",f:1},INR:{l:"en-IN",f:80},LKR:{l:"en-LK",f:300}};
  function guessCur(){
    var c=(window.EF_CONFIG||{}).currency; if(c&&CUR[c])return c;
    try{var s=localStorage.getItem("ef-cur");if(s&&CUR[s])return s}catch(e){}
    var l=(navigator.language||"en-US");
    if(/-IN$/.test(l))return "INR"; if(/-CA$/.test(l))return "CAD"; if(/-GB$/.test(l))return "GBP";
    if(/-AU$/.test(l))return "AUD"; if(/-LK$/.test(l))return "LKR";
    if(/^(de|fr|es|it|nl|pt)-/.test(l)&&!/-(BR|CA)$/.test(l))return "EUR"; return "USD";
  }
  var cur=guessCur();
  function money(v,dec){
    try{return new Intl.NumberFormat(CUR[cur].l,{style:"currency",currency:cur,maximumFractionDigits:dec||0}).format(v)}
    catch(e){return cur+" "+Math.round(v).toLocaleString()}
  }
  function num(v,d){return Number(v).toLocaleString(undefined,{maximumFractionDigits:d==null?1:d})}
  function pmt(r,n,p){return r===0?p/n:p*r/(1-Math.pow(1+r,-n))}
  function yrs(m){var y=Math.floor(m/12),mo=m%12;return (y?y+" yr"+(y>1?"s":""):"")+(y&&mo?" ":"")+(mo?mo+" mo":"")||"0 mo"}
  var COL={a:"var(--brand)",b:"var(--gold)",c:"#6b8afd",d:"var(--muted)"};

  /* ---------- Calculator definitions ---------- */
  var DEF = {
    mortgage:{
      inputs:[["price","Home price","money",50000,3000000,5000,450000],["down","Down payment","pct",0,60,1,20],["rate","Interest rate (annual)","pct",0,20,0.05,6.5],["years","Loan term","years",5,40,1,30],["tax","Property tax / year","money",0,50000,100,4500],["ins","Home insurance / year","money",0,20000,100,1500]],
      calc:function(v){
        var loan=v.price*(1-v.down/100),r=v.rate/1200,n=v.years*12,m=pmt(r,n,loan),esc=(v.tax+v.ins)/12,total=m*n;
        var bal=loan,rows=[],ser=[[0,loan]];
        for(var y=1;y<=v.years;y++){var pi=0,pp=0;for(var k=0;k<12;k++){var i=bal*r,p=m-i;pi+=i;pp+=p;bal=Math.max(0,bal-p)}rows.push([y,money(pp),money(pi),money(bal)]);ser.push([y,bal])}
        return {head:money(m+esc),headLabel:"Estimated monthly payment",
          rows:[["Principal & interest",money(m)],["Taxes & insurance",money(esc)],["Loan amount",money(loan)],["Down payment",money(v.price-loan)],["Total interest",money(total-loan)],["Total of all payments",money(total)]],
          bar:[["Principal",loan,COL.a],["Interest",total-loan,COL.b],["Tax & insurance",esc*n,COL.c]],
          chart:{s:ser,label:"Loan balance by year"},table:{h:["Year","Principal","Interest","Balance"],r:rows}};
      }},
    "compound-interest":{
      inputs:[["p","Starting amount","money",0,1000000,500,10000],["c","Monthly contribution","money",0,20000,50,500],["rate","Annual return","pct",0,25,0.1,7],["years","Years to grow","years",1,60,1,20],["freq","Compounding","select",[["12","Monthly"],["4","Quarterly"],["1","Annually"],["365","Daily"]],"12"]],
      calc:function(v){
        var f=+v.freq,r=v.rate/100,bal=v.p,dep=v.p,ser=[[0,bal]],rows=[];
        var mr=Math.pow(1+r/f,f/12)-1;
        for(var y=1;y<=v.years;y++){for(var k=0;k<12;k++){bal=bal*(1+mr)+v.c;dep+=v.c}ser.push([y,bal]);rows.push([y,money(dep),money(bal-dep),money(bal)])}
        return {head:money(bal),headLabel:"Future value after "+v.years+" years",
          rows:[["Total contributed",money(dep)],["Interest earned",money(bal-dep)],["Growth multiple",num(bal/Math.max(dep,1),2)+"×"],["Rule of 72 doubling time",v.rate>0?num(72/v.rate)+" yrs":"—"]],
          bar:[["Contributions",dep,COL.a],["Interest",bal-dep,COL.b]],chart:{s:ser,label:"Balance by year"},table:{h:["Year","Contributed","Interest","Balance"],r:rows}};
      }},
    "loan-emi":{
      inputs:[["amt","Loan amount","money",1000,2000000,1000,25000],["rate","Interest rate (annual)","pct",0,40,0.1,10.5],["years","Tenure","years",1,30,1,5]],
      calc:function(v){
        var r=v.rate/1200,n=v.years*12,e=pmt(r,n,v.amt),bal=v.amt,rows=[],ser=[[0,bal]];
        for(var y=1;y<=v.years;y++){var pi=0,pp=0;for(var k=0;k<12;k++){var i=bal*r,p=e-i;pi+=i;pp+=p;bal=Math.max(0,bal-p)}rows.push([y,money(pp),money(pi),money(bal)]);ser.push([y,bal])}
        return {head:money(e),headLabel:"Monthly EMI / payment",rows:[["Total interest",money(e*n-v.amt)],["Total payable",money(e*n)],["Number of payments",n]],
          bar:[["Principal",v.amt,COL.a],["Interest",e*n-v.amt,COL.b]],chart:{s:ser,label:"Outstanding balance"},table:{h:["Year","Principal","Interest","Balance"],r:rows}};
      }},
    "home-affordability":{
      inputs:[["inc","Gross annual income","money",10000,1000000,1000,95000],["debt","Monthly debt payments","money",0,20000,50,400],["down","Cash for down payment","money",0,1000000,1000,60000],["rate","Mortgage rate","pct",0,15,0.05,6.5],["years","Loan term","years",10,40,1,30],["dti","Max debt-to-income","pct",28,50,1,36]],
      calc:function(v){
        var maxHousing=Math.max(0,v.inc/12*v.dti/100-v.debt),cap28=v.inc/12*0.28,pay=Math.min(maxHousing,Math.max(cap28,0))*0.82;
        var r=v.rate/1200,n=v.years*12,loan=r===0?pay*n:pay*(1-Math.pow(1+r,-n))/r,price=loan+v.down;
        return {head:money(price),headLabel:"Home price you can likely afford",
          rows:[["Max loan amount",money(loan)],["Est. principal & interest",money(pay)+"/mo"],["Total housing budget (incl. tax/ins.)",money(pay/0.82)+"/mo"],["Down payment share",num(v.down/Math.max(price,1)*100)+"%"]],
          bar:[["Loan",loan,COL.a],["Down payment",v.down,COL.b]],note:"Uses the 28% front-end and your chosen back-end debt-to-income limits; ~18% of the housing budget is reserved for taxes and insurance."};
      }},
    retirement:{
      inputs:[["age","Current age","num",18,75,1,35],["ret","Retirement age","num",40,80,1,65],["sav","Current savings","money",0,5000000,1000,50000],["c","Monthly contribution","money",0,20000,50,800],["rate","Return before retirement","pct",0,15,0.1,7],["inf","Inflation","pct",0,10,0.1,2.5],["need","Desired yearly income (today's money)","money",10000,500000,1000,60000],["swr","Safe withdrawal rate","pct",2,6,0.1,4]],
      calc:function(v){
        var y=Math.max(0,v.ret-v.age),mr=v.rate/1200,bal=v.sav,ser=[[v.age,bal]];
        for(var i=1;i<=y;i++){for(var k=0;k<12;k++)bal=bal*(1+mr)+v.c;ser.push([v.age+i,bal])}
        var needNominal=v.need*Math.pow(1+v.inf/100,y),target=needNominal/(v.swr/100),real=bal/Math.pow(1+v.inf/100,y),gap=target-bal;
        var extra=0;if(gap>0){var n=y*12;extra=mr===0?gap/n:gap*mr/(Math.pow(1+mr,n)-1)}
        return {head:money(bal),headLabel:"Projected savings at age "+v.ret,
          rows:[["Target nest egg",money(target)],["In today's money",money(real)],["Projected yearly income ("+v.swr+"% rule)",money(bal*v.swr/100)],[gap>0?"Shortfall":"Surplus",money(Math.abs(gap))],[gap>0?"Extra needed per month":"On track","—".length&&gap>0?money(extra):"✓"]],
          bar:[["Projected",Math.min(bal,target),COL.a],[gap>0?"Gap":"Surplus",Math.abs(gap),gap>0?"var(--warn)":COL.b]],chart:{s:ser,label:"Savings by age",xl:"Age"}};
      }},
    "savings-goal":{
      inputs:[["goal","Savings goal","money",500,2000000,500,30000],["have","Already saved","money",0,2000000,100,2000],["years","Time to reach goal","years",1,40,1,3],["rate","Interest / return","pct",0,15,0.1,4]],
      calc:function(v){
        var n=v.years*12,r=v.rate/1200,fvHave=v.have*Math.pow(1+r,n),need=Math.max(0,v.goal-fvHave),m=r===0?need/n:need*r/(Math.pow(1+r,n)-1),ser=[[0,v.have]],b=v.have;
        for(var y=1;y<=v.years;y++){for(var k=0;k<12;k++)b=b*(1+r)+m;ser.push([y,b])}
        return {head:money(m),headLabel:"Save this much every month",rows:[["Per week",money(m*12/52)],["Total you'll deposit",money(m*n)],["Interest earned",money(v.goal-v.have-m*n)]],
          bar:[["Already saved",v.have,COL.c],["Deposits",m*n,COL.a],["Interest",Math.max(0,v.goal-v.have-m*n),COL.b]],chart:{s:ser,label:"Progress toward goal"}};
      }},
    "debt-payoff":{
      inputs:[["b1","Debt 1 balance","money",0,200000,100,6000],["r1","Debt 1 APR","pct",0,40,0.1,22],["m1","Debt 1 minimum","money",0,5000,5,150],
              ["b2","Debt 2 balance","money",0,200000,100,3500],["r2","Debt 2 APR","pct",0,40,0.1,9],["m2","Debt 2 minimum","money",0,5000,5,90],
              ["b3","Debt 3 balance","money",0,200000,100,12000],["r3","Debt 3 APR","pct",0,40,0.1,6.5],["m3","Debt 3 minimum","money",0,5000,5,240],
              ["extra","Extra payment each month","money",0,10000,25,300]],
      calc:function(v){
        function run(order){
          var d=[1,2,3].map(function(i){return {b:v["b"+i],r:v["r"+i]/1200,m:v["m"+i],i:i}}).filter(function(x){return x.b>0});
          var budget=d.reduce(function(s,x){return s+x.m},0)+v.extra,mo=0,int=0,ser=[[0,d.reduce(function(s,x){return s+x.b},0)]];
          while(d.some(function(x){return x.b>0.005})&&mo<600){
            mo++;var left=budget;
            d.forEach(function(x){if(x.b>0){var i=x.b*x.r;int+=i;x.b+=i}});
            d.forEach(function(x){if(x.b>0){var p=Math.min(x.m,x.b);x.b-=p;left-=p}});
            d.slice().sort(order).forEach(function(x){if(x.b>0&&left>0){var p=Math.min(left,x.b);x.b-=p;left-=p}});
            if(mo%12===0)ser.push([mo/12,d.reduce(function(s,x){return s+Math.max(0,x.b)},0)]);
          }
          return {mo:mo,int:int,ser:ser};
        }
        var av=run(function(a,b){return b.r-a.r}),sn=run(function(a,b){return a.b-b.b});
        var best=av.int<=sn.int?"Avalanche":"Snowball";
        return {head:yrs(av.mo),headLabel:"Debt-free (avalanche method)",
          rows:[["Avalanche: total interest",money(av.int)],["Avalanche: months",av.mo],["Snowball: total interest",money(sn.int)],["Snowball: months",sn.mo],["Interest saved by "+best,money(Math.abs(av.int-sn.int))]],
          bar:[["Avalanche interest",av.int,COL.a],["Snowball interest",sn.int,COL.b]],chart:{s:av.ser,label:"Total debt remaining (avalanche)"},
          note:av.mo>=600?"At these payments the debt doesn't clear within 50 years — increase the extra payment.":"Avalanche pays highest-APR debt first (cheapest). Snowball pays smallest balance first (fastest early wins)."};
      }},
    "credit-card-payoff":{
      inputs:[["bal","Card balance","money",100,100000,50,5000],["apr","APR","pct",0,40,0.1,21.9],["pay","Monthly payment","money",10,10000,5,200]],
      calc:function(v){
        var r=v.apr/1200,b=v.bal,mo=0,int=0,ser=[[0,b]];
        if(v.pay<=b*r)return {head:"Never",headLabel:"Payment doesn't cover the interest",rows:[["Monthly interest",money(b*r)],["Minimum to make progress",money(b*r+1)]],note:"Raise your payment above the monthly interest charge."};
        while(b>0.005&&mo<600){mo++;var i=b*r;int+=i;b=b+i-v.pay;if(mo%12===0)ser.push([mo/12,Math.max(0,b)])}
        var to36=pmt(r,36,v.bal);
        return {head:yrs(mo),headLabel:"Time to pay off",rows:[["Total interest",money(int)],["Total paid",money(v.bal+int)],["Payment to be debt-free in 3 yrs",money(to36)]],
          bar:[["Balance",v.bal,COL.a],["Interest",int,"var(--warn)"]],chart:{s:ser,label:"Balance by year"}};
      }},
    budget:{
      inputs:[["inc","Monthly take-home pay","money",500,100000,50,5200],["needs","Needs %","pct",30,70,1,50],["wants","Wants %","pct",0,50,1,30]],
      calc:function(v){
        var s=Math.max(0,100-v.needs-v.wants);
        return {head:money(v.inc*s/100),headLabel:"Monthly savings & debt payoff ("+s+"%)",
          rows:[["Needs ("+v.needs+"%) — rent, groceries, utilities, minimum debt",money(v.inc*v.needs/100)],["Wants ("+v.wants+"%) — dining, travel, subscriptions",money(v.inc*v.wants/100)],["Savings ("+s+"%) — emergency fund, investing, extra debt",money(v.inc*s/100)],["Yearly savings",money(v.inc*s/100*12)]],
          bar:[["Needs",v.needs,COL.a],["Wants",v.wants,COL.b],["Savings",s,COL.c]],pctBar:true};
      }},
    sip:{
      inputs:[["m","Monthly investment (SIP)","money",10,100000,10,200],["rate","Expected annual return","pct",1,25,0.5,12],["years","Investment period","years",1,40,1,15],["step","Annual step-up","pct",0,25,1,10]],
      calc:function(v){
        var r=v.rate/1200,b=0,inv=0,m=v.m,ser=[[0,0]],rows=[];
        for(var y=1;y<=v.years;y++){for(var k=0;k<12;k++){b=(b+m)*(1+r);inv+=m}ser.push([y,b]);rows.push([y,money(m)+"/mo",money(inv),money(b)]);m*=1+v.step/100}
        return {head:money(b),headLabel:"Estimated corpus",rows:[["Total invested",money(inv)],["Estimated gains",money(b-inv)],["Wealth multiple",num(b/Math.max(inv,1),2)+"×"]],
          bar:[["Invested",inv,COL.a],["Gains",b-inv,COL.b]],chart:{s:ser,label:"Corpus by year"},table:{h:["Year","SIP","Invested","Value"],r:rows}};
      }},
    inflation:{
      inputs:[["amt","Amount today","money",1,10000000,10,1000],["inf","Inflation rate","pct",0,20,0.1,3],["years","Years","years",1,60,1,20]],
      calc:function(v){
        var f=v.amt*Math.pow(1+v.inf/100,v.years),pp=v.amt/Math.pow(1+v.inf/100,v.years),ser=[];
        for(var y=0;y<=v.years;y++)ser.push([y,v.amt*Math.pow(1+v.inf/100,y)]);
        return {head:money(f),headLabel:"Future cost of "+money(v.amt)+" today",rows:[["Purchasing power of "+money(v.amt)+" in "+v.years+" yrs",money(pp)],["Value lost",num((1-pp/v.amt)*100)+"%"],["Prices double every",v.inf>0?num(72/v.inf)+" yrs":"—"]],
          chart:{s:ser,label:"Cost over time"}};
      }},
    "emergency-fund":{
      inputs:[["exp","Essential monthly expenses","money",200,50000,50,3200],["months","Months of cover","select",[["3","3 months"],["6","6 months"],["9","9 months"],["12","12 months"]],"6"],["have","Already saved","money",0,500000,100,4000],["save","You can save per month","money",0,20000,25,400]],
      calc:function(v){
        var t=v.exp*+v.months,gap=Math.max(0,t-v.have),mo=v.save>0?Math.ceil(gap/v.save):Infinity;
        return {head:money(t),headLabel:"Your emergency fund target",rows:[["Still to save",money(gap)],["Time to reach target",gap===0?"Done ✓":(isFinite(mo)?yrs(mo):"Add a monthly amount")],["Progress",num(Math.min(100,v.have/t*100))+"%"]],
          bar:[["Saved",Math.min(v.have,t),COL.a],["Remaining",gap,COL.d]]};
      }}
  };

  /* ---------- Rendering ---------- */
  function fmtVal(t,v){return t==="money"?money(v):t==="pct"?num(v,2)+"%":t==="years"?v+" yr"+(v==1?"":"s"):num(v,0)}
  function svgChart(s,xl){
    if(!s||s.length<2)return "";
    var W=600,H=220,P=36,maxY=Math.max.apply(null,s.map(function(p){return p[1]}))||1,minX=s[0][0],maxX=s[s.length-1][0]||1;
    function X(x){return P+(x-minX)/(maxX-minX||1)*(W-P-10)}function Y(y){return H-24-(y/maxY)*(H-40)}
    var d=s.map(function(p,i){return (i?"L":"M")+X(p[0]).toFixed(1)+","+Y(p[1]).toFixed(1)}).join(" ");
    var area=d+" L"+X(maxX)+","+Y(0)+" L"+X(minX)+","+Y(0)+" Z";
    var ticks=[0,.5,1].map(function(t){return '<text x="4" y="'+(Y(maxY*t)+4)+'" font-size="10" fill="currentColor" opacity=".6">'+money(maxY*t).replace(/\.00$/,"")+'</text><line x1="'+P+'" x2="'+W+'" y1="'+Y(maxY*t)+'" y2="'+Y(maxY*t)+'" stroke="currentColor" opacity=".1"/>'}).join("");
    return '<svg class="chart" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Chart" style="color:var(--ink)">'+ticks+
      '<path d="'+area+'" fill="var(--brand)" opacity=".12"/><path d="'+d+'" fill="none" stroke="var(--brand)" stroke-width="2.5"/>'+
      '<text x="'+P+'" y="'+(H-6)+'" font-size="10" fill="currentColor" opacity=".6">'+(xl?xl+" ":"")+minX+'</text><text x="'+(W-10)+'" y="'+(H-6)+'" font-size="10" text-anchor="end" fill="currentColor" opacity=".6">'+maxX+'</text></svg>';
  }
  function mount(el){
    var key=el.getAttribute("data-calc"),D=DEF[key];if(!D)return;var compact=el.hasAttribute("data-compact");
    var html='<div class="card"><div class="currency-pick">Currency <select aria-label="Currency">'+Object.keys(CUR).map(function(c){return '<option'+(c===cur?" selected":"")+'>'+c+'</option>'}).join("")+'</select></div>';
    D.inputs.forEach(function(f,ix){
      var id="i-"+f[0];var hidden=compact&&ix>3;
      if(f[2]==="select"){html+='<div class="field"><label for="'+id+'">'+f[1]+'</label><select id="'+id+'" data-k="'+f[0]+'">'+f[3].map(function(o){return '<option value="'+o[0]+'"'+(o[0]===f[4]?" selected":"")+'>'+o[1]+'</option>'}).join("")+'</select></div>';return}
      var val=f[2]==="money"?f[6]*CUR[cur].f:f[6],max=f[2]==="money"?f[4]*CUR[cur].f:f[4],step=f[2]==="money"?f[5]*CUR[cur].f:f[5];
      html+='<div class="field"'+(hidden?' hidden':'')+'><label for="'+id+'">'+f[1]+' <output data-o="'+f[0]+'"></output></label>'+
        '<input type="range" min="'+f[3]+'" max="'+max+'" step="'+step+'" value="'+val+'" data-k="'+f[0]+'" data-t="'+f[2]+'" aria-label="'+f[1]+' slider">'+
        '<input type="number"'+(compact?' hidden':'')+' id="'+id+'" min="'+f[3]+'" step="'+step+'" value="'+val+'" data-k="'+f[0]+'" data-t="'+f[2]+'" inputmode="decimal"></div>';
    });
    html+='</div><div class="result" aria-live="polite"></div>';
    el.innerHTML=html;
    var out=el.querySelector(".result");
    function vals(){var o={};el.querySelectorAll("[data-k]").forEach(function(i){if(i.type!=="range")o[i.getAttribute("data-k")]=i.tagName==="SELECT"?i.value:(parseFloat(i.value)||0)});return o}
    function render(){
      var v=vals();
      el.querySelectorAll("output[data-o]").forEach(function(o){var inp=el.querySelector('input[type=number][data-k="'+o.getAttribute("data-o")+'"]');o.textContent=fmtVal(inp.getAttribute("data-t"),+inp.value)});
      var R=D.calc(v),h='<div class="eyebrow">'+R.headLabel+'</div><div class="big-num">'+R.head+'</div>';
      if(R.bar){var tot=R.bar.reduce(function(s,b){return s+Math.max(0,b[1])},0)||1;
        h+='<div class="bar">'+R.bar.map(function(b){return '<i style="width:'+(Math.max(0,b[1])/tot*100)+'%;background:'+b[2]+'"></i>'}).join("")+'</div><div class="legend">'+R.bar.map(function(b){return '<span><i style="background:'+b[2]+'"></i>'+b[0]+(R.pctBar?" "+b[1]+"%":"")+'</span>'}).join("")+'</div>'}
      h+='<div style="margin-top:14px">'+R.rows.map(function(r){return '<div class="kv"><span>'+r[0]+'</span><b>'+r[1]+'</b></div>'}).join("")+'</div>';
      if(compact){out.innerHTML=h.split('<div class="bar">')[0]+'<div class="kv"><span>Loan amount</span><b>'+R.rows[2][1]+'</b></div><a class="btn btn-primary" style="width:100%;margin-top:14px" href="'+(document.body.getAttribute("data-root")||"")+'calculators/'+key+'.html">Full breakdown & schedule →</a>';return}
      if(R.chart)h+='<div class="notice" style="margin-top:14px">'+R.chart.label+'</div>'+svgChart(R.chart.s,R.chart.xl);
      if(R.note)h+='<p class="notice" style="margin-top:10px">'+R.note+'</p>';
      if(R.table)h+='<details style="margin-top:14px"><summary>Year-by-year schedule</summary><div class="table-wrap"><table><thead><tr>'+R.table.h.map(function(x){return "<th>"+x+"</th>"}).join("")+'</tr></thead><tbody>'+R.table.r.map(function(r){return "<tr>"+r.map(function(c){return "<td>"+c+"</td>"}).join("")+"</tr>"}).join("")+'</tbody></table></div></details>';
      h+='<a class="btn btn-primary" style="width:100%;margin-top:18px" href="'+(document.body.getAttribute("data-root")||"")+'get-help.html?topic='+key+'">Get free expert help with this →</a><p class="notice center" style="margin:8px 0 0">Free · No obligation · No credit check</p>';
      out.innerHTML=h;
    }
    el.addEventListener("input",function(e){
      var k=e.target.getAttribute("data-k");if(!k)return;
      el.querySelectorAll('input[data-k="'+k+'"]').forEach(function(i){if(i!==e.target)i.value=e.target.value});render();
    });
    el.addEventListener("change",function(e){if(e.target.closest(".currency-pick")){var old=CUR[cur].f;cur=e.target.value;try{localStorage.setItem("ef-cur",cur)}catch(x){}
      var ratio=CUR[cur].f/old;el.querySelectorAll('input[data-t="money"]').forEach(function(i){if(i.type==="range"){i.max=+i.max*ratio;i.step=+i.step*ratio}i.value=Math.round(+i.value*ratio)});render()}else render()});
    render();
  }
  document.querySelectorAll("[data-calc]").forEach(mount);
})();
