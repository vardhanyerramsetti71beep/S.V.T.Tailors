/**
 * S. V. T. TAILORS - ESTABLISHED 05-01-1965
 * Interactive Web Application & Bespoke Ordering
 * Location: Eluru Road, near Ram Mandiram, Governorpet, Vijayawada, AP 520002
 * Phone / WhatsApp: +91 98481 33417
 * Diploma Holders: Y. Subba Rao & Y.B. Srinivas
 */

// Global State
const SVT_STATE = {
  cart: JSON.parse(localStorage.getItem('svt_cart')) || [],
  phone: '919848133417',
  activeCategory: 'all',
  customizer: {
    garmentId: 'suit-2pc',
    garmentName: 'Bespoke 2-Piece Suit',
    fabricChoice: 'store-wool',
    fitType: 'Slim Bespoke Fit',
    collarLapel: 'Notch Lapel',
    cuffPocket: 'Standard 2-Button Cuff',
    monogram: '',
    measurementType: 'standard',
    standardSize: '40 (M)',
    customMeasurements: {
      chest: 40,
      waist: 34,
      shoulder: 18,
      sleeve: 25,
      length: 29,
      inseam: 31
    },
    expressSpeed: false,
    notes: ''
  }
};

// Catalog Garments Data (Exclusive Gents Bespoke Wear)
const GARMENTS = [
  {
    id: 'suit-2pc',
    title: "Bespoke 2-Piece Classic Suit",
    category: 'suits',
    categoryName: "Men's Suiting",
    leadTime: '5-7 Days',
    image: 'public/images/bespoke_suit.jpg',
    badge: 'Signature Craft',
    express: true,
    desc: 'Hand-canvassed single or double-breasted jacket and matching tailored trousers. Custom cut for business, ceremonies, and galas.',
    features: ['Hand-sewn pick stitching', 'Premium Bemberg silk lining', 'Double or single rear vents', 'Inner passport & phone pockets']
  },
  {
    id: 'shirt-formal',
    title: "Artisan Formal & Casual Shirt",
    category: 'shirts',
    categoryName: "Shirts & Trousers",
    leadTime: '3-4 Days',
    image: 'public/images/tailored_shirts.jpg',
    badge: 'Popular Choice',
    express: true,
    desc: 'Crisp hand-finished shirts with fused German interlinings for razor-sharp collars that never wilt in Andhra weather.',
    features: ['German collar fusing', 'Mother-of-pearl buttons', 'French or barrel cuffs', 'Tailored or relaxed taper']
  },
  {
    id: 'trouser-chinos',
    title: "Custom Cut Trousers & Gurkhas",
    category: 'shirts',
    categoryName: "Shirts & Trousers",
    leadTime: '3-4 Days',
    image: 'public/images/custom_cut_trousers_gurkha.jpg',
    badge: 'Comfort Fit',
    express: true,
    desc: 'Precision rise and break trousers. Options for classic belt loops, side adjusters, or high-waisted Gurkha style.',
    features: ['Curved waistband for zero slip', 'Double hook & eye closure', 'Bar-tacked pocket corners', 'Comfort crotch saddle']
  },
  {
    id: 'festive-sherwani',
    title: "Royal Wedding Sherwani & Kurta",
    category: 'ethnic',
    categoryName: "Traditional & Ethnic",
    leadTime: '7-10 Days',
    image: 'public/images/festive_sherwani.jpg',
    badge: 'Wedding Special',
    express: true,
    desc: 'Magnificent groom & celebration wear featuring regal mandarin collars, handcrafted button plackets, and matching churidar or dhoti.',
    features: ['Regal structured fit', 'Custom zari/thread border placement', 'Comfort cotton lining', 'Matching pocket square & stole styling']
  },
  {
    id: 'safari-suit',
    title: "Classic South Indian Safari Suit",
    category: 'suits',
    categoryName: "Men's Suiting",
    leadTime: '4-5 Days',
    image: 'public/images/classic_safari_suit.jpg',
    badge: 'Timeless Heritage',
    express: true,
    desc: 'The iconic half-sleeve or full-sleeve Safari Suit, renowned across coastal Andhra for distinction and effortless comfort.',
    features: ['Four flap bellows pockets', 'Epaulette shoulder options', 'Action back pleats for mobility', 'Breathable linen or twill']
  },
  {
    id: 'nehru-jacket',
    title: "Bespoke Nehru & Modi Bundi Jacket",
    category: 'ethnic',
    categoryName: "Traditional & Ethnic",
    leadTime: '3-5 Days',
    image: 'public/images/bespoke_modi_bundi_jacket.jpg',
    badge: 'Gentleman Classic',
    express: true,
    desc: 'Mandarin collar sleeveless vest / waist-coat crafted in pure raw silk, linen, or fine wool. Worn with pride over kurtas or formal shirts.',
    features: ['Handcrafted welt pockets', 'Covered fabric or metallic brass buttons', 'Mandarin standing collar with stiff fusing', 'Smooth satin back lining with adjuster']
  },
  {
    id: 'jodhpuri-suit',
    title: "Royal Jodhpuri Bandhgala Suit",
    category: 'suits',
    categoryName: "Men's Suiting",
    leadTime: '6-8 Days',
    image: 'public/images/royal_jodhpuri_bandhgala.jpg',
    badge: 'Aristocratic Style',
    express: true,
    desc: 'The epitome of Indian gentleman formal wear. Closed-neck royal Bandhgala jacket with matching trousers, perfect for VIP banquets and weddings.',
    features: ['High-structured shoulder padding', 'Hand-stitched closed bandhgala collar', 'Gold / horn designer buttons', 'Bemberg luxury lining']
  },
  {
    id: 'uniform-corporate',
    title: "Men's Corporate & Institutional Uniforms",
    category: 'uniforms',
    categoryName: "Uniforms & Bulk",
    leadTime: '5-7 Days',
    image: 'public/images/corporate_institutional_uniforms.jpg',
    badge: 'Institutional Fit',
    express: false,
    desc: 'High-durability tailored gents uniforms for schools, colleges, security staff, and corporate offices with embroidery support.',
    features: ['Reinforced double stitching', 'Stain-resistant fabric blends', 'Colorfast dye guaranteed', 'Batch sizing & doorstep distribution']
  },
  {
    id: 'alteration-master',
    title: "Master Gents Alterations & Re-fitting",
    category: 'uniforms',
    categoryName: "Alterations",
    leadTime: '24-48 Hours',
    image: 'public/images/tailor_craft.jpg',
    badge: 'Quick Service',
    express: true,
    desc: 'Brought ready-made gents garments or lost/gained weight? Our master tailors reshape suits, shirts, and trousers to custom perfection.',
    features: ['Suit shoulder & chest slimming', 'Trouser taper & hem adjustment', 'Waist nip & tuck', 'Sleeve shortening with genuine buttons']
  }
];

// Fabric Catalog Data
const FABRICS = [
  { id: 'bring-own', name: 'I Will Provide My Own Fabric', tag: 'Client Fabric', desc: 'Bring cloth to our Governorpet shop or request doorstep pickup in Vijayawada' },
  { id: 'giza-cotton', name: '100% Egyptian Giza Cotton', tag: 'Luxury Cotton', desc: 'Ultra-breathable 80s & 100s two-ply yarn, perfect for shirts & kurtas' },
  { id: 'store-wool', name: 'Italian Super 120s Wool Blend', tag: 'Premium Wool', desc: 'Wrinkle-resistant luxury drape for two-piece suits and party blazers' },
  { id: 'pure-linen', name: 'Pure Irish / European Linen', tag: 'Pure Linen', desc: 'Naturally cooling breathable weave for safari suits & summer shirts' },
  { id: 'raw-silk', name: 'Pure Raw Silk / Brocade', tag: 'Wedding Silk', desc: 'Lustrous festive fabric ideal for wedding sherwanis, royal bandhgalas and kurtas' },
  { id: 'raymond-terry', name: 'Raymond Classic Terry-Rayon', tag: 'Everyday Formal', desc: 'Durable, crisp everyday formal fabric for trousers and jackets' }
];

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  renderCatalog();
  setupFilterTabs();
  setupCustomizer();
  setupVisualGuideHotspots();
  setupOrderTracker();
  setupDoorstepForm();
  updateCartUI();
  setupMobileMenu();
  setupNavScroll();
  setupAuthSession();
});

// Setup Logged In User State across website
function setupAuthSession() {
  const savedUser = localStorage.getItem('svt_user');
  if (!savedUser) return;

  try {
    const user = JSON.parse(savedUser);
    const navText = document.getElementById('navAccountText');
    if (navText) {
      const firstName = (user.name || '').split(' ')[0] || 'My Account';
      navText.textContent = `Hi, ${firstName}`;
    }

    // Prefill Doorstep Form
    const dsName = document.getElementById('dsName');
    const dsPhone = document.getElementById('dsPhone');
    if (dsName && !dsName.value) dsName.value = user.name || '';
    if (dsPhone && !dsPhone.value) dsPhone.value = user.mobile || '';

    // Prefill Cart Drawer Form
    const chkName = document.getElementById('checkoutName');
    const chkPhone = document.getElementById('checkoutPhone');
    const chkArea = document.getElementById('checkoutArea');
    if (chkName && !chkName.value) chkName.value = user.name || '';
    if (chkPhone && !chkPhone.value) chkPhone.value = user.mobile || '';
    if (chkArea && !chkArea.value && user.locality) chkArea.value = user.locality;
  } catch (e) {
    console.log('Auth session parse notice:', e);
  }
}

// Render Catalog Grid
function renderCatalog(filter = 'all') {
  const container = document.getElementById('catalogGrid');
  if (!container) return;

  const filtered = filter === 'all' 
    ? GARMENTS 
    : GARMENTS.filter(g => g.category === filter);

  container.innerHTML = filtered.map(item => `
    <div class="catalog-card" data-category="${item.category}">
      <div class="card-img-wrapper">
        <img src="${item.image}" alt="${item.title}" loading="lazy">
        <span class="card-badge">${item.badge}</span>
        ${item.express ? '<span class="card-express-badge">⚡ Tatkal 24-48hr</span>' : ''}
      </div>
      <div class="card-content">
        <div class="card-header-row">
          <small style="color: var(--secondary-hover); font-weight: 700; text-transform: uppercase;">${item.categoryName}</small>
          <div class="card-turnaround" style="color: var(--secondary-hover); font-weight: 700; font-size: 0.8rem; background: var(--secondary-light); padding: 4px 10px; border-radius: 4px;">
            <i class="fas fa-clock"></i> ${item.leadTime}
          </div>
        </div>
        <h3>${item.title}</h3>
        <p class="card-desc">${item.desc}</p>
        <ul class="card-features-list">
          ${item.features.map(f => `<li><i class="fas fa-check-circle"></i> ${f}</li>`).join('')}
        </ul>
        <div class="card-actions">
          <button class="btn-card-order" onclick="openCustomizerFor('${item.id}')">
            <img src="public/images/logo_gentleman_badge.png" class="btn-mini-logo" alt="SVT"> Customize &amp; Order
          </button>
          <button class="btn-card-whatsapp" title="Inquire on WhatsApp" onclick="quickInquiry('${item.title}')">
            <i class="fab fa-whatsapp"></i>
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

// Category filter tabs
function setupFilterTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.getAttribute('data-cat');
      SVT_STATE.activeCategory = cat;
      renderCatalog(cat);
    });
  });
}

// Setup Customizer Logic
function setupCustomizer() {
  updateCustomizerSummary();

  // Garment selector in customizer
  const garmentSelect = document.getElementById('customizerGarmentSelect');
  if (garmentSelect) {
    garmentSelect.innerHTML = GARMENTS.map(g => `<option value="${g.id}">${g.title} (${g.leadTime})</option>`).join('');
    garmentSelect.addEventListener('change', (e) => {
      const g = GARMENTS.find(item => item.id === e.target.value);
      if (g) {
        SVT_STATE.customizer.garmentId = g.id;
        SVT_STATE.customizer.garmentName = g.title;
        updateCustomizerSummary();
      }
    });
  }

  // Fabric radio options
  const fabricContainer = document.getElementById('fabricOptionsGrid');
  if (fabricContainer) {
    fabricContainer.innerHTML = FABRICS.map(f => `
      <div class="option-box ${f.id === SVT_STATE.customizer.fabricChoice ? 'selected' : ''}" onclick="selectFabric('${f.id}')">
        <span class="title">${f.name}</span>
        <span class="sub" style="color: var(--secondary-hover); font-weight: 700;">${f.tag}</span>
        <p style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">${f.desc}</p>
      </div>
    `).join('');
  }

  // Fit radio options
  const fitBoxes = document.querySelectorAll('.fit-option-box');
  fitBoxes.forEach(box => {
    box.addEventListener('click', () => {
      fitBoxes.forEach(b => b.classList.remove('selected'));
      box.classList.add('selected');
      SVT_STATE.customizer.fitType = box.getAttribute('data-fit');
      updateCustomizerSummary();
    });
  });

  // Measurement method tabs inside customizer
  const methodTabs = document.querySelectorAll('.measure-method-tab');
  methodTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      methodTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const method = tab.getAttribute('data-method');
      SVT_STATE.customizer.measurementType = method;

      document.getElementById('measureStandardSection').style.display = method === 'standard' ? 'block' : 'none';
      document.getElementById('measureCustomSection').style.display = method === 'custom' ? 'block' : 'none';
      document.getElementById('measureSampleSection').style.display = method === 'sample' ? 'block' : 'none';
      document.getElementById('measureDoorstepSection').style.display = method === 'doorstep' ? 'block' : 'none';
      updateCustomizerSummary();
    });
  });

  // Express checkbox
  const expressCheckbox = document.getElementById('expressCheckbox');
  if (expressCheckbox) {
    expressCheckbox.addEventListener('change', (e) => {
      SVT_STATE.customizer.expressSpeed = e.target.checked;
      updateCustomizerSummary();
    });
  }
}

// Select fabric helper
window.selectFabric = function(fabricId) {
  const f = FABRICS.find(item => item.id === fabricId);
  if (!f) return;
  SVT_STATE.customizer.fabricChoice = f.id;

  const boxes = document.querySelectorAll('#fabricOptionsGrid .option-box');
  boxes.forEach(b => b.classList.remove('selected'));
  if (event && event.currentTarget) {
    event.currentTarget.classList.add('selected');
  }
  updateCustomizerSummary();
};

// Open customizer directly for an item
window.openCustomizerFor = function(garmentId) {
  const g = GARMENTS.find(item => item.id === garmentId);
  if (!g) return;
  SVT_STATE.customizer.garmentId = g.id;
  SVT_STATE.customizer.garmentName = g.title;

  const garmentSelect = document.getElementById('customizerGarmentSelect');
  if (garmentSelect) garmentSelect.value = g.id;

  updateCustomizerSummary();

  const customizerSection = document.getElementById('customizerSection');
  if (customizerSection) {
    customizerSection.scrollIntoView({ behavior: 'smooth' });
    showToast(`Configuring: ${g.title}`);
  }
};

// Update Customizer UI summary (No price tags)
function updateCustomizerSummary() {
  const c = SVT_STATE.customizer;

  const nameEl = document.getElementById('summaryGarmentName');
  const fabricNameEl = document.getElementById('summaryFabricName');
  const fitEl = document.getElementById('summaryFit');
  const speedEl = document.getElementById('summarySpeed');
  const measureTypeEl = document.getElementById('summaryMeasurementType');

  if (nameEl) nameEl.textContent = c.garmentName;
  
  const f = FABRICS.find(item => item.id === c.fabricChoice);
  if (fabricNameEl) fabricNameEl.textContent = f ? f.name : 'Standard';
  
  if (fitEl) fitEl.textContent = c.fitType;
  if (speedEl) speedEl.textContent = c.expressSpeed ? '⚡ Priority Tatkal (24-48hr)' : 'Standard (5-7 Days)';

  if (measureTypeEl) {
    if (c.measurementType === 'standard') measureTypeEl.textContent = 'Standard Sizing';
    else if (c.measurementType === 'custom') measureTypeEl.textContent = 'Custom Body Inches';
    else if (c.measurementType === 'sample') measureTypeEl.textContent = 'Sample Garment Fit';
    else if (c.measurementType === 'doorstep') measureTypeEl.textContent = 'Doorstep Visit (Vijayawada)';
  }
}

// Add Customizer item to Cart
window.addCustomizerToCart = function() {
  const c = SVT_STATE.customizer;

  // Read current measurements if custom
  let measurementDetail = '';
  if (c.measurementType === 'standard') {
    const sizeSelect = document.getElementById('standardSizeSelect');
    measurementDetail = `Standard Size: ${sizeSelect ? sizeSelect.value : '40'}`;
  } else if (c.measurementType === 'custom') {
    const chest = document.getElementById('inputChest')?.value || '40';
    const waist = document.getElementById('inputWaist')?.value || '34';
    const shoulder = document.getElementById('inputShoulder')?.value || '18';
    const length = document.getElementById('inputLength')?.value || '29';
    measurementDetail = `Custom Fit: Chest ${chest}", Waist ${waist}", Shoulder ${shoulder}", Length ${length}"`;
  } else if (c.measurementType === 'sample') {
    measurementDetail = `Sample Fit: Sending old garment to workshop`;
  } else if (c.measurementType === 'doorstep') {
    measurementDetail = `Doorstep: Master visit at home in Vijayawada`;
  }

  const notesInput = document.getElementById('customizerNotes');
  const notes = notesInput ? notesInput.value.trim() : '';

  const cartItem = {
    cartId: 'item_' + Date.now(),
    title: c.garmentName,
    fabric: FABRICS.find(f => f.id === c.fabricChoice)?.name || 'Custom Fabric',
    fit: c.fitType,
    measurements: measurementDetail,
    express: c.expressSpeed,
    notes: notes
  };

  SVT_STATE.cart.push(cartItem);
  saveCart();
  updateCartUI();
  toggleCartDrawer(true);
  showToast(`Added ${c.garmentName} to your order bag!`);
};

// Cart Drawer & Checkout Handlers
function saveCart() {
  localStorage.setItem('svt_cart', JSON.stringify(SVT_STATE.cart));
}

function updateCartUI() {
  const badge = document.getElementById('cartBadge');
  const count = SVT_STATE.cart.length;
  if (badge) badge.textContent = count;

  const itemsContainer = document.getElementById('cartItemsList');
  const footerCount = document.getElementById('cartFooterCount');

  if (footerCount) footerCount.textContent = `${count} Garment${count !== 1 ? 's' : ''}`;

  if (!itemsContainer) return;

  if (count === 0) {
    itemsContainer.innerHTML = `
      <div style="text-align: center; padding: 40px 20px; color: var(--gray-600);">
        <i class="fas fa-shopping-bag" style="font-size: 3rem; color: #cbd5e1; margin-bottom: 14px;"></i>
        <h4>Your Order Bag is Empty</h4>
        <p style="font-size: 0.85rem; margin-top: 6px;">Select a gents garment from the catalog or customize your bespoke fit above!</p>
      </div>
    `;
    return;
  }

  itemsContainer.innerHTML = SVT_STATE.cart.map((item, idx) => `
    <div class="cart-item">
      <div class="cart-item-info">
        <h4>${item.title}</h4>
        <p><strong>Fabric:</strong> ${item.fabric}</p>
        <p><strong>Fit & Sizing:</strong> ${item.measurements}</p>
        ${item.express ? '<p style="color: #b45309; font-weight: 700;">⚡ Priority Tatkal 24-48hr Stitching</p>' : ''}
        ${item.notes ? `<p style="font-size: 0.75rem; color: #64748b;"><em>"${item.notes}"</em></p>` : ''}
      </div>
      <button class="cart-item-remove" onclick="removeCartItem(${idx})" title="Remove item">
        <i class="fas fa-trash-alt"></i>
      </button>
    </div>
  `).join('');
}

window.removeCartItem = function(idx) {
  SVT_STATE.cart.splice(idx, 1);
  saveCart();
  updateCartUI();
  showToast('Item removed from order bag');
};

window.toggleCartDrawer = function(forceOpen = null) {
  const drawer = document.getElementById('cartDrawer');
  const backdrop = document.getElementById('cartBackdrop');
  if (!drawer || !backdrop) return;

  const isOpen = forceOpen !== null ? forceOpen : !drawer.classList.contains('active');
  if (isOpen) {
    drawer.classList.add('active');
    backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  } else {
    drawer.classList.remove('active');
    backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }
};

// Helper to save order/booking to MySQL backend
async function syncBookingToDB(payload) {
  try {
    const res = await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      return data;
    }
  } catch (err) {
    console.log('[API Notice] DB sync queued locally or server offline:', err);
  }
  return null;
}

// Checkout via WhatsApp (Without price tags)
window.checkoutWhatsApp = async function() {
  if (SVT_STATE.cart.length === 0) {
    showToast('Please add garments to your bag first!');
    return;
  }

  const customerName = document.getElementById('checkoutName')?.value.trim() || 'Valued Customer';
  const customerPhone = document.getElementById('checkoutPhone')?.value.trim() || 'Not Provided';
  const customerArea = document.getElementById('checkoutArea')?.value.trim() || 'Vijayawada';
  let orderId = 'SVT-' + Math.floor(1000 + Math.random() * 9000);

  // Sync with MySQL database
  if (customerPhone && customerPhone !== 'Not Provided') {
    const garmentsSummary = SVT_STATE.cart.map(i => `${i.title} (${i.fabric}, ${i.measurements})`).join('; ');
    const stdSize = document.getElementById('standardSizeSelect')?.value;
    const chest = document.getElementById('inputChest')?.value;
    const waist = document.getElementById('inputWaist')?.value;

    const dbRes = await syncBookingToDB({
      name: customerName,
      mobile: customerPhone,
      locality: customerArea,
      pref_date: new Date().toISOString().split('T')[0],
      pref_time: '10:00:00',
      garnments: garmentsSummary,
      shirt_size: stdSize || (chest ? `Chest ${chest}"` : null),
      pant_size: waist ? `Waist ${waist}"` : null
    });

    if (dbRes && dbRes.booking_id) {
      orderId = `SVT-BK${dbRes.booking_id}`;
    }
  }

  let msg = `*🧵 NEW BESPOKE ORDER - S. V. T. TAILORS*\n`;
  msg += `_Eluru Road, Near Ram Mandiram, Governorpet, Vijayawada_\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `📋 *Order ID:* #${orderId}\n`;
  msg += `👤 *Customer:* ${customerName}\n`;
  msg += `📞 *Phone:* ${customerPhone}\n`;
  msg += `📍 *Location/Area:* ${customerArea}, Vijayawada\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `*ITEMS TO TAILOR:*\n`;

  SVT_STATE.cart.forEach((item, index) => {
    msg += `\n${index + 1}. *${item.title}*\n`;
    msg += `   • Fabric: ${item.fabric}\n`;
    msg += `   • Fit/Size: ${item.measurements}\n`;
    if (item.express) msg += `   • Speed: ⚡ Priority Tatkal (24-48 Hours)\n`;
    if (item.notes) msg += `   • Special Instructions: ${item.notes}\n`;
  });

  msg += `\n━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `_Please confirm my tailoring order and advise on fabric drop-off / doorstep measurement._`;

  const encodedMsg = encodeURIComponent(msg);
  const waUrl = `https://wa.me/${SVT_STATE.phone}?text=${encodedMsg}`;
  
  // Show Receipt Modal & Open WhatsApp
  showReceiptModal({
    orderId,
    customerName,
    customerPhone,
    customerArea,
    items: [...SVT_STATE.cart]
  });

  window.open(waUrl, '_blank');
};

// Checkout Website Direct (Digital Receipt Summary)
window.checkoutDirect = async function() {
  if (SVT_STATE.cart.length === 0) {
    showToast('Please add garments to your bag first!');
    return;
  }

  const nameInput = document.getElementById('checkoutName');
  const phoneInput = document.getElementById('checkoutPhone');
  const areaInput = document.getElementById('checkoutArea');

  const customerName = nameInput?.value.trim() || 'Valued Customer';
  const customerPhone = phoneInput?.value.trim() || 'N/A';
  const customerArea = areaInput?.value.trim() || 'Governorpet, Vijayawada';
  let orderId = 'SVT-' + Math.floor(1000 + Math.random() * 9000);

  // Sync to database
  if (customerPhone && customerPhone !== 'N/A') {
    const garmentsSummary = SVT_STATE.cart.map(i => `${i.title} (${i.fabric}, ${i.measurements})`).join('; ');
    const stdSize = document.getElementById('standardSizeSelect')?.value;
    const chest = document.getElementById('inputChest')?.value;
    const waist = document.getElementById('inputWaist')?.value;

    const dbRes = await syncBookingToDB({
      name: customerName,
      mobile: customerPhone,
      locality: customerArea,
      pref_date: new Date().toISOString().split('T')[0],
      pref_time: '10:00:00',
      garnments: garmentsSummary,
      shirt_size: stdSize || (chest ? `Chest ${chest}"` : null),
      pant_size: waist ? `Waist ${waist}"` : null
    });

    if (dbRes && dbRes.booking_id) {
      orderId = `SVT-BK${dbRes.booking_id}`;
    }
  }

  showReceiptModal({
    orderId,
    customerName,
    customerPhone,
    customerArea,
    items: [...SVT_STATE.cart]
  });
};

// Show Receipt Modal (No price tags)
function showReceiptModal(order) {
  const modalBackdrop = document.getElementById('receiptModalBackdrop');
  const content = document.getElementById('receiptContent');
  if (!modalBackdrop || !content) return;

  // Save order to tracking storage
  saveOrderForTracking(order);

  content.innerHTML = `
    <div class="receipt-success-badge">
      <i class="fas fa-check"></i>
    </div>
    <div style="text-align: center; margin-bottom: 20px;">
      <h3 style="font-size: 1.5rem; color: var(--primary);">Tailoring Order Logged!</h3>
      <p style="color: var(--secondary-hover); font-weight: 700; letter-spacing: 1px;">ORDER ID: #${order.orderId}</p>
      <small style="color: var(--gray-600);">S. V. T. Tailors • Eluru Road, Governorpet, Vijayawada</small>
    </div>

    <div style="background: var(--cream); border-radius: var(--radius-md); padding: 18px; margin-bottom: 20px; font-size: 0.88rem;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
        <span><strong>Client:</strong> ${order.customerName}</span>
        <span><strong>Phone:</strong> ${order.customerPhone}</span>
      </div>
      <div><strong>Vijayawada Address:</strong> ${order.customerArea}</div>
      <div style="margin-top: 6px;"><strong>Status:</strong> <span style="color: var(--emerald); font-weight: 700;">Order Logged • Fabric Assignment</span></div>
    </div>

    <div style="margin-bottom: 20px;">
      <h4 style="font-size: 0.95rem; margin-bottom: 10px; border-bottom: 1px solid var(--gray-300); padding-bottom: 6px;">Garment Summary (${order.items.length} Item${order.items.length !== 1 ? 's' : ''})</h4>
      ${order.items.map(item => `
        <div style="font-size: 0.85rem; margin-bottom: 10px; background: #fff; padding: 10px; border: 1px solid var(--gray-300); border-radius: 6px;">
          <strong style="color: var(--primary); font-size: 0.92rem;">${item.title}</strong><br>
          <small style="color: var(--gray-600);">${item.fabric} • ${item.measurements}</small>
          ${item.notes ? `<br><small style="color: #64748b;"><em>Note: ${item.notes}</em></small>` : ''}
        </div>
      `).join('')}
    </div>

    <div style="display: flex; flex-direction: column; gap: 10px;">
      <a href="https://wa.me/${SVT_STATE.phone}?text=Hello%20SVT%20Tailors,%20I%20placed%20Order%20%23${order.orderId}.%20Please%20confirm." target="_blank" class="btn-checkout-wa" style="text-decoration: none;">
        <i class="fab fa-whatsapp"></i> Chat with Master Tailor on WhatsApp
      </a>
      <button class="btn-secondary-outline" style="color: var(--primary); border-color: var(--primary);" onclick="window.print()">
        <i class="fas fa-print"></i> Print / Save Order Summary
      </button>
      <button class="btn-track" style="justify-content: center; width: 100%;" onclick="trackThisOrder('${order.orderId}')">
        <i class="fas fa-search"></i> Track Live Status of #${order.orderId}
      </button>
    </div>
  `;

  // Clear cart after placement
  SVT_STATE.cart = [];
  saveCart();
  updateCartUI();
  toggleCartDrawer(false);

  modalBackdrop.classList.add('active');
  triggerConfetti();
}

window.closeReceiptModal = function() {
  const modalBackdrop = document.getElementById('receiptModalBackdrop');
  if (modalBackdrop) modalBackdrop.classList.remove('active');
};

// Visual Guide Hotspots
function setupVisualGuideHotspots() {
  const hotspots = document.querySelectorAll('.measure-hotspot');
  const titleEl = document.getElementById('guideSpotTitle');
  const textEl = document.getElementById('guideSpotText');
  const tipEl = document.getElementById('guideSpotTip');

  const guideData = {
    'neck': {
      title: 'Collar & Neck Measurement',
      text: 'Wrap the measuring tape around the base of your neck where your shirt collar rests. Allow one finger space between the tape and neck for comfort.',
      tip: 'Pro Tip: For stiff formal Italian collars, keep exact snug measurement. For casual kurtas, add 0.5 inches.'
    },
    'chest': {
      title: 'Chest Measurement',
      text: 'Stand naturally. Measure around the fullest part of your chest, keeping the tape level parallel to the floor and snug under the armpits.',
      tip: 'Pro Tip: Do not puff up or suck in your chest. Breathe normally for a natural bespoke silhouette.'
    },
    'shoulder': {
      title: 'Shoulder Point-to-Point',
      text: 'Measure from the tip of the left shoulder bone, following the natural curve of the neck base, across to the tip of the right shoulder bone.',
      tip: 'Pro Tip: Wearing a well-fitted shirt makes it easy to measure exactly from seam to seam.'
    },
    'sleeve': {
      title: 'Sleeve Length',
      text: 'From the outer edge of your shoulder bone down the outside of your slightly bent arm to the base of the thumb or desired cuff edge.',
      tip: 'Pro Tip: Bespoke suits look sharp when 1/4 to 1/2 inch of shirt cuff peeks out under jacket sleeves.'
    },
    'waist': {
      title: 'Waist & Trouser Belt Line',
      text: 'Measure around your natural waistline where you prefer wearing trousers or safari bottoms. Keep one finger between tape and body.',
      tip: 'Pro Tip: High-rise trousers sit near the belly button; mid-rise sit 1-2 inches below.'
    },
    'inseam': {
      title: 'Trouser Inseam / Full Length',
      text: 'Measure from the inner crotch down the inside of the leg to the top of your shoes where the trouser fabric breaks.',
      tip: 'Pro Tip: Specify whether you prefer No Break (modern cropped), Half Break (classic), or Full Break.'
    }
  };

  hotspots.forEach(spot => {
    spot.addEventListener('click', () => {
      hotspots.forEach(s => s.classList.remove('active'));
      spot.classList.add('active');
      const point = spot.getAttribute('data-point');
      const data = guideData[point];
      if (data && titleEl && textEl && tipEl) {
        titleEl.textContent = data.title;
        textEl.textContent = data.text;
        tipEl.textContent = data.tip;
      }
    });
  });
}

// Order Tracker
function setupOrderTracker() {
  const btn = document.getElementById('btnSearchTrack');
  const input = document.getElementById('trackOrderInput');

  if (btn && input) {
    btn.addEventListener('click', () => {
      runTracking(input.value.trim());
    });
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') runTracking(input.value.trim());
    });
  }
}

window.trackThisOrder = function(orderId) {
  closeReceiptModal();
  const trackSection = document.getElementById('trackerSection');
  const input = document.getElementById('trackOrderInput');
  if (trackSection) {
    trackSection.scrollIntoView({ behavior: 'smooth' });
    if (input) input.value = orderId;
    runTracking(orderId);
  }
};

async function runTracking(id) {
  const resultBox = document.getElementById('trackResultBox');
  if (!resultBox) return;

  if (!id) {
    showToast('Please enter an Order ID or Mobile Number');
    return;
  }

  // Attempt to fetch live booking details from MySQL database
  let dbBooking = null;
  try {
    const res = await fetch(`/api/track?q=${encodeURIComponent(id)}`);
    if (res.ok) {
      const json = await res.json();
      if (json.bookings && json.bookings.length > 0) {
        dbBooking = json.bookings[0];
      }
    }
  } catch (e) {
    console.log('[Track Notice] Server offline, using local tracker mode:', e);
  }

  const isDemo = id.toUpperCase() === 'SVT-1965' || id.toUpperCase() === 'SVT-7821';
  const stage = dbBooking ? 2 : (isDemo ? 3 : 2); // stage 1 to 5

  const steps = [
    { title: 'Order Logged', date: dbBooking ? (dbBooking.pref_date || 'Day 0') : 'Same Day' },
    { title: 'Fabric Cut', date: 'Day 1' },
    { title: 'Master Stitch', date: 'Day 2-3' },
    { title: 'Steam Press', date: 'Day 4' },
    { title: 'Ready for You', date: 'Day 5' }
  ];

  const clientName = dbBooking ? dbBooking.name : 'Valued Client';
  const displayId = dbBooking ? `SVT-BK${dbBooking.booking_id}` : id.toUpperCase();
  const garments = dbBooking ? dbBooking.garnments : null;
  const locality = dbBooking ? dbBooking.locality : null;
  const sizes = dbBooking && (dbBooking.shirt_size || dbBooking.pant_size) 
    ? `Shirt: ${dbBooking.shirt_size || 'Custom'}, Pant: ${dbBooking.pant_size || 'Custom'}`
    : null;

  resultBox.style.display = 'block';
  resultBox.innerHTML = `
    <div style="border-top: 1px solid var(--gray-300); padding-top: 24px; margin-top: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
        <div>
          <h4 style="font-size: 1.15rem; color: var(--primary); margin-bottom: 4px;">
            Tracking Order #${displayId}
          </h4>
          <p style="font-size: 0.88rem; color: var(--gray-700); margin-bottom: 2px;">
            👤 <strong>Customer:</strong> ${clientName} ${locality ? `• 📍 ${locality}` : ''}
          </p>
          ${garments ? `<p style="font-size: 0.82rem; color: var(--gray-600); margin-bottom: 2px;">👔 <strong>Garments:</strong> ${garments}</p>` : ''}
          ${sizes ? `<p style="font-size: 0.82rem; color: var(--secondary-hover); font-weight: 600;">📏 <strong>Recorded Measurements:</strong> ${sizes}</p>` : ''}
          <p style="font-size: 0.85rem; color: var(--emerald); font-weight: 700; margin-top: 4px;">
            <i class="fas fa-spinner fa-spin"></i> Active at Governorpet Atelier
          </p>
        </div>
        <a href="https://wa.me/${SVT_STATE.phone}?text=Status%20update%20for%20order%20${displayId}" target="_blank" class="btn-track" style="font-size: 0.8rem;">
          <i class="fab fa-whatsapp"></i> Inquire on WhatsApp
        </a>
      </div>

      <div class="tracker-timeline">
        <div class="tracker-progress-bar" style="width: ${(stage - 1) * 25}%"></div>
        ${steps.map((s, idx) => {
          let statusClass = '';
          if (idx + 1 < stage) statusClass = 'completed';
          else if (idx + 1 === stage) statusClass = 'current';
          return `
            <div class="tracker-step ${statusClass}">
              <div class="tracker-icon">
                <i class="fas ${idx + 1 < stage ? 'fa-check' : (idx + 1 === stage ? 'fa-user-tie' : 'fa-clock')}"></i>
              </div>
              <span>${s.title}</span>
              <small style="color: var(--gray-600); font-size: 0.7rem;">${s.date}</small>
            </div>
          `;
        }).join('')}
      </div>

      <div style="background: var(--cream); border-radius: var(--radius-sm); padding: 14px; margin-top: 24px; font-size: 0.85rem; color: var(--gray-700);">
        <strong>Master Tailor Note:</strong> Pattern cutting &amp; fabric alignment confirmed for ${clientName}. Hand-finishing in progress under Master Sri Subba Rao garu. Delivery scheduled on time!
      </div>
    </div>
  `;
}
window.runTracking = runTracking;

function saveOrderForTracking(order) {
  let existing = JSON.parse(localStorage.getItem('svt_orders')) || [];
  existing.unshift(order);
  localStorage.setItem('svt_orders', JSON.stringify(existing.slice(0, 10)));
}

// Doorstep Measurement Form in Vijayawada & Outstation
function setupDoorstepForm() {
  const form = document.getElementById('doorstepForm');
  if (!form) return;

  const areaSelect = document.getElementById('dsArea');
  const otherGroup = document.getElementById('dsOtherAreaGroup');
  const otherInput = document.getElementById('dsOtherAreaInput');

  if (areaSelect && otherGroup) {
    areaSelect.addEventListener('change', () => {
      const isOther = areaSelect.value.startsWith('Other');
      otherGroup.style.display = isOther ? 'block' : 'none';
      if (isOther && otherInput) {
        otherInput.focus();
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('dsName').value.trim();
    const phone = document.getElementById('dsPhone').value.trim();
    const area = document.getElementById('dsArea').value;
    const isOutstation = area.startsWith('Other');
    const specificLoc = otherInput ? otherInput.value.trim() : '';
    const locality = isOutstation ? (specificLoc || 'Outside Vijayawada') : area;
    const date = document.getElementById('dsDate').value;
    const time = document.getElementById('dsTime').value;
    const garments = document.getElementById('dsGarments').value.trim();

    // Sync with MySQL database
    let bookingRef = '';
    const dbRes = await syncBookingToDB({
      name: name,
      mobile: phone,
      locality: locality,
      pref_date: date,
      pref_time: time,
      garnments: garments
    });
    if (dbRes && dbRes.booking_id) {
      bookingRef = `#SVT-BK${dbRes.booking_id}`;
    }

    let text = `*🛵 DOORSTEP & HOME VISIT BOOKING - S. V. T. TAILORS*\n`;
    text += `━━━━━━━━━━━━━━━━━━━━\n`;
    if (bookingRef) text += `📋 *Booking ID:* ${bookingRef}\n`;
    text += `👤 *Client Name:* ${name}\n`;
    text += `📞 *Phone:* ${phone}\n`;
    if (isOutstation) {
      text += `🚀 *Service Type:* Outstation / Far From City Client\n`;
      text += `📍 *Town / Area / Landmark:* ${specificLoc || 'Outside Vijayawada'}\n`;
    } else {
      text += `📍 *Vijayawada Locality:* ${area}\n`;
    }
    text += `📅 *Preferred Date:* ${date}\n`;
    text += `⏰ *Preferred Slot:* ${time}\n`;
    text += `👔 *Garments to Stitch:* ${garments}\n`;
    text += `━━━━━━━━━━━━━━━━━━━━\n`;
    text += isOutstation 
      ? `_Requesting master tailor outstation appointment or video measurement session._`
      : `_Please confirm appointment for master tailor home visit._`;

    const waUrl = `https://wa.me/${SVT_STATE.phone}?text=${encodeURIComponent(text)}`;
    window.open(waUrl, '_blank');
    showToast(bookingRef ? `Booking ${bookingRef} saved to database! Opening WhatsApp...` : 'Home visit booking requested! Opening WhatsApp...');
    form.reset();
    if (otherGroup) otherGroup.style.display = 'none';
  });
}

// Quick WhatsApp Inquiry
window.quickInquiry = function(garmentName) {
  const msg = `Hello S. V. T. Tailors, I would like to inquire about bespoke stitching for *${garmentName}*. Please let me know available slots, fabric suggestions, and turnaround time.`;
  window.open(`https://wa.me/${SVT_STATE.phone}?text=${encodeURIComponent(msg)}`, '_blank');
};

// Toast notification helper
function showToast(message) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<i class="fas fa-info-circle" style="color: var(--secondary);"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Mobile Menu Toggle
function setupMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const menu = document.getElementById('navMenu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      menu.classList.toggle('active-mobile');
    });
    // Close on link click
    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('active-mobile');
      });
    });
  }
}

// Navbar scroll shadow
function setupNavScroll() {
  window.addEventListener('scroll', () => {
    const nav = document.querySelector('.main-nav');
    if (nav) {
      if (window.scrollY > 40) {
        nav.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
      } else {
        nav.style.boxShadow = 'none';
      }
    }
  });
}

// Confetti animation on order placement
function triggerConfetti() {
  const count = 50;
  const colors = ['#d4af37', '#0b1528', '#25d366', '#c59b27', '#ffffff'];

  for (let i = 0; i < count; i++) {
    const el = document.createElement('div');
    el.style.position = 'fixed';
    el.style.zIndex = '9999';
    el.style.width = Math.random() * 8 + 6 + 'px';
    el.style.height = Math.random() * 8 + 6 + 'px';
    el.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    el.style.left = Math.random() * 100 + 'vw';
    el.style.top = '-20px';
    el.style.borderRadius = '50%';
    el.style.pointerEvents = 'none';
    el.style.opacity = '1';
    el.style.transition = `transform ${Math.random() * 2 + 1.5}s cubic-bezier(0.25, 1, 0.5, 1), opacity 2s ease`;
    document.body.appendChild(el);

    setTimeout(() => {
      el.style.transform = `translate(${Math.random() * 200 - 100}px, ${window.innerHeight + 50}px) rotate(${Math.random() * 360}deg)`;
      el.style.opacity = '0';
    }, 20);

    setTimeout(() => el.remove(), 3500);
  }
}
