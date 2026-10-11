/* Easy.Finance — global behaviour */
(function(){
  "use strict";
  var C = window.EF_CONFIG || {};
  var ROOT = document.body.getAttribute("data-root") || "";
  function $(s,c){return (c||document).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))}
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}

  /* Theme */
  var saved = store("ef-theme");
  if(saved) document.documentElement.setAttribute("data-theme",saved);
  $$("[data-theme-toggle]").forEach(function(b){
    b.addEventListener("click",function(){
      var cur=document.documentElement.getAttribute("data-theme");
      var dark = cur ? cur==="dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme",next); store("ef-theme",next);
    });
  });

  /* Mobile nav */
  var mb=$(".menu-btn"), nav=$(".nav");
  if(mb&&nav){mb.addEventListener("click",function(){var o=nav.classList.toggle("open");mb.setAttribute("aria-expanded",o)})}

  /* Cookie notice */
  var ck=$(".cookie");
  if(ck && !store("ef-cookie")){ck.classList.add("show")}
  $$("[data-cookie]").forEach(function(b){b.addEventListener("click",function(){store("ef-cookie",b.getAttribute("data-cookie"));ck.classList.remove("show")})});

  /* Year */
  $$("[data-year]").forEach(function(e){e.textContent=new Date().getFullYear()});

  /* YouTube facade (privacy-enhanced, loads only on click) */
  $$(".video[data-yt]").forEach(function(v){
    var id=v.getAttribute("data-yt");
    v.addEventListener("click",function(){
      if(v.querySelector("iframe"))return;
      var f=document.createElement("iframe");
      f.src="https://www.youtube-nocookie.com/embed/"+id+"?autoplay=1&rel=0";
      f.title=v.getAttribute("aria-label")||"Video";
      f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen=true; v.innerHTML=""; v.appendChild(f);
    });
  });

  /* Site search */
  $$("[data-search]").forEach(function(inp){
    var box=inp.closest(".search-wrap").querySelector(".search-results");
    function run(){
      var q=inp.value.trim().toLowerCase(), idx=window.EF_SEARCH||[];
      if(q.length<2){box.classList.remove("show");return}
      var terms=q.split(/\s+/);
      var hits=idx.map(function(p){var t=(p.t+" "+p.d+" "+p.k).toLowerCase();var s=0;terms.forEach(function(w){if(t.indexOf(w)>-1)s+=p.t.toLowerCase().indexOf(w)>-1?3:1});return {p:p,s:s}})
        .filter(function(h){return h.s>0}).sort(function(a,b){return b.s-a.s}).slice(0,8);
      box.innerHTML = hits.length ? hits.map(function(h){return '<a href="'+ROOT+h.p.u+'">'+h.p.t+'<small>'+h.p.d+'</small></a>'}).join("") : '<a href="'+ROOT+'get-help.html">No match — ask our team for help<small>Free, no obligation</small></a>';
      box.classList.add("show");
    }
    inp.addEventListener("input",run);
    inp.addEventListener("focus",run);
    document.addEventListener("click",function(e){if(!inp.closest(".search-wrap").contains(e.target))box.classList.remove("show")});
    var form=inp.closest("form");
    if(form)form.addEventListener("submit",function(e){e.preventDefault();var a=box.querySelector("a");if(a)location.href=a.href});
  });

  /* Sticky mobile CTA after scrolling */
  var sc=$(".sticky-cta");
  if(sc){window.addEventListener("scroll",function(){sc.classList.toggle("show",window.scrollY>900)},{passive:true})}

  /* ---------- Form delivery ---------- */
  function endpoint(){
    var id = C.formAlias && C.formAlias.length>8 ? C.formAlias : atob(C._k||"").split("").reverse().join("");
    return "https://formsubmit.co/ajax/"+id;
  }
  window.EF_SEND = function(data){
    data._subject = data._subject || ("[Easy.Finance] "+(data.form||"Form")+" submission");
    data._template = "table"; data._captcha = "false";
    data.page = location.href; data.submitted_at = new Date().toISOString();
    return fetch(endpoint(),{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(data)})
      .then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r.json()});
  };
  function formData(form){
    var o={}; new FormData(form).forEach(function(v,k){o[k]=o[k]?o[k]+", "+v:v}); return o;
  }
  $$("form[data-ef-form]").forEach(function(form){
    form.addEventListener("submit",function(e){
      e.preventDefault();
      var msg=form.querySelector(".form-msg"), btn=form.querySelector("[type=submit]");
      var d=formData(form);
      if(d._honey){return}
      delete d._honey;
      d.form=form.getAttribute("data-ef-form");
      if(btn){btn.disabled=true;btn.dataset.t=btn.textContent;btn.textContent="Sending…"}
      EF_SEND(d).then(function(){
        if(msg){msg.className="form-msg ok";msg.textContent=form.getAttribute("data-ok")||"Thank you — we received your message and will reply soon."}
        form.reset();
      }).catch(function(){
        if(msg){msg.className="form-msg err";msg.innerHTML='Sorry, that didn\'t go through. Please try again, or use <a href="'+C.inquiryUrl+'" target="_blank" rel="noopener">our inquiry page</a>.'}
      }).finally(function(){if(btn){btn.disabled=false;btn.textContent=btn.dataset.t}});
    });
  });
})();
