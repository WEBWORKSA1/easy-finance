/* Easy.Finance — multi-step lead wizard */
(function(){
  "use strict";
  var w=document.querySelector("[data-lead]");if(!w)return;
  var steps=[].slice.call(w.querySelectorAll(".step")),i=0,data={};
  var bar=w.querySelector(".progress i"),lbl=w.querySelector(".step-label"),back=w.querySelector("[data-back]"),next=w.querySelector("[data-next]");
  var map={mortgage:"Mortgage / home loan","home-affordability":"Mortgage / home loan","loan-emi":"Personal or auto loan","debt-payoff":"Debt relief & consolidation","credit-card-payoff":"Debt relief & consolidation",retirement:"Investing & retirement",sip:"Investing & retirement","compound-interest":"Investing & retirement",budget:"Budget & money coaching","emergency-fund":"Budget & money coaching","savings-goal":"Budget & money coaching",inflation:"Investing & retirement"};
  function show(n){
    i=Math.max(0,Math.min(n,steps.length-1));
    steps.forEach(function(s,k){s.classList.toggle("active",k===i)});
    bar.style.width=((i+1)/steps.length*100)+"%";
    lbl.textContent="Step "+(i+1)+" of "+steps.length+" · about "+Math.max(1,steps.length-i)*15+" seconds left";
    back.style.visibility=i?"visible":"hidden";
    var last=i===steps.length-1;next.textContent=last?"Get my free match →":"Continue →";
    next.style.display=steps[i].hasAttribute("data-auto")?"none":"";
    var f=steps[i].querySelector("input,select,button.opt");if(f&&i)setTimeout(function(){f.focus()},50);
  }
  w.addEventListener("click",function(e){
    var o=e.target.closest(".opt");if(!o)return;
    var st=o.closest(".step");st.querySelectorAll(".opt").forEach(function(x){x.classList.remove("sel")});o.classList.add("sel");
    data[st.getAttribute("data-name")]=o.getAttribute("data-v");
    setTimeout(function(){show(i+1)},180);
  });
  back.addEventListener("click",function(){show(i-1)});
  next.addEventListener("click",function(){
    var st=steps[i],ok=true;
    st.querySelectorAll("input,select,textarea").forEach(function(f){if(!f.checkValidity()){ok=false;f.reportValidity()}else if(f.name&&f.type!=="checkbox")data[f.name]=f.value;else if(f.type==="checkbox")data[f.name]=f.checked?"yes":"no"});
    if(st.getAttribute("data-name")&&!data[st.getAttribute("data-name")]){ok=false}
    if(!ok)return;
    if(i<steps.length-1)return show(i+1);
    if(w.querySelector("[name=_honey]").value)return;
    next.disabled=true;next.textContent="Sending…";
    data.form="Lead request";data._subject="[Easy.Finance] New lead: "+(data.need||"General")+" — "+(data.country||"");
    window.EF_SEND(data).then(function(){
      w.querySelector(".lead-body").innerHTML='<div class="center" style="padding:24px 0"><div style="font-size:3rem">✅</div><h2>You\'re matched to our review queue</h2><p class="lede">Thanks'+(data.name?", "+data.name.split(" ")[0]:"")+'. A specialist will reply within 1 business day with options for <b>'+(data.need||"your request")+'</b>. Meanwhile, try our <a href="calculators/">free calculators</a>.</p></div>';
    }).catch(function(){next.disabled=false;next.textContent="Try again →";var m=w.querySelector(".form-msg");m.className="form-msg err";m.textContent="Network issue — please try again in a moment."});
  });
  var t=new URLSearchParams(location.search).get("topic");
  if(t&&map[t]){var o=w.querySelector('.opt[data-v="'+map[t]+'"]');if(o){o.classList.add("sel");data.need=map[t];show(1);return}}
  show(0);
})();
