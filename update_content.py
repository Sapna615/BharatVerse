import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from culture.models import CulturalEntry, State

# Update Entries
entries = CulturalEntry.objects.all()
for e in entries:
    if 'Dance' in e.title:
        e.short_description = f"The {e.title} is a mesmerizing performing art that captures the vibrant spirit and rhythm of {e.state.name}. Known for its high energy and intricate footwork."
        e.detailed_story = f"Historically, this dance form originated in the rural heartlands of {e.state.name} as a celebration of the harvest season. Over centuries, it evolved from simple village gatherings to highly choreographed performances that tell epic tales of love, valor, and mythology. The performers wear dazzling traditional attire, often hand-woven and heavily embroidered with mirrors and threads that catch the light as they spin."
        e.cultural_significance = f"This dance is far more than entertainment; it is the heartbeat of {e.state.name}'s cultural identity. It serves as a medium to pass down oral histories from one generation to the next, fostering a deep sense of community and shared heritage."
        e.practice_description = f"Practiced in large circular formations or synchronized rows, the dance is accompanied by traditional percussion instruments like the Dhol and melodic instruments like the Flute or Sarangi. It takes years of rigorous practice to master the complex rhythms."
    elif 'Craft' in e.title:
        e.short_description = f"The {e.title} represents centuries of artisanal excellence, showcasing the delicate handiwork and indigenous materials of {e.state.name}."
        e.detailed_story = f"Rooted in the ancient artisan guilds of {e.state.name}, this craft has been passed down through families for generations. Artisans spend weeks, sometimes months, meticulously carving, weaving, or painting these masterpieces. Each motif and pattern tells a story of the local flora, fauna, and spiritual beliefs."
        e.cultural_significance = f"Economically and spiritually, this craft sustains entire villages. It is a symbol of resilience, preserving traditional knowledge in the face of modern mass production. Many of these artifacts are used in sacred rituals and weddings."
        e.practice_description = f"The process begins with the careful sourcing of raw, natural materials—be it clay, silk, wood, or natural dyes. Artisans use primitive but highly specialized hand tools, relying on muscle memory and inherited techniques to shape the final product."
    elif 'Music' in e.title:
        e.short_description = f"The enchanting melodies of {e.title} evoke the soulful landscapes and timeless traditions of {e.state.name}."
        e.detailed_story = f"This musical tradition traces its roots to the royal courts and Sufi shrines of {e.state.name}. It is characterized by its complex raga structures and emotionally charged lyrical poetry. Historically, these songs were sung to invoke the rains, celebrate the birth of a child, or express the yearning of the soul for the divine."
        e.cultural_significance = f"Music here is a spiritual discipline. It breaks down social barriers, bringing together people of different backgrounds in a shared experience of transcendence and joy."
        e.practice_description = f"Musicians undergo the rigorous 'Guru-Shishya' (teacher-student) tradition. Performances are highly improvisational, usually starting with a slow, meditative 'alap' and gradually building to a fast-paced, ecstatic climax."
    
    e.save()
    print(f"Updated {e.title}")

print("Successfully enriched all cultural entries!")
