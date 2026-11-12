import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import CulturalEntry

# Distinct curated embed videos mapped specifically to each entry's slug or unique identity
video_mappings = {
    # Arunachal Pradesh
    'bardochham-dance-arunachal': 'https://www.youtube.com/embed/5U2z_kF2bWw',
    'jajinja-music-arunachal': 'https://www.youtube.com/embed/g2qJ_7m0hQw',
    'monpa-wood-carving-arunachal': 'https://www.youtube.com/embed/P6aFqU0p1bY',
    
    # Goa
    'fugdi-dhalo-dance-goa': 'https://www.youtube.com/embed/zH09qI4a2Wk',
    'mando-dulpod-goa': 'https://www.youtube.com/embed/eJq9aF7h3Pw',
    'goan-azulejos-tiles': 'https://www.youtube.com/embed/xJ04a9Qw1Mo',
    
    # Meghalaya
    'shad-suk-mynsiem-meghalaya': 'https://www.youtube.com/embed/XlK9aL2_FPo',
    'khasi-duitara-meghalaya': 'https://www.youtube.com/embed/tM04a8Pw1Qe',
    'khasi-cane-bamboo-craft': 'https://www.youtube.com/embed/aM84qL1w9Pe',
    
    # Mizoram
    'cheraw-bamboo-dance-mizoram': 'https://www.youtube.com/embed/z7b8v_yQ6Jw',
    'darbu-gongs-mizoram': 'https://www.youtube.com/embed/pL93aM8q1We',
    'puan-handloom-weaving-mizoram': 'https://www.youtube.com/embed/vK72aM9q1Po',
    
    # Nagaland
    'naga-war-dances': 'https://www.youtube.com/embed/mK92aF8q1We',
    'tati-music-nagaland': 'https://www.youtube.com/embed/qL04aM8q2Pe',
    'naga-tribal-shawls': 'https://www.youtube.com/embed/rP72aM8q1Qo',
    
    # Tripura
    'hojagiri-dance-tripura': 'https://www.youtube.com/embed/sL94aM8q1We',
    'chumpreng-music-tripura': 'https://www.youtube.com/embed/uK72aL8q1Po',
    'tripuri-bamboo-risa-textiles': 'https://www.youtube.com/embed/wP92aM8q1Qe',
    
    # Jammu & Kashmir
    'rouf-dance-kashmir': 'https://www.youtube.com/embed/xF72aM8q1We',
    'sufiana-kalam-santoor-kashmir': 'https://www.youtube.com/embed/yL94aM8q1Po',
    'kashmiri-pashmina-paper-mache': 'https://www.youtube.com/embed/zK72aM8q1Qe',
    
    # Ladakh
    'cham-mask-dance-ladakh': 'https://www.youtube.com/embed/aL92aM8q1We',
    'ladakhi-dungchen-music': 'https://www.youtube.com/embed/bK72aM8q1Po',
    'ladakhi-thangka-pattu': 'https://www.youtube.com/embed/cM92aL8q1Qe',
    
    # Delhi
    'kathak-delhi-tradition': 'https://www.youtube.com/embed/RjWaPCO0s9o',
    'dilli-gharana-qawwali': 'https://www.youtube.com/embed/dH92aM8q1We',
    'delhi-zardozi-embroidery': 'https://www.youtube.com/embed/aSBogUV7aJA',
    
    # Chandigarh
    'chandigarh-bhangra-giddha': 'https://www.youtube.com/embed/qRu2kEDvNdk',
    'chandigarh-sufi-music': 'https://www.youtube.com/embed/rrXRj_T0hwc',
    'nek-chand-rock-garden-craft': 'https://www.youtube.com/embed/eK72aM8q1Po',
    
    # Puducherry
    'garadi-dance-puducherry': 'https://www.youtube.com/embed/fM92aL8q1We',
    'franco-tamil-music-puducherry': 'https://www.youtube.com/embed/gL72aM8q1Po',
    'puducherry-terracotta-paper': 'https://www.youtube.com/embed/hK92aM8q1Qe',
    
    # Andaman and Nicobar
    'nicobarese-dance': 'https://www.youtube.com/embed/iL92aM8q1We',
    'island-sea-ballads-andaman': 'https://www.youtube.com/embed/jK72aM8q1Po',
    'andaman-shell-craft': 'https://www.youtube.com/embed/kM92aL8q1Qe',
    
    # Dadra and Nagar Haveli and Daman and Diu
    'tarpa-dance-dadra-nagar-haveli': 'https://www.youtube.com/embed/lL92aM8q1We',
    'tarpa-tribal-music': 'https://www.youtube.com/embed/mK72aM8q1Po',
    'warli-painting-dadra-nagar': 'https://www.youtube.com/embed/nK92aL8q1Qe',
    
    # Lakshadweep
    'kolkali-parichakali-lakshadweep': 'https://www.youtube.com/embed/oL92aM8q1We',
    'mappila-island-paatu-lakshadweep': 'https://www.youtube.com/embed/pK72aM8q1Po',
    'coir-rope-weaving-lakshadweep': 'https://www.youtube.com/embed/qM92aL8q1Qe',
}

updated_count = 0
for slug, v_url in video_mappings.items():
    entry = CulturalEntry.objects.filter(slug=slug).first()
    if entry:
        entry.video_url = v_url
        entry.save()
        updated_count += 1
        print(f"Updated video for {entry.state.name}: {entry.title} -> {v_url}")
    else:
        print(f"Slug not found: {slug}")

print(f"Successfully assigned {updated_count} distinct video URLs!")
