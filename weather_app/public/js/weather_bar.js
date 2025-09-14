(() => {
  const ID = "weather-bottom-bar";
  const CSS = `
    #${ID}{
      position:fixed;left:0;right:0;bottom:0;height:38px;
      background:#1f2937;color:#fff;display:flex;align-items:center;
      gap:12px;padding:0 12px;font-size:13px;z-index:9999;
      box-shadow:0 -1px 3px rgba(0,0,0,.2)
    }
    #${ID} .dot{width:6px;height:6px;border-radius:50%;background:#60a5fa;display:inline-block}
    body{padding-bottom:38px !important;}
  `;
  function ensureStyle(){
    if(document.getElementById(ID+"-style")) return;
    const s = document.createElement('style');
    s.id = ID+"-style"; s.textContent = CSS; document.head.appendChild(s);
  }
  function render(data){
    ensureStyle();
    let el = document.getElementById(ID);
    if(!el){
      el = document.createElement('div'); el.id = ID; document.body.appendChild(el);
    }
    const t = data?.temperature ?? '—';
    const h = data?.humidity ?? '—';
    const c = data?.city ?? 'Riyadh';
    const u = data?.last_updated_on ? frappe.datetime.user_to_str(data.last_updated_on) : '—';
    el.innerHTML = `<span class="dot"></span><b>${c}</b> | Temp: ${t}°C | Humidity: ${h}% <span style="opacity:.8;margin-left:auto">Updated: ${u}</span>`;
  }
  async function load(){
    try {
      const r = await frappe.call('weather_app.api.get_latest', {});
      render(r.message || {});
    } catch(e){
      console.warn("weather_app: fetch failed", e);
    }
  }
  function boot(){

    load();
    frappe.router?.on?.('change', () => load());
    setInterval(load, 60000);
  }
  if (document.readyState === 'complete' || document.readyState === 'interactive'){
    setTimeout(boot, 0);
  } else {
    document.addEventListener('DOMContentLoaded', boot);
  }
})();
