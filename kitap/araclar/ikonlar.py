"""Kutu etiketlerinde kullanılan küçük SVG ikonlar (beyaz çizgi, 24x24)."""

def _svg(ic):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round">' + ic + '</svg>')

IKONLAR = {
    "kavram": _svg('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.4 1.1 2.2h5c0-.8.3-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>'),
    "hayat": _svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>'),
    "dikkat": _svg('<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/>'),
    "ornek": _svg('<path d="M4 20l4-1 11-11-3-3L5 16l-1 4z"/><path d="M14 6l3 3"/>'),
    "ipucu": _svg('<path d="M7 3v18M17 3v18M7 8h10M7 13h10M7 18h10"/>'),
    "hata": _svg('<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21M8 8l5 5M13 8l-5 5"/>'),
    "hedef": _svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
    "test": _svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
    "lab": _svg('<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>'),
}
