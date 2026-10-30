// そふぁら サイトプロトタイプ：メニュー、カート（試作）、絞り込み、数量
(() => {
  const KEY = "sofara-proto-cart";
  const products = window.PRODUCTS || {};
  const css = document.querySelector('link[href*="style.css"]');
  const imgBase = new URL("../img/", css.href).href;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  const load = () => {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; }
  };
  const save = cart => {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch { /* 保存できない環境でも表示は続ける */ }
  };
  let cart = load();
  const yen = n => n.toLocaleString("ja-JP") + "円";

  // ---- drawers ----
  const overlay = $(".overlay");
  let lastFocus = null;
  const open = id => {
    const d = document.getElementById(id);
    if (!d) return;
    lastFocus = document.activeElement;
    $$(".drawer.is-open").forEach(x => close(x, false));
    $("[data-toast]").classList.remove("is-show");
    d.classList.add("is-open");
    d.setAttribute("aria-hidden", "false");
    overlay.classList.add("is-open");
    document.body.classList.add("is-locked");
    $("[data-close]", d)?.focus();
  };
  const close = (d = $(".drawer.is-open"), restore = true) => {
    if (!d) return;
    d.classList.remove("is-open");
    d.setAttribute("aria-hidden", "true");
    overlay.classList.remove("is-open");
    document.body.classList.remove("is-locked");
    if (restore && lastFocus) lastFocus.focus();
  };
  document.addEventListener("click", e => {
    const o = e.target.closest("[data-open]");
    if (o) { if (o.dataset.open === "cart") renderCart(); open(o.dataset.open); return; }
    if (e.target.closest("[data-close]")) { close(); return; }
    if (e.target.closest(".drawer .menu-list a")) close(undefined, false);
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });

  // ---- toast ----
  const toast = $("[data-toast]");
  let toastTimer;
  const showToast = msg => {
    toast.textContent = msg;
    toast.classList.add("is-show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-show"), 2600);
  };

  // ---- cart ----
  const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
  const renderBadge = () => $$(".badge").forEach(b => { const c = count(); b.textContent = c; b.dataset.count = c; });
  const renderCart = () => {
    const list = $("[data-cart-items]");
    const ids = Object.keys(cart).filter(id => products[id]);
    if (!ids.length) {
      list.innerHTML = '<li class="cart-empty">カートは空です</li>';
    } else {
      list.innerHTML = ids.map(id => {
        const p = products[id];
        return `<li class="cart-item"><img src="${imgBase}${p.img}" alt=""><div><b>${p.name}</b><span>${yen(p.price)} × ${cart[id]}${p.cool ? "　クール便" : ""}</span></div><button type="button" data-remove="${id}">削除</button></li>`;
      }).join("");
    }
    const total = ids.reduce((s, id) => s + (products[id].price || 0) * cart[id], 0);
    $("[data-cart-total]").textContent = yen(total);
  };
  document.addEventListener("click", e => {
    const add = e.target.closest("[data-add]");
    if (add) {
      const id = add.dataset.add;
      const qtyEl = add.dataset.qtyFrom && document.getElementById(add.dataset.qtyFrom);
      const n = qtyEl ? Number(qtyEl.textContent) || 1 : 1;
      cart[id] = (cart[id] || 0) + n;
      save(cart);
      renderBadge();
      showToast(`「${products[id].name}」をカートに入れました（試作のため購入はできません）`);
      return;
    }
    const rm = e.target.closest("[data-remove]");
    if (rm) { delete cart[rm.dataset.remove]; save(cart); renderBadge(); renderCart(); }
  });
  renderBadge();

  // ---- quantity ----
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-qty]");
    if (!b) return;
    const out = b.parentElement.querySelector("output");
    out.textContent = Math.min(20, Math.max(1, Number(out.textContent) + Number(b.dataset.qty)));
  });

  // ---- shop filter ----
  const chips = $$("[data-filter]");
  if (chips.length) {
    const apply = key => {
      chips.forEach(c => c.setAttribute("aria-pressed", String(c.dataset.filter === key)));
      $$("[data-group]").forEach(g => {
        const cats = g.dataset.group.split(" ");
        const showGroup = key === "all" || cats.includes(key);
        g.hidden = !showGroup;
        $$("[data-cat]", g).forEach(item => { item.hidden = !(key === "all" || item.dataset.cat === key || (key === "frozen" && g.id === "frozen")); });
      });
    };
    chips.forEach(c => c.addEventListener("click", () => {
      apply(c.dataset.filter);
      history.replaceState(null, "", c.dataset.filter === "all" ? location.pathname : "#" + c.dataset.filter);
    }));
    const fromHash = location.hash.slice(1);
    if (["frozen", "bread", "rice"].includes(fromHash)) apply(fromHash);
  }
})();
