import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import State, CulturalCategory, CulturalEntry, Festival, Cuisine, Tradition, FolkArt

dance_cat, _ = CulturalCategory.objects.get_or_create(slug='dance', defaults={'name': 'Dance', 'description': 'Classical and folk dance forms'})
music_cat, _ = CulturalCategory.objects.get_or_create(slug='music', defaults={'name': 'Music', 'description': 'Classical ragas and folk melodies'})
craft_cat, _ = CulturalCategory.objects.get_or_create(slug='craft', defaults={'name': 'Craft', 'description': 'Handloom textiles and indigenous crafts'})
story_cat, _ = CulturalCategory.objects.get_or_create(slug='story', defaults={'name': 'Story', 'description': 'Myths, legends, and community memories'})

remaining_regions_data = [
    {
        'name': 'Arunachal Pradesh',
        'slug': 'arunachal-pradesh',
        'region': 'Northeast India',
        'description': 'The Land of Dawn-Lit Mountains, Arunachal Pradesh is a biodiversity hotspot and a cradle of diverse indigenous tribes, Theravada and Mahayana Buddhist monasteries, and vibrant animist folklore.',
        'cultural_summary': 'Rich in tribal heritage, bamboo craftsmanship, masked dances like Bardochham, and vibrant harvest festivals.',
        'dance': {
            'title': 'Bardochham Mask Dance',
            'slug': 'bardochham-dance-arunachal',
            'short_description': 'A vibrant folk dance performed by the Sherdukpen community depicting the triumph of good over evil spirits.',
            'detailed_story': 'Bardochham is performed by the Sherdukpen tribe of West Kameng during festive community gatherings. Dancers wear dramatic painted wooden masks representing animals, birds, and mystical forces, moving rhythmically to the beat of drums (dha) and cymbals to ward off malevolent spirits.',
            'cultural_significance': 'Embodies the deep ecological respect and spiritual cosmology of the eastern Himalayan foothills.',
            'practice_description': 'Dancers wear intricately painted wooden masks and brocade robes, dancing in a circle to hypnotic percussion.'
        },
        'music': {
            'title': 'Ja-jin-ja Folk Ballads',
            'slug': 'jajinja-music-arunachal',
            'short_description': 'Traditional community chorus songs celebrating ancestral lineages, weddings, and harvest seasons.',
            'detailed_story': 'Ja-jin-ja is sung collectively by elders during community feasts. Accompanied by bamboo flutes and metal gongs, these ballads pass tribal memory and oral codes across generations without written scripture.',
            'cultural_significance': 'Serves as an auditory living archive of Arunachal’s tribal genealogies and oral law.',
            'practice_description': 'Sung in a call-and-response choral style by village leaders around community hearths.'
        },
        'craft': {
            'title': 'Monpa Wood Carving & Thangkas',
            'slug': 'monpa-wood-carving-arunachal',
            'short_description': 'Masterful Himalayan wood carving of bowls, mask effigies, and sacred Buddhist scroll paintings.',
            'detailed_story': 'Practiced around Tawang and West Kameng, Monpa master artisans carve ceremonial masks, wooden cups (dapa), and low tables (choktse) embellished with traditional Buddhist dragon and lotus motifs.',
            'cultural_significance': 'Preserves medieval Himalayan woodcraft and monastery art in living monastic guilds.',
            'practice_description': 'Artisans use native walnut, pine, and birch timbers, hand-chiseling motifs before applying natural mineral lacquers.'
        },
        'festival': {
            'name': 'Losar & Nyokum',
            'slug': 'losar-nyokum-arunachal',
            'month': 'February',
            'description': 'Losar marks the Tibetan and Monpa New Year with monastic dances, while Nyokum is the grand agricultural festival of the Nyishi tribe.',
            'cultural_significance': 'Unites communities in prayers for bumper harvests, peace, and protection against natural calamities.'
        },
        'cuisine': {
            'name': 'Thukpa & Zan with Bamboo Shoot',
            'slug': 'thukpa-zan-arunachal',
            'description': 'Hearty Himalayan noodle soup combined with Zan (millet porridge) flavored with wild fermented bamboo shoot and smoked meat.',
            'ingredients': 'Handmade wheat noodles, mountain herbs, fermented bamboo shoot (Ekung), roasted millet, wild ginger, broth.',
            'cultural_context': 'Nutritious mountain cuisine designed to sustain energy in high-altitude sub-zero climates.'
        }
    },
    {
        'name': 'Goa',
        'slug': 'goa',
        'region': 'West India',
        'description': 'Goa is a vibrant coastal tapestry of Konkani traditions, Portuguese colonial architecture, sun-kissed beaches, and a unique composite syncretic ethos known as Sussegad.',
        'cultural_summary': 'Celebrated for its Azulejos tilecraft, Mando melodies, Fugdi folk dances, and mouthwatering coastal Konkani gastronomy.',
        'dance': {
            'title': 'Fugdi & Dhalo Folk Dance',
            'slug': 'fugdi-dhalo-dance-goa',
            'short_description': 'An exuberant Konkani women’s folk dance performed during festivals like Ganesh Chaturthi and Shigmo.',
            'detailed_story': 'Fugdi is an energetic, rhythmic dance performed exclusively by women in circles, stepping in pairs with rapid handclaps and footwork, culminating in a fast tempo accompanied by the blowing sound ‘foo-foo’. Dhalo, by contrast, is slow and devotional, performed in courtyards on moonlit winter nights.',
            'cultural_significance': 'Celebrates sisterhood, community joy, and rural Konkani identity beyond social barriers.',
            'practice_description': 'Dancers wear traditional nine-yard Nauvari sarees and fresh mogra flowers, dancing without musical instruments relying on vocal rhythms.'
        },
        'music': {
            'title': 'Mando & Dulpod Ballads',
            'slug': 'mando-dulpod-goa',
            'short_description': 'A graceful lyrical Konkani musical genre combining Indian melodies with Western violin and guitar harmonies.',
            'detailed_story': 'Mando emerged in the 19th century as a high-society Konkani ballroom love song accompanied by the Gumott (earthen drum) and violin. It typically transitions into the fast-paced Dulpod, reflecting everyday Goan village life and humor.',
            'cultural_significance': 'Recognized as one of the finest examples of East-West musical syncretism in Asia.',
            'practice_description': 'Performed in evening dress with vocal soloists supported by violins, guitars, and the resonant earthen Gumott.'
        },
        'craft': {
            'title': 'Goan Azulejos Tile Art',
            'slug': 'goan-azulejos-tiles',
            'short_description': 'Hand-painted glazed ceramic blue tiles depicting historic scenes, folklore, and street name plaques.',
            'detailed_story': 'Introduced through Portuguese trade routes, Goan Azulejo artists adopted the cobalt-blue and yellow tin-glazed ceramic tradition, infusing it with indigenous tropical motifs like palm trees, taverns, and fishermen.',
            'cultural_significance': 'Defines the architectural visual character of Old Goa, Panaji, and heritage Latin quarters (Fontainhas).',
            'practice_description': 'Bisque ceramic tiles are hand-painted using cobalt oxide mineral glazes and fired at high temperatures.'
        },
        'festival': {
            'name': 'Shigmo & Feast of St. Francis Xavier',
            'slug': 'shigmo-st-francis-goa',
            'month': 'March & December',
            'description': 'Shigmo is Goa’s vibrant spring carnival celebrated with street floats and temple lamps, while the Feast of St. Francis Xavier draws millions to Old Goa.',
            'cultural_significance': 'Illustrates Goa’s unique multi-faith harmony and shared festive celebrations.'
        },
        'cuisine': {
            'name': 'Goan Fish Curry & Bebinca',
            'slug': 'goan-fish-curry-bebinca',
            'description': 'Tangy coconut and kokum-infused kingfish curry paired with steamed red rice, finished with multi-layered baked Bebinca dessert.',
            'ingredients': 'Fresh kingfish, freshly grated coconut, Kashmiri chilies, kokum, coriander seeds, coconut milk, jaggery, eggs, ghee.',
            'cultural_context': 'The quintessential Goan midday meal, balancing Portuguese baking techniques with ancient Saraswat coastal spices.'
        }
    },
    {
        'name': 'Meghalaya',
        'slug': 'meghalaya',
        'region': 'Northeast India',
        'description': 'The Abode of the Clouds, Meghalaya is famous for its mist-shrouded green plateaus, matrilineal Khasi, Garo, and Jaintia societies, and living root bridges.',
        'cultural_summary': 'Renowned for the 100 Drums Wangala festival, living root architecture, Duitara music, and cane-and-bamboo craftsmanship.',
        'dance': {
            'title': 'Shad Suk Mynsiem & Nongkrem Dance',
            'slug': 'shad-suk-mynsiem-meghalaya',
            'short_description': 'The Dance of Peaceful Hearts, an elegant Khasi thanksgiving festival dance held each spring.',
            'detailed_story': 'Shad Suk Mynsiem is celebrated by the Khasi people to offer gratitude for peaceful hearts and prosperous harvests. Unmarried women dressed in pure silk (Dhara) and pure gold crowns (Pansngiat) dance in a slow, graceful inner circle, while young men with feather quivers dance vigorously on the perimeter to protect them.',
            'cultural_significance': 'Reflects the matrilineal social code of the Khasi community, symbolizing the mother as the core of lineage protected by brothers.',
            'practice_description': 'Accompanied by the Tangmuri (wooden pipe), Nakra (big drum), and Ksing (cymbals) in an open community field.'
        },
        'music': {
            'title': 'Khasi Duitara & Folk Ballads',
            'slug': 'khasi-duitara-meghalaya',
            'short_description': 'Soulful folk melodies played on the two-stringed wooden Duitara and bamboo flutes.',
            'detailed_story': 'The Duitara is a carved wooden plucked lute played with a wooden plectrum. Master musicians strum timeless ballads recounting Khasi folklore, the origins of the living root bridges, and sacred groves (Law Kyntang).',
            'cultural_significance': 'An organic oral tradition preserving the indigenous tribal philosophy of living in balance with nature.',
            'practice_description': 'Handcrafted from jackfruit wood, strung with muga silk or animal gut, played alongside the bamboo whistle.'
        },
        'craft': {
            'title': 'Khasi Cane & Bamboo Weaving (Khoh & Knup)',
            'slug': 'khasi-cane-bamboo-craft',
            'short_description': 'Waterproof leaf umbrellas (Knup) and conical harvesting baskets (Khoh) engineered from indigenous bamboo.',
            'detailed_story': 'In the wettest place on earth, Meghalaya artisans weave the Knup—a rain shield worn over the head and back, made of woven bamboo stuffed with broad water-resistant palm leaves—enabling farmers to cultivate steep slopes during torrential monsoons.',
            'cultural_significance': 'Demonstrates sophisticated traditional ecological design adapted to extreme rainfall environments.',
            'practice_description': 'Native bamboo strips are seasoned in smoke, hand-plaited, and reinforced with cane lashings.'
        },
        'festival': {
            'name': 'Wangala (100 Drums Festival)',
            'slug': 'wangala-festival-meghalaya',
            'month': 'November',
            'description': 'The post-harvest thanksgiving festival of the Garo tribe, featuring 100 drummers playing simultaneously in unison.',
            'cultural_significance': 'Offers thanksgiving to Misi Saljong, the Sun-god of fertility, uniting hundreds of Garo villages in rhythm.'
        },
        'cuisine': {
            'name': 'Jadoh & Dohneiiong with Tungrymbai',
            'slug': 'jadoh-dohneiiong-meghalaya',
            'description': 'Fragrant Khasi red rice cooked with delicate meat broth, paired with pork cooked in roasted black sesame paste.',
            'ingredients': 'Short-grain red rice, ginger, onions, wild black sesame paste (Neiiong), fermented soy beans (Tungrymbai), bay leaves.',
            'cultural_context': 'The cornerstone of Khasi festive meals, rich in savory, nutty flavors developed from indigenous fermentation.'
        }
    },
    {
        'name': 'Mizoram',
        'slug': 'mizoram',
        'region': 'Northeast India',
        'description': 'The Land of the Hill People, Mizoram is characterized by rolling pine hills, close-knit egalitarian villages, and the timeless code of Tlawmngaihna (selfless community service).',
        'cultural_summary': 'World-famous for the intricate Cheraw bamboo dance, vibrant handwoven Puan textiles, and rhythmic harvest festivals.',
        'dance': {
            'title': 'Cheraw (Bamboo Dance)',
            'slug': 'cheraw-bamboo-dance-mizoram',
            'short_description': 'One of India’s most visually breathtaking rhythmic dances where dancers step in and out of clashing bamboo staves.',
            'detailed_story': 'Cheraw is Mizoram’s most famous traditional dance. Four to eight people sit facing each other on the ground, clapping long bamboo poles together in rhythmic syncopation, while female dancers step intricately in and out of the closing staves with flawless timing.',
            'cultural_significance': 'Originally performed to ensure safe passage for souls of young mothers, it is now the crown jewel of Mizo national celebrations.',
            'practice_description': 'Requires extraordinary coordination, precision, and agility, accompanied by traditional gongs (Darbu).'
        },
        'music': {
            'title': 'Darbu Gongs & Lengzem Chants',
            'slug': 'darbu-gongs-mizoram',
            'short_description': 'Ceremonial brass gong trios played in interlocking polyrhythms during village festivals.',
            'detailed_story': 'The Darbu is a set of three small brass gongs, each producing a different pitch. Played together by three musicians, they produce mesmerizing syncopated beats that accompany community singing and victory dances.',
            'cultural_significance': 'Serves as the rhythmic heartbeat of traditional Mizo celebrations and civic assemblies.',
            'practice_description': 'Played with padded wooden mallets, passed down orally through youth dormitories (Zawlbuk).'
        },
        'craft': {
            'title': 'Puan Handloom Weaving',
            'slug': 'puan-handloom-weaving-mizoram',
            'short_description': 'Intricately patterned handwoven wrap-around skirts holding deep cultural and social significance.',
            'detailed_story': 'Every Mizo woman historically mastered the loin loom. Puan variants like Puanchei, Ngotekherh, and Kawrchei feature bold geometric stripes of black, white, and red, worn on weddings and national celebrations.',
            'cultural_significance': 'Recognized with a Geographical Indication (GI) tag, symbolizing Mizo women’s artisanal pride and ethnic identity.',
            'practice_description': 'Woven on backstrap and loin looms using pure cotton yarn dyed with natural vegetable colors.'
        },
        'festival': {
            'name': 'Chapchar Kut',
            'slug': 'chapchar-kut-mizoram',
            'month': 'March',
            'description': 'The grand spring harvest festival celebrated after the clearing of jhum forest slopes, marked by community singing and mass Cheraw dancing.',
            'cultural_significance': 'The ultimate expression of Mizo joy, reconciliation, and community egalitarian bonding.'
        },
        'cuisine': {
            'name': 'Bai & Sawhchiar',
            'slug': 'bai-sawhchiar-mizoram',
            'description': 'Subtle vegetable and pork stew cooked without oil, seasoned with fermented pork fat, wild local herbs, and local soda (Ching).',
            'ingredients': 'Mustard leaves, tender bamboo shoots, local beans, Ching (filtered wood ash water), pork fat, red rice.',
            'cultural_context': 'Organic, wholesome, and oil-free cuisine highlighting the pure natural flavors of high-altitude forest produce.'
        }
    },
    {
        'name': 'Nagaland',
        'slug': 'nagaland',
        'region': 'Northeast India',
        'description': 'The Land of Festivals, Nagaland is home to 16 recognized major tribes, each with its own language, distinctive warrior tradition, handwoven shawls, and rich oral epics.',
        'cultural_summary': 'Globally renowned for the Hornbill Festival, ceremonial spear dances, indigenous wood sculpture, and distinctive handloom shawls.',
        'dance': {
            'title': 'War Dances of the Nagas (Modse & Warrior Drills)',
            'slug': 'naga-war-dances',
            'short_description': 'Dynamic tribal dances showcasing martial agility, spear twirling, and thunderous victory chants.',
            'detailed_story': 'Performed by male dancers adorned in ceremonial hornbill feathers, boar tusk neckpieces, and bear-fur armlets. Dancers leap and parry with carved wooden shields and metal spears to the hypnotic beat of log drums, reenacting the defense of their ancestral hill settlements.',
            'cultural_significance': 'Instills bravery, discipline, and communal solidarity among youth, honoring ancestral guardians.',
            'practice_description': 'Accompanied by the beating of enormous carved village log drums (Khashi) and vocal war cries.'
        },
        'music': {
            'title': 'Tati String Melodies & Folk Chants',
            'slug': 'tati-music-nagaland',
            'short_description': 'Haunting folk tunes played on the single-stringed Tati instrument made of dried gourd and brass.',
            'detailed_story': 'The Tati is a single-stringed traditional instrument popular among the Angami and Chakhesang tribes. Accompanied by rhythmic whistling and choral harmonies, storytellers sing of ancestral migrations, romantic legends, and hunting feats.',
            'cultural_significance': 'Preserves the living oral poetry and indigenous languages of the Naga hill communities.',
            'practice_description': 'A plucked lute crafted from a hollow dried gourd attached to a bamboo cane, strummed with the index finger.'
        },
        'craft': {
            'title': 'Naga Tribal Shawls (Tsungkotepsu & Loramhoushu)',
            'slug': 'naga-tribal-shawls',
            'short_description': 'Striking geometric handwoven shawls denoting tribal identity, bravery, and social standing.',
            'detailed_story': 'Each Naga tribe weaves its own distinct shawl with specific symbolic motifs: the Ao Tsungkotepsu features hand-painted figures of tigers, mithun, and cock; the Angami Loramhoushu features bold black and red blocks. Traditionally, only accomplished leaders could wear certain patterns.',
            'cultural_significance': 'A GI-tagged textile tradition representing personal honor, tribal heritage, and artisanal mastery.',
            'practice_description': 'Handwoven on backstrap looms using indigenous handspun cotton and dyed with wild forest roots and barks.'
        },
        'festival': {
            'name': 'Hornbill Festival & Moatsu',
            'slug': 'hornbill-festival-nagaland',
            'month': 'December',
            'description': 'The Festival of Festivals held at Kisama Heritage Village, showcasing the dances, crafts, music, and food of all 16 Naga tribes.',
            'cultural_significance': 'Serves as an extraordinary platform for inter-tribal cultural harmony and global heritage tourism.'
        },
        'cuisine': {
            'name': 'Smoked Pork with Axone & Raja Mircha',
            'slug': 'smoked-pork-axone-nagaland',
            'description': 'Tender wood-smoked pork slow-cooked with fermented soya bean cakes (Axone) and fiery Naga King Chili (Ghost Pepper).',
            'ingredients': 'Hearth-smoked pork, Axone (fermented soybean paste), Raja Mircha (Bhut Jolokia), local ginger, bamboo shoots.',
            'cultural_context': 'The definitive celebratory dish of Nagaland, celebrated for its complex earthy aroma and intense natural heat.'
        }
    },
    {
        'name': 'Tripura',
        'slug': 'tripura',
        'region': 'Northeast India',
        'description': 'A historic kingdom nestled in riverine hills, Tripura blends indigenous Tipra tribal traditions with royal Manikya architecture and Bengali cultural exchanges.',
        'cultural_summary': 'Famous for the acrobatic Hojagiri pitcher dance, Kharchi Puja rituals, delicate bamboo screen carving, and Risa handlooms.',
        'dance': {
            'title': 'Hojagiri Dance of the Reang',
            'slug': 'hojagiri-dance-tripura',
            'short_description': 'A breathtaking acrobatic balancing dance performed by Reang tribal women balancing bottles and earthen lamps.',
            'detailed_story': 'Hojagiri is performed during the Mailuma (Goddess of Wealth) festival. Young Reang women balance an earthen pitcher or lit lamps on their head while balancing their feet on an earthen pitcher, executing graceful wave-like hip movements without disturbing the balanced objects.',
            'cultural_significance': 'Demonstrates unparalleled equilibrium, agility, and devotion to agricultural abundance.',
            'practice_description': 'Requires years of rigorous balance training from childhood; accompanied by the Kham drum and Sumui flute.'
        },
        'music': {
            'title': 'Chumpreng & Sarinda Melodies',
            'slug': 'chumpreng-music-tripura',
            'short_description': 'Classical and folk melodies played on the bow-strung Sarinda and wooden Chumpreng.',
            'detailed_story': 'Tripura’s folk music blends sweet tribal lullabies with devotional songs honoring Tripurasundari. The Chumpreng, an indigenous lute, and the Kham drum accompany poetic verses celebrating nature and river journeys.',
            'cultural_significance': 'Reflects the gentle lyricism of Tripura’s forested river valleys and courtly patronages.',
            'practice_description': 'Performed by village bards using string instruments made of wild toon wood and animal skins.'
        },
        'craft': {
            'title': 'Tripuri Bamboo Matting & Risa Textiles',
            'slug': 'tripuri-bamboo-risa-textiles',
            'short_description': 'Delicate woven bamboo screens, furniture, and the sacred ceremonial Risa handwoven breast-cloth.',
            'detailed_story': 'Tripura produces some of India’s finest bamboo craft, from split-bamboo screens so fine they resemble silk curtains, to the Risa—a ceremonial handwoven textile worn during religious rites with symbolic geometric embroidery.',
            'cultural_significance': 'Central to tribal rite-of-passage ceremonies (Risa Sormani) and recognized nationally for sustainable craftsmanship.',
            'practice_description': 'Woven on backstrap looms and carved with fine blades using indigenous Muli bamboo.'
        },
        'festival': {
            'name': 'Kharchi Puja (Festival of 14 Gods)',
            'slug': 'kharchi-puja-tripura',
            'month': 'July',
            'description': 'A week-long royal temple festival in Old Agartala honoring the Fourteen Deities, purifying the Mother Earth after her fertility period.',
            'cultural_significance': 'Unites both tribal and non-tribal communities in shared ancient sacrificial and temple rituals.'
        },
        'cuisine': {
            'name': 'Mui Borok & Chakhwi with Berma',
            'slug': 'mui-borok-chakhwi-tripura',
            'description': 'Traditional Tipra cuisine cooked without oil using Berma (fermented fish paste), green vegetables, and alkaline bamboo ash.',
            'ingredients': 'Berma (sun-dried fermented fish), bamboo shoots, green chilies, wild beans, local herbs, rice flour.',
            'cultural_context': 'Nutritious, gut-friendly indigenous food that sustains community health through traditional fermentation.'
        }
    },
    {
        'name': 'Jammu & Kashmir',
        'slug': 'jammu-kashmir',
        'region': 'North India',
        'description': 'The Crown of India, Jammu & Kashmir combines the temple traditions of Jammu, the mystical Sufi gardens and Dal Lake of the Kashmir Valley, and timeless artisanal heritage.',
        'cultural_summary': 'Famous for Pashmina weaving, Papier-mâché, Santoor music, Rouf dance, and the 36-course royal Wazwan.',
        'dance': {
            'title': 'Rouf Dance & Kud',
            'slug': 'rouf-dance-kashmir',
            'short_description': 'A lyrical folk dance performed by Kashmiri women in rows, interlocking arms to celebrate spring and Eid.',
            'detailed_story': 'During the festival of Eid and the arrival of spring (Navreh), Kashmiri women face each other in two parallel rows, linking their arms around each other’s waists. They glide forward and backward in synchronized rhythmic steps, singing melodious couplets in pure Kashmiri.',
            'cultural_significance': 'Symbolizes feminine grace, communal joy, and the reawakening of nature across the valley after harsh winters.',
            'practice_description': 'Dancers wear colorful embroidered Pherans, silver Kasaba headdresses, and large silver earrings.'
        },
        'music': {
            'title': 'Sufiana Kalam & Santoor Melodies',
            'slug': 'sufiana-kalam-santoor-kashmir',
            'short_description': 'Classical Sufi choral music played on the 100-stringed Santoor, Sehtar, and Wasool drum.',
            'detailed_story': 'Sufiana Kalam is the classical music of Kashmir, set to 54 classical Maqams (modal scales). Originating in the medieval period, it sets the mystic verses of Lal Ded, Sheikh Noor-ud-din (Nund Rishi), and Habba Khatoon to celestial melodies played on the 100-stringed hammered Santoor.',
            'cultural_significance': 'The ultimate expression of Kashmiriyat—the syncretic cultural soul bridging Hindu Shaivism and Sufism.',
            'practice_description': 'Musicians sit cross-legged, striking the metal strings of the trapezoidal Santoor with curved walnut-wood mallets (Mezrab).'
        },
        'craft': {
            'title': 'Kashmiri Pashmina & Paper Mâché',
            'slug': 'kashmiri-pashmina-paper-mache',
            'short_description': 'Cashmere goat wool handwoven into gossamer shawls with Sozni embroidery, alongside lacquered paper-mâché boxes.',
            'detailed_story': 'Introduced by Mir Sayyid Ali Hamadani and patronized by Sultan Zain-ul-Abidin, Kashmiri artisans spin Changthangi goat down-fleece into Pashmina shawls so fine they pass through a ring. Meanwhile, sakhta paper pulp is molded into exquisite gold-leaf painted boxes (Papier-mâché).',
            'cultural_significance': 'World-renowned GI-tagged crafts representing centuries of Persian-Kashmiri guild craftsmanship.',
            'practice_description': 'Spun on wooden Charkhas, woven on handlooms, and embroidered with single-needle Sozni threadwork.'
        },
        'festival': {
            'name': 'Herath (Shivratri) & Tulip Festival',
            'slug': 'herath-tulip-kashmir',
            'month': 'February & April',
            'description': 'Herath is the Kashmiri Pandit celebration of Shiva and Parvati with earthen pitcher rituals (Vatuk), while the Tulip Festival marks bloom along Dal Lake.',
            'cultural_significance': 'Celebrates the distinct rituals and seasonal beauty of the valley with shared confectionery and walnuts.'
        },
        'cuisine': {
            'name': 'Kashmiri Wazwan & Kahwa',
            'slug': 'kashmiri-wazwan-kahwa',
            'description': 'A royal 36-course banquet featuring Rogan Josh, Rista, and Gustaba simmered in yogurt and saffron, finished with cardamom Kahwa green tea.',
            'ingredients': 'Mutton, Kashmiri cockscomb herb (Mawal), dried fennel powder, ginger powder, saffron, green cardamom, cinnamon, almonds.',
            'cultural_context': 'Prepared by master chefs (Vastas) for weddings and state banquets, served in giant shared copper platters (Trami).'
        }
    },
    {
        'name': 'Ladakh',
        'slug': 'ladakh',
        'region': 'North India',
        'description': 'The Land of High Passes, Ladakh is a high-altitude cold desert nestled between the Himalayas and Karakoram, renowned for ancient Tibetan Buddhist monasteries, stupas, and stark sublime landscapes.',
        'cultural_summary': 'Famous for monastic Cham mask dances, Thangka scroll paintings, butter tea, and the grand Hemis monastic festival.',
        'dance': {
            'title': 'Cham Sacred Monastic Mask Dance',
            'slug': 'cham-mask-dance-ladakh',
            'short_description': 'Ritualistic sacred monastic dance performed by Lamas dressed in wrathful deity masks and silk brocades.',
            'detailed_story': 'Performed in the central courtyard of major monasteries like Hemis, Thiksey, and Lamayuru. Lamas wear hand-carved wooden or papier-mâché masks representing protective dharmapalas, moving in deliberate meditative circles to the sound of long horns (Dungchen) and cymbals to purify evil spirits and bring spiritual peace.',
            'cultural_significance': 'A profound living ritual meditation based on Tantric Buddhist texts aimed at subduing negative inner passions.',
            'practice_description': 'Accompanied by deep monastic chanting, cymbals (Silnyen), and thunderous bass notes of temple trumpets.'
        },
        'music': {
            'title': 'Ladakhi Lha-rnga & Dungchen Horns',
            'slug': 'ladakhi-dungchen-music',
            'short_description': 'Grand resonant acoustic calls echoed across mountain valleys from monastery rooftops.',
            'detailed_story': 'The Dungchen is a telescoping bronze horn up to three meters long. Its deep, foghorn-like notes reverberate across mountain passes to announce morning meditation, ceremonies, and seasonal festivals.',
            'cultural_significance': 'Auditory symbol of Himalayan Tibetan Buddhism, connecting physical landscape with spiritual transcendence.',
            'practice_description': 'Played in pairs by trained monk hornists from high monastery terraces overlooking the Indus River.'
        },
        'craft': {
            'title': 'Ladakhi Thangka Painting & Pattu Weaving',
            'slug': 'ladakhi-thangka-pattu',
            'short_description': 'Sacred Buddhist scroll paintings created with natural mineral pigments, along with thick handwoven yak-wool textiles.',
            'detailed_story': 'Thangkas depict Buddhas, mandalas, and bodhisattvas with geometric precision according to the sacred Iconometry canon. The colors are derived from crushed lapis lazuli, malachite, cinnabar, and gold leaf on treated cotton canvas.',
            'cultural_significance': 'Serves as visual aids for meditation, religious instruction, and ritual display in monastery shrines.',
            'practice_description': 'Prepared through strict geometric grids (Thik-tse) using natural yak-skin glue and pure mineral ground pigments.'
        },
        'festival': {
            'name': 'Hemis Festival & Losar',
            'slug': 'hemis-festival-ladakh',
            'month': 'June & December',
            'description': 'Hemis commemorates the birth anniversary of Guru Padmasambhava with vibrant mask dances, while Losar marks the Ladakhi New Year.',
            'cultural_significance': 'Draws thousands of pilgrims and global travelers into the sacred courtyards of the historic Drukpa monastery.'
        },
        'cuisine': {
            'name': 'Skyu & Gur Gur Butter Tea',
            'slug': 'skyu-butter-tea-ladakh',
            'description': 'Traditional thumb-pressed wheat pasta stew simmered with root vegetables, served alongside salty, warm yak-butter tea.',
            'ingredients': 'Whole wheat dough, root turnips, wild mountain peas, mutton or dried vegetables, brick tea, yak butter, rock salt.',
            'cultural_context': 'Vital cold-climate nourishment providing sustained thermoregulation and hydration in arid 12,000-foot altitudes.'
        }
    },
    {
        'name': 'Delhi',
        'slug': 'delhi',
        'region': 'North India',
        'description': 'The historic capital of India, Delhi is an ancient palimpsest of eight historical cities, spanning Indraprastha, the Delhi Sultanate, the Mughal Empire, and modern democratic India.',
        'cultural_summary': 'Famous for Delhi Gharana classical music, Kathak heritage, Qawwalis of Nizamuddin, Zardozi embroidery, and legendary street food.',
        'dance': {
            'title': 'Kathak (Delhi Darbar Tradition)',
            'slug': 'kathak-delhi-tradition',
            'short_description': 'The refined classical dance form nurtured in the imperial courts of Delhi, celebrated for lightning chakkars (pirouettes) and subtle Abhinaya.',
            'detailed_story': 'While originating among temple storytellers (Kathakars), Kathak in Delhi flourished under imperial Mughal patronage. Dancers combined subtle devotional micro-expressions with dazzling rhythmic footwork (Tatkar) and rapid spins (Chakkars) accompanied by the Pakhawaj and Tabla.',
            'cultural_significance': 'Represents one of India’s eight classical dance forms, embodying seamless Hindu-Muslim artistic dialogue.',
            'practice_description': 'Dancers wear ankle bells (Ghungroos) weighing several pounds, matching complex mathematical rhythmic cycles (Teental).'
        },
        'music': {
            'title': 'Dilli Gharana Khayal & Sufi Qawwali',
            'slug': 'dilli-gharana-qawwali',
            'short_description': 'Pioneered by Hazrat Amir Khusrau, the foundational Dilli Gharana of Tabla and the mystic Qawwali at Dargah Nizamuddin Auliya.',
            'detailed_story': 'Hazrat Amir Khusrau invented the Qawwali genre and revolutionized Indian classical music in Delhi in the 13th century. Every Thursday evening, Qawwals gather at the courtyard of Nizamuddin Auliya, singing ecstatic Persian and Hindavi verses to clapping rhythms and harmoniums.',
            'cultural_significance': 'The historical ground zero for Hindustani classical instrumental music and mystic devotional poetry.',
            'practice_description': 'Characterized by fast vocal improvisations (Taan), clapping syncopation, and harmonium-led choral crescendos.'
        },
        'craft': {
            'title': 'Zardozi Embroidery & Ivory Parchin Kari',
            'slug': 'delhi-zardozi-embroidery',
            'short_description': 'Opulent metallic thread embroidery using gold and silver wire (Zar), beads, and precious stones on velvet and silk.',
            'detailed_story': 'Zardozi reached its artistic zenith in Old Delhi (Shahjahanabad). Master artisans (Karigars) in the narrow lanes of Chandni Chowk still stretch royal silks across wooden frames (Adda), stitching real metallic wires and pearls to create heirloom wedding garments.',
            'cultural_significance': 'A GI-tagged luxury royal craft that adorned court costumes, royal canopies, and state draperies.',
            'practice_description': 'Stitched using a hooked needle (Ari) on tightly stretched fabric over wooden timber looms.'
        },
        'festival': {
            'name': 'Qutub Festival & Phool Walon Ki Sair',
            'slug': 'qutub-phool-walon-ki-sair',
            'month': 'October & November',
            'description': 'Phool Walon Ki Sair is a historic syncretic festival where floral fans are offered both at the shrine of Qutbuddin Bakhtiar Kaki and the Yogmaya Temple.',
            'cultural_significance': 'A historic 19th-century symbol of Delhi’s secular composite culture (Ganga-Jamuni Tehzeeb).'
        },
        'cuisine': {
            'name': 'Dilli Mughlai Nihari & Chaat',
            'slug': 'dilli-nihari-chaat',
            'description': 'Slow-cooked overnight beef/shank Nihari stew simmered with 50 spices, alongside iconic Chandni Chowk street Chaat and stuffed Parathas.',
            'ingredients': 'Meat shanks, bone marrow, brown onions, mace, nutmeg, star anise, rose water, yoghurt, tamarind, cumin, crispy papdi.',
            'cultural_context': 'The legendary gastronomic legacy of Shahjahanabad, combining royal imperial kitchens with bustling bazaar street flavors.'
        }
    },
    {
        'name': 'Chandigarh',
        'slug': 'chandigarh',
        'region': 'North India',
        'description': 'India’s City Beautiful, Chandigarh is a masterclass in modernist urban architecture designed by Le Corbusier, serving as the joint capital of Punjab and Haryana.',
        'cultural_summary': 'Known for the whimsical Rock Garden sculptures, Sukhna Lake sunsets, vibrant Bhangra culture, and open garden green spaces.',
        'dance': {
            'title': 'Modern Pan-Punjabi Bhangra & Giddha',
            'slug': 'chandigarh-bhangra-giddha',
            'short_description': 'Energetic, modern folk dance ensembles showcasing the highest caliber of acrobatic Punjabi harvest dancing.',
            'detailed_story': 'Chandigarh serves as the cultural stage for college and national Bhangra and Giddha championships. Teams perform complex synchronized acrobatic formations, clapping Saap instruments and dancing to the booming beat of the Dhol.',
            'cultural_significance': 'The modern youthful heartbeat of Punjabi performing arts celebrated globally.',
            'practice_description': 'Dancers wear vibrant satin Kurtas and lungis, executing high kicks and tower pyramids with infectious joy.'
        },
        'music': {
            'title': 'Punjabi Classical & Contemporary Sufi Soirees',
            'slug': 'chandigarh-sufi-music',
            'short_description': 'Soulful evenings of Punjabi classical poetry, Tumbi folk solos, and live concerts at Tagore Theatre.',
            'detailed_story': 'Chandigarh hosts celebrated annual music festivals at the Tagore Theatre, bringing together classical Hindustani maestros and contemporary Punjabi Sufi singers singing the verses of Baba Farid, Bulleh Shah, and Shiv Kumar Batalvi.',
            'cultural_significance': 'Fosters intellectual and artistic revival across the northwestern plains of India.',
            'practice_description': 'Accompanied by the single-stringed Tumbi, harmonium, acoustic guitars, and Tabla.'
        },
        'craft': {
            'title': 'Nek Chand Rock Garden Recycled Sculptures',
            'slug': 'nek-chand-rock-garden-craft',
            'short_description': 'Visionary outsider art sculptures created from discarded ceramic tiles, glass bangles, industrial slag, and river rocks.',
            'detailed_story': 'Created secretly over 18 years by road inspector Nek Chand, the Rock Garden is an internationally renowned 40-acre wonderland of fantasy courtyards and statues sculpted entirely from industrial waste, broken ceramic chinaware, and discarded materials.',
            'cultural_significance': 'A global triumph of sustainable artistic imagination and civic environmental recycling.',
            'practice_description': 'Armatures of steel rods and cement packed with broken glass, ceramic tea saucers, and terracotta pot-sherds.'
        },
        'festival': {
            'name': 'Chandigarh Rose Festival & Mango Mela',
            'slug': 'chandigarh-rose-festival',
            'month': 'February',
            'description': 'A massive three-day floral extravaganza held at the Zakir Hussain Rose Garden, showcasing hundreds of rare rose species, folk dances, and cultural contests.',
            'cultural_significance': 'Celebrates nature, civic pride, and seasonal blooms in India’s planned city.'
        },
        'cuisine': {
            'name': 'Chole Bhature & Malai Lassi',
            'slug': 'chandigarh-chole-bhature-lassi',
            'description': 'Spicy dark chickpeas stewed in roasted tea water and anardana, served with puffed golden Bhature and thick sweet curd lassi.',
            'ingredients': 'Kabuli chickpeas, pomegranate seeds (anardana), black tea bags, carom seeds, refined flour, curd, cardamom, malai.',
            'cultural_context': 'The quintessential North Indian indulgence, synonymous with lively family morning breakfasts across the city.'
        }
    },
    {
        'name': 'Puducherry',
        'slug': 'puducherry',
        'region': 'South India',
        'description': 'A charming coastal union territory known as the French Riviera of the East, blending Tamil heritage with French colonial boulevards, spiritual retreats, and serene coastal tranquility.',
        'cultural_summary': 'Famous for Garadi folk dance, Franco-Tamil Creole cuisine, Sri Aurobindo Ashram, and handmade terracotta pottery.',
        'dance': {
            'title': 'Garadi Folk Dance',
            'slug': 'garadi-dance-puducherry',
            'short_description': 'An ancient mythic dance celebrating the victory of Lord Rama’s Vanara army, performed with ten iron rings on each leg.',
            'detailed_story': 'According to legend, Garadi was performed by the monkey warriors (Vanaras) in jubilant celebration of Lord Rama’s victory over Ravana. Dancers wear monkey masks, hold short wooden sticks, and wear ten large hollow iron rings (Anjali) on each leg that rattle rhythmically as they march.',
            'cultural_significance': 'A distinctive living folk ritual preserving early Tamil epic dance traditions.',
            'practice_description': 'Dancers perform martial steps in a ring for hours without tiring, driven by the rhythmic clanging of the leg rings and drums.'
        },
        'music': {
            'title': 'Franco-Tamil Fusion & Carnatic Melodies',
            'slug': 'franco-tamil-music-puducherry',
            'short_description': 'Harmonious blending of classical Carnatic ragas, French accordion melodies, and devotional hymns.',
            'detailed_story': 'Puducherry’s cultural calendar features serene evening concerts in the French Quarter and seaside promenades, where traditional Carnatic veena and flute compositions merge seamlessly with Western acoustic instruments.',
            'cultural_significance': 'Reflects Puducherry’s unique peaceful synthesis of Mediterranean European and Tamil aesthetics.',
            'practice_description': 'Performed in heritage courtyards with veena, mridangam, violin, and classical acoustic guitar.'
        },
        'craft': {
            'title': 'Terracotta Sculptures & Handmade Paper',
            'slug': 'puducherry-terracotta-paper',
            'short_description': 'Colossal clay Ayyanar horses, pottery idols, and artisanal 100% cotton-rag handmade paper.',
            'detailed_story': 'The master potters of Villianur in Puducherry craft majestic terracotta horses and decorative lamps using fine local alluvial clay. Nearby, the Sri Aurobindo Ashram Handmade Paper Mill produces acid-free, eco-friendly rag paper exported worldwide.',
            'cultural_significance': 'Preserves ancient Dravidian village guardian pottery alongside sustainable artisanal papermaking.',
            'practice_description': 'Clay is kneaded, wheel-thrown, hand-molded into hollow sections, and wood-fired in traditional village kilns.'
        },
        'festival': {
            'name': 'Fête de Puducherry & Masi Magam',
            'slug': 'fete-de-puducherry-masi-magam',
            'month': 'August & February',
            'description': 'Fête de Puducherry celebrates national de jure transfer day with carnivals, while Masi Magam features hundreds of temple deities taking a ceremonial holy sea bath.',
            'cultural_significance': 'A vibrant convergence of sacred coastal temple rituals and French-Indian civic festivals.'
        },
        'cuisine': {
            'name': 'Franco-Tamil Creole Cuisine',
            'slug': 'franco-tamil-creole-cuisine',
            'description': 'Unique culinary blend featuring Bouillabaisse-inspired Meen Curry, Vindaloo with French wine vinegar, and baguette pairings.',
            'ingredients': 'Fresh ocean seafood, coconut milk, curry leaves, tamarind, Dijon-style mustard, mild spices, fresh baguettes.',
            'cultural_context': 'A distinct historic cuisine developed by French-Indian household chefs, balancing European subtlety with South Indian spice.'
        }
    },
    {
        'name': 'Andaman and Nicobar',
        'slug': 'andaman-nicobar',
        'region': 'South India',
        'description': 'An emerald archipelago in the Bay of Bengal, Andaman and Nicobar is an island wonderland of indigenous indigenous tribes, coral reefs, and the sacred national memorial Cellular Jail.',
        'cultural_summary': 'Known for Nicobarese circle dances, shell and cane crafts, rich maritime folklore, and pristine island ecology.',
        'dance': {
            'title': 'Nicobarese Folk Dance',
            'slug': 'nicobarese-dance',
            'short_description': 'A graceful circle dance performed by Nicobarese villagers on full moon nights around seaside bonfires.',
            'detailed_story': 'Performed during the Ossuary Feast, dancers link arms over each other’s shoulders, moving in rhythmic unison with gentle steps and swaying movements to vocal island songs, thanking the spirits of ancestors and the bountiful sea.',
            'cultural_significance': 'Represents the harmonious communal bonding and sacred ecological worldview of the islanders.',
            'practice_description': 'Dancers wear traditional skirts woven from coconut leaves, moving without percussion, accompanied solely by choral chants.'
        },
        'music': {
            'title': 'Island Sea Ballads & Shell Horns',
            'slug': 'island-sea-ballads-andaman',
            'short_description': 'Lyrical chants celebrating maritime navigation, canoe voyages, and deep sea fishing expeditions.',
            'detailed_story': 'Traditional island singers recount ancestral sea crossings across the Nicobar and Andaman archipelago, blowing into sacred conch and large sea snail shells to signal between islands and call community assemblies.',
            'cultural_significance': 'An ancient oral navigational archive preserving traditional knowledge of monsoon winds and currents.',
            'practice_description': 'Performed a cappella or with hollow wooden drums and shell percussion.'
        },
        'craft': {
            'title': 'Mother-of-Pearl Shell Craft & Cane Mats',
            'slug': 'andaman-shell-craft',
            'short_description': 'Carved mother-of-pearl ornaments, conch lamps, and intricately woven resilient Pandanus cane mats.',
            'detailed_story': 'Artisans polish and carve locally collected oyster, turbo, and king conch shells into glowing lamps, jewellery, and decorative table inlays. Nicobarese weavers produce durable water-resistant mats from split cane and pandanus palm leaves.',
            'cultural_significance': 'A sustainable coastal craft reflecting the richness of marine biodiversity and tribal resourcefulness.',
            'practice_description': 'Shells are hand-ground, polished with fine emery, and carved with traditional marine and floral motifs.'
        },
        'festival': {
            'name': 'Island Tourism Festival & Subhash Mela',
            'slug': 'island-tourism-festival-andaman',
            'month': 'January',
            'description': 'A grand 10-day cultural showcase at Port Blair celebrating mainland and indigenous island heritage, arts, and music.',
            'cultural_significance': 'Unites diverse communities across the archipelago into a joyful celebration of national unity.'
        },
        'cuisine': {
            'name': 'Andaman Coconut Seafood Curry',
            'slug': 'andaman-coconut-seafood-curry',
            'description': 'Succulent fresh reef fish and prawns simmered in freshly squeezed coconut milk with curry leaves and crushed island black pepper.',
            'ingredients': 'Fresh coastal prawns, red snapper, coconut milk, mustard seeds, curry leaves, ginger, black pepper, lime juice.',
            'cultural_context': 'Fresh tropical coastal cuisine celebrating the pristine marine bounty of the Bay of Bengal.'
        }
    },
    {
        'name': 'Dadra and Nagar Haveli and Daman and Diu',
        'slug': 'dadra-nagar-haveli-daman-diu',
        'region': 'West India',
        'description': 'A charming coastal and forested union territory in Western India, blending tribal Warli culture with 400 years of Portuguese sea-fortress history in Daman and Diu.',
        'cultural_summary': 'Famous for Tarpa wind instrument dances, Warli paintings, Diu fortress architecture, and coastal seafood traditions.',
        'dance': {
            'title': 'Tarpa Folk Dance',
            'slug': 'tarpa-dance-dadra-nagar-haveli',
            'short_description': 'An ancient tribal circular dance powered by the deep, continuous drone of the Tarpa wind instrument.',
            'detailed_story': 'During harvest festivals like Diwali and Nariyal Poornima, men and women join hands in a spiraling circle around the Tarpa player. The player blows continuously into the windpipe, and the spiral coils inward and outward without breaking rhythm, mirroring the lifecycle of the cosmos.',
            'cultural_significance': 'Central to Warli tribal community life, celebrating the mother earth (Palghat) and agricultural fertility.',
            'practice_description': 'The Tarpa is crafted from a dried bottle gourd, bamboo pipes, and palm leaf funnels, played using circular breathing.'
        },
        'music': {
            'title': 'Tarpa & Dholak Tribal Melodies',
            'slug': 'tarpa-tribal-music',
            'short_description': 'Hypnotic continuous-pitch wind music that guides the tempo of tribal village dancers for hours.',
            'detailed_story': 'The master Tarpa player holds prestigious status in the village. His improvisations signal changes in dance steps, moving from slow meditative pacing to rapid celebratory twirls under moonlit village banyan trees.',
            'cultural_significance': 'An unbroken indigenous wind instrument tradition dating back thousands of years.',
            'practice_description': 'Crafted completely from organic biodegradable forest materials with no metal components.'
        },
        'craft': {
            'title': 'Warli Bamboo & Canvas Painting',
            'slug': 'warli-painting-dadra-nagar',
            'short_description': 'Monochromatic geometric tribal art depicting the circle of life, mother goddess, and community harvest dances.',
            'detailed_story': 'Warli paintings use basic geometric shapes—circles, triangles, and lines—to represent the sun, moon, mountains, and human figures. Painted using white rice paste on earthen mud walls, the central motif is almost always the spiraling Tarpa dance.',
            'cultural_significance': 'An internationally revered prehistoric folk art tradition recognized with a Geographical Indication (GI) tag.',
            'practice_description': 'Drawn with chewed bamboo twigs using rice flour paste, water, and gum resin on cow-dung treated canvas.'
        },
        'festival': {
            'name': 'Tarpa Festival & Nariyal Poornima',
            'slug': 'tarpa-festival-daman-diu',
            'month': 'December & August',
            'description': 'Celebrates the beginning of the fishing season with coconuts offered to the Arabian Sea, alongside tribal dances and craft fairs.',
            'cultural_significance': 'Brings together tribal villagers and coastal fishing communities in shared thanksgiving.'
        },
        'cuisine': {
            'name': 'Ubadiyu & Damania Fish Curry',
            'slug': 'ubadiyu-damania-fish-curry',
            'description': 'Fragrant winter vegetables slow-cooked in earthen pots buried upside-down in smoking farm embers, paired with Portuguese-Konkani fish curry.',
            'ingredients': 'Wild yam, broad beans (papdi), potatoes, wild carom herbs, fresh pomfret, kokum, coconut paste, green chilies.',
            'cultural_context': 'Earthy, smoky village feast prepared collectively after the winter harvest in open farmlands.'
        }
    },
    {
        'name': 'Lakshadweep',
        'slug': 'lakshadweep',
        'region': 'South India',
        'description': 'A tropical paradise of 36 coral atolls and lagoons in the Arabian Sea, Lakshadweep is celebrated for its serene marine life, coconut groves, and unique Mappila-Malayalam island culture.',
        'cultural_summary': 'Famous for Kolkali stick dances, Parichakali sword dances, coir matting, and tuna delicacies like Mus Kavaab.',
        'dance': {
            'title': 'Kolkali & Parichakali Dance',
            'slug': 'kolkali-parichakali-lakshadweep',
            'short_description': 'A rapid, rhythmic stick dance performed in circles, evolving into the martial shield-and-sword Parichakali dance.',
            'detailed_story': 'In Kolkali, pairs of male dancers strike short polished wooden sticks together in synchronized, accelerating rhythms while singing devotional folk songs. Parichakali introduces painted shields and swords, tracing roots back to ancient Kerala martial training adapted for island defense.',
            'cultural_significance': 'Enhances community brotherhood, physical stamina, and preserves maritime folk poetry.',
            'practice_description': 'Performed in traditional white lungis and turbans, accelerating to breathtaking tempos accompanied by harmonium and duff.'
        },
        'music': {
            'title': 'Mappila Island Paatu & Duffmuttu',
            'slug': 'mappila-island-paatu-lakshadweep',
            'short_description': 'Devotional island ballads sung in Arabi-Malayalam dialect to the percussion of the round Duff tambourine.',
            'detailed_story': 'Sung during weddings, sea expeditions, and religious festivals, these songs recount the journeys of historic saint Sheikh Ubaidullah who brought Islam to the islands, and sailors braving stormy monsoon seas.',
            'cultural_significance': 'The primary oral poetic vehicle of Lakshadweep’s coastal Islamic heritage.',
            'practice_description': 'Singers hold the Duff frame drum in the left hand, striking the goat-skin surface with the fingers and palm of the right.'
        },
        'craft': {
            'title': 'Coir Rope Weaving & Coral Woodcraft',
            'slug': 'coir-rope-weaving-lakshadweep',
            'short_description': 'World-famous golden coir yarn spun from soaked coconut husks, alongside delicate shell and coral carving.',
            'detailed_story': 'Lakshadweep coir has been famous across the Indian Ocean since antiquity for its exceptional strength and resistance to saltwater. Women in every atoll soak coconut husks in lagoon shallows before beating them into golden fibers and twisting them into yarn.',
            'cultural_significance': 'Historically served as the primary trade currency of the islands and remains a vital women-led cooperative handicraft.',
            'practice_description': 'Spun by hand and with traditional spinning wheels (ratts) from brackish-water cured coconut husks.'
        },
        'festival': {
            'name': 'Eid-ul-Fitr & Milad-un-Nabi',
            'slug': 'eid-milad-lakshadweep',
            'month': 'Lunar Calendar',
            'description': 'Celebrated with widespread prayer gatherings at historical coral-stone mosques (Ujra Mosque), community feasts, and Kolkali performances.',
            'cultural_significance': 'Unites families across all coral atolls in feasting, reconciliation, and vibrant cultural performances.'
        },
        'cuisine': {
            'name': 'Mus Kavaab & Batla Appam',
            'slug': 'mus-kavaab-batla-appam-lakshadweep',
            'description': 'Spicy, tender boneless Skipjack tuna skewers marinated in coconut and ground island spices, paired with soft steamed rice appams.',
            'ingredients': 'Fresh Skipjack tuna (Mus), ground coconut, shallots, garlic, dried red chilies, turmeric, curry leaves, rice batter.',
            'cultural_context': 'The signature delicacy of the atolls, built around the sustainable pole-and-line tuna fishing tradition.'
        }
    }
]

print(f"Beginning seeding for {len(remaining_regions_data)} remaining states and union territories...")

for item in remaining_regions_data:
    st, created = State.objects.get_or_create(
        slug=item['slug'],
        defaults={
            'name': item['name'],
            'region': item['region'],
            'description': item['description'],
            'cultural_summary': item['cultural_summary'],
            'is_featured': True
        }
    )
    if not created:
        st.name = item['name']
        st.region = item['region']
        st.description = item['description']
        st.cultural_summary = item['cultural_summary']
        st.is_featured = True
        st.save()
    print(f"State ready: {st.name} ({st.region})")

    # 1. Dance entry
    d_data = item['dance']
    CulturalEntry.objects.update_or_create(
        slug=d_data['slug'],
        defaults={
            'title': d_data['title'],
            'category': dance_cat,
            'state': st,
            'short_description': d_data['short_description'],
            'detailed_story': d_data['detailed_story'],
            'cultural_significance': d_data['cultural_significance'],
            'practice_description': d_data['practice_description'],
            'status': 'published',
            'featured': True
        }
    )

    # 2. Music entry
    m_data = item['music']
    CulturalEntry.objects.update_or_create(
        slug=m_data['slug'],
        defaults={
            'title': m_data['title'],
            'category': music_cat,
            'state': st,
            'short_description': m_data['short_description'],
            'detailed_story': m_data['detailed_story'],
            'cultural_significance': m_data['cultural_significance'],
            'practice_description': m_data['practice_description'],
            'status': 'published',
            'featured': True
        }
    )

    # 3. Craft entry
    c_data = item['craft']
    CulturalEntry.objects.update_or_create(
        slug=c_data['slug'],
        defaults={
            'title': c_data['title'],
            'category': craft_cat,
            'state': st,
            'short_description': c_data['short_description'],
            'detailed_story': c_data['detailed_story'],
            'cultural_significance': c_data['cultural_significance'],
            'practice_description': c_data['practice_description'],
            'status': 'published',
            'featured': True
        }
    )

    # 4. Festival
    f_data = item['festival']
    Festival.objects.update_or_create(
        slug=f_data['slug'],
        defaults={
            'name': f_data['name'],
            'state': st,
            'month': f_data['month'],
            'description': f_data['description'],
            'cultural_significance': f_data['cultural_significance'],
            'featured': True
        }
    )

    # 5. Cuisine
    cu_data = item['cuisine']
    Cuisine.objects.update_or_create(
        slug=cu_data['slug'],
        defaults={
            'name': cu_data['name'],
            'state': st,
            'description': cu_data['description'],
            'ingredients': cu_data['ingredients'],
            'cultural_context': cu_data['cultural_context']
        }
    )

print("All remaining States and Union Territories have been successfully seeded!")
