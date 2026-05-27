/**
 * invoiceGenerator.js
 * Gera e abre uma nota fiscal em HTML/CSS para impressão ou download como PDF.
 */

function fmt(value) {
  const amount = Number(value || 0);
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(amount);
}

function fmtDate(value) {
  if (!value) return '-';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return '-';
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(parsed);
}

function fmtAddress(address) {
  if (!address) return 'Endereço não disponível';
  const parts = [
    [address.street, address.number].filter(Boolean).join(', '),
    address.complement,
    address.neighborhood,
    [address.city, address.state].filter(Boolean).join(' - '),
    address.postal_code ? `CEP ${address.postal_code}` : '',
  ].filter(Boolean);
  return parts.join(', ') || 'Endereço não disponível';
}

function fmtDoc(type, number) {
  if (!type || !number) return number || '-';
  return `${type}: ${number}`;
}

function statusLabel(status) {
  const map = {
    CONFIRMED: 'Confirmado',
    DELIVERED: 'Entregue',
    CANCELED: 'Cancelado',
    PENDING: 'Pendente',
  };
  return map[status] || status || '-';
}

function statusColor(status) {
  const map = {
    CONFIRMED: '#059669',
    DELIVERED: '#0284c7',
    CANCELED: '#e11d48',
    PENDING: '#d97706',
  };
  return map[status] || '#64748b';
}

function buildInvoiceHtml(order) {
  const producer = order.producer_data || {};
  const retailer = order.retailer_data || {};
  const items = Array.isArray(order.items) ? order.items : [];
  const issueDate = fmtDate(order.created_at);
  const orderNumber = order.id;

  const itemRows = items
    .map((item) => {
      const product = item.product_data || {};
      const qty = Number(item.quantity || 0);
      const unitPrice = Number(item.unit_price || 0);
      const totalItem = qty * unitPrice;
      return `
        <tr>
          <td>${product.name || `Produto #${item.product}`}</td>
          <td>${product.category_name || '-'}</td>
          <td class="center">${qty}</td>
          <td class="right">${fmt(unitPrice)}</td>
          <td class="right">${fmt(totalItem)}</td>
        </tr>`;
    })
    .join('');

  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Nota Fiscal — Pedido #${orderNumber}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --green: #15803d;
      --green-light: #dcfce7;
      --green-dark: #052e16;
      --ink: #0f172a;
      --muted: #64748b;
      --border: #e2e8f0;
      --bg: #f8fafc;
      --white: #ffffff;
    }

    html, body {
      font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif;
      font-size: 14px;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.6;
    }

    .page {
      max-width: 820px;
      margin: 0 auto;
      background: var(--white);
      padding: 0;
      min-height: 100vh;
    }

    /* ── Header ── */
    .header {
      background: var(--green-dark);
      color: var(--white);
      padding: 40px 48px 32px;
      position: relative;
      overflow: hidden;
    }

    .header::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 60% 80% at 90% 50%, #14532d44 0%, transparent 70%);
    }

    .header-inner {
      position: relative;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 24px;
    }

    .header-brand {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .brand-name {
      font-family: 'DM Serif Display', Georgia, serif;
      font-size: 28px;
      letter-spacing: -0.5px;
      color: var(--white);
    }

    .brand-tagline {
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #86efac;
    }

    .header-meta {
      text-align: right;
    }

    .invoice-label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.26em;
      text-transform: uppercase;
      color: #86efac;
      margin-bottom: 6px;
    }

    .invoice-number {
      font-family: 'DM Serif Display', Georgia, serif;
      font-size: 36px;
      color: var(--white);
      letter-spacing: -1px;
    }

    .invoice-date {
      font-size: 12px;
      color: #a7f3d0;
      margin-top: 4px;
    }

    /* ── Status bar ── */
    .status-bar {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
      background: #f0fdf4;
      border-bottom: 1px solid var(--border);
      padding: 10px 48px;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: ${statusColor(order.status)};
    }

    .status-text {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: ${statusColor(order.status)};
    }

    /* ── Content ── */
    .content {
      padding: 40px 48px;
    }

    /* ── Parties ── */
    .parties-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 36px;
    }

    .party-card {
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px 22px;
      background: #fafafa;
    }

    .party-role {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      color: var(--green);
      margin-bottom: 10px;
    }

    .party-name {
      font-size: 16px;
      font-weight: 700;
      color: var(--ink);
      margin-bottom: 2px;
    }

    .party-trade {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 10px;
    }

    .party-detail {
      font-size: 12px;
      color: var(--muted);
      line-height: 1.7;
    }

    /* ── Divider ── */
    .section-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      color: var(--green);
      margin-bottom: 14px;
    }

    /* ── Items table ── */
    .items-section {
      margin-bottom: 36px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    thead tr {
      background: var(--green-dark);
      color: var(--white);
    }

    thead th {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      padding: 10px 14px;
      text-align: left;
    }

    thead th.right { text-align: right; }
    thead th.center { text-align: center; }

    tbody tr {
      border-bottom: 1px solid var(--border);
    }

    tbody tr:last-child {
      border-bottom: none;
    }

    tbody tr:nth-child(even) {
      background: #f8fafc;
    }

    tbody td {
      padding: 12px 14px;
      font-size: 13px;
      color: var(--ink);
    }

    tbody td.right { text-align: right; font-weight: 600; }
    tbody td.center { text-align: center; }

    /* ── Totals ── */
    .totals-section {
      margin-bottom: 36px;
    }

    .totals-box {
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      margin-left: auto;
      max-width: 320px;
    }

    .totals-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 11px 20px;
      font-size: 13px;
      border-bottom: 1px solid var(--border);
    }

    .totals-row:last-child {
      border-bottom: none;
    }

    .totals-row.grand {
      background: var(--green-dark);
      color: var(--white);
      padding: 14px 20px;
    }

    .totals-label { color: var(--muted); }
    .totals-value { font-weight: 700; }

    .grand .totals-label { color: #a7f3d0; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; }
    .grand .totals-value { font-size: 20px; font-family: 'DM Serif Display', Georgia, serif; }

    /* ── Footer ── */
    .footer {
      border-top: 1px solid var(--border);
      padding: 20px 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .footer-note {
      font-size: 11px;
      color: var(--muted);
    }

    .footer-brand {
      font-family: 'DM Serif Display', Georgia, serif;
      font-size: 14px;
      color: var(--green);
    }

    /* ── Print ── */
    @media print {
      html, body { background: var(--white); }
      .page { margin: 0; box-shadow: none; }
      .no-print { display: none !important; }
    }

    @page {
      size: A4;
      margin: 0;
    }
  </style>
</head>
<body>
  <div class="page">

    <!-- Header -->
    <div class="header">
      <div class="header-inner">
        <div class="header-brand">
          <div class="brand-name">🌿 Cultiva</div>
          <div class="brand-tagline">Plataforma de Agricultura Familiar</div>
        </div>
        <div class="header-meta">
          <div class="invoice-label">Nota Fiscal</div>
          <div class="invoice-number">#${String(orderNumber).padStart(5, '0')}</div>
          <div class="invoice-date">Emitida em ${issueDate}</div>
        </div>
      </div>
    </div>

    <!-- Status bar -->
    <div class="status-bar">
      <div class="status-dot"></div>
      <div class="status-text">${statusLabel(order.status)}</div>
    </div>

    <!-- Content -->
    <div class="content">

      <!-- Parties -->
      <div class="parties-grid">
        <div class="party-card">
          <div class="party-role">Produtor (Vendedor)</div>
          <div class="party-name">${producer.name || '-'}</div>
          <div class="party-trade">${producer.trade_name || ''}</div>
          <div class="party-detail">
            ${fmtDoc(producer.document_type, producer.document_number)}<br/>
            ${fmtAddress(producer.address)}<br/>
            ${producer.email || ''}
          </div>
        </div>

        <div class="party-card">
          <div class="party-role">Varejista (Comprador)</div>
          <div class="party-name">${retailer.name || '-'}</div>
          <div class="party-trade">${retailer.trade_name || ''}</div>
          <div class="party-detail">
            ${fmtDoc(retailer.document_type, retailer.document_number)}<br/>
            ${fmtAddress(retailer.address)}<br/>
            ${retailer.email || ''}
          </div>
        </div>
      </div>

      <!-- Items -->
      <div class="items-section">
        <div class="section-label">Itens do Pedido</div>
        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Categoria</th>
              <th class="center">Qtd.</th>
              <th class="right">Preço Unit.</th>
              <th class="right">Total</th>
            </tr>
          </thead>
          <tbody>
            ${itemRows}
          </tbody>
        </table>
      </div>

      <!-- Totals -->
      <div class="totals-section">
        <div class="totals-box">
          <div class="totals-row">
            <span class="totals-label">Subtotal</span>
            <span class="totals-value">${fmt(order.subtotal_value)}</span>
          </div>
          <div class="totals-row">
            <span class="totals-label">Taxa de serviço (5%)</span>
            <span class="totals-value">${fmt(order.fee_value)}</span>
          </div>
          <div class="totals-row grand">
            <span class="totals-label">Total</span>
            <span class="totals-value">${fmt(order.total_value)}</span>
          </div>
        </div>
      </div>

    </div><!-- /content -->

    <!-- Footer -->
    <div class="footer">
      <div class="footer-note">
        Documento gerado automaticamente pela plataforma Cultiva em ${issueDate}.<br/>
        Este documento não tem valor fiscal legal.
      </div>
      <div class="footer-brand">Cultiva</div>
    </div>

  </div>
</body>
</html>`;
}

/**
 * Abre uma nova janela com a nota fiscal em HTML e dispara o diálogo de impressão/PDF.
 * @param {Object} order - Objeto bruto do pedido retornado pela API.
 */
export function downloadInvoice(order) {
  const html = buildInvoiceHtml(order);
  const win = window.open('', '_blank', 'width=900,height=700');
  if (!win) {
    alert('Por favor, permita popups para baixar a nota fiscal.');
    return;
  }
  win.document.write(html);
  win.document.close();
  win.focus();
  // Aguarda fonts carregarem antes de imprimir
  setTimeout(() => {
    win.print();
  }, 800);
}
