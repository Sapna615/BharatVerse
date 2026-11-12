import os
import re
from django.db.models import Q

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('AI_API_KEY')
        self.demo_mode = not bool(self.api_key)

    def _get_demo_warning(self):
        return "\n\n*(Verified BharatVerse Knowledge Engine • Demo Mode)*"

    def ask_cultural_question(self, question, context_data=None):
        if not question:
            return "Please ask any question about India's culture, festivals, art forms, or literature!"

        q_clean = question.strip().lower()
        from culture.models import LiteraryWork, CulturalEntry, State, Festival, Tradition, FolkArt, Cuisine
        from games.models import Game
        from quizzes.models import Quiz

        # 1. Check for specific common cultural concepts
        if any(term in q_clean for term in ['diwali', 'deepavali', 'festival of lights']):
            return (
                "**Diwali (Deepavali) — The Festival of Lights:**\n\n"
                "• **Significance:** Celebrates the triumph of light over spiritual darkness, righteousness over ignorance, and truth over falsehood.\n"
                "• **Key Traditions:** Lighting earthen *diyas*, creating vibrant colored *rangolis*, exchanging traditional sweets, and welcoming Goddess Lakshmi for prosperity.\n"
                "• **Regional Diversity:** In North India, it marks the return of Lord Rama to Ayodhya; in Bengal, Kali Puja is celebrated; in South India, it commemorates the victory over Narakasura."
                + self._get_demo_warning()
            )

        if any(term in q_clean for term in ['holi', 'festival of colors']):
            return (
                "**Holi — The Spring Festival of Colors:**\n\n"
                "• **Significance:** Celebrates the arrival of spring (Vasant Ritu), the rebirth of nature, and the victory of devotion (Prahlad) over tyranny (Holika).\n"
                "• **Celebrations:** Holika Dahan pyres on the eve, followed by throwing natural colored herbal powders (*gulal*), singing folk songs, and sharing delicacies like *Gujiya* and *Thandai*."
                + self._get_demo_warning()
            )

        if any(term in q_clean for term in ['dance', 'classical dance', 'kathak', 'bharatanatyam', 'kathakali', 'odissi']):
            return (
                "**The Classical Dance Heritage of India:**\n\n"
                "Recognized by the Sangeet Natak Akademi, India's classical dances trace their philosophical roots to Sage Bharata’s *Natya Shastra*:\n\n"
                "1. **Bharatanatyam** (Tamil Nadu) — Geometric symmetry, sculptural postures, and *abhinaya*.\n"
                "2. **Kathakali** (Kerala) — Vivid dramatic face paint, elaborate costumes, and martial storytelling.\n"
                "3. **Kathak** (North India) — Complex rhythmic footwork (*tatkar*) and dazzling pirouettes (*chakkars*).\n"
                "4. **Odissi** (Odisha) — Sculptural *tribhanga* postures evoking Konark temple reliefs.\n"
                "5. **Manipuri** (Manipur) — Gentle, devotional *Raas Leela* movements.\n"
                "6. **Kuchipudi** (Andhra Pradesh) — Expressive lyrical dance-dramas and brass plate balancing.\n"
                "7. **Mohiniyattam** (Kerala) — Flowing enchantress dance in white and gold attire.\n"
                "8. **Sattriya** (Assam) — Monastic dance founded by 15th-century saint Mahapurusha Srimanta Sankardev."
                + self._get_demo_warning()
            )

        # 2. Check for State query (e.g. "rajasthan", "punjab", "kerala", "gujarat")
        words = re.findall(r'\b\w+\b', q_clean)
        for st in State.objects.all():
            st_name = st.name.lower()
            if st_name in q_clean or any(w == st_name for w in words):
                entries = CulturalEntry.objects.filter(state=st, status='published')[:3]
                entry_list = "\n".join([f"• **{e.title}** ({e.category.name}): {e.short_description[:120]}..." for e in entries])
                return (
                    f"**Living Heritage of {st.name} ({st.region}):**\n\n"
                    f"{st.description}\n\n"
                    f"**Signature Cultural Traditions:**\n"
                    f"{entry_list if entry_list else 'Rich oral traditions, indigenous handicrafts, and living folk customs.'}\n\n"
                    f"👉 [Explore the full cultural profile of {st.name}](/explore/states/{st.slug}/)"
                    + self._get_demo_warning()
                )

        # 3. Check for matching Cultural Entry by keyword search
        for e in CulturalEntry.objects.filter(status='published'):
            e_lower = e.title.lower()
            if any(term in q_clean for term in e_lower.split() if len(term) >= 4):
                return (
                    f"**{e.title}** ({e.category.name} of {e.state.name}):\n\n"
                    f"{e.short_description}\n\n"
                    f"**Cultural Significance:**\n{e.cultural_significance[:350]}...\n\n"
                    f"👉 [Read the complete story on BharatVerse](/explore/culture/{e.slug}/)"
                    + self._get_demo_warning()
                )

        # 4. Check for Literary Works / Scriptures
        for w in LiteraryWork.objects.filter(status='published'):
            w_lower = w.title.lower()
            if any(term in q_clean for term in w_lower.split() if len(term) >= 4) or (w.author_creator and any(term in q_clean for term in w.author_creator.lower().split() if len(term) >= 4)):
                return (
                    f"**{w.title}** ({w.get_work_type_display()}):\n\n"
                    f"• **Author / Attribution:** {w.author_creator or 'Living Oral Tradition'}\n"
                    f"• **Language:** {w.language} | **Tradition:** {w.tradition}\n\n"
                    f"**Overview:** {w.brief_intro}\n\n"
                    f"**Significance:** {w.cultural_significance[:300]}...\n\n"
                    f"👉 [Read in Digital Library](/explore/library/{w.slug}/)"
                    + self._get_demo_warning()
                )

        # 5. Fallback with helpful dynamic search prompt
        return (
            f"You asked about *\"{question}\"*.\n\n"
            "BharatVerse archives thousands of living heritage records. You can ask me about:\n"
            "• **Any Indian State:** e.g., *'Tell me about Kerala'*, *'Culture of Rajasthan'*, *'Punjab'*\n"
            "• **Classical Arts & Dances:** e.g., *'Kathakali'*, *'Bharatanatyam'*, *'Warli Art'*\n"
            "• **Festivals & Lore:** e.g., *'Diwali'*, *'Holi'*, *'Bihu'*, *'Onam'*\n"
            "• **Literary Classics:** e.g., *'Gitanjali'*, *'Thirukkural'*, *'Meghaduta'*"
            + self._get_demo_warning()
        )
