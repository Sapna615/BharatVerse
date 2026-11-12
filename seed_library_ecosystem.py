import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import State, CulturalCategory, CulturalEntry, LiteraryWork

# 1. Ensure categories are present
categories_to_seed = [
    {
        'name': 'Literature',
        'slug': 'literature',
        'description': 'Classical epics, regional poetry, plays, prose, and celebrated literary works across India.',
        'icon': 'fas fa-book'
    },
    {
        'name': 'Sacred Texts & Philosophy',
        'slug': 'sacred-texts',
        'description': 'Sacred scriptures, philosophical treatises, ethical codes, and foundational spiritual heritage.',
        'icon': 'fas fa-om'
    },
    {
        'name': 'Manuscripts & Archives',
        'slug': 'manuscripts',
        'description': 'Ancient palm-leaf, birch-bark, copper plate, and illuminated paper codices documenting civilisational knowledge.',
        'icon': 'fas fa-scroll'
    },
    {
        'name': 'Oral Literature & Folklore',
        'slug': 'oral-tradition',
        'description': 'Living oral narratives, bardic ballads, folk epics, lullabies, and communal storytelling traditions.',
        'icon': 'fas fa-microphone-alt'
    },
    {
        'name': 'Traditional Knowledge & Science',
        'slug': 'traditional-knowledge',
        'description': 'Documented indigenous treatises on Ayurveda, metallurgy, astronomy, architecture (Vastu), and botany.',
        'icon': 'fas fa-seedling'
    },
    {
        'name': 'Visual Arts & Painting',
        'slug': 'visual-arts',
        'description': 'Miniature schools, murals, folk scroll paintings, rock art, and visual storytelling across regions.',
        'icon': 'fas fa-palette'
    },
    {
        'name': 'Architecture & Built Heritage',
        'slug': 'architecture',
        'description': 'Rock-cut temples, stepwells (Baoris), stupas, forts, wooden palaces, and vernacular living dwellings.',
        'icon': 'fas fa-monument'
    },
    {
        'name': 'Clothing, Textiles & Jewellery',
        'slug': 'clothing-textiles',
        'description': 'Handloom weaves, resist-dyeing, tribal metalwork, regional drapery, and festive heirloom ornaments.',
        'icon': 'fas fa-vest'
    }
]

created_categories = {}
for cat_data in categories_to_seed:
    cat, created = CulturalCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'icon': cat_data['icon']
        }
    )
    if not created:
        cat.name = cat_data['name']
        cat.description = cat_data['description']
        cat.icon = cat_data['icon']
        cat.save()
    created_categories[cat.slug] = cat
    print(f"Synced Category: {cat.name} ({cat.slug})")

# 2. Seed Rich Literary Works across India's diverse traditions
works_data = [
    {
        'title': 'Silappadikaram (The Tale of an Anklet)',
        'slug': 'silappadikaram-tamil-epic',
        'author_creator': 'Ilango Adigal (Chera Prince-Poet)',
        'work_type': 'book',
        'tradition': 'Classical Sangam / Tamil Literature',
        'language': 'Classical Tamil',
        'script': 'Tamil-Brahmi / Vatteluttu',
        'historical_period': 'c. 5th–6th Century CE',
        'classification_type': 'original',
        'state_name': 'Tamil Nadu',
        'category_slug': 'literature',
        'brief_intro': 'One of the Five Great Epics of Tamil literature, narrating the virtuous Kannagi’s moral trial, Kovalan’s tragic fate, and the burning of Madurai against royal injustice.',
        'synopsis': 'Silappadikaram is an unparalleled jewel of early Indian literature. It follows Kovalan, a merchant of Poompuhar, his noble wife Kannagi, and Madhavi, an accomplished court dancer. After losing his fortune, Kovalan journeys with Kannagi to Madurai to rebuild their life by selling her ruby-filled anklet. Wrongfully accused of stealing the Queen’s pearl anklet by a dishonest court goldsmith, Kovalan is executed without fair trial by the Pandyan king Nedunjeliyan. Kannagi shatters the remaining anklet in the royal court, exposing the king’s catastrophic error, causing the king and queen to die of shock. Kannagi invokes Agni and burns corrupt Madurai, becoming celebrated as Pattini Devi (the embodiment of righteousness).',
        'cultural_significance': 'Silappadikaram bridges social reality, fine arts, urban planning, dance musicology (Arangetru Kadai), and justice. It establishes the Pattini cult revered across Tamil Nadu, Kerala, and Sri Lanka. Unlike courtly panegyrics, its protagonist is an ordinary merchant woman whose virtue subverts absolute monarchical authority.',
        'historical_context': 'Composed during the late Sangam or post-Sangam era, the text provides vivid descriptions of major ports like Kaveripoompattinam (Poompuhar), music theory (Yazh tuning), and inter-kingdom diplomatic relationships between Cheras, Cholas, and Pandyas.',
        'themes': 'Dharma (Aram), royal accountability, unyielding justice, maritime trade, Bharatanatyam precursors, and feminine spiritual authority.',
        'available_translations': 'Translated into English by Alain Daniélou (1965), R. Parthasarathy (Columbia University Press, 1993, Sahitya Akademi Award winner), and multiple modern Indian languages.',
        'custodian_collection': 'U. V. Swaminatha Iyer Library, Chennai; palm-leaf recensions recovered from Thanjavur and Tirunelveli.',
        'rights_attribution': 'Ancient Classical Heritage (Public Domain); modern critical texts preserved by Sahitya Akademi.',
        'excerpt_content': '''"Oh witness of the Sun! Is it righteous that my innocent husband be struck down as a thief?
If I be chaste and truthful, let the city of Madurai know the blazing fire of injustice!"
With trembling hands, Kannagi broke her gold anklet upon the throne steps;
Rubies spilled across the polished marble, while the royal queen's anklet bore only pearls.
The Pandyan King gasped: "I am no king, I am the robber. Today the justice of the Pandyas is extinguished."''',
        'external_reading_url': 'https://archive.org/details/the-tale-of-an-anklet-silappadikaram-parthasarathy',
        'featured': True,
        'related_entry_slugs': ['bharatanatyam', 'thanjavur-paintings']
    },
    {
        'title': 'Guru Granth Sahib (Adi Granth)',
        'slug': 'guru-granth-sahib',
        'author_creator': 'Compiled by Guru Arjan Dev (1604 CE), conferred eternal Guruship by Guru Gobind Singh (1708 CE)',
        'work_type': 'sacred_text',
        'tradition': 'Sikh Tradition & Bhagat Sahit',
        'language': 'Sant Bhasha (Punjabi, Braj Bhasha, Persian, Sanskrit, Awadhi, Marathi dialectic blend)',
        'script': 'Gurmukhi',
        'historical_period': '1469–1708 CE',
        'classification_type': 'original',
        'state_name': 'Punjab',
        'category_slug': 'sacred-texts',
        'brief_intro': 'The eternal living Guru of Sikhism, comprising 1,430 Angs (pages) of profound philosophical poetry arranged across 31 classical musical Ragas.',
        'synopsis': 'The Guru Granth Sahib is unique among world scriptures for its radically universalist and interfaith composition. Along with the divine revelations of six Sikh Gurus (Guru Nanak, Guru Angad, Guru Amar Das, Guru Ram Das, Guru Arjan, and Guru Tegh Bahadur), it lovingly canonizes the sacred compositions (Bani) of 15 non-Sikh Bhagats and Sufi saints across India—including Bhagat Kabir, Bhagat Namdev (Maharashtra), Bhagat Ravidas, Bhagat Jaidev (Bengal), Bhagat Ramanand, and Sheikh Farid (Punjab Sufi). Set strictly to classical Indian ragas, every hymn explores oneness (Ik Onkar), egalitarian community service (Seva), righteous honest labor (Kirat Karo), and divine remembrance (Naam Simran).',
        'cultural_significance': 'It is reverently treated as a Living Guru rather than a book. It dismantled rigid caste hierarchies, ritualistic dogma, and linguistic discrimination by communicating highest mystical philosophy in the people’s vernaculars set to sublime classical melody.',
        'historical_context': 'Compiled at Amritsar in 1604 as the Adi Granth and installed at Sri Harmandir Sahib with Baba Buddha as first Granthi. In 1708 at Nanded, the tenth master Guru Gobind Singh commanded: "Sab Sikhan ko hukam hai, Guru manyo Granth."',
        'themes': 'Divine oneness (Ik Onkar), radical equality, devotion through classical Raga, compassion (Daya), casteless brotherhood, and inner truth (Sat).',
        'available_translations': 'Complete English translations by Max Arthur Macauliffe, Dr. Gopal Singh, Manmohan Singh, and Sant Singh Khalsa. Available widely on open academic research portals.',
        'custodian_collection': 'Sri Harmandir Sahib (Golden Temple), Amritsar; Takht Sri Hazur Sahib, Nanded; historical Birhs preserved in museum archives.',
        'rights_attribution': 'Sacred Pan-Indian Heritage. Canonized public spiritual legacy.',
        'excerpt_content': '''ੴ ਸਤਿ ਨਾਮੁ ਕਰਤਾ ਪੁਰਖੁ ਨਿਰਭਉ ਨਿਰਵੈਰੁ ਅਕਾਲ ਮੂਰਤਿ ਅਜੂਨੀ ਸੈਭੰ ਗੁਰ ਪ੍ਰਸਾਦਿ ॥
ਜਪੁ ॥ ਆਦਿ ਸਚੁ ਜੁਗਾਦਿ ਸਚੁ ॥ ਹੈ ਭੀ ਸਚੁ ਨਾਨਕ ਹੋਸੀ ਭੀ ਸਚੁ ॥

"There is One Sovereign Supreme Reality, whose name is Eternal Truth;
The Creative Being Personified, Without Fear, Without Enmity,
Timeless Form, Beyond Birth, Self-Existent, Realized by Guru's Grace.
Meditate! True in the Primal Beginning; True throughout the cosmic ages;
True Here and Now; O Nanak, Forever and Ever True."''',
        'external_reading_url': 'https://www.srigranth.org/',
        'featured': True,
        'related_entry_slugs': ['bhangra-punjab-dance', 'phulkari-embroidery', 'punjab-music-entry']
    },
    {
        'title': 'Ramcharitmanas & Valmiki Ramayana (The Epic Traditions)',
        'slug': 'ramayana-literary-tradition',
        'author_creator': 'Maharishi Valmiki (Sanskrit Adi-Kavya) & Goswami Tulsidas (Awadhi Ramcharitmanas)',
        'work_type': 'book',
        'tradition': 'Pan-Indian Epic Tradition & Bhakti Movement',
        'language': 'Awadhi & Classical Sanskrit',
        'script': 'Devanagari / Kaithi',
        'historical_period': 'Ancient Antiquity (Valmiki) / 1574 CE (Tulsidas)',
        'classification_type': 'retelling',
        'state_name': 'Uttar Pradesh',
        'category_slug': 'literature',
        'brief_intro': 'India’s foundational epic explored as an expansive literary tradition with dozens of diverse regional retellings across states and Southeast Asia.',
        'synopsis': 'Rather than existing as a single monolithic text, the Ramayana is a vibrant civilisational ecosystem. Originating with Maharishi Valmiki’s Sanskrit Adikavya (celebrated for poetic meter Anushtubh), it was retold into Awadhi verse as Ramcharitmanas by Goswami Tulsidas in Varanasi and Ayodhya. It also flourished into Kamban’s Kamba Ramayanam (Tamil 12th c.), Krittibas Ojha’s Krittivasi Ramayan (Bengali 15th c.), Madhava Kandali’s Saptakanda Ramayana (Assamese 14th c.), Ezhuthachan’s Adhyathma Ramayanam Kilippattu (Malayalam 16th c.), and regional folk performance traditions like Ramlila (UNESCO Intangible Heritage).',
        'cultural_significance': 'The epic shaped moral philosophy, sculpture, puppet theatre (Kathputli, Togalu Gombeyaata), classical dance dramas (Kathakali, Yakshagana), and communal musical sankirtan across every region of India and Southeast Asia (Ramakien in Thailand, Kakawin in Java).',
        'historical_context': 'Tulsidas began composing the Ramcharitmanas in 1574 CE at Ayodhya on Rama Navami, democratizing spiritual poetry for ordinary commoners who did not know Sanskrit.',
        'themes': 'Maryada (righteous conduct), filial duty, compassion, democratic retellings, nature and ecology of Dandakaranya, and Bhakti.',
        'available_translations': 'Freely translated into dozens of global languages, including English verse translations by Ralph T.H. Griffith and modern Gita Press publications.',
        'custodian_collection': 'Tulsi Mandir, Varanasi; Saraswathi Mahal Library, Thanjavur; National Museum, New Delhi.',
        'rights_attribution': 'Classical Public Domain & UNESCO Intangible Cultural Heritage legacy.',
        'excerpt_content': '''मंगल भवन अमंगल हारी। द्रवहु सुदसरथ अजिर बिहारी॥
सीय राम मय सब जग जानी। करहुँ प्रनाम जोरि जुग पानी॥

"May that supreme fountain of auspiciousness, which removes all adversity, shower blessing upon all.
Knowing the entire universe to be permeated by Sita and Rama, I bow to all with folded hands in reverence."''',
        'external_reading_url': 'https://archive.org/details/RamcharitmanasGitaPress',
        'featured': True,
        'related_entry_slugs': ['kathak-dance', 'kathakali-dance-theatre']
    },
    {
        'title': 'Thirukkural (The Book of Divine Ethics)',
        'slug': 'thirukkural-ethics',
        'author_creator': 'Thiruvalluvar (Ancient Tamil Philosopher-Poet)',
        'work_type': 'sacred_text',
        'tradition': 'Classical Secular & Ethical Philosophy',
        'language': 'Classical Tamil',
        'script': 'Tamil',
        'historical_period': 'c. 3rd Century BCE – 5th Century CE',
        'classification_type': 'original',
        'state_name': 'Tamil Nadu',
        'category_slug': 'sacred-texts',
        'brief_intro': 'A universal masterwork of 1,330 couplets (Kurals) divided into Virtue (Aram), Wealth (Porul), and Love (Inbam), completely non-denominational and universal in human wisdom.',
        'synopsis': 'The Thirukkural is universally hailed as one of the greatest moral and philosophical treatises in world literature. Composed by the sage Thiruvalluvar in exactly two-line aphorisms (kural venba), it systematically outlines how human beings should live an upright, compassionate, and meaningful earthly life. Crucially, the work invokes no sectarian deities or supernatural dogma; its ethical imperatives address universal human dignity, hospitality (Virundhombal), truthfulness (Vaimai), avoidance of wrath, statecraft, agricultural dignity, friendship, and reciprocal conjugal love.',
        'cultural_significance': 'Recognized as the "Universal Veda" (Ulaga Podhumarai). Its ethical tenets guided classical Tamil jurisprudence, inspired Mahatma Gandhi and Leo Tolstoy, and remains a touchstone for humanist moral philosophy.',
        'historical_context': 'Presented before the Third Tamil Sangam at Madurai. It represents the pinnacle of classical Tamil moral rationality and empirical insight.',
        'themes': 'Universal ethics, vegetarianism, truthful speech, good governance, mutual respect, hard work, and domestic felicity.',
        'available_translations': 'Translated into over 42 languages, including the famous 19th-century translation by Rev. G. U. Pope, Father Beschi (Latin), and modern English versions by Rajaji and P. S. Sundaram.',
        'custodian_collection': 'Government Oriental Manuscripts Library, Chennai; Saraswathi Mahal Library, Thanjavur.',
        'rights_attribution': 'Classical World Heritage (Public Domain).',
        'excerpt_content': '''அகர முதல எழுத்தெல்லாம் ஆதி
பகவன் முதற்றே உலகு. (குறள் 1)

"As the letter 'A' is the first of all letters,
So the Eternal Divine Source is the origin of the cosmos."

பிறப்பொக்கும் எல்லா உயிர்க்கும் சிறப்பொவ்வா
செய்தொழில் வேற்றுமை யான். (குறள் 972)

"All human beings are equal by virtue of birth;
Their distinctions arise only from the quality of their actions."''',
        'external_reading_url': 'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0001.html',
        'featured': True,
        'related_entry_slugs': ['bharatanatyam']
    },
    {
        'title': 'Bower Manuscript & Birch-Bark Medical Codices',
        'slug': 'bower-manuscript-ayurveda',
        'author_creator': 'Compiled by Buddhist Monks / Yashomitra (Discovered near Kucha on Silk Route)',
        'work_type': 'manuscript',
        'tradition': 'Ancient Indian Medicine & Buddhist Epigraphy',
        'language': 'Hybrid Sanskrit',
        'script': 'Early Gupta Brahmi Script',
        'historical_period': 'c. 4th–5th Century CE',
        'classification_type': 'original',
        'state_name': 'Jammu & Kashmir',
        'category_slug': 'manuscripts',
        'brief_intro': 'One of the oldest surviving written Indian birch-bark manuscripts in the world, preserving ancient recipes of Ayurveda, pharmacology, and divination.',
        'synopsis': 'Discovered in 1890 inside a stupa near Kucha in Chinese Turkestan by British intelligence officer Lieutenant Hamilton Bower, this extraordinary birch-bark codex consists of 51 leaves inscribed in black ink with the early Gupta variety of Brahmi script. It contains ancient medical treatises on garlic (Lasuna Kalpa), eye ointments, compound herbal prescriptions identical to the Charaka and Sushruta Samhitas, veterinary treatments, and invocations to protect children.',
        'cultural_significance': 'Proved that classical Indian Ayurvedic medicine and Sanskrit scientific literature were actively circulating, practiced, and preserved along the Silk Route over 1,500 years ago.',
        'historical_context': 'Deciphered by legendary orientalist A. F. Rudolf Hoernle between 1893 and 1912, it transformed Indian paleography and medical history.',
        'themes': 'Traditional herbal pharmacopeia, Gupta-era paleography, cross-cultural transmission of knowledge, and ancient conservation.',
        'available_translations': 'Critical edition and translation published by A. F. Rudolf Hoernle (Archaeological Survey of India, 1893–1912).',
        'custodian_collection': 'Bodleian Library, University of Oxford (MS. Ind. Inst. Misc. 79); facsimile copies at National Museum, New Delhi.',
        'rights_attribution': 'Ancient Scientific Manuscript Archive (Public Domain).',
        'excerpt_content': '''Leaf II, Recto: "The sage said: Whosoever consumes the prepared essence of Lasuna (garlic)
mixed with clarified butter, their digestive fire increases, the joints regain ease,
the eyes retain their clarity, and longevity is bestowed like unto the gods."
(Inscribed on Himalayan Birch-bark, Sanskrit in Gupta Brahmi script)''',
        'external_reading_url': 'https://archive.org/details/bowermanuscriptf00hoeruoft',
        'featured': True,
        'related_entry_slugs': []
    },
    {
        'title': 'Jataka Tales (Pali Buddhist Canonical Literature)',
        'slug': 'jataka-tales-buddhist-literature',
        'author_creator': 'Preserved in the Pali Canon (Khuddaka Nikaya, Sutta Pitaka)',
        'work_type': 'book',
        'tradition': 'Buddhist Literary & Ethical Tradition',
        'language': 'Pali',
        'script': 'Brahmi / Devanagari / Sinhala',
        'historical_period': 'c. 4th Century BCE – 2nd Century CE',
        'classification_type': 'original',
        'state_name': 'Bihar',
        'category_slug': 'literature',
        'brief_intro': 'A magnificent collection of 547 moral tales recounting previous incarnations of Gautama Buddha as animals, kings, ascetics, and householders embodying moral perfection.',
        'synopsis': 'The Jatakas represent the oldest and largest collection of folklore and fable in world literature. Each tale features the Bodhisattva (Buddha in a prior lifetime) demonstrating one of the Ten Perfections (Paramitas)—such as generosity (Dana), ethical discipline (Sila), patience (Khanti), or wisdom (Panna). Famous stories like the Mahakapi Jataka (The Great Monkey King who saves his troop by bridging a river with his own body), the Sibi Jataka (the king who offers his own flesh to save a dove), and the Vessantara Jataka are foundational to Asian moral imagination.',
        'cultural_significance': 'Directly inspired the world-renowned narrative murals of Ajanta Caves (Maharashtra), the carved stupa railings of Sanchi and Bharhut (Madhya Pradesh), and influenced Aesop’s Fables and the Panchatantra.',
        'historical_context': 'Originating in Magadha and North India, recorded in Pali and translated widely into Tibetan, Chinese, and regional Indian vernaculars.',
        'themes': 'Selfless sacrifice, compassion towards all living creatures, karmic consequence, animal intelligence, and civic leadership.',
        'available_translations': 'Pali Text Society translation by E. B. Cowell (6 volumes, Cambridge University Press, 1895–1907); accessible editions by Sahitya Akademi.',
        'custodian_collection': 'Nalanda Mahavihara archives; Pali manuscripts preserved at Asiatic Society, Kolkata and Mahabodhi Society, Bodh Gaya.',
        'rights_attribution': 'Classical Buddhist Canonical Heritage (Public Domain).',
        'excerpt_content': '''"Let not the virtuous despair in times of peril.
As the great monkey king stretched his body from bough to cliff to let the small monkeys flee to safety,
saying: 'Pain to my own limbs is joy, for my people are delivered,'
even so does the wise shepherd endure sorrow for the welfare of all."
(From the Mahakapi Jataka, Pali Verse)''',
        'external_reading_url': 'https://archive.org/details/jatakastories01cowe',
        'featured': True,
        'related_entry_slugs': ['madhubani-painting', 'warli-tribal-art']
    },
    {
        'title': 'Tattvartha Sutra (The Compendium of Reality)',
        'slug': 'tattvartha-sutra-jain-philosophy',
        'author_creator': 'Acharya Umaswati (Revered Master of Digambara & Svetambara traditions)',
        'work_type': 'sacred_text',
        'tradition': 'Jain Philosophical Tradition',
        'language': 'Classical Sanskrit',
        'script': 'Devanagari',
        'historical_period': 'c. 2nd–4th Century CE',
        'classification_type': 'original',
        'state_name': 'Gujarat',
        'category_slug': 'sacred-texts',
        'brief_intro': 'The foundational scripture accepted unanimously by all traditions of Jainism, synthesizing epistemology, metaphysics, ethics, and liberation.',
        'synopsis': 'Tattvartha Sutra consists of 357 concise aphorisms arranged across 10 chapters. It begins with the celebrated definition of the path to liberation (Moksha): "Samyag-darsana-jnana-caritrani moksamargah" (Right faith, right knowledge, and right conduct constitute the path to liberation). It outlines the seven fundamental realities (Tattvas), karma theory, cosmological atomism (Pudgala), and the foundational ethical vow of Ahimsa (non-violence) in thought, word, and deed.',
        'cultural_significance': 'The text introduced the universal motto of Jainism: "Parasparopagraho Jivanam" (Souls render service to one another / all life is interconnected). It represents one of the world’s earliest treatises on non-violent environmental ethics and multi-faceted truth (Anekantavada).',
        'historical_context': 'Composed in Sanskrit at Pataliputra or western India, making ancient Prakrit Jain canonical philosophy accessible to pan-Indian philosophical debates.',
        'themes': 'Ahimsa (non-harm), Anekantavada (non-absolutism), ecological interdependence, karma particles, and mental equanimity.',
        'available_translations': 'Translated into English by Nathmal Tatia (HarperCollins, 1994) and Dr. K. K. Dixit (L.D. Institute of Indology, Ahmedabad).',
        'custodian_collection': 'Lalbhai Dalpatbhai Institute of Indology, Ahmedabad; Jaisalmer Shastra Bhandar; Moodabidri Palm Leaf Library.',
        'rights_attribution': 'Classical Philosophical Heritage (Public Domain).',
        'excerpt_content': '''सम्यग्दर्शनज्ञानचारित्राणि मोक्षमार्गः ॥ १.१ ॥
परस्परोपग्रहो जीवानाम् ॥ ५.२१ ॥

"Right Perception, Right Knowledge, and Right Conduct together form the path to liberation.
The essential nature of living beings is to support and assist one another."''',
        'external_reading_url': 'https://archive.org/details/tattvarthasutra00umas',
        'featured': False,
        'related_entry_slugs': []
    },
    {
        'title': 'Kalam-e-Bulleh Shah & Waris Shah’s Heer (Punjabi Sufi Literature)',
        'slug': 'bulleh-shah-heer-waris-shah',
        'author_creator': 'Baba Bulleh Shah & Waris Shah',
        'work_type': 'book',
        'tradition': 'Punjabi Sufi Poetry & Kissa Tradition',
        'language': 'Punjabi',
        'script': 'Shahmukhi & Gurmukhi',
        'historical_period': '18th Century CE (c. 1720–1766 CE)',
        'classification_type': 'original',
        'state_name': 'Punjab',
        'category_slug': 'literature',
        'brief_intro': 'Lyrical masterpieces of mystical Punjabi Sufi Kafi poetry and the tragic romance of Heer-Ranjha, celebrated for radical love transcending religious divisions.',
        'synopsis': 'Bulleh Shah’s kafis and Waris Shah’s epic rendition of Heer Ranjha represent the apex of Punjab’s composite literary soul. Bulleh Shah challenged ritualistic clericalism and orthodoxy through poems of ecstatic devotion to the beloved. In Heer Ranjha, Waris Shah turned a folk ballad of Jhang into a sweeping cultural encyclopedia of 18th-century Punjab—documenting wedding ceremonies, agriculture, crafts, religious discourse, and the unyielding spiritual purity of Heer and Ranjha’s love.',
        'cultural_significance': 'Sung across generations by qawwals, classical dhadi singers, and folk musicians across Punjab on both sides of the border. It embodies the shared syncretic composite heritage of the subcontinent.',
        'historical_context': 'Composed during turbulent political transitions in 18th-century Punjab, advocating communal harmony, inner purity, and social courage.',
        'themes': 'Divine love (Ishq-e-Haqiqi), human unity, rejection of dogmatism, rural Punjabi life, and resistance against social tyranny.',
        'available_translations': 'Translated by Christopher Shackle (Harvard University Press Murty Classical Library), Kartar Singh Duggal, and Sant Singh Sekhon.',
        'custodian_collection': 'Punjab University Library, Lahore; Punjabi University, Patiala; Sahitya Akademi Archives.',
        'rights_attribution': 'Classical Folk & Sufi Heritage (Public Domain).',
        'excerpt_content': '''ਬੁੱਲ੍ਹਾ ਕੀ ਜਾਣਾ ਮੈਂ ਕੌਣ?
ਨਾ ਮੈਂ ਮੋਮਨ ਵਿੱਚ ਮਸੀਤਾਂ, ਨਾ ਮੈਂ ਵਿੱਚ ਕੁਫ਼ਰ ਦੀਆਂ ਰੀਤਾਂ,
ਨਾ ਮੈਂ ਪਾਕਾਂ ਵਿੱਚ ਪਲੀਤਾਂ, ਨਾ ਮੈਂ ਮੂਸਾ ਨਾ ਫ਼ਿਰਔਨ...
ਬੁੱਲ੍ਹਾ ਕੀ ਜਾਣਾ ਮੈਂ ਕੌਣ!

"Bullah! to me, I am not known:
Not among believers in the mosque am I, nor in the rituals of disbelief;
Neither among the pure nor the tainted; neither Moses nor Pharaoh...
Bullah! to me, I am not known!"''',
        'external_reading_url': 'https://archive.org/details/bulleshahverses00bull',
        'featured': True,
        'related_entry_slugs': ['bhangra-punjab-dance', 'punjab-music-entry']
    },
    {
        'title': 'Gitanjali (Song Offerings)',
        'slug': 'gitanjali-rabindranath-tagore',
        'author_creator': 'Rabindranath Tagore (Gurudev)',
        'work_type': 'book',
        'tradition': 'Modern Bengal Renaissance & Mystic Lyricism',
        'language': 'Bengali',
        'script': 'Bengali',
        'historical_period': '1910 (Bengali) / 1912 (English translation)',
        'classification_type': 'original',
        'state_name': 'West Bengal',
        'category_slug': 'literature',
        'brief_intro': 'Tagore’s immortal collection of lyrical verses, which won the 1913 Nobel Prize in Literature—the first Nobel Prize awarded to an Asian writer.',
        'synopsis': 'Gitanjali is an offering of profound songs exploring intimate communication with the Infinite. Written in melodious Bengali and translated by Tagore into English prose-poetry with an introduction by W. B. Yeats, the poems touch upon divine immanence in nature, the simplicity of rural life, the plight of the humble worker, and fearless intellectual freedom.',
        'cultural_significance': 'Marked modern India’s profound poetic entry onto the global intellectual stage. Poem 35, "Where the mind is without fear," became a universal anthem of civil liberties and human spiritual freedom.',
        'historical_context': 'Composed in Santiniketan and Shelaidaha during a period of deep national awakening and personal introspection.',
        'themes': 'Universal brotherhood, divine presence in labor, fearlessness of truth, and lyrical simplicity.',
        'available_translations': 'Tagore’s own authorized English translation (Macmillan, 1913); translated into French by André Gide, and dozens of Indian languages.',
        'custodian_collection': 'Rabindra Bhavana Archives, Visva-Bharati University, Santiniketan; National Library of India, Kolkata.',
        'rights_attribution': 'Public Domain worldwide.',
        'excerpt_content': '''"Where the mind is without fear and the head is held high;
Where knowledge is free;
Where the world has not been broken up into fragments by narrow domestic walls;
Where words come out from the depth of truth;
Where tireless striving stretches its arms towards perfection;
Where the clear stream of reason has not lost its way into the dreary desert sand of dead habit;
Into that heaven of freedom, my Father, let my country awake."
(Gitanjali, Verse 35)''',
        'external_reading_url': 'https://www.gutenberg.org/ebooks/7164',
        'featured': True,
        'related_entry_slugs': []
    },
    {
        'title': 'Hortus Malabaricus & Varthamanappusthakam (Kerala Historical Archives)',
        'slug': 'hortus-malabaricus-kerala-manuscript',
        'author_creator': 'Itti Achuden Vaidyan, Hendrik van Rheede & Paremakkal Thoma Kathanar',
        'work_type': 'manuscript',
        'tradition': 'Botanical Science & Early Modern Travelogue',
        'language': 'Malayalam & Latin',
        'script': 'Kolezhuthu / Malayalam / Roman',
        'historical_period': '1678–1693 CE (Hortus) / 1785 CE (Varthamanappusthakam)',
        'classification_type': 'original',
        'state_name': 'Kerala',
        'category_slug': 'manuscripts',
        'brief_intro': 'A 12-volume monumental botanical compilation recording Kerala’s indigenous medicinal flora, along with the first printed travelogue in any Indian language.',
        'synopsis': 'Hortus Malabaricus ("Garden of Malabar") was compiled in Kochi through the knowledge of local master Ayurvedic physician Itti Achuden Vaidyan and three Konkani scholars (Ranga Bhat, Vinayaka Pandit, Appu Bhat). It classifies 742 medicinal plants of the Western Ghats with detailed copperplate engravings and botanical properties. It also holds the historic distinction of containing the first printed Malayalam script in history (Itti Achuden’s signed declaration in Kolezhuthu script in 1675). Alongside, Varthamanappusthakam by Paremakkal Thoma Kathanar documents the 18th-century maritime voyage of Indian St. Thomas Christians to Rome, reflecting early Indian global intellectual interaction.',
        'cultural_significance': 'Recognized as an irreplaceable bridge between traditional indigenous ethno-botanical medicine and early modern European science. Referenced extensively by Carl Linnaeus in establishing modern botanical binomial nomenclature.',
        'historical_context': 'Compiled in Cochin between 1678 and 1693, testifying to the rigorous scientific heritage of Kerala’s traditional Ezhava and Vaidya herbalists.',
        'themes': 'Indigenous biodiversity conservation, ethno-botany, early printing history, and cross-cultural scholarly collaboration.',
        'available_translations': 'English translation in 12 volumes by Prof. K. S. Manilal (University of Kerala, 2003, awarded Padma Shri); Latin original digitized by national botanical archives.',
        'custodian_collection': 'University of Amsterdam; Kerala State Archives; Leiden University Library.',
        'rights_attribution': 'Historical Public Domain Archive. Digitized educational record.',
        'excerpt_content': '''Itti Achuden Vaidyan's Inscription (Cochin, 1675 CE):
"I, Itti Achuden, physician of Kollat in Kodakarapally, have examined the trees, shrubs, and herbs of Malabar according to the ancestral palm-leaf granthas of my family, and recorded their names, medicinal properties, and preparations truthfully for this work."
(Earliest surviving printed Malayalam font in world history)''',
        'external_reading_url': 'https://archive.org/details/horti-malabarici-manilal',
        'featured': False,
        'related_entry_slugs': ['kathakali-dance-theatre', 'kalaripayattu-martial-art']
    },
    {
        'title': 'Alha-Khand & Oral Ballads of Bundelkhand',
        'slug': 'alha-khand-oral-epic',
        'author_creator': 'Attributed to court bard Jagnik of Mahoba (Living Bardic Oral Tradition)',
        'work_type': 'oral_tradition',
        'tradition': 'Bundelkhandi Bardic Oral Tradition',
        'language': 'Bundeli & Braj Bhasha',
        'script': 'Oral Performance / Devanagari',
        'historical_period': '12th Century CE onwards',
        'classification_type': 'original',
        'state_name': 'Madhya Pradesh',
        'category_slug': 'oral-tradition',
        'brief_intro': 'One of the world’s longest surviving living oral folk epics, performed by village bards during the monsoon across North and Central India.',
        'synopsis': 'The Alha-Khand celebrates the extraordinary 52 battles of the warrior brothers Alha and Udal, generals of King Parmal of Mahoba against Prithviraj Chauhan of Delhi. Transmitted purely through oral recitation for over 800 years by traditional bards called Alha-gaitas accompanied by the beating of the Dholak and Nagada, the epic’s thunderous meter (Alha chhand) rouses village gatherings during the rainy season. It honors valor, unwavering loyalty to the soil, resistance against humiliation, and devotion to Sharada Devi of Maihar.',
        'cultural_significance': 'A quintessential example of India’s living oral memory that survived without royal patronage or printing presses. It demonstrates how community bards preserve history in living dialect.',
        'historical_context': 'First transcribed from oral reciters by British collector Charles Elliott in Farrukhabad in 1865, and rendered into English ballad meter by William Waterfield in 1876.',
        'themes': 'Martial honor, folk chivalry, bardic memory, oral formulaic transmission, and community identity.',
        'available_translations': 'The Lay of Alha: A Saga of Rajput Chivalry translated by William Waterfield & George Grierson (Oxford University Press, 1923).',
        'custodian_collection': 'Living community bards of Bundelkhand, Mahoba, and Bundelkhand University Folk Archives.',
        'rights_attribution': 'Living Oral Heritage. Community Public Domain.',
        'excerpt_content': '''"जा दिन जनम भयो आल्हा को, धरती धंसी अढ़ाई हाथ!
बारह बरस ले कूकुर जीवे, अरु तेरह ले जिये सियार।
बरस अठारह छत्री जीवे, आगे जीवन को धिक्कार!"

"On the day Alha was born, the very earth sank two and a half cubits!
Twelve years lives a dog, and thirteen lives a jackal;
Eighteen years lives a true braveheart, anything beyond is in vain!"
(Bundelkhandi Monsoon Bardic Ballad)''',
        'external_reading_url': 'https://archive.org/details/layofalhasagaof00wateuoft',
        'featured': False,
        'related_entry_slugs': []
    },
    {
        'title': 'Sushruta Samhita & Charaka Samhita (Treatises on Healing & Surgery)',
        'slug': 'sushruta-charaka-samhita',
        'author_creator': 'Acharya Sushruta (Father of Surgery) & Acharya Charaka',
        'work_type': 'treatise',
        'tradition': 'Ancient Indian Medical & Surgical Sciences',
        'language': 'Classical Sanskrit',
        'script': 'Devanagari / Sharada',
        'historical_period': 'c. 6th Century BCE – 2nd Century CE',
        'classification_type': 'original',
        'state_name': 'Uttar Pradesh',
        'category_slug': 'traditional-knowledge',
        'brief_intro': 'Foundational scientific treatises detailing surgical reconstruction (rhinoplasty), over 120 surgical instruments, and internal medicine based on bodily equilibrium.',
        'synopsis': 'The Sushruta Samhita and Charaka Samhita form the twin pillars of traditional Indian health sciences (Ayurveda). The Sushruta Samhita is particularly renowned worldwide for pioneering surgical procedures: plastic surgery (pedicled flap rhinoplasty), cataract couching, lithotomy, cesarean operations, and anatomical dissection using water decomposition. It categorizes surgical instruments into Yantras (blunt) and Shastras (cutting instruments designed inspired by birds’ beaks and beasts’ claws). The Charaka Samhita focuses on internal medicine, diagnostics, ecology of herbs, and the prevention of epidemic diseases (Janapadodhwamsa).',
        'cultural_significance': 'Sushruta is recognized by international medical historians as the Father of Plastic Surgery. The texts were translated into Arabic during the Abbasid Caliphate as Kitab-i-Susrud and influenced Islamic and European medicine.',
        'historical_context': 'Taught at the ancient medical schools of Varanasi and Taxila. Preserved through palm-leaf and paper manuscripts across Nepal, Kashmir, and Kerala.',
        'themes': 'Surgical innovation, preventative medicine, medical ethics, anatomical observation, and botanical pharmacology.',
        'available_translations': 'English translations by Kaviraj Kunjalal Bhishagratna (3 volumes, 1907–1916) and modern critical editions by Prof. P. V. Sharma.',
        'custodian_collection': 'Banaras Hindu University Ayurvedic Library; Wellcome Collection, London; Nepal National Archives.',
        'rights_attribution': 'Ancient Scientific Heritage (Public Domain).',
        'excerpt_content': '''"The surgeon who knows both anatomy and surgical practice from direct observation,
and whose hands are skilled with precision instruments,
he alone is true master of the healing art.
Neither book learning alone, nor unguided manual boldness, can save the stricken life."
(Sushruta Samhita, Sutrasthana)''',
        'external_reading_url': 'https://archive.org/details/englishtranslati01susrrich',
        'featured': False,
        'related_entry_slugs': []
    }
]

for w_data in works_data:
    state_obj = None
    if w_data.get('state_name'):
        state_obj = State.objects.filter(name__icontains=w_data['state_name']).first()
    
    cat_obj = created_categories.get(w_data.get('category_slug'))
    
    work, created = LiteraryWork.objects.get_or_create(
        slug=w_data['slug'],
        defaults={
            'title': w_data['title'],
            'author_creator': w_data['author_creator'],
            'work_type': w_data['work_type'],
            'tradition': w_data['tradition'],
            'language': w_data['language'],
            'script': w_data['script'],
            'historical_period': w_data['historical_period'],
            'classification_type': w_data['classification_type'],
            'state': state_obj,
            'category': cat_obj,
            'brief_intro': w_data['brief_intro'],
            'synopsis': w_data['synopsis'],
            'cultural_significance': w_data['cultural_significance'],
            'historical_context': w_data['historical_context'],
            'themes': w_data['themes'],
            'available_translations': w_data['available_translations'],
            'custodian_collection': w_data['custodian_collection'],
            'rights_attribution': w_data['rights_attribution'],
            'excerpt_content': w_data['excerpt_content'],
            'external_reading_url': w_data['external_reading_url'],
            'featured': w_data['featured'],
            'status': 'published'
        }
    )
    if not created:
        work.title = w_data['title']
        work.author_creator = w_data['author_creator']
        work.work_type = w_data['work_type']
        work.tradition = w_data['tradition']
        work.language = w_data['language']
        work.script = w_data['script']
        work.historical_period = w_data['historical_period']
        work.classification_type = w_data['classification_type']
        work.state = state_obj
        work.category = cat_obj
        work.brief_intro = w_data['brief_intro']
        work.synopsis = w_data['synopsis']
        work.cultural_significance = w_data['cultural_significance']
        work.historical_context = w_data['historical_context']
        work.themes = w_data['themes']
        work.available_translations = w_data['available_translations']
        work.custodian_collection = w_data['custodian_collection']
        work.rights_attribution = w_data['rights_attribution']
        work.excerpt_content = w_data['excerpt_content']
        work.external_reading_url = w_data['external_reading_url']
        work.featured = w_data['featured']
        work.status = 'published'
        work.save()

    # Link related entries if any
    for entry_slug in w_data.get('related_entry_slugs', []):
        entry = CulturalEntry.objects.filter(slug__icontains=entry_slug).first()
        if entry:
            work.related_entries.add(entry)
            
    print(f"Seeded Literary Work: {work.title} ({work.work_type})")

print("Seeding of Cultural Library Ecosystem Complete!")
