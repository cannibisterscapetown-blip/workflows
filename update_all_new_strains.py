
import subprocess

products = [
    {
        "id": "9016555864276",
        "name": "Sticky Rice",
        "metafields_file": "sticky_rice_metafields.json",
        "tags": "New Strains, Hybrid, Indica Leaning, Creative, Relaxed, Candy, Gas",
        "description": "<p>Experience the best of both worlds with <strong>Sticky Rice</strong>, a potent hybrid crossing Lemon Cherry Gelato and Permanent Marker. Expect a surge of creative energy and focus that settles into a soothing, full-body relaxation. With flavours of sweet candy and gas, it's perfect for managing stress while staying productive.</p><ul><li><strong>Lineage:</strong> Lemon Cherry Gelato x Permanent Marker</li><li><strong>Effects:</strong> Creative, Focused, Relaxed</li></ul>"
    },
    {
        "id": "9016556454100",
        "name": "Lit Pineapple",
        "metafields_file": "lit_pineapple_metafields.json",
        "tags": "New Strains, Sativa, Tropical, Pineapple, Energetic, Euphoric",
        "description": "<p>Light up your day with <strong>Lit Pineapple</strong>, a sativa-dominant treat bursting with tropical flavour. Combining Pina Acai and LIT OG genetics, this strain delivers an energetic and euphoric high ideal for social gatherings or creative endeavours. Enjoy notes of fresh pineapple and citrus in every puff.</p><ul><li><strong>Lineage:</strong> Pina Acai x LIT OG</li><li><strong>Effects:</strong> Energetic, Euphoric, Uplifted</li></ul>"
    },
    {
        "id": "9016555995348",
        "name": "Highlighter",
        "metafields_file": "highlighter_metafields.json",
        "tags": "New Strains, Hybrid, Relaxed, Earthy, Gas, Meditative",
        "description": "<p>Unwind with <strong>Highlighter</strong>, a unique cross of Bubble Bath and Permanent Marker. This hybrid offers a robust, tranquilising high that melts away tension while keeping your mind happy and meditative. Its complex profile features soapy, earthy, and piney notes for a truly distinct experience.</p><ul><li><strong>Lineage:</strong> Bubble Bath x Permanent Marker</li><li><strong>Effects:</strong> Relaxed, Meditative, Happy</li></ul>"
    }
]

for p in products:
    print(f"\n🚀 Updating {p['name']} ({p['id']})...")
    cmd = [
        "python3", "update_product.py",
        "--product-id", p["id"],
        "--description", p["description"],
        "--tags", p["tags"],
        "--metafields", p["metafields_file"],
        "--yes"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Finished {p['name']}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update {p['name']}: {e}")
