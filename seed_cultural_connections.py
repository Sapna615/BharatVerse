import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import CulturalEntry, CulturalConnection, State

# Clear any broken connections
CulturalConnection.objects.all().delete()

# Helper to find entry by title snippet or slug snippet
def find_entry(term):
    e = CulturalEntry.objects.filter(slug__icontains=term).first()
    if not e:
        e = CulturalEntry.objects.filter(title__icontains=term).first()
    return e

connections_data = [
    # Manipur Connections (Solving user's exact screenshot!)
    ('thang-ta', 'pena', 'Musical Accompaniment', 'The sacred single-string Pena bowed lute accompanies ancient Thang-Ta combat chants during Meitei Lai Haraoba rituals.'),
    ('thang-ta', 'pung-cholom', 'Rhythmic Synchronization', 'Pung Cholom drum rhythms set the explosive tempo and martial footwork for Thang-Ta sword routines.'),
    ('thang-ta', 'shaphee-lanphee', 'Ceremonial Honor Attire', 'The legendary embroidered Shaphee Lanphee shawl was historically awarded by Meitei royalty as a medal of honor to champion Thang-Ta warriors.'),
    ('thang-ta', 'khamba-and-thoibi', 'Heroic Legend Lore', 'The national epic of Khamba and Thoibi features heroic combat duels honoring traditional Thang-Ta martial courage.'),
    ('thang-ta', 'paika', 'Inter-State Martial Tradition', 'Shares sacred martial weapon arts origins with Jharkhand\'s Paika sword-and-shield warrior dance.'),
    ('thang-ta', 'choliya', 'Himalayan Martial Counterpart', 'Parallels Uttarakhand\'s Choliya martial sword dance in using weaponry to ward off malevolent spirits.'),

    # Punjab Connections
    ('bhangra', 'dhol', 'Primary Percussion Beat', 'The deep syncopated heartbeat of the double-headed Dhol drum drives every Bhangra step and leap.'),
    ('bhangra', 'tumbi', 'Folk Melodic Lead', 'The high-pitched single-string plucks of the Tumbi define the iconic modern and traditional Bhangra melodies.'),
    ('bhangra', 'giddha', 'Gender Partner Tradition', 'Bhangra (traditionally danced by men) and Giddha (danced by women) form the twin harvest celebratory pillars of Punjab.'),
    ('giddha', 'phulkari', 'Traditional Attire', 'Giddha dancers wear colorful dupattas richly embroidered with generational geometric Phulkari needlework.'),
    ('bhangra', 'garba', 'National Harvest Celebration', 'Both Bhangra and Gujarat’s Garba celebrate seasonal harvest and community unity through rhythmic circle choreography.'),

    # Rajasthan Connections
    ('blue-pottery', 'bagru', 'Artisanal Guild Lineage', 'Both Blue Pottery and Bagru block printing developed under Jaipur royal atelier patronage as signature Rajasthani crafts.'),
    ('ghoomar', 'kalbelia', 'Folk Choreography Sisterhood', 'While Ghoomar embodies royal courtly etiquette, Kalbelia expresses nomadic desert serpent rhythms across Rajasthan.'),
    ('ghoomar', 'ravanahatha', 'Desert Melodic Accompaniment', 'The ancient bowed Ravanahatha provides the haunting modal melodies accompanying Rajasthani folk songs.'),
    ('dhola-maru', 'ravanahatha', 'Ballad Recitation', 'Wandering Bhopa bards recite the tragic romance of Dhola and Maru accompanied by the bowing of the Ravanahatha.'),

    # Kerala Connections
    ('kathakali', 'chenda', 'Dramatic Percussion Drive', 'The thunderous Chenda drum builds the dramatic crescendos accompanying demonic clashes in Kathakali.'),
    ('kathakali', 'mohiyattam', 'Temple Classical Contrast', 'Kathakali represents dynamic Tandava heroic drama while Mohiniyattam embodies delicate Lasya enchantment in Kerala temples.'),
    ('kathakali', 'theyyam', 'Sacred Ritual Precursor', 'Theyyam\'s towering painted headgear and spirit channelings served as archaic ritual ancestors to Kathakali theater.'),
    ('mohiyattam', 'kasavu', 'Pristine Handloom Costume', 'Mohiniyattam dancers exclusively wear pristine off-white handloom Kasavu cotton with shimmering golden zari borders.'),

    # Tamil Nadu Connections
    ('bharatanatyam', 'nadaswaram', 'Temple Auspicious Sound', 'The sacred vibrations of the Nadaswaram reed horn herald temple ceremonies where Bharatanatyam was historically offered.'),
    ('bharatanatyam', 'veena', 'Carnatic Melodic Resonance', 'The Saraswati Veena provides the nuanced gamaka microtones that guide Bharatanatyam abhinaya facial expressions.'),
    ('bharatanatyam', 'kanchipuram', 'Sacred Temple Loom', 'Bharatanatyam dancers wear pure Kanchipuram silk pleats woven with temple tower (gopuram) motifs that fan out during araimandi bends.'),
    ('bharatanatyam', 'odissi', 'Classical Sibling Traditions', 'Both Bharatanatyam and Odisha\'s Odissi descend from ancient Natya Shastra temple dancer (Devadasi/Mahari) lineages.'),

    # Gujarat Connections
    ('garba', 'dandiya', 'Navratri Festive Pair', 'Garba circle clapping leads directly into high-energy Dandiya Raas stick percussion during the nine nights of Navratri.'),
    ('garba', 'patola', 'Royal Festive Silk', 'Patola double-ikat sarees with royal elephant and parrot motifs are prized as the most auspicious heirloom garments worn at Garba celebrations.'),

    # Maharashtra Connections
    ('warli', 'sohrai', 'Indigenous Mural Sisterhood', 'Warli murals share deep philosophical and visual kinship with Jharkhand\'s Sohrai ritual wall paintings.'),
    ('lavani', 'powada', 'Maratha Performing Heritage', 'Lavani folk dance rhythms and Powada warrior ballads evolved side-by-side in 17th-century Maratha military encampments.'),
    ('lavani', 'paithani', 'Nauvari Saree Drapery', 'Lavani dancers drape opulent nine-yard Paithani silk sarees with peacock pallus to execute acrobatic spins and gestures.'),

    # West Bengal Connections
    ('purulia-chhau', 'durga-puja', 'Mythological Combat Enactment', 'Purulia Chhau dancers wearing painted clay masks enact Goddess Durga vanquishing the demon Mahishasura at festive pandals.'),
    ('purulia-chhau', 'baul', 'Bengali Performing Spectrum', 'Chhau represents martial acrobatics while Baul music embodies wandering mystic spirituality across rural Bengal.'),

    # Uttar Pradesh Connections
    ('kathak', 'banarasi-zari', 'Courtly Royal Costume', 'Kathak dancers under Awadh court patronage wore layered Banarasi silk angrakhas that swirl during rapid chakkars (spins).'),
    ('kathak', 'shehnai', 'Banaras Gharana Synergy', 'Kathak footwork is accompanied by the evocative Banaras Thumri melodies played on the sacred Shehnai of Varanasi.')
]

created_count = 0
for src_term, tgt_term, rel_type, desc in connections_data:
    source = find_entry(src_term)
    target = find_entry(tgt_term)

    if source and target and source != target:
        conn, created = CulturalConnection.objects.get_or_create(
            source_entry=source,
            target_entry=target,
            relationship_type=rel_type,
            defaults={'description': desc}
        )
        if not created:
            conn.description = desc
            conn.save()
        created_count += 1

# Automatically create intra-state and intra-category semantic connections for all entries
# so that every single cultural entry on the entire platform has rich connections mapped!
for state in State.objects.all():
    state_entries = list(CulturalEntry.objects.filter(state=state, status='published'))
    if len(state_entries) >= 2:
        for i in range(len(state_entries)):
            src = state_entries[i]
            tgt = state_entries[(i + 1) % len(state_entries)]
            if src != tgt:
                rel = f"{state.name} Heritage Synergy"
                desc = f"Both {src.title} and {tgt.title} belong to the living cultural ecosystem of {state.name}, representing complementary facets of regional artistic identity."
                CulturalConnection.objects.get_or_create(
                    source_entry=src,
                    target_entry=tgt,
                    relationship_type=rel,
                    defaults={'description': desc}
                )
                created_count += 1

print(f"Successfully seeded {created_count} cultural connections in database! Total now: {CulturalConnection.objects.count()}")
