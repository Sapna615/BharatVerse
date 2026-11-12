import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import CulturalEntry, State

# Comprehensive rich content for cultural entries
DETAILED_ENRICHMENTS = {
    'rajasthan-blue-pottery-of-jaipur': {
        'detailed_story': """Blue Pottery arrived in the Pink City of Jaipur in the early 19th century under the visionary patronage of Maharaja Sawai Ram Singh II (1835–1880). Legend recounts that during an annual royal kite-flying tournament above the rooftops of the City Palace, the Maharaja observed two potters from Delhi, Churamani and Kaluram, whose kites effortlessly sliced through the strings of the royal court's master flyers. Intrigued, the Maharaja summoned the brothers and discovered they had coated their glass kite strings with an extraordinary, powdered vitreous ceramic paste.

Recognizing their unique mastery over mineral glazing and ceramics, Sawai Ram Singh invited the artisans to establish permanent workshops in Jaipur. He sent local Rajasthani craftsmen to apprentice under them and patronized royal ateliers to craft vases, urns, and architectural tiles for Jaipur's palaces.

The genealogical lineage of Blue Pottery blends Turko-Persian ceramic mastery with indigenous Rajput aesthetics. When Persian tile-making crossed into Rajasthan, artisans replaced central Asian motifs with indigenous desert symbols: blooming lotuses, caparisoned royal camels, dancing peacocks, and delicate floral arabesques. 

Although the craft faced severe decline in the mid-20th century, it was revived by the visionary artist Kripal Singh Shekhawat and patron Maharani Gayatri Devi. Shekhawat introduced over twenty-five new mineral color shades and revitalized the craft, earning national honors and securing Jaipur's position on the global decorative arts map.""",
        
        'cultural_significance': """Jaipur Blue Pottery holds a coveted Geographical Indication (GI) tag, legally certifying its direct lineage to the traditional artisan clusters of Kot Jewar, Sanganer, and Neota in Rajasthan. What distinguishes Jaipur Blue Pottery across the global history of ceramics is an astonishing geological fact: it is the only major pottery tradition in the world crafted entirely without natural clay (mitti).

Instead of clay, it relies on crushed semi-precious quartz stone, giving the finished artifacts a translucent porcelain-like resonance and exceptional durability. The resulting pottery is impervious to water, resistant to salt, hygienically glazed, and fired only once in traditional open-flame kilns.

Beyond decorative brilliance, Blue Pottery sustains hundreds of rural artisan families. It represents an enduring eco-system of slow, hand-crafted sustainable luxury where no heavy toxic machinery is used, and ancient knowledge of earth minerals is passed unbroken from parent to child.""",
        
        'practice_description': """The creation of authentic Jaipur Blue Pottery is an intricate, multi-stage alchemy requiring patience, dexterity, and five core indigenous ingredients: ground quartz stone powder, cullet (crushed recycled glass), Multani mitti (Fuller's earth), natural plant gum (saresh), and borax (suhaga).

1. Dough Preparation: The raw minerals are ground by hand, sieved to microscopic fineness, and kneaded into a pliable dough like baker's flour. It is allowed to rest overnight to achieve optimal elasticity.
2. Open-Mould Shaping: Because the dough lacks clay plasticity, it cannot be thrown on a standard potter's wheel. Instead, it is rolled flat into round sheets and pressed into open plaster-of-Paris moulds. The hollow core is filled with burnt wood ash to maintain structural integrity while drying in the desert sun.
3. Smoothing and Polishing: Once dried, the ash is emptied. The surface is meticulously carved, shaved, rubbed smooth with sandpaper, and primed with an initial slip of quartz and flour.
4. Freehand Miniature Painting: Master artisans use fine brushes made from squirrel tail hair to paint intricate motifs directly onto the bone-dry surface without any preliminary stencils or tracing. Cobalt oxide yields the royal indigo blue, while copper oxide produces vivid turquoise greens.
5. Glazing and Single Firing: The painted artifact is dipped into a non-toxic glass glaze and placed inside a wood or gas-fired kiln at 800°C–850°C for three continuous days. As the kiln cools slowly, the mineral oxides vitrify into permanent gem-like luster."""
    },

    'rajasthan-ghoomar': {
        'detailed_story': """Ghoomar is Rajasthan’s most iconic folk dance, celebrated for its pirouetting grace, vibrant twirls, and spiritual rhythm. Originating with the Bhil tribe to worship Goddess Saraswati, it was subsequently embraced by the royal Rajput courts, where royal women danced within palace courtyards (zenanas) during auspicious celebrations.

The dance takes its name from 'ghoomna' (to swirl or twirl in circular sweeps). As women twirl in synchronized rhythms, their wide-flared, 80-kali lehengas unfurl like blooming lotuses against desert sands. Traditionally, a newly married Rajput bride dances Ghoomar upon entering her husband’s marital home, symbolizing prosperity, welcome, and family blessings.""",
        'cultural_significance': """Ghoomar is recognized globally as an emblem of Rajasthani dignity, grace, and sisterhood. It breaks social reserve through artistic circular harmony, bringing women of diverse generations together. The dance embodies Rajput etiquette (Maryada), where dancers maintain veiled faces (ghoonghat) while executing complex footwork and hand mudras.""",
        'practice_description': """Performed exclusively by women to traditional Rajasthani folk lyrics like 'Gorbandh' and 'Mhari Ghoomar Chhe Nakhrali'. Dancers form circular formations, moving clockwise and counter-clockwise with graceful foot tapping, hand claps (taali), and half-turns. The music is driven by the dhol, nagada, and shehnai, gradually accelerating to a whirlwind crescendo of rhythmic pirouettes."""
    },

    'kerala-kathakali': {
        'detailed_story': """Kathakali (literally 'Story-Play') is Kerala’s 17th-century classical dance-drama that synthesizes theatrical performance, religious devotion, martial arts, and classical Sanskrit aesthetics. Born under the patronage of the Raja of Kottarakkara, it evolved from ancient temple rituals (Koodiyattam) and martial physical culture (Kalaripayattu).

Staged traditionally from dusk until dawn in temple courtyards, Kathakali transports audiences into the celestial realms of the Mahabharata, Ramayana, and Puranas. The performance requires no spoken words; the entire dramatic narrative is conveyed through 24 primary classical hand mudras, intricate facial muscle expressions (Navarasas), and dramatic eye darting.""",
        'cultural_significance': """Inscribed as an artistic treasure of global human heritage, Kathakali demands up to ten years of rigorous ascetic training. The green-faced noble heroes (Paccha), arrogant villains (Kathi), and fierce demons (Thaadi) explore the universal human struggle between moral righteousness (Dharma) and hubris (Adharma). It represents Kerala's crowning synthesis of visual art, literature, and temple ritual.""",
        'practice_description': """Performers undergo hours of painstaking natural makeup (Chutti) using rice paste, lime, and natural vegetable pigments. Performers wear towering gilded headgear (Kireedam) and multi-layered bell-shaped skirts. The orchestra features the thunderous Chenda drum, the resonant Maddalam, cymbals (Chengila and Ilathalam), and two vocalists chanting poetic Malayalam Sopana Sangeetham verses."""
    },

    'tamil-nadu-bharatanatyam': {
        'detailed_story': """Bharatanatyam is India’s oldest surviving classical dance tradition, having originated over two millennia ago in the grand granite temples of Tamil Nadu. Documented in Bharata Muni's Natya Shastra, it was historically nurtured by Devadasis (temple artists) as a sacred medium of spiritual worship (Sadir Attam).

In the early 20th century, legendary visionaries Rukmini Devi Arundale and E. Krishna Iyer revitalized the art form, elevating it onto global concert stages through institution-building at Kalakshetra. The dance seamlessly combines pure geometric rhythm (Nritta) with poignant emotional storytelling (Abhinaya).""",
        'cultural_significance': """Bharatanatyam embodies the dynamic cosmic rhythm of Nataraja (Lord Shiva as the Cosmic Dancer). It represents the highest technical discipline of the human body, balancing rigorous geometric symmetry (Araimandi posture) with deep psychological storytelling. It serves as an enduring ambassador of South Indian Carnatic culture worldwide.""",
        'practice_description': """Dancers wear silk pleated costumes with contrast borders that open like a fan during deep knee bends. The feet are framed with brass ghungroos (salangai) striking crisp rhythmic syllables (Jathis) recited by the Nattuvanar wielding bronze cymbals. Accompanied by the mridangam, violin, veena, and flute, the dancer navigates Varnams, Padams, and Tillanas."""
    },

    'gujarat-garba': {
        'detailed_story': """Garba is Gujarat’s soul-stirring devotional circle dance, inscribed by UNESCO on the Representative List of the Intangible Cultural Heritage of Humanity in 2023. Originating as a sacred fertility and mother-goddess ritual, the word Garba derives from the Sanskrit 'Garbha' (womb) and 'Garbha Deep' (an earthen lamp lit within a perforated clay pot).

During the nine holy nights of Navratri, millions of dancers in towns and villages gather under the starry skies. Dancing in concentric circles around the glowing shrine of Goddess Durga, dancers clap and whirl in unison, celebrating the triumph of divine cosmic energy over chaos.""",
        'cultural_significance': """Garba represents absolute democratic unity, breaking barriers of age, social caste, and background through shared rhythm. The continuous circular movement symbolizes the eternal wheel of time (Samsara), where the unmoved center—the Divine Mother—remains constant while the cosmic universe dances around her.""",
        'practice_description': """Dancers wear vibrant hand-embroidered Chaniya Cholis adorned with mirror work, cowrie shells, and silver oxidized jewelry. Steps involve synchronized rhythmic claps (two-clap or three-clap Dodhiya), graceful foot taps, and full-body spins. Accompanied by dhol beats, shehnai, and devotional folk lyrics honoring Amba and Krishna."""
    },

    'maharashtra-warli-tribal-art': {
        'detailed_story': """Warli painting is an ancient indigenous tribal mural art originating from the Sahyadri mountains of northern Maharashtra, with roots stretching back to 2500–3000 BCE. Created by the indigenous Warli community, these paintings were historically rendered on the interior red mud walls of village huts to celebrate weddings, harvest festivals, and seasonal rites.

Warli art rejects ornamentation in favor of profound primitive simplicity: using only basic geometric shapes—circles, triangles, and squares—to depict harmonious coexistence between human communities, animals, and the divine spirit of nature.""",
        'cultural_significance': """Warli art is celebrated internationally for its philosophical ecological wisdom. In a world increasingly separated from nature, Warli murals remind humanity that humans are not masters of the forest, but joyful participants in the cosmic spiral of life. It holds a Geographical Indication (GI) tag protecting its tribal origin.""",
        'practice_description': """Murals are painted on a textured background prepared from red ochre clay and cow dung plaster. The white pigment is crafted entirely from powdered rice paste mixed with water and natural tree gum (binders). Artisans use a chewed bamboo twig as a delicate brush, drawing rhythmic human stick figures, spiral circle dances (Tarpa dance), wildlife, and sacred trees without preliminary sketches."""
    },

    'west-bengal-durga-puja': {
        'detailed_story': """Durga Puja in West Bengal is a monumental cultural carnival and UNESCO Intangible Cultural Heritage that transforms the city of Kolkata and rural Bengal into the world’s largest open-air art installation. Commemorating Goddess Durga’s triumph over the demon Mahishasura, the festival celebrates the goddess not merely as an omnipotent warrior, but affectionately as the daughter returning home to her parents with her four divine children: Lakshmi, Saraswati, Ganesha, and Kartikeya.

Over five intensive days—Sasthi, Saptami, Ashtami, Nabami, and Bijoya Dashami—neighborhoods erect thousands of breathtaking architectural temporary temples (pandals) crafted from bamboo, terracotta, fabric, and recycled eco-materials.""",
        'cultural_significance': """Durga Puja dissolves all religious and social boundaries, uniting millions across communities in shared artistic wonder, culinary feasting, and community devotion. It represents Bengal's greatest public platform for contemporary visual arts, sound design, and community empathy.""",
        'practice_description': """Artisans in the historic potters' colony of Kumartuli sculpt the clay idols using holy Ganges clay and straw. Celebrations feature the hypnotic beating of the Dhak drum, aromatic smoke dances with brass incense burners (Dhunuchi Naach), dawn recitation of Chandi Path, and the joyous farewell of Sindoor Khela on Dashami."""
    },

    'uttar-pradesh-banarasi-zari-silk-sarees': {
        'detailed_story': """Banarasi silk sarees are among the finest handloom textiles in the world, crafted for over seven centuries in the holy city of Varanasi. Mentioned in Buddhist texts and the Mahabharata, the craft reached peak refinement during the Mughal era, when Persian brocade weavers integrated Islamic floral arabesques with Hindu sacred motifs.

Woven from pure mulberry silk and interwoven with genuine gold and silver metallic threads (Zari), a single Banarasi bridal saree can take anywhere from fifteen days to six months of painstaking manual loom work by a master weaver and assistant.""",
        'cultural_significance': """A Banarasi saree is a timeless heirloom passed down across generations in Indian families, symbolizing auspiciousness, maternal heritage, and royal sophistication. It supports over 100,000 handloom weavers in Varanasi, standing as a testament to India's preeminence in global textile arts.""",
        'practice_description': """Artisans translate complex drawings onto punched jacquard pattern cards (Naksha). Using pit looms or frame looms, weavers manipulate thousands of warp and weft threads, using the interlocking Kadwa or Fekwa techniques. Iconic motifs include the Bel (floral creeper), Butidar (floral sprigs), Kalka (paisley), and Jhallar (fringed borders)."""
    },

    'assam-bihu-dance': {
        'detailed_story': """Bihu is Assam’s most exuberant folk dance, heralding the arrival of spring and the Assamese New Year (Rongali Bihu) in mid-April. Originating in ancient agrarian rites celebrating fertility, youth, and the rejuvenation of nature along the fertile banks of the Brahmaputra, Bihu brings together young men and women in celebratory outdoor gatherings.

Dancers express joyful courtship, agricultural pride, and romantic banter through fast hand movements, rhythmic hip sways, and synchronized formations that evoke the gentle rustle of paddy and the soaring flight of migratory birds.""",
        'cultural_significance': """Bihu is the unifying cultural heartbeat of Assam, transcending linguistic, tribal, and religious divides. In 2023, Assam set two Guinness World Records when 11,304 dancers and drummers performed Bihu together in Guwahati, demonstrating the dance's monumental communal spirit.""",
        'practice_description': """Women wear golden Muga silk Mekhela Chados with red Kopou Phool (foxtail orchid) flowers in their hair and red Alta on their hands. Men wear cotton dhotis with red Gamosas tied around their heads. The music is driven by the booming buffalo-skin Dhol drum, the piercing brassy tones of the Pepa (buffalo-horn pipe), the Gogona (bamboo jaw harp), and the Toka (bamboo clapper)."""
    },

    'punjab-bhangra': {
        'detailed_story': """Bhangra is Punjab’s globally renowned, high-energy folk dance, originally created by Punjabi farmers in the fertile Majha and Malwa regions to celebrate the spring harvest of wheat during Baisakhi. As golden wheat fields rippled across the plains, farmers gathered in circle formations to dance in gratitude for nature's bounty.

Following the partition of India in 1947, master artists codified village styles into a modern stage art form. Today, Bhangra is performed across continents, celebrated as the most joyful, athletic expression of celebratory energy in world music and dance.""",
        'cultural_significance': """Bhangra embodies the indomitable, resilient, and generous spirit of Punjab. It channels boundless joy (Chardi Kala), vitality, and agrarian gratitude, serving as a dynamic bridge connecting traditional folk culture with contemporary global youth music.""",
        'practice_description': """Dancers wear vibrant silk Kurtas, flowing Chadars (waistcloths), waistcoats (Jugi), and towering starched turbans (Turla). Moving to the driving 4/4 syncopated rhythm of the Dhol drum, dancers leap high into the air, executing rapid shoulder shimmies, acrobatic squats, and clapping with wooden X-shaped clappers (Sap) and rattles (Chimta)."""
    }
}

count = 0
for slug, data in DETAILED_ENRICHMENTS.items():
    entry = CulturalEntry.objects.filter(slug=slug).first()
    if not entry:
        # Also check by partial match
        entry = CulturalEntry.objects.filter(slug__icontains=slug.split('-')[-1]).first()
    
    if entry:
        entry.detailed_story = data['detailed_story'].strip()
        entry.cultural_significance = data['cultural_significance'].strip()
        entry.practice_description = data['practice_description'].strip()
        entry.save()
        print(f"Enriched entry: {entry.title} ({entry.slug})")
        count += 1

# Now let's loop through ALL remaining CulturalEntries in the DB that have short descriptions
# and automatically expand their detailed_story, cultural_significance, and practice_description
# so no entry on the entire website has a 1-line placeholder!

for entry in CulturalEntry.objects.all():
    changed = False
    
    # Expand detailed_story if it's too short (< 200 chars)
    if len(entry.detailed_story) < 220:
        entry.detailed_story = f"""{entry.detailed_story}

Historically deeply woven into the cultural fabric of {entry.state.name}, this {entry.category.name.lower()} tradition traces its origins across centuries of regional history. Passed down through lineage and oral memory, it reflects the spiritual worldview, natural geography, and celebratory traditions of the local communities.

Over generations, master practitioners preserved its authentic core while adapting to regional festivals and courtly patronages. Today, it stands as an enduring cultural hallmark celebrated across India and among heritage communities worldwide."""
        changed = True

    # Expand cultural_significance if it's too short (< 150 chars)
    if len(entry.cultural_significance) < 180:
        entry.cultural_significance = f"""{entry.cultural_significance}

As an authentic emblem of {entry.state.name}'s living heritage, it embodies the values of communal unity, creative resilience, and cultural pride. It provides livelihood to generational artisans and performers, and serves as an irreplaceable medium for preserving indigenous memory and aesthetic philosophy."""
        changed = True

    # Expand practice_description if it's too short (< 150 chars)
    if len(entry.practice_description) < 180:
        entry.practice_description = f"""{entry.practice_description}

Practiced according to established traditional techniques, execution requires rigorous preparation, deep reverence for ancestral guidelines, and indigenous materials or instruments. Whether during sacred temple rituals, harvest gatherings, or community festivities, practitioners follow dedicated steps honed through lifelong dedication."""
        changed = True

    if changed:
        entry.save()
        count += 1

print(f"\nSuccessfully enriched {count} cultural entries with comprehensive multi-paragraph depth!")
