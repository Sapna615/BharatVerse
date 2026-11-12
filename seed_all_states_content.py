import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import State, CulturalCategory, CulturalEntry, Festival, Cuisine
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

# Ensure standard categories exist
dance, _ = CulturalCategory.objects.get_or_create(name='Dance', defaults={'slug': 'dance'})
music, _ = CulturalCategory.objects.get_or_create(name='Music', defaults={'slug': 'music'})
craft, _ = CulturalCategory.objects.get_or_create(name='Craft', defaults={'slug': 'craft'})
story, _ = CulturalCategory.objects.get_or_create(name='Story', defaults={'slug': 'story'})

# Clean out old placeholder dummy entries that were generated earlier
deleted_entries, _ = CulturalEntry.objects.filter(title__endswith='Entry').delete()
deleted_fests, _ = Festival.objects.filter(name__endswith='Festival', slug__endswith='-festival').delete()
deleted_cuisines, _ = Cuisine.objects.filter(name__endswith='Cuisine', slug__endswith='-cuisine').delete()
print(f"Cleaned placeholders: {deleted_entries} entries, {deleted_fests} festivals, {deleted_cuisines} cuisines.")

# Known media files to assign where available
MEDIA_MAP = {
    'kathakali': 'games/kathakali_kerala_1791571279095.jpg',
    'warli-tribal-art': 'games/warli_art.jpg',
    'sitar-and-shahiri-traditions': 'games/sitar_maharashtra.jpg',
    'gujarati-thali': 'games/gujarati_thali_1791571296550.jpg',
    'banarasi-zari-silk-sarees': 'games/banarasi-saree_wiki.jpg',
    'assam-bamboo-and-cane-crafts': 'games/bamboo-craft_wiki.jpg',
    'dev-deepawali-of-varanasi': 'games/diwali_up.jpg',
    'heer-ranjha': 'games/punjab_folklore_1791571311179.jpg',
    'blue-pottery-of-jaipur': 'games/hawa_mahal_1791472781004.jpg',
    'mysore-silk-weaving': 'games/hampi_1791472757322.jpg',
}

STATE_DATA = {
    'rajasthan': {
        'name': 'Rajasthan',
        'region': 'North India',
        'description': 'The land of royalty, desert dunes, grand forts, vibrant folk music, and colourful tapestries.',
        'dances': [
            ('Ghoomar', 'A graceful Rajasthani folk dance performed by women swirling in flared lehengas, traditionally honouring Goddess Saraswati.',
             'Ghoomar originated with the Bhil tribe and was later adopted by Rajput royalty. The mesmerizing twirls celebrate auspicious occasions, weddings, and Holi.'),
            ('Kalbelia', 'A sensuous, hypnotic dance performed by the snake-charmer community of Rajasthan, recognized by UNESCO as Intangible Cultural Heritage.',
             'Dancers dressed in flowing black skirts adorned with silver ribbons mimic the fluid movements of a serpent, accompanied by the poongi wind instrument.'),
            ('Bhavai', 'A thrilling folk dance featuring female performers balancing up to eight brass or earthen pots on their heads while dancing atop swords or glass shards.',
             'Bhavai requires extraordinary dexterity, balance, and lifelong practice, symbolizing the strength and resilience of desert women fetching water.')
        ],
        'music': [
            ('Ravanahatha', 'An ancient bowed stringed instrument believed to have been invented by Ravana, crafted from coconut shell, bamboo, and goat hide.',
             'Played by wandering bards known as Bhopas to recite the epic tales of folk deities Pabuji and Devnarayan across Rajasthani villages.'),
            ('Kamayacha', 'A rare, bowed instrument made of mango wood with a parchment belly and 17 steel and gut strings, played by the Manganiyar community.',
             'The rich, haunting timbre of the Kamayacha evokes the vast silence of the Thar Desert, accompanying generational ballads of romance and bravery.')
        ],
        'crafts': [
            ('Blue Pottery of Jaipur', 'Distinctive ceramic ware crafted from quartz powder, raw glaze, and fullers earth without clay, adorned with cobalt blue motifs.',
             'Introduced from Turko-Persian traditions and patronized by Sawai Ram Singh II, Jaipur blue pottery is an iconic global craft.'),
            ('Bandhani Tie-Dye', 'The ancient art of resist tie-dyeing, producing mesmerizing patterns of dots, waves, and diamonds on silk and cotton fabrics.',
             'Practiced in Jodhpur and Bikaner, Bandhani turbans and odhnis signify social status, seasons, and celebratory joy in Rajasthani society.')
        ],
        'stories': [
            ('Dhola Maru', 'The timeless desert ballad of Prince Dhola and Princess Maru, celebrated for their undying romance against separations and sorcery.',
             'Sung by Langa and Manganiyar musicians around campfires, Dhola Maru is the romantic heartbeat of Rajasthani folklore.')
        ],
        'festivals': [
            ('Pushkar Camel Fair', 'November', 'One of the world\'s largest livestock fairs held on the banks of sacred Lake Pushkar, accompanied by vibrant cultural festivities.', 'Unites pilgrims, nomadic pastoralists, and artists in a colourful desert carnival.'),
            ('Gangaur', 'March-April', 'A vibrant festival celebrating Gauri (Goddess Parvati) as the epitome of marital fidelity and spring harvest.', 'Women carry decorated clay idols of Isar and Gauri in grand royal processions through heritage streets.')
        ],
        'cuisines': [
            ('Dal Baati Churma', 'A trio comprising hard wheat dough balls baked on cow-dung fire or tandoor, spicy mixed lentil stew, and sweetened crushed wheat crumble.', 'Wheat flour, mixed lentils, ghee, jaggery, cumin, garlic, cloves.', 'The quintessential Rajasthani meal born from warrior campaigns in desert conditions.'),
            ('Ker Sangri', 'A tart, savory stir-fry of wild desert berries (Ker) and dried desert beans (Sangri) seasoned with red chilies and mustard oil.', 'Ker berries, Sangri beans, dry red chilies, turmeric, amchur (mango powder), mustard oil.', 'A prized famine-survival delicacy celebrated as royal banqueting fare.')
        ]
    },
    'kerala': {
        'name': 'Kerala',
        'region': 'South India',
        'description': 'God\'s Own Country, famed for its lush backwaters, Kathakali theatrics, Ayurvedic traditions, and fragrant spice plantations.',
        'dances': [
            ('Kathakali', 'A classical dance-drama featuring elaborate facial makeup (Chutti), towering headgears, and precise mudras portraying mythological epics.',
             'Kathakali integrates acting (Abhinaya), martial footwork, and percussion to depict clashes of gods and demons from the Mahabharata and Ramayana.'),
            ('Mohiniyattam', 'The classical "dance of the enchantress", known for delicate swayings, undulating torso movements, and pristine white-and-gold kasavu costumes.',
             'Rooted in the myth of Mohini who captivated demons, it expresses devotion (Bhakti) and delicate romantic grace (Lasya).'),
            ('Theyyam', 'A dramatic sacred ritual dance where performers are believed to channel the deities and spirits of ancestors in temple groves.',
             'Featuring towering headdresses up to thirty feet high and fiery torches, Theyyam dissolves caste boundaries as devotees seek divine blessings.')
        ],
        'music': [
            ('Chenda Melam', 'A thunderous orchestral ensemble led by the cylindrical wooden drum known as the Chenda, common at temple festivals.',
             'Creating rhythmic crescendos called Panchari Melam, the Chenda sets temple courtyard stones vibrating with spiritual ecstasy.'),
            ('Idakka', 'An hourglass-shaped pressure drum played in temple sanctums, capable of producing acoustic vocal intervals and subtle microtones.',
             'Considered a "deva vadyam" (instrument of gods), the Idakka accompanies Sopana Sangeetham singing before temple deities.')
        ],
        'crafts': [
            ('Aranmula Kannadi', 'A handheld metal mirror cast from a secret copper-tin alloy rather than silvered glass, producing flawless reflection without distortion.',
             'Handcrafted by a single clan of master metallurgists in Aranmula village, this mirror is considered an auspicious harbinger of prosperity.'),
            ('Kasavu Handloom', 'Crisp off-white handloom cotton sarees with opulent gold-zari borders, woven traditionally in Balaramapuram and Chendamangalam.',
             'Kasavu embodies the subtle elegance of Kerala\'s aesthetic, worn during festivals like Onam and weddings.')
        ],
        'stories': [
            ('Legend of King Mahabali', 'The benevolent Asura king whose utopian reign of absolute equality and prosperity is commemorated every year during Onam.',
             'Banished to the netherworld by Vishnu\'s Vamana avatar, Mahabali is granted permission to visit his beloved people once a year.')
        ],
        'festivals': [
            ('Onam', 'August-September', 'A ten-day harvest carnival welcoming the spirit of King Mahabali with floral carpets (Pookkalam) and boat races.', 'Kerala\'s most beloved state festival celebrating harmony, abundance, and unity.'),
            ('Thrissur Pooram', 'May', 'The mother of all poorams held at the Vadakkunnathan temple, featuring caparisoned elephants and world-famous Kudamattam umbrella displays.', 'Showcases competitive percussion orchestras and magnificent pyrotechnics.')
        ],
        'cuisines': [
            ('Appam with Ishtu', 'Lacy, fermented rice and coconut milk pancakes with a fluffy center, paired with a mild, aromatic vegetable or meat coconut stew.', 'Fermented rice batter, coconut milk, curry leaves, ginger, green chilies, shallots.', 'A beloved Christian Syrian and Kerala household breakfast staple.'),
            ('Kerala Sadya', 'A grand vegetarian feast of over twenty-four traditional dishes served ceremoniously on a fresh plantain leaf.', 'Red Matta rice, Sambar, Avial, Thoran, Payasam, Olan, Injipuli, Pachadi.', 'The ultimate cultural banquet celebrating Onam, festivals, and weddings.')
        ]
    },
    'tamil-nadu': {
        'name': 'Tamil Nadu',
        'region': 'South India',
        'description': 'The land of ancient Dravidian temples, Bharatanatyam precision, Carnatic music ragas, and classical Tamil literature.',
        'dances': [
            ('Bharatanatyam', 'One of India\'s most celebrated classical dance forms, defined by geometric lines, crisp adavus, and intense facial bhavas.',
             'Originated in Tamil Nadu temples as Sadir Attam, Bharatanatyam interprets sacred Hindu philosophies through structured rhythmic syllables (Jathis).'),
            ('Karakattam', 'An energetic folk dance performed balancing brass pots adorned with coconut and flower arrangements atop the head.',
             'Dedicated to Mariamman, the goddess of rain, dancers demonstrate remarkable agility while navigating obstacles without dropping the pots.')
        ],
        'music': [
            ('Nadaswaram and Thavil', 'A commanding double-reed woodwind instrument paired with the thunderous Thavil drum, considered the supreme mangala vadya.',
             'No South Indian Hindu wedding or temple dawn ritual is complete without the auspicious vibrations of the Nadaswaram.'),
            ('Carnatic Veena', 'A majestic plucked string instrument with twenty-four brass frets, symbolizing Saraswati\'s divine wisdom and melodic mastery.',
             'Crafted from aged jackwood in Thanjavur, the Saraswati veena produces the subtle gamakas (oscillations) fundamental to Carnatic music.')
        ],
        'crafts': [
            ('Kanchipuram Silk Sarees', 'Heavy, lustrous mulberry silk sarees with contrasting borders and pallus woven using the interlocking korvai technique.',
             'Renowned for motifs inspired by temple architecture, peacock plumes, and floral creepers with genuine silver-gold zari.'),
            ('Thanjavur Paintings', 'Classical South Indian paintings made on wooden boards, adorned with 22-karat gold foil and semi-precious stones.',
             'Originating under Maratha patronage in the 16th century, these paintings depict Hindu deities with rounded faces and glowing eyes.')
        ],
        'stories': [
            ('The Epic of Silappadikaram', 'The dramatic story of Kannagi, who proved the innocence of her husband Kovalan in the royal court of the Pandyan king.',
             'Kannagi\'s fiery curse burned the city of Madurai, establishing her as Pattini Kadavul, the deity of unyielding truth and chastity.')
        ],
        'festivals': [
            ('Pongal', 'January', 'A four-day harvest thanksgiving festival to the Sun God, celebrating the boiling over of newly harvested rice in earthen pots.', 'Signifies agricultural abundance, prosperity, and reverence toward cattle and nature.'),
            ('Karthigai Deepam', 'November-December', 'The festival of lights where thousands of clay oil lamps illuminate temples and homes, culminating in the sacred flame on Thiruvannamalai hill.', 'Celebrates Lord Shiva manifesting as the infinite column of light.')
        ],
        'cuisines': [
            ('Masala Dosa with Sambar', 'A paper-thin, crispy fermented rice and lentil crepe stuffed with spiced potato masala, served with piping hot lentil stew and coconut chutney.', 'Parboiled rice, urad dal, potatoes, mustard seeds, curry leaves, tamarind, sambar spices.', 'The beloved South Indian staple enjoyed worldwide.'),
            ('Chettinad Curry', 'A fiery, deeply aromatic curry enriched with freshly roasted spices including kalpasi (black stone flower) and star anise.', 'Chicken or vegetables, shallots, fennel, black peppercorns, star anise, poppy seeds, curry leaves.', 'Crafted by the aristocratic Chettiar merchant community of Tamil Nadu.')
        ]
    },
    'gujarat': {
        'name': 'Gujarat',
        'region': 'West India',
        'description': 'The land of vibrant textiles, coastal trade, festive Garba nights, architectural stepwells, and hospitable merchant traditions.',
        'dances': [
            ('Garba', 'A spirited circle dance performed around an earthen lamp (Garbha Deep) honoring Goddess Durga during the nine nights of Navratri.',
             'UNESCO-inscribed in 2023, Garba brings together millions in rhythmic clapping, synchronized spins, and vibrant chaniya cholis.'),
            ('Dandiya Raas', 'A high-energy partner dance where participants strike polished wooden sticks in rhythmic patterns to festive music.',
             'Re-enacting the playful battles between Goddess Durga and Mahishasura as well as Krishna\'s Raas Leela with the Gopis in Vrindavan.')
        ],
        'music': [
            ('Jantar', 'An ancient string instrument featuring two large dried-gourd resonators connected by a bamboo neck, played with peacock feathers.',
             'Used by traditional folk singers in Gujarat and Rajasthan to recite epic songs of Devnarayan.'),
            ('Sugam Sangeet', 'A poetic, melodic genre of semi-classical Gujarati music setting celebrated Gujarati ghazals and poems to sweet ragas.',
             'Popularized by legends like Hemu Gadhvi and Avinash Vyas, it captures the soul of Gujarati language and literature.')
        ],
        'crafts': [
            ('Patola Silk Weaving', 'An exceptionally intricate double-ikat woven silk textile made in Patan, where warp and weft are both tie-dyed before weaving.',
             'Taking up to six months to weave a single saree, genuine Patola never fades and is a treasured family heirloom across generations.'),
            ('Rogan Art', 'A rare freehand fabric painting craft using thick, brightly colored paste boiled from castor oil and natural pigments.',
             'Practiced exclusively by the Khatri family in Nirona village, Kutch, using a thin metal stylus guided by the artisan\'s fingertips.')
        ],
        'stories': [
            ('Krishna at Dwarka', 'The mythological golden kingdom built by Lord Krishna on Gujarat\'s western sea coast after leaving Mathura.',
             'Dwarka symbolizes righteous governance, devotion, and the maritime spirit that continues to define Gujarat\'s coastal prosperity.')
        ],
        'festivals': [
            ('Navratri Garba Festival', 'October', 'The world\'s longest dance festival spanning nine consecutive nights of non-stop community dancing and spiritual devotion.', 'Celebrates the victory of Good over Evil with kaleidoscopic attire and live folk orchestras.'),
            ('Uttarayan Kite Festival', 'January', 'A grand festival marking the Sun\'s journey into the Northern Hemisphere, with millions flying vibrant kites across city skies.', 'Terraces fill with shouts of "Kai Po Che" amidst festive feasts of Undhiyu and sesame sweets.')
        ],
        'cuisines': [
            ('Gujarati Thali', 'A balanced, wholesome platter incorporating sweet, salty, spicy, and tangy notes across bread, lentils, vegetables, and snacks.', 'Kadhi, Gujarati Dal, Shaak, Rotli, Puri, Farsan, Chutney, Shrikhand, Rice.', 'Emphasizes Ayurvedic nutritional harmony with distinctive gentle sweetness.'),
            ('Khaman Dhokla', 'A spongy, steamed snack made from fermented gram flour, tempered with mustard seeds, sesame, curry leaves, and green chilies.', 'Gram flour (Besan), eno or fruit salt, lemon juice, mustard seeds, green chilies, cilantro.', 'The quintessential Gujarati street food and tea-time delicacy.')
        ]
    },
    'maharashtra': {
        'name': 'Maharashtra',
        'region': 'West India',
        'description': 'The land of Maratha warriors, Sahyadri fortresses, saintly Varkari traditions, Bollywood glamour, and dynamic festivities.',
        'dances': [
            ('Lavani', 'A rhythmic, vivacious dance combining traditional song and dance performed to the rapid beats of the Dholki drum.',
             'Worn in nine-yard Nauvari sarees, dancers enchant audiences with quick footwork, sharp expressions, and social or romantic commentary.'),
            ('Koli Dance', 'The joyful folk dance of the coastal fishermen (Kolis) of Mumbai and the Konkan coast.',
             'Dancers depict the casting of fishing nets, rowing against crashing Arabian Sea waves, and the joyous return with boatloads of catch.')
        ],
        'music': [
            ('Powada Ballads', 'A stirring dramatic narrative poetry genre composed by Shahirs to celebrate the valor of Chhatrapati Shivaji Maharaj.',
             'Delivered with raw energy and percussive Daf accompaniment, Powada inspired generations of freedom fighters and patriots.'),
            ('Tutari', 'A curved brass wind horn blown at solemn royal proclamations and festive celebrations to announce an auspicious arrival.',
             'A proud symbol of Maratha sovereignty and heraldic pomp that echoes through historic forts across the Western Ghats.')
        ],
        'crafts': [
            ('Warli Tribal Art', 'An ancient indigenous mural painting tradition created using white rice paste on earthen mud walls.',
             'Using primitive geometric shapes—circles, triangles, and squares—Warli art depicts harmony between humans, spirits, and wild nature.'),
            ('Paithani Silk Sarees', 'Luxurious silk sarees woven in Paithan featuring rich metallic zari borders and elaborate peacock motifs on the pallu.',
             'Considered the queen of Maharashtrian sarees, Paithani weaving dates back to the Satavahana dynasty over two thousand years ago.')
        ],
        'stories': [
            ('Tales of Chhatrapati Shivaji Maharaj', 'The legendary saga of the 17th-century founder of the Maratha Empire, revered for his tactical brilliance and justice.',
             'His valor, fortress engineering in Rajgad and Raigad, and respect for all faiths form the bedrock of Maharashtrian identity.')
        ],
        'festivals': [
            ('Ganesh Chaturthi', 'August-September', 'A ten-day mega-festival welcoming Lord Ganesha into homes and giant public pandals with thunderous Dhol-Tasha beats.', 'Culminates in grand immersion processions (Visarjan) into the sea amidst chants of "Ganpati Bappa Morya".'),
            ('Gudi Padwa', 'March-April', 'The traditional Maharashtrian New Year celebrated by hoisting a silk-draped Gudi flag outside front doorways.', 'Marks the arrival of spring and commemorates the legendary victories of ancient kings.')
        ],
        'cuisines': [
            ('Puran Poli', 'A delicate, sweet flatbread stuffed with a fragrant filling of boiled chana dal, jaggery, cardamom, and nutmeg, slathered in pure ghee.', 'Chana dal, jaggery, wheat flour, cardamom, nutmeg, ghee.', 'The sacred festival dessert cooked on Holi, Gudi Padwa, and Ganesh Chaturthi.'),
            ('Misal Pav', 'A fiery sprouted-moth bean curry topped with crunchy farsan, onions, coriander, and lime, soaked up with buttered pav bread.', 'Sprouted moth beans (matki), onions, coconut, goda masala, farsan, pav bread.', 'Maharashtra\'s legendary breakfast and street-food classic, known for its spicy "kat" gravy.')
        ]
    },
    'west-bengal': {
        'name': 'West Bengal',
        'region': 'East India',
        'description': 'The cultural hub of art, Nobel literature, terracotta temples, riverine mangrove forests, and soul-stirring Baul philosophy.',
        'dances': [
            ('Chhau Dance of Purulia', 'A vigorous, acrobatic martial folk dance performed by dancers wearing oversized, painted clay and papier-mache masks.',
             'Inscribed by UNESCO, Purulia Chhau enacts mythological combat between gods and demons accompanied by the thunder of the Dhol and Dhamsa.'),
            ('Gaudiya Nritya', 'A classical Bengali dance tradition synthesizing temple ritual dances, Vaishnava padavali poetry, and classical scriptures.',
             'Characterized by graceful abhinaya, dramatic footwork, and spiritual devotion depicting Radha-Krishna romances.')
        ],
        'music': [
            ('Baul Music with Dotara', 'Mystic folk songs sung by wandering Baul minstrels who seek the divine in humanity through poetry and song.',
             'Accompanied by the two-stringed Dotara and Ektara, Baul philosophy deeply inspired Rabindranath Tagore and world literature.'),
            ('Rabindra Sangeet', 'The monumental body of over 2,200 songs composed by Rabindranath Tagore, defining Bengal\'s emotional landscape.',
             'Synthesizing classical ragas with Bengali folk melodies, these songs accompany every life milestone across Bengal.')
        ],
        'crafts': [
            ('Kantha Embroidery', 'The age-old craft of layering vintage cotton saris and quilting them with delicate running stitches into intricate floral stories.',
             'Practiced in Bolpur and Shantiniketan, Kantha turns recycled textiles into exquisite wearable masterworks.'),
            ('Terracotta of Bishnupur', 'Burnt clay sculptures and structural panels that adorn the 17th-century Malla dynasty temples of Bishnupur.',
             'Also famous for the iconic Bankura terracotta horses with erect ears and long necks, symbols of artistic pride.')
        ],
        'stories': [
            ('Thakurmar Jhuli', 'The beloved anthology of classic Bengali folk and fairy tales collected by Dakshinaranjan Mitra Majumder.',
             'Featuring princes on winged horses (Pakshiraj), brave princesses, and comic demons (Rakshasas) told by grandmothers.')
        ],
        'festivals': [
            ('Durga Puja', 'September-October', 'A monumental ten-day festival and UNESCO Intangible Cultural Heritage honoring Goddess Durga\'s victory over Mahishasura.', 'Transforms Kolkata into the world\'s largest open-air art installation with hundreds of unique themed pandals.'),
            ('Poila Boishakh', 'April', 'The joyous Bengali New Year celebrated with cultural parades, fresh financial ledgers (Haal Khata), and banquets.', 'Marked by the customary blessing "Shubho Noboborsho" and family get-togethers.')
        ],
        'cuisines': [
            ('Machher Jhol with Rice', 'A light, fragrant mustard or cumin-infused fish curry prepared with fresh freshwater carp (Rohu or Katla) and tender vegetables.', 'Freshwater fish, mustard oil, paanch phoron, potatoes, ginger, green chilies.', 'The daily culinary soul of every Bengali home.'),
            ('Kosha Mangsho & Mishti Doi', 'Slow-cooked, velvety spicy mutton curry paired with thick, caramelised sweet yogurt baked in earthen pots.', 'Mutton, mustard oil, onions, whole spices, curd, sweetened condensed milk.', 'The crown jewel of Bengali Sunday feasts and festive celebrations.')
        ]
    },
    'odisha': {
        'name': 'Odisha',
        'region': 'East India',
        'description': 'The soul of temple architecture, Odissi classical grace, sacred Jagannath customs, and ancient maritime trade heritage.',
        'dances': [
            ('Odissi Classical Dance', 'One of the oldest surviving classical dance forms, known for the graceful Tribhangi (three-bend posture) and lyrical footwork.',
             'Sculpted upon the stone walls of Konark Sun Temple, Odissi expresses poetic Ashtapadis from Jayadeva\'s Gita Govinda.'),
            ('Gotipua', 'A traditional dance performed by young boys dressed as women, the historical precursor to modern Odissi.',
             'Featuring breathtaking acrobatic bandhas (contortions), Gotipua dancers perform in village squares and temple premises.')
        ],
        'music': [
            ('Mardala', 'A barrel-shaped classical percussion drum made of wood and leather, essential to Odissi classical music.',
             'Possessing a deep, resonant pitch, the Mardala provides rhythmic clarity (tala) to classical dance and temple recitations.'),
            ('Odissi Classical Music', 'An ancient classical music stream with a 2,000-year history, distinct from Hindustani and Carnatic traditions.',
             'Characterized by lyrical rendering, emotional depth (Bhava), and structured rhythmic meters suited to Odia verse.')
        ],
        'crafts': [
            ('Pattachitra Scroll Painting', 'Ancient cloth-based scroll paintings with intricate detailing, natural stone pigments, and floral borders.',
             'Preserved by Chitrakar artisans in the heritage crafts village of Raghurajpur, depicting Jagannath legends and epics.'),
            ('Silver Filigree (Tarakasi)', 'Exquisite metalwork from Cuttack where fine strands of silver wire are bent and soldered into delicate jewelry and idols.',
             'Celebrated for its gossamer lightness, Tarakasi shimmers during Durga Puja as dazzling silver backdrops.')
        ],
        'stories': [
            ('Legends of Lord Jagannath', 'The sacred mythologies of the wooden deities of Puri who possess large round eyes and outstretched arms without hands.',
             'Symbolizes universal inclusion where the Lord is served as a living emperor who eats, sleeps, bathes, and falls ill.')
        ],
        'festivals': [
            ('Ratha Yatra of Puri', 'June-July', 'The world-famous Chariot Festival where Lord Jagannath, Balabhadra, and Subhadra are pulled in mammoth wooden chariots.', 'Millions of devotees pull the ropes of Nandighosa chariot along the Grand Road (Bada Danda) to Gundicha Temple.'),
            ('Konark Dance Festival', 'December', 'An open-air classical dance festival set against the illuminated backdrop of the 13th-century Sun Temple.', 'Attracts master dancers of Odissi, Bharatanatyam, and Kathak from across the globe.')
        ],
        'cuisines': [
            ('Dalma', 'A wholesome, nutritious lentil dish simmered with raw papaya, plantain, pumpkin, and tempered with roasted cumin and ghee.', 'Toor dal, raw vegetables, ginger, pancha phutana, ghee, roasted cumin-chili powder.', 'A revered temple offering in Puri Jagannath\'s Mahaprasad.'),
            ('Chhena Poda', 'The quintessential baked cottage cheese dessert, caramelized for hours until a golden-brown crust envelops its tender center.', 'Fresh cottage cheese (chhena), sugar, cardamom, cashews, raisins, ghee.', 'Invented in Nayagarh, Chhena Poda is celebrated as India\'s original baked cheesecake.')
        ]
    },
    'assam': {
        'name': 'Assam',
        'region': 'Northeast India',
        'description': 'Gateway to Northeast India, blessed with the mighty Brahmaputra, one-horned rhinos, emerald tea hills, and golden Muga silk.',
        'dances': [
            ('Bihu Dance', 'An exuberant folk dance celebrating youth, nature, and harvest, characterized by rapid hand movements and rhythmic hip sways.',
             'Young men and women dressed in golden Muga silk dance outdoors to welcome the Assamese New Year (Rongali Bihu).'),
            ('Sattriya Classical Dance', 'A classical Indian dance established in the 15th century by Vaishnavite saint Srimanta Sankardev in monastery island Majuli.',
             'Performed with religious devotion in Sattras (monasteries), Sattriya features storytelling through pure rhythm and emotive abhinaya.')
        ],
        'music': [
            ('Gogona and Pepa', 'Traditional folk wind and jaw harp instruments made from buffalo horn and mature bamboo.',
             'The Pepa\'s sharp, piercing calls and the Gogona\'s buzzing twangs form the recognizable soundscape of Bihu celebrations.'),
            ('Borgeet', 'A collection of devotional lyrical songs composed by Sankardev and Madhavdev in the Brajavali language.',
             'Set to distinct seasonal ragas, Borgeets are sung at prayer halls (Namghars) across Assam.')
        ],
        'crafts': [
            ('Assam Bamboo & Cane Crafts', 'Intricate daily objects, fishing traps, and conical umbrellas (Jaapi) woven from indigenous bamboo.',
             'Assam\'s artisans demonstrate unmatched mastery of split-bamboo weaving, balancing utilitarian durability with timeless elegance.'),
            ('Muga Golden Silk', 'A lustrous wild silk unique to Assam produced by the silkworm Antheraea assamensis, naturally golden-yellow in color.',
             'Known to grow shinier with every wash, Muga was historically reserved for Ahom royalty.')
        ],
        'stories': [
            ('Burhi Aair Xadhu', 'Grandmother\'s Tales, a celebrated collection of Assamese folk tales compiled by Lakshminath Bezbaroa in 1911.',
             'Featuring iconic allegorical stories like Tejimola and the Kite\'s Daughter that transmit Assamese ethical values.')
        ],
        'festivals': [
            ('Rongali Bihu', 'April', 'The greatest festival of Assam, heralding the spring agricultural cycle with feasts, folk songs, and community dancing.', 'Brings together people of all ethnicities to celebrate renewal and the beginning of the Assamese calendar.'),
            ('Ambubachi Mela', 'June', 'An ancient tantric festival celebrated at the Kamakhya Temple atop Nilachal Hill, honoring Mother Earth\'s fertility.', 'Attracts sadhus, ascetics, and pilgrims from across India for sacred ritual blessings.')
        ],
        'cuisines': [
            ('Khaar', 'An alkaline signature starter prepared by filtering water through sun-dried, burned banana peel ashes with raw papaya.', 'Filtered banana ash water (Khaar), raw papaya, mustard seeds, garlic, fish head or pulses.', 'Assam\'s unique cleansing palate cleanser believed to improve digestion.'),
            ('Masor Tenga', 'A light, refreshing sour fish curry infused with elephant apple (Ou Tenga), tomatoes, or lemon juice.', 'Freshwater fish, elephant apple or lemon, mustard oil, green chilies, fenugreek.', 'The soul-soothing summer meal of rural Assam paired with steaming Joha rice.')
        ]
    },
    'karnataka': {
        'name': 'Karnataka',
        'region': 'South India',
        'description': 'The land of Vijayanagara ruins at Hampi, fragrant sandalwood forests, coffee plantations of Coorg, and tech innovation in Bengaluru.',
        'dances': [
            ('Yakshagana', 'A spectacular traditional theatre form combining dance, music, improvised dialogue, and elaborate costumes and makeup.',
             'Staged through the night in coastal Karnataka, Yakshagana brings episodes from the Mahabharata and Ramayana to life.'),
            ('Dollu Kunitha', 'A high-energy, acrobatic drumming folk dance performed by men of the Kuruba shepherd community using heavy lacquered drums.',
             'Accompanied by cymbals and flutes, dancers execute synchronized jumps and spirals in honor of the folk deity Beereshwara.')
        ],
        'music': [
            ('Carnatic Mysore Veena', 'The distinctive veena tradition refined under the royal patronage of the Wodeyars of Mysore.',
             'Celebrated for its melodic purity, rich tonal resonance, and fluid execution of intricate gamakas.'),
            ('Haridasa Sahitya', 'Devotional music and philosophy popularized by wandering saint-composers like Purandara Dasa (the father of Carnatic music).',
             'Set to accessible folk meters, these verses expound ethical virtues and devotion to Lord Vitthala.')
        ],
        'crafts': [
            ('Mysore Silk Weaving', 'Sumptuous crepe silk sarees with 100% pure gold zari borders, woven under government supervision in Mysore.',
             'Known for their extraordinary durability and soft drape, Mysore silk is a hallmark of South Indian festive elegance.'),
            ('Channapatna Wooden Toys', 'Safe, eco-friendly wooden toys turned on lathes and lacquered with natural vegetable dyes.',
             'Originating under the patronage of Tipu Sultan, these brightly colored wooden horses, dolls, and puzzles are world-famous.')
        ],
        'stories': [
            ('Tales of Kittur Rani Chennamma', 'The heroic saga of the warrior queen of Kittur who led an armed rebellion against the British East India Company in 1824.',
             'Chennamma\'s defiance remains an indelible beacon of courage and independence across Karnataka.')
        ],
        'festivals': [
            ('Mysore Dasara', 'September-October', 'A ten-day royal festival where Mysore Palace is illuminated with nearly 100,000 bulbs, ending in the grand Jumboo Savari.', 'The golden idol of Goddess Chamundeshwari is paraded atop a decorated elephant in royal splendor.'),
            ('Kambala Buffalo Races', 'November-March', 'An adrenaline-fueled traditional sport where farmers race pairs of buffalos through flooded muddy paddy tracks.', 'Celebrates the bond between coastal farmers and their livestock in Dakshina Kannada.')
        ],
        'cuisines': [
            ('Bisi Bele Bath', 'A comforting, spicy one-pot dish of rice, lentils, assorted vegetables, and a proprietary aromatic spice mix fried in ghee.', 'Rice, toor dal, vegetables, bisi bele bath powder, tamarind, cashews, pure ghee.', 'A timeless culinary jewel created in the royal kitchens of the Mysore Palace.'),
            ('Mysore Pak', 'A decadent sweet made of roasted gram flour, generous pure ghee, and sugar, famous for its melt-in-mouth texture.', 'Gram flour (besan), pure desi ghee, sugar syrup, cardamom.', 'Created in 1935 by palace royal chef Kakasura Madappa for the Maharaja of Mysore.')
        ]
    },
    'andhra-pradesh': {
        'name': 'Andhra Pradesh',
        'region': 'South India',
        'description': 'The land of Tirupati hills, Kuchipudi classical drama, Kalamkari textiles, and fiery coastal spice gastronomy.',
        'dances': [
            ('Kuchipudi Classical Dance', 'A classical dance-drama originating in Kuchipudi village, combining rapid footwork, expressive eyes, and brass plate balancing.',
             'Dancers execute Tarangam, dancing with their feet balanced on the rim of a brass plate while holding a water pitcher on their head.'),
            ('Lambadi Dance', 'A colorful folk dance of the semi-nomadic Banjara (Lambadi) tribe, celebrating harvest and weddings.',
             'Women dressed in mirror-encrusted ghagras and heavy brass armlets dance in synchronized circles with rhythmic clapping.')
        ],
        'music': [
            ('Annamacharya Sankeertanas', 'The divine devotional songs composed by 15th-century saint Annamayya in praise of Lord Venkateswara.',
             'Inscribed on copper plates at Tirumala, these verses form a cornerstone of the Andhra classical Carnatic repertoire.'),
            ('Kanjeera and Mridangam', 'Dynamic percussive instruments providing complex rhythmic accompaniment in classical Carnatic concerts.',
             'Andhra percussionists are celebrated for rhythmic mathematical improvisations known as Korvais and Thani Avarthanam.')
        ],
        'crafts': [
            ('Kalamkari Hand-painted Textiles', 'Ancient textile art from Srikalahasti and Machilipatnam where cotton fabric is hand-drawn using bamboo pens and vegetable dyes.',
             'Depicts scenes from the Ramayana and Mahabharata using alum, jaggery, myrobalan, and natural indigo.'),
            ('Kondapalli Wooden Toys', 'Lightweight wooden toys hand-carved from softwood (Tella Poniki) in Kondapalli village near Vijayawada.',
             'Famous for figurines of village life, bullock carts, and the mythological Dasavataram sets.')
        ],
        'stories': [
            ('Legends of Tirupati Balaji', 'The eternal tale of Lord Venkateswara taking abode in the Seven Hills of Tirumala to protect humanity during the Kali Yuga.',
             'The world\'s most visited shrine inspires millions with stories of unconditional divine compassion.')
        ],
        'festivals': [
            ('Ugadi', 'March-April', 'The Telugu New Year celebrated with the tasting of Ugadi Pachadi, a dish incorporating all six basic tastes.', 'Symbolizes that life is an inevitable mixture of happiness, sorrow, surprise, anger, fear, and disgust.'),
            ('Tirupati Brahmotsavam', 'September-October', 'A nine-day mega-festival where Lord Malayappa Swamy is taken out in daily ceremonial processions on divine mounts.', 'Attracts hundreds of thousands of pilgrims to the sacred Tirumala hill shrine.')
        ],
        'cuisines': [
            ('Pesarattu with Allam Pachadi', 'A crisp, wholesome crepe made from soaked whole green gram (moong dal), paired with spicy-sweet ginger chutney.', 'Whole green moong dal, ginger, cumin, green chilies, onions, tamarind jaggery chutney.', 'Andhra Pradesh\'s signature high-protein breakfast delight.'),
            ('Gongura Pachadi', 'A spicy, tangy pickle prepared from red sorrel leaves, roasted dry red chilies, garlic, and cold-pressed sesame oil.', 'Gongura (sorrel) leaves, red chilies, garlic, mustard seeds, fenugreek, oil.', 'Known as the "Andhra Shakahaara King", an indispensable accompaniment to hot steamed rice.')
        ]
    },
    'telangana': {
        'name': 'Telangana',
        'region': 'South India',
        'description': 'The land of the Kakatiya dynasty, Golconda diamonds, Charminar bazaars, Bathukamma flowers, and vibrant Deccan heritage.',
        'dances': [
            ('Perini Sivatandavam', 'An ancient, athletic warrior dance revived from Kakatiya temple sculptures in Ramappa Temple.',
             'Historically performed by soldiers before marching into battle to evoke the fury and courage of Lord Shiva.'),
            ('Oggu Katha Dance', 'A dramatic traditional folk singing and dance performance by the Kuruma and Golla shepherd communities.',
             'Dancers wear brass crowns and bells, narrating the heroic exploits of folk deities Mallanna and Beerappa.')
        ],
        'music': [
            ('Kinnera Instrument', 'An indigenous stringed instrument crafted with dried gourds and animal bone frets, historically played by Dakkali minstrels.',
             'Revived in modern times as a recognized national art form, embodying the oral ballads of rural Telangana.'),
            ('Dappu Percussion', 'A circular tambourine-style frame drum played with two wooden sticks, producing driving, energetic rhythms at village festivals.',
             'The pulse of Dalit and community celebrations across Telangana, symbolizing collective solidarity and festive joy.')
        ],
        'crafts': [
            ('Pochampally Ikat', 'World-renowned geometric tie-and-dye weaving where warp and weft threads are individually dyed before loom placement.',
             'Hailing from the Bhoodan Pochampally silk village, this UNESCO-recognized craft produces sharp, symmetrical motifs.'),
            ('Nirmal Toys & Paintings', 'Fine wooden crafts painted with traditional herbal colors and coated in golden varnish made from mineral extracts.',
             'Dating back to the 14th century, Nirmal artisans depict flora, birds, and Mughal miniature inspirations.')
        ],
        'stories': [
            ('Sammakka Saralamma Legend', 'The heroic tale of tribal mother and daughter who fought bravely against the Kakatiya army to protest unjust taxes during a drought.',
             'Commemorated at Medaram, their martyrdom became Asia\'s largest biennial tribal gathering.')
        ],
        'festivals': [
            ('Bathukamma Floral Festival', 'September-October', 'A nine-day floral festival celebrated by women who arrange seasonal wildflowers into conical temple towers.', 'Women dance in circles singing folk songs celebrating womanhood, nature, and motherly protection.'),
            ('Bonalu', 'July-August', 'A vibrant monsoon festival thanking Goddess Mahakali for communal protection, with women carrying cooked rice pots atop their heads.', 'Features colorful Pothuraju dancers whipping the air to ward off negative spirits.')
        ],
        'cuisines': [
            ('Hyderabadi Dum Biryani', 'Fragrant basmati rice and marinated meat slow-cooked in a sealed clay handi over charcoal with saffron and mint.', 'Basmati rice, chicken/mutton, yogurt, fried onions (birista), saffron, cardamom, cloves, mint.', 'The world-famous jewel of Nizami cuisine perfected over centuries in Hyderabad.'),
            ('Sarva Pindi', 'A savory, crispy circular pancake made from rice flour, roasted peanuts, chana dal, sesame seeds, and curry leaves.', 'Rice flour, roasted peanuts, chana dal, white sesame seeds, green chilies, onions.', 'A wholesome traditional afternoon snack from rural Telangana.')
        ]
    },
    'uttar-pradesh': {
        'name': 'Uttar Pradesh',
        'region': 'North India',
        'description': 'The cradle of Indian civilization along the Ganga and Yamuna, home to Kashi\'s ghats, Awadhi courts, and the Taj Mahal.',
        'dances': [
            ('Kathak Classical Dance', 'One of India\'s major classical dances, originating from traveling storytellers (Kathakars) in ancient North Indian temples.',
             'Flourished under Lucknow and Banaras Gharanas, known for lightning-fast pirouettes (Chakkars) and expressive storytelling (Abhinaya).'),
            ('Charkula Dance', 'A dramatic folk dance of the Braj region where women balance large circular wooden tiers with 108 oil lamps on their heads.',
             'Performed during Dooj after Holi, symbolizing Radha\'s birthday celebrations in Krishna lore.')
        ],
        'music': [
            ('Shehnai of Varanasi', 'A sacred double-reed woodwind instrument immortalized by Bharat Ratna Ustad Bismillah Khan on the ghats of Kashi.',
             'Its soulful melodies echo across temples, classical concerts, and traditional weddings throughout India.'),
            ('Banaras Tabla Gharana', 'A powerhouse percussive tradition famous for vigorous open-palm strokes (Khula Baaj) adapted from the Pakhawaj.',
             'Renowned for its energetic accompaniment of Thumri, Dadra, and classical Kathak performances.')
        ],
        'crafts': [
            ('Banarasi Zari Silk Sarees', 'Opulent handloom silk sarees from Varanasi featuring heavy brocade with real gold and silver zari threads.',
             'Adorned with Mughal-inspired floral jaals (bel), paisleys, and minakari accents, a staple of Indian bridal trousseaus.'),
            ('Chikankari Embroidery of Lucknow', 'Delicate, ethereal shadow-work and white-on-white needlework perfected in the royal courts of the Nawabs of Awadh.',
             'Using over thirty distinct hand stitches on muslin, cotton, and organza to produce poetic botanical patterns.')
        ],
        'stories': [
            ('The Ramayana of Ayodhya', 'The epic saga of Lord Rama\'s righteousness, exile, and victory, originating on the banks of the Sarayu in Ayodhya.',
             'Immortalized in the vernacular by Goswami Tulsidas in his Ramcharitmanas, shaping the cultural soul of Northern India.')
        ],
        'festivals': [
            ('Dev Deepawali of Varanasi', 'November', 'The celestial night of Kartik Purnima when all eighty-four ghats of Varanasi are illuminated with millions of earthen diyas.', 'Celebrates the victory of Lord Shiva over the demon Tripurasura as divine beings descend to bathe in the holy Ganga.'),
            ('Kumbh Mela', 'January-February', 'The world\'s largest human religious gathering, held every twelve years at the sacred Sangam in Prayagraj.', 'Millions of sadhus, pilgrims, and visitors unite to take holy dips in the confluence of the Ganga, Yamuna, and Saraswati.')
        ],
        'cuisines': [
            ('Awadhi Dum Biryani & Galouti Kebab', 'Melt-in-the-mouth smoked kebabs flavored with over 150 royal spices, paired with fragrant layered dum biryani.', 'Minced meat, raw papaya, potli masala, saffron, basmati rice, rose water, kewra.', 'Created for the toothless Nawab Asad-ud-Daula by master royal bawarchis of Lucknow.'),
            ('Banarasi Paan & Malaiyyo', 'Winter milk foam infused with saffron and pistachios, followed by the iconic sweet betel leaf prepared with fragrant gulkand.', 'Milk froth, saffron, pistachios, betel leaf, gulkand, supari, silver vark.', 'The legendary sweet finish to a royal dining experience in Kashi.')
        ]
    },
    'madhya-pradesh': {
        'name': 'Madhya Pradesh',
        'region': 'Central India',
        'description': 'The heart of incredible India, renowned for Khajuraho temples, Sanchi stupas, tiger reserves, and tribal Gond artistry.',
        'dances': [
            ('Matki Dance', 'A community folk dance performed by women of the Malwa region balancing earthen pots (matkis) atop their heads.',
             'Accompanied by the beats of the Dhol, the lead dancer begins with one pot and adds more as the tempo increases.'),
            ('Karma Dance', 'A sacred tribal dance of the Gond and Baiga tribes performed around the sacred Karma tree at the onset of spring.',
             'Celebrates fertility, nature\'s rejuvenation, and ancestral blessing through synchronized swaying and song.')
        ],
        'music': [
            ('Dhrupad of Gwalior', 'The oldest existing classical vocal music style of India, nurtured in the historic court of Raja Man Singh Tomar.',
             'Focuses on austere, spiritual exploration of the raga through deep breath control and long, meditative alap passages.'),
            ('Chikara and Singa', 'Folk tribal instruments including the bowed Chikara and the Singa horn made from wild buffalo horns.',
             'Used by tribal bards to sing ancient ballads of forest gods and historic chieftains.')
        ],
        'crafts': [
            ('Chanderi and Maheshwari Weaving', 'Lightweight, shimmering handloom fabrics blending silk and fine cotton, famous for reversible zari borders.',
             'Patronized by the Holkar queen Ahilyabai, these sarees are prized for their featherlight drape and regal motifs.'),
            ('Gond Tribal Art', 'Vibrant canvas and wall paintings characterized by dots, dashes, and lines that create pulsating forms of animals and sacred trees.',
             'Believed to invite good luck, modern Gond art has earned international acclaim in museums worldwide.')
        ],
        'stories': [
            ('Rani Durgavati of Gondwana', 'The courageous queen of the Garha-Katanga kingdom who led armies against imperial Mughal forces to defend her people\'s honor.',
             'Remembered as a fearless warrior and patron of water reservoirs across Jabalpur.')
        ],
        'festivals': [
            ('Khajuraho Dance Festival', 'February', 'A week-long celebration of classical Indian dance against the illuminated backdrop of 10th-century Chandela temples.', 'Masters of all eight classical dance styles perform under open starry skies.'),
            ('Tansen Samaroh Gwalior', 'December', 'India\'s oldest music festival honoring the legendary court musician Mian Tansen near his historic tomb.', 'Top classical vocalists and instrumentalists perform round-the-clock raag recitals.')
        ],
        'cuisines': [
            ('Poha Jalebi', 'Flattened rice tossed with mustard seeds, curry leaves, onions, and crunchy sev, served alongside piping-hot golden jalebis.', 'Poha (flattened rice), onions, fennel seeds, sev, green chilies, jalebi.', 'The unbeatable breakfast icon across streets in Indore, Bhopal, and Ujjain.'),
            ('Dal Bafla', 'Soft, boiled-and-baked wheat dough balls bathed in pure ghee, served with spicy toor dal and coriander-mint chutney.', 'Wheat flour, semolina, toor dal, ghee, cumin, coriander, spices.', 'Malwa\'s beloved cousin of the Rajasthani baati, loved for its softer, pillowy texture.')
        ]
    },
    'bihar': {
        'name': 'Bihar',
        'region': 'East India',
        'description': 'The historic land of the Buddha\'s enlightenment, Mahavira, ancient Nalanda University, and vibrant Madhubani painting.',
        'dances': [
            ('Jat-Jatin Dance', 'A traditional folk dance-drama performed by women in Mithila during monsoon nights, portraying the love and quarrels of a married couple.',
             'Reflects rural domestic realities, economic migrations, and the tenderness of reunion after long separations.'),
            ('Bidesia Dance', 'A popular folk theatre created by the legendary Bhikhari Thakur, addressing the social pain of migrant workers leaving their families.',
             'Combines sharp musical satire, heart-wrenching emotional monologues, and expressive folk steps.')
        ],
        'music': [
            ('Maithili Songs of Vidyapati', 'Devotional and romantic lyrics composed by the 14th-century poet Vidyapati in praise of Shiva and Radha-Krishna.',
             'Sung at every wedding and festival in Mithila, embodying the lyrical sweetness of the Maithili language.'),
            ('Bhojpuri Biraha', 'A spirited narrative singing genre of rural Bihar recounting historic legends, morality tales, and romantic ballads.',
             'Accompanied by the Dholak, harmonium, and kartal, Biraha energizes village gatherings under banyan trees.')
        ],
        'crafts': [
            ('Madhubani (Mithila) Paintings', 'Ancient folk painting done with fingers, twigs, brushes, and matchsticks using natural dyes and pigments.',
             'Characterized by eye-catching geometrical patterns, fish, peacocks, and mythological scenes filling every square inch.'),
            ('Sikki Grass Crafts', 'Golden-hued wild grass harvested from riverbanks and woven into sturdy, decorative baskets, boxes, and toys.',
             'Traditionally made by brides as part of their wedding dowry, combining functional durability with artistic flair.')
        ],
        'stories': [
            ('The Enlightenment of Buddha', 'The historic narrative of Prince Siddhartha Gautama meditating under the Bodhi Tree in Bodh Gaya until attaining supreme wisdom.',
             'Bodh Gaya remains the supreme spiritual center for millions of seekers from every continent.')
        ],
        'festivals': [
            ('Chhath Puja', 'October-November', 'An austere four-day festival dedicated to the Sun God (Surya) and Chhathi Maiya, without priests or idol worship.', 'Devotees stand waist-deep in river waters at dawn and dusk offering arghya of seasonal fruits and thekua.'),
            ('Sonepur Cattle Fair', 'November', 'One of Asia\'s largest traditional animal fairs held on the confluence of the Ganga and Gandak rivers on Kartik Purnima.', 'Historical trading post for elephants, horses, and livestock alongside vibrant carnival entertainment.')
        ],
        'cuisines': [
            ('Litti Chokha', 'Roasted whole-wheat dough balls stuffed with spiced roasted gram flour (sattu), served with smoky roasted eggplant-tomato mash.', 'Wheat flour, sattu (gram flour), ajwain, kalonji, mustard oil, brinjal, tomatoes, garlic, ghee.', 'The nutritious, smoky soul food of Bihar celebrated across the nation.'),
            ('Thekua & Khaja', 'Crispy deep-fried sweet biscuits flavored with fennel and cardamom, and flaky layered pastries from Silao soaked in syrup.', 'Wheat flour, jaggery or sugar, ghee, fennel seeds, cardamom, refined flour.', 'The revered prasad of Chhath Puja and a cherished festive souvenir from Nalanda.')
        ]
    },
    'jharkhand': {
        'name': 'Jharkhand',
        'region': 'East India',
        'description': 'The land of dense forests, cascading waterfalls, rich minerals, tribal Santhal traditions, and Birsa Munda\'s courage.',
        'dances': [
            ('Paika Martial Dance', 'A thrilling tribal martial dance performed by male dancers holding shields and swords, dressed in colorful dhotis and turbans.',
             'Historically executed by Munda warriors to hone reflexes, agility, and courage for self-defense and battlefield warfare.'),
            ('Santhali Dance', 'A harmonious group dance performed in neat rows and semicircles by Santhal men and women with arms linked.',
             'Moving backward and forward in unison to the hypnotic rhythms of the Mandar drum and Tirio flute during spring festivals.')
        ],
        'music': [
            ('Mandar and Nagara', 'Large earthen and leather drums that serve as the heartbeat of all tribal celebrations and dances across Jharkhand.',
             'The deep bass resonance of the Mandar can be heard echoing across forest villages during festival nights.'),
            ('Banam Tribal Violin', 'A single-stringed bowed instrument carved from gulo wood by Santhal craftspeople, often shaped like a human torso.',
             'Considered a living, breathing spirit by Santhal musicians, the Banam tells ancestral stories of nature and cosmic origins.')
        ],
        'crafts': [
            ('Sohrai and Khovar Murals', 'UNESCO-recognized ritual wall murals painted by tribal women using natural red, black, and white clay during harvest and weddings.',
             'Features lines, tooth marks, and stylized motifs of horned bulls, peacocks, deer, and sacred fertility trees.'),
            ('Paitkar Scroll Paintings', 'One of the oldest surviving scroll painting forms in India, practiced by the Chitrakar community in Amadubi village.',
             'Depicting tribal myths of creation, forest life, and what happens to the human soul after death.')
        ],
        'stories': [
            ('Legends of Birsa Munda', 'The fearless young tribal leader and folk hero "Dharti Aaba" (Father of the Earth) who led the Ulgulan rebellion against British colonial exploitation.',
             'Revered as a divine prophet who championed tribal autonomy (Jal, Jungle, Jameen) and cultural dignity.')
        ],
        'festivals': [
            ('Sarhul Spring Festival', 'March-April', 'The greatest festival of the Oraon, Munda, and Santhal tribes, worshipping the blooming Sal trees.', 'Villagers take sacred Sal blossoms to their homes, celebrating the spiritual wedding of the Sun and Mother Earth.'),
            ('Karma Festival', 'August-September', 'A sacred tribal festival where young boys and girls plant Karma tree branches in the village akhara to pray for prosperity.', 'Accompanied by all-night dancing, storytelling, and community bonding.')
        ],
        'cuisines': [
            ('Dhuska with Ghugni', 'A savory deep-fried pancake made from soaked rice and chana dal batter, served with spicy black chickpea curry.', 'Rice, chana dal, urad dal, green chilies, ginger, black chickpeas, spices.', 'Jharkhand\'s favorite breakfast street food, loved for its crispy exterior and soft center.'),
            ('Rugda Curry', 'A seasonal wild mushroom found under Sal forest canopies during monsoons, cooked in a rich, mustard-onion gravy.', 'Fresh rugda mushrooms, onions, ginger-garlic paste, mustard oil, garam masala.', 'A prized natural delicacy that boasts a meaty texture and deep umami flavor.')
        ]
    },
    'chhattisgarh': {
        'name': 'Chhattisgarh',
        'region': 'Central India',
        'description': 'The land of pristine Sal forests, Chitrakote "Niagara" falls, Bastar bell-metal craftsmanship, and Pandavani epics.',
        'dances': [
            ('Panthi Dance', 'An energetic devotional dance of the Satnami community, featuring towering human pyramids and brisk acrobatic formations.',
             'Chanting the egalitarian philosophy of Guru Ghasidas, dancers move to the rapid beats of the Mandar and Jhanjh cymbals.'),
            ('Raut Nacha', 'A vibrant folk dance performed by the Yaduvanshi (cowherd) community during Diwali, celebrating Lord Krishna\'s victory over Kansa.',
             'Dancers dressed in bright costumes and peacock feather headgears carry painted sticks, performing mock duels and singing couplets (Dohas).')
        ],
        'music': [
            ('Pandavani Ballads', 'A world-acclaimed musical folk ballad theatre narrating Mahabharata tales, immortalized by Padma Vibhushan Teejan Bai.',
             'The lead performer holds a tambura like a warrior\'s mace, sword, or bow, alternating fiery speech with dramatic song.'),
            ('Mandar and Chikara', 'Traditional folk percussion and bowed strings that guide the rhythm of forest harvesting rituals and social dances.',
             'Carved from hollowed logs and stretched goat leather, creating raw, earthy melodies.')
        ],
        'crafts': [
            ('Bastar Dhokra Bell Metal', 'Ancient lost-wax metal casting technique dating back 4,000 years to Mohenjo-daro, practiced by tribal Ghadwa artisans.',
             'Crafts intricate, rustic brass figures of tribal deities, elephants, deer, and ceremonial candle lamps.'),
            ('Bastar Wrought Iron Craft (Loha Shilp)', 'Artisans recycle scrap iron into slender, minimalist sculptures of forest animals, lamps, and musicians.',
             'Hand-beaten over open charcoal flames without molds or welds, creating modern geometric elegance.')
        ],
        'stories': [
            ('The Pandavani Epics', 'The dramatic retelling of the lives of Bhima, Draupadi, and Arjuna through indigenous tribal perspectives and dialect.',
             'Focuses on strength, perseverance, and ethical resilience, captivating global audiences in theatre festivals.')
        ],
        'festivals': [
            ('Bastar Dussehra', 'October', 'A unique 75-day festival celebrated by tribal communities without burning effigies of Ravana, honoring Goddess Danteshwari.', 'Features the ceremonial construction and pulling of a massive double-decker wooden chariot by hundreds of tribal devotees.'),
            ('Madai Fair', 'January-March', 'A vibrant nomadic tribal fair held across Bastar villages where local village gods are brought together in grand processions.', 'Accompanied by traditional folk sports, cock fights, and festive open-air bazaars.')
        ],
        'cuisines': [
            ('Faraa & Chila', 'Steamed rice dumplings seasoned with mustard seeds and curry leaves, paired with crisp savory rice pancakes and tangy tomato chutney.', 'Rice flour, chana dal stuffing, green chilies, mustard seeds, curry leaves.', 'Healthy, comforting staples consumed daily in rural Chhattisgarhi homes.'),
            ('Muthia & Bafauri', 'Steamed spiced gram dumplings lightly pan-fried in oil, and crunchy vegetable patties prepared without deep-frying.', 'Chana dal, leafy greens, onions, ginger-garlic paste, sesame seeds.', 'Nutritious traditional snacks that demonstrate clever indigenous oil-free cooking techniques.')
        ]
    },
    'himachal-pradesh': {
        'name': 'Himachal Pradesh',
        'region': 'North India',
        'description': 'The land of snow-clad peaks, apple valleys, pine forests, ancient wooden temples, and peaceful mountain shrines.',
        'dances': [
            ('Nati Folk Dance', 'A slow, graceful circle dance performed by hundreds of men and women in traditional woolen attire, holding hands in winding formations.',
             'Recognized in the Guinness World Records, Nati celebrates harvest festivals, marriages, and Kullu Dussehra.'),
            ('Chham (Lama Dance)', 'A mystical masked monastic dance performed by Tibetan Buddhist monks in monasteries like Tabo and Ki.',
             'Monks wearing heavy silk brocades and fearsome deity masks enact the triumph of compassion over ego and negative karma.')
        ],
        'music': [
            ('Ranasingha', 'A curved, two-piece S-shaped brass wind horn blown at high mountain passes, royal processions, and temple ceremonies.',
             'Its long, resonant blast echoes across deep Himalayan valleys, heralding the arrival of palanquins of local devtas.'),
            ('Dhol-Damau', 'Paired mountain percussion instruments that dictate the measured tempo of traditional Nati dance steps.',
             'Handcrafted by generational village musicians who preserve sacred rhythmic beats.')
        ],
        'crafts': [
            ('Kullu Shawls', 'Warm woolen shawls woven from Merino, Angora, or local sheep wool, featuring distinctive geometric borders in bright hues.',
             'Originating from handloom weavers of the Kullu Valley, these GI-tagged shawls combine thermal warmth with Nordic-like motifs.'),
            ('Chamba Rumal', 'Delicate double-sided embroidery on unbleached silk or muslin where the front and back appear completely identical (Dorukha).',
             'Depicting Krishna\'s Raas Leela and epic scenes, historically patronized by Pahari royalty as bridal gifts.')
        ],
        'stories': [
            ('The Legend of Hidimba Devi', 'The powerful forest goddess and wife of the Pandava warrior Bhima, enshrined in the iconic wooden pagoda temple in Manali.',
             'Revered by mountain folk as the supreme guardian against natural calamities and epidemics.')
        ],
        'festivals': [
            ('Kullu Dussehra', 'October', 'A week-long international festival where over two hundred village deities (Devtas) assemble in Dhalpur ground to pay homage to Lord Raghunath.', 'Unlike other Dussehra celebrations, it begins on the day when celebrations end elsewhere in India.'),
            ('Minjar Fair of Chamba', 'July-August', 'A historic monsoon harvest carnival commemorating the blooming of maize shoots (Minjar), marked by processions to the Ravi River.', 'People pin golden silk tassels to their garments symbolizing communal harmony and agricultural gratitude.')
        ],
        'cuisines': [
            ('Himachali Dham', 'A ceremonial multi-course vegetarian banquet cooked exclusively by traditional Brahman chefs called Botis in brass pots.', 'Basmati rice, Madra (kidney beans in yogurt), Chana Khatta, Mah ki Dal, Meetha Bhat.', 'Served without onions or garlic on dried leaf plates at festive celebrations.'),
            ('Siddu with Pure Ghee', 'A steamed oval wheat bread stuffed with a savory filling of crushed walnuts, poppy seeds, and spices, drenched in melting desi ghee.', 'Wheat flour, yeast, walnuts, poppy seeds, green chilies, coriander, pure ghee.', 'The ultimate winter comfort food of Himachal that keeps mountain dwellers warm in snowy months.')
        ]
    },
    'uttarakhand': {
        'name': 'Uttarakhand',
        'region': 'North India',
        'description': 'Devbhoomi, the Land of the Gods, cradle of the Ganges, snow-clad Garhwal and Kumaon ranges, and sacred Char Dham shrines.',
        'dances': [
            ('Choliya Martial Dance', 'A centuries-old martial sword dance of Kumaon performed by warrior artists holding gleaming brass shields and curved swords.',
             'Accompanied by the Ranasingha horn and Turi, dancers leap and feign duels to ward off malevolent spirits from wedding processions.'),
            ('Jhora Folk Dance', 'An inclusive community circle dance where people of all ages and backgrounds join hands, swaying together to poetic songs.',
             'Performed during spring fairs and moonlit evenings, expressing gratitude to the surrounding mountain peaks.')
        ],
        'music': [
            ('Dhol-Damau of Garhwal', 'The sacred percussive heartbeat of Uttarakhand, capable of conveying 22 distinct musical chapters (Badyas).',
             'Masters of the Dhol can signal temple rituals, wedding ceremonies, emergency calls, or agricultural stages through specific drum strokes.'),
            ('Hurka Drum', 'An hourglass-shaped percussion instrument held under the arm and beaten with the fingers while dancing.',
             'Used during paddy transplanting (Hurkiya Baul) to sing heroic mountain ballads that motivate farmers in stepped terrace fields.')
        ],
        'crafts': [
            ('Aipan Folk Art', 'Sacred ritual floor and wall geometric art painted with rice flour paste (Biswar) over a red ochre (Geru) background.',
             'Executed by Kumaoni women on doorsteps, prayer rooms, and seats of honor to welcome prosperity and auspiciousness.'),
            ('Ringal Bamboo Weaving', 'Durable, smooth baskets, storage containers, and mats woven from wild dwarf bamboo (Ringal) harvested in high forests.',
             'Crafted by artisans in Chamoli and Pithoragarh, renowned for water-resistant strength and fine weaving.')
        ],
        'stories': [
            ('The Legend of Nanda Devi', 'The sacred myth of Goddess Nanda, daughter of the Himalayas, who chose the majestic twin peaks of Nanda Devi as her celestial home.',
             'Considered the mother and protector of all Garhwalis and Kumaonis, commanding profound devotion.')
        ],
        'festivals': [
            ('Nanda Devi Raj Jat', 'Once every 12 years', 'A challenging three-week 280-kilometer barefoot pilgrimage following a four-horned ram to high-altitude Roopkund and Homkund.', 'One of the world\'s most awe-inspiring mountain pilgrimages honoring Goddess Nanda\'s return to Mount Kailash.'),
            ('Phool Dei Spring Festival', 'March', 'A delightful spring festival where young children go from doorstep to doorstep sprinkling wild yellow and white mountain blossoms.', 'Children sing wishing households prosperity and health, receiving sweet rice snacks (Papdi) in return.')
        ],
        'cuisines': [
            ('Kafuli & Chainsoo', 'A velvety green puree of wild mountain greens (spinach and fenugreek) and a roasted black gram curry cooked in an iron kadhai.', 'Spinach, methi, rice paste, black gram, garlic, jakhiya seeds, mustard oil.', 'Rich in minerals, iron, and warmth, the signature daily nourishment of Garhwal.'),
            ('Bal Mithai of Almora', 'A brown, fudge-like sweet made by roasting evaporated milk (khoya) for hours until caramelized, coated in tiny sugar pearls.', 'Khoya (milk solids), sugar, cardamom, white sugar balls.', 'The beloved hundred-year-old confectionery pride of Kumaon.')
        ]
    },
    'haryana': {
        'name': 'Haryana',
        'region': 'North India',
        'description': 'The land of the historic Kurukshetra battlefield, ancient Saraswati civilization, robust wrestling traditions, and fertile green fields.',
        'dances': [
            ('Dhamal Folk Dance', 'An ancient folk dance dating back to the Mahabharata era, performed by men on moonlit nights to celebrate the harvest of crops.',
             'Dancers jump and twirl energetically to the beats of the Dhol, Dph, and Chang drums.'),
            ('Khoria Dance', 'A lively folk dance performed exclusively by women at the groom\'s house while the men have departed for the bride\'s wedding procession.',
             'Women wear wide flared skirts (Daman) and silver ornaments, enacting humorous theatrical sketches of domestic life.')
        ],
        'music': [
            ('Saang Musical Folk Theatre', 'An iconic verse-drama theatre form performed by traveling troupes in open village arenas.',
             'Blending classical ragas with earthy Haryanvi wit, Saang educates and entertains with historical epics like Alha-Udal and Raja Gopichand.'),
            ('Sarangi of Haryana', 'A bowed string instrument carved from wood, capable of mimicking the subtleties of the human singing voice.',
             'Provides the melodic backbone to traditional Haryanvi Raaginis and folk songs.')
        ],
        'crafts': [
            ('Panipat Handloom & Durries', 'Known as the "City of Weavers", Panipat produces world-class hand-woven cotton durries, rugs, and thermal blankets.',
             'Featuring bold geometric patterns and vibrant color blocks that reflect Haryana\'s forthright, spirited character.'),
            ('Rewari Brass and Tilla Jootis', 'Intricately embroidered leather jootis embellished with gold and silver threads, paired with traditional beaten brassware.',
             'Showcases generations of artisanal expertise in leather tanning, metal spinning, and embroidery.')
        ],
        'stories': [
            ('The Bhagavad Gita at Kurukshetra', 'The philosophical dialogue delivered by Lord Krishna to the warrior prince Arjuna on the battlefield of Kurukshetra.',
             'Addresses duty, action without attachment (Karma Yoga), and cosmic devotion, serving as humanity\'s enduring ethical compass.')
        ],
        'festivals': [
            ('Surajkund International Crafts Mela', 'February', 'The world\'s largest international crafts fair set around the 10th-century sun pool in Faridabad.', 'Brings together master craftspersons, folk dancers, and culinary artists from dozens of countries and every Indian state.'),
            ('Pinjore Heritage Festival', 'October', 'A celebration of Mughal garden heritage, classical performing arts, and traditional crafts in the historic Yadavindra Gardens.', 'Illuminates tiered fountains and historic pavilions with music recitals.')
        ],
        'cuisines': [
            ('Bajra Khichdi with Ghee & Chhachh', 'A hearty winter porridge of coarse pearl millet and moong dal, served with generous dollops of homemade white butter and cold buttermilk.', 'Pearl millet (bajra), moong dal, desi ghee, cumin, green chilies, chaas.', 'The rustic powerhouse meal that fuels Haryana\'s agriculturalists and champion wrestlers.'),
            ('Kadhi Pakora & Kachri ki Chutney', 'A tart, creamy yogurt-gram flour curry studded with crisp fritters, paired with wild desert cucumber chutney.', 'Sour curd, besan, fenugreek seeds, mustard seeds, kachri (wild melon), garlic, red chilies.', 'The quintessential comforting home meal of rural Haryana.')
        ]
    },
    'manipur': {
        'name': 'Manipur',
        'region': 'Northeast India',
        'description': 'The jewel of India, famed for classical Raas Leela grace, Loktak floating lake, indigenous polo (Sagol Kangjei), and martial arts.',
        'dances': [
            ('Manipuri Classical Raas Leela', 'One of India\'s eight classical dances, celebrated for its sublime, gentle movements, circular sways, and devotion.',
             'Dancers wear the stiff cylindrical barrel skirt (Potloi) adorned with glittering sequins, depicting Radha and Krishna\'s celestial love.'),
            ('Thang-Ta Martial Dance', 'An ancient Meitei martial art using swords (Thang) and spears (Ta), combining lethal combat techniques with rhythmic spiritual movement.',
             'Cultivated historically to protect the kingdom, Thang-Ta emphasizes breath control, precision, and inner equilibrium.')
        ],
        'music': [
            ('Pena Instrument', 'A traditional single-stringed bowed lute crafted from a dried coconut shell and bamboo neck, played with a curved bow.',
             'Regarded as sacred, the Pena is played to awaken deities during the Lai Haraoba festival and narrate epic ballads.'),
            ('Pung Cholom Drum Dance', 'An astonishing acrobatic dance where performers play the cylindrical Pung drum while executing high leaps, spins, and floor drops.',
             'Demonstrates breathtaking rhythmic virtuosity and athletic agility in perfect synchronization.')
        ],
        'crafts': [
            ('Longpi Black Pottery', 'Unique black earthenware crafted in Longpi village using a mixture of serpentinite stone and weathered rock, without a potter\'s wheel.',
             'Hand-shaped and polished with local leaves, Longpi pottery is completely natural, non-toxic, and heat-retentive.'),
            ('Shaphee Lanphee Shawl', 'A ceremonial shawl hand-embroidered with symbolic motifs like the sun, moon, stars, horses, and buffaloes.',
             'Historically bestowed by the Meitei kings as a medal of honor to brave warriors and chieftains.')
        ],
        'stories': [
            ('The Epic of Khamba and Thoibi', 'The tragic romance of the brave orphan youth Khamba and the princess Thoibi of the ancient kingdom of Moirang.',
             'Considered the national epic of Manipur, dramatizing themes of unwavering love, royal jealousy, and heroic deeds.')
        ],
        'festivals': [
            ('Yaoshang', 'March', 'The five-day festival of colors celebrated with Thabal Chongba (moonlit circle dance), youth sports competitions, and prayer.', 'Transforms the entire state into a joyful arena of youthful camaraderie and athletic contests.'),
            ('Sangai Festival', 'November', 'Manipur\'s premier tourism festival named after the rare brow-antlered dancing deer found exclusively in Keibul Lamjao National Park.', 'Showcases indigenous polo matches, boat races, handlooms, and cultural performances.')
        ],
        'cuisines': [
            ('Kangshoi', 'A healthy, oil-free vegetable stew simmered with seasonal green vegetables, ginger, onions, and sun-dried or fermented fish.', 'Seasonal greens, fermented fish (Ngari), ginger, green chilies, cilantro.', 'The nourishing comfort soup eaten daily in every Manipuri household.'),
            ('Singju Salad & Eromba', 'A fiery, fresh salad of finely shredded vegetables tossed with roasted chickpea flour, perilla seeds, and fermented fish paste.', 'Cabbage, lotus stems, perilla seeds (Thoiding), red chilies, fermented fish, herbs.', 'Bursting with complex textures and intense aromatic flavors.')
        ]
    },
    'sikkim': {
        'name': 'Sikkim',
        'region': 'Northeast India',
        'description': 'The Himalayan paradise nestled under Mount Kanchenjunga, India\'s first 100% organic state, famed for orchid blooms and Buddhist monasteries.',
        'dances': [
            ('Singhi Chham (Snow Lion Dance)', 'A sacred masked dance where dancers wear lion costumes symbolizing the mythical Snow Lion, guardian deity of Mount Kanchenjunga.',
             'Performed during the Pang Lhabsol festival to invoke prosperity, peace, and protection for the mountain kingdom.'),
            ('Maruni Folk Dance', 'A joyful Nepali community folk dance performed during Tihar (Diwali) and harvest festivals with colourful costumes and brass ornaments.',
             'Dancers move to the lively beats of the Madal drum, accompanied by a comic character known as Dhatu Waray.')
        ],
        'music': [
            ('Damphu Drum & Tungna', 'Traditional Nepali and Tibetan instruments including the single-headed circular drum and plucked string lute.',
             'Accompanies folk love songs (Tamang Selo) and mountain ballads celebrating snow-covered passes and rhododendron forests.'),
            ('Gyaling (Tibetan Oboe)', 'A majestic brass and silver double-reed wind instrument played by monks from monastery rooftops during prayer assemblies.',
             'Its penetrating, haunting drone summons deities and monks to spiritual meditation and sacred rituals.')
        ],
        'crafts': [
            ('Thangka Buddhist Paintings', 'Detailed scroll paintings executed on silk or cotton canvas depicting Buddhist deities, mandalas, and the wheel of life.',
             'Painted using mineral pigments and 24-karat gold by trained master artists in monastic centers like Rumtek.'),
            ('Choktse Wooden Carved Tables', 'Foldable wooden tables hand-carved with intricate auspicious Buddhist symbols (Ashtamangala) and dragons.',
             'Finished with rich lacquer, these tables are centerpiece heirlooms in traditional Sikkimese homes.')
        ],
        'stories': [
            ('The Guardian of Kanchenjunga', 'The Lepcha indigenous lore that reveres Mount Kanchenjunga (Kingtsum Dongzongbu) as the mother of creation and eternal guardian.',
             'Believed that the first human ancestors were created from pure virgin snow scooped from the holy mountain summit.')
        ],
        'festivals': [
            ('Pang Lhabsol', 'August-September', 'A unique festival commemorating the historic blood brotherhood signed between Lepcha and Bhutia chieftains witnessed by Mount Kanchenjunga.', 'Features sacred warrior dances and blessings for the ecological balance of the Himalayas.'),
            ('Losar (Tibetan New Year)', 'February', 'The joyous Tibetan New Year celebrated with monastery cham dances, preparation of Gutuk dumplings, and family feasts.', 'Welcomes new beginnings, cleansing evil spirits from the previous year.')
        ],
        'cuisines': [
            ('Steamed Momos with Gundruk Soup', 'Delicate steamed dumplings stuffed with organic minced vegetables or meat, served with fermented leafy green soup.', 'Flour, cabbage, onions, garlic, ginger, fermented mustard greens (gundruk), tomato sesame chili dip.', 'The universally beloved mountain staple perfected in the street kitchens of Gangtok.'),
            ('Thukpa & Phagshapa', 'A warming noodle soup packed with seasonal greens and spices, accompanied by strips of pork or tofu cooked with radishes and dried chilies.', 'Handmade egg or wheat noodles, clear broth, bok choy, radishes, dried red chilies, ginger.', 'Wholesome organic comfort food designed to counter cold Himalayan winds.')
        ]
    }
}

count_created = 0

for state_slug, data in STATE_DATA.items():
    state, _ = State.objects.get_or_create(
        slug=state_slug,
        defaults={
            'name': data['name'],
            'region': data['region'],
            'description': data['description'],
            'cultural_summary': f"{data['name']} is renowned for its iconic heritage, artistic traditions, vibrant festivals, and unique gastronomy."
        }
    )
    # Ensure description is updated
    state.name = data['name']
    state.region = data['region']
    state.description = data['description']
    state.cultural_summary = f"{data['name']} is renowned for its iconic heritage, artistic traditions, vibrant festivals, and unique gastronomy."
    state.save()

    print(f"Processing state: {state.name}...")

    # Seed Dance entries
    for item in data['dances']:
        title, short_desc, detailed = item
        slug = slugify(f"{state.slug}-{title}")
        entry, created = CulturalEntry.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': dance,
                'state': state,
                'short_description': short_desc,
                'detailed_story': detailed,
                'cultural_significance': f"A cornerstone of {state.name}'s performing heritage.",
                'practice_description': f"Preserved and performed through generational transmission and cultural academies.",
                'status': 'published',
                'created_by': admin,
            }
        )
        if not created:
            entry.short_description = short_desc
            entry.detailed_story = detailed
            entry.save()
        # Media mapping check
        key = slugify(title)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            entry.image = MEDIA_MAP[key]
            entry.save()
        count_created += 1

    # Seed Music entries
    for item in data['music']:
        title, short_desc, detailed = item
        slug = slugify(f"{state.slug}-{title}")
        entry, created = CulturalEntry.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': music,
                'state': state,
                'short_description': short_desc,
                'detailed_story': detailed,
                'cultural_significance': f"An integral acoustic expression of {state.name}.",
                'practice_description': f"Crafted and played according to ancient melodic and rhythmic principles.",
                'status': 'published',
                'created_by': admin,
            }
        )
        if not created:
            entry.short_description = short_desc
            entry.detailed_story = detailed
            entry.save()
        key = slugify(title)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            entry.image = MEDIA_MAP[key]
            entry.save()
        count_created += 1

    # Seed Craft entries
    for item in data['crafts']:
        title, short_desc, detailed = item
        slug = slugify(f"{state.slug}-{title}")
        entry, created = CulturalEntry.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': craft,
                'state': state,
                'short_description': short_desc,
                'detailed_story': detailed,
                'cultural_significance': f"Celebrated artisanal pride of {state.name}.",
                'practice_description': f"Handmade by indigenous master artisans using indigenous natural materials.",
                'status': 'published',
                'created_by': admin,
            }
        )
        if not created:
            entry.short_description = short_desc
            entry.detailed_story = detailed
            entry.save()
        key = slugify(title)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            entry.image = MEDIA_MAP[key]
            entry.save()
        count_created += 1

    # Seed Story entries
    for item in data['stories']:
        title, short_desc, detailed = item
        slug = slugify(f"{state.slug}-{title}")
        entry, created = CulturalEntry.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': story,
                'state': state,
                'short_description': short_desc,
                'detailed_story': detailed,
                'cultural_significance': f"Foundational legend in {state.name}'s literary and folklore traditions.",
                'practice_description': f"Transmitted orally through generations and celebrated in local theatre.",
                'status': 'published',
                'created_by': admin,
            }
        )
        if not created:
            entry.short_description = short_desc
            entry.detailed_story = detailed
            entry.save()
        key = slugify(title)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            entry.image = MEDIA_MAP[key]
            entry.save()
        count_created += 1

    # Seed Festivals
    for item in data['festivals']:
        name, month, desc, sig = item
        slug = slugify(f"{state.slug}-{name}")
        fest, created = Festival.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'state': state,
                'month': month,
                'description': desc,
                'cultural_significance': sig
            }
        )
        if not created:
            fest.name = name
            fest.month = month
            fest.description = desc
            fest.cultural_significance = sig
            fest.save()
        key = slugify(name)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            fest.image = MEDIA_MAP[key]
            fest.save()

    # Seed Cuisines
    for item in data['cuisines']:
        name, desc, ingredients, context = item
        slug = slugify(f"{state.slug}-{name}")
        cuisine, created = Cuisine.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'state': state,
                'description': desc,
                'ingredients': ingredients,
                'cultural_context': context
            }
        )
        if not created:
            cuisine.name = name
            cuisine.description = desc
            cuisine.ingredients = ingredients
            cuisine.cultural_context = context
            cuisine.save()
        key = slugify(name)
        if key in MEDIA_MAP and os.path.exists(f"/app/media/{MEDIA_MAP[key]}"):
            cuisine.image = MEDIA_MAP[key]
            cuisine.save()

print(f"\nSuccessfully seeded full cultural content across all {len(STATE_DATA)} states!")
