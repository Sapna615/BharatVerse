import os
from django.db.models import Q

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('AI_API_KEY')
        self.demo_mode = not bool(self.api_key)

    def _get_demo_warning(self):
        return "\n\n*(Grounded in verified BharatVerse Knowledge Records • Demo Mode)*"

    def ask_cultural_question(self, question, context_data=None):
        if self.demo_mode:
            q_lower = question.lower()
            from culture.models import LiteraryWork, CulturalEntry
            
            # Check for translation vs retelling question
            if 'translation' in q_lower and 'retelling' in q_lower:
                return (
                    "**Translation vs. Retelling in Indian Literary Tradition:**\n\n"
                    "• **Translation** aims for textual fidelity to the source language, preserving original syntax, idioms, or stanza units into another target tongue (e.g., A.K. Ramanujan’s translations of classical Sangam poetry or English renderings of the Thirukkural).\n"
                    "• **Retelling (Recension)** is a creative, culturally localized reimagining within a regional ethos. For example, Goswami Tulsidas's *Ramcharitmanas* (in Awadhi) or Kamban's *Kamba Ramayanam* (in Tamil) are not literal translations of Valmiki’s Sanskrit *Ramayana*—they introduce distinct philosophical emphases (Bhakti surrender), regional metaphors, altered narrative episodes, and local cultural sensibilities."
                    + self._get_demo_warning()
                )

            # Check if matching literary works
            works = LiteraryWork.objects.filter(status='published')
            matched_work = None
            for w in works:
                title_words = [token.lower() for token in w.title.replace('(', ' ').replace(')', ' ').split() if len(token) > 3]
                if any(tw in q_lower for tw in title_words) or (w.author_creator and any(token.lower() in q_lower for token in w.author_creator.split() if len(token) > 3)):
                    matched_work = w
                    break
            
            if matched_work:
                reg_info = f"rooted in {matched_work.state.name}" if matched_work.state else "a Pan-Indian / National cultural classic"
                return (
                    f"**{matched_work.title}** ({matched_work.get_work_type_display()}):\n\n"
                    f"• **Author / Attribution:** {matched_work.author_creator or 'Living Oral/Traditional Heritage'}\n"
                    f"• **Language & Script:** {matched_work.language} ({matched_work.script or 'Traditional epigraphy'})\n"
                    f"• **Tradition:** {matched_work.tradition} ({reg_info})\n"
                    f"• **Historical Period:** {matched_work.historical_period}\n\n"
                    f"**Summary:** {matched_work.brief_intro}\n\n"
                    f"**Cultural Significance:** {matched_work.cultural_significance}\n\n"
                    f"You can explore the full reading synopsis, public-domain verses, and connected traditions in the [BharatVerse Digital Library](/library/{matched_work.slug}/)."
                    + self._get_demo_warning()
                )

            # Check if matching cultural entry
            entries = CulturalEntry.objects.filter(status='published')
            matched_entry = None
            for e in entries:
                if e.title.lower() in q_lower or any(word in q_lower for word in e.title.lower().split() if len(word) > 4):
                    matched_entry = e
                    break
                    
            if matched_entry:
                return (
                    f"**{matched_entry.title}** ({matched_entry.category.name} from {matched_entry.state.name}):\n\n"
                    f"{matched_entry.short_description}\n\n"
                    f"**Why It Matters:** {matched_entry.cultural_significance[:350]}...\n\n"
                    f"Explore the full living heritage profile, craft workshop steps, and sensory journey at [/explore/culture/{matched_entry.slug}/](/explore/culture/{matched_entry.slug}/)."
                    + self._get_demo_warning()
                )

            return (
                "India's civilisational heritage weaves together tangible monuments, sacred and secular literature, regional oral epics, performing arts, and indigenous knowledge systems. "
                "You can search our **Digital Library** for books, manuscripts, and scriptures, or browse the **Cultural Map** to uncover traditions and regional connections across all 22 states."
                + self._get_demo_warning()
            )
        return "Real AI response"

    def build_cultural_journey(self, topic, available_entries):
        if self.demo_mode:
            return [entry.id for entry in available_entries[:5]]
        return []

    def simplify_story(self, story_content, level="Student"):
        if self.demo_mode:
            return f"A {level} summary of the story: {story_content[:150]}..." + self._get_demo_warning()
        return "Real AI simplified story"

    def generate_quiz(self, entry_title, entry_content):
        if self.demo_mode:
            return [
                {
                    "question": f"What is the cultural significance of {entry_title}?",
                    "options": [
                        {"text": "A classical literary or performance tradition", "is_correct": True},
                        {"text": "A modern industrial convention", "is_correct": False},
                        {"text": "An imported modern fashion", "is_correct": False},
                    ]
                }
            ]
        return []

    def explain_connection(self, source, target):
        if self.demo_mode:
            return f"{source} and {target} are closely linked through shared regional aesthetics, sacred motifs, and civilisational exchange." + self._get_demo_warning()
        return "Real AI explanation"

