# Instruction-Dataset im Chat-Format
# Quelle: chapters/18_modellanpassung.tex (Zeile 211)
DATASET = [
    {
        "messages": [
            {
                "role": "system",
                "content": "Du bist ein SQL-Experte. "
                           "Generiere nur SQL-Queries, keine Erklaerungen.",
            },
            {
                "role": "user",
                "content": "Finde alle Kunden, die in den letzten 30 Tagen "
                           "mehr als 500 EUR ausgegeben haben.",
            },
            {
                "role": "assistant",
                "content": (
                    "SELECT c.customer_id, c.name, SUM(o.total) as total_spent\n"
                    "FROM customers c\n"
                    "JOIN orders o ON c.customer_id = o.customer_id\n"
                    "WHERE o.order_date >= DATE('now', '-30 days')\n"
                    "GROUP BY c.customer_id\n"
                    "HAVING total_spent > 500\n"
                    "ORDER BY total_spent DESC;"
                ),
            },
        ]
    },
    # 500+ weitere Beispiele
]

