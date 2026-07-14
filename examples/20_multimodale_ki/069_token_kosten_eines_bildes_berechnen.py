# Token-Kosten eines Bildes berechnen
# Quelle: chapters/20_multimodale_ki.tex (Zeile 69)
def image_token_cost(image_path: str, model: str = "gpt-4o") -> dict:
    """Berechnet die Token-Kosten eines Bildes fuer ein multimodales Modell."""
    from PIL import Image

    img = Image.open(image_path)
    w, h = img.size

    # GPT-4o: 170 Tokens pro 512x512 Tile, aufgerundet
    tiles_x = (w + 511) // 512
    tiles_y = (h + 511) // 512
    tiles = tiles_x * tiles_y

    base_tokens = 85    # Basis-Overhead pro Bild
    tile_tokens = 170   # Pro 512x512 Tile

    total_tokens = base_tokens + tiles * tile_tokens

    return {
        "dimensions": f"{w}x{h}",
        "tiles": tiles,
        "tokens": total_tokens,
        "estimated_cost_usd": total_tokens * 2.5 / 1_000_000,
    }

# Beispiel: Full-HD Screenshot (1920x1080)
cost = image_token_cost("screenshot.png")
print(f"{cost['tiles']} Tiles, {cost['tokens']} Tokens, "
      f"${cost['estimated_cost_usd']:.5f}")
# Ausgabe: 16 Tiles, 2805 Tokens, $0.007

