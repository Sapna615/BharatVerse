import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bharatverse.settings')
django.setup()

from quizzes.models import Quiz, Question, QuizOption

def add_q(quiz, text, options_list, correct_idx):
    q = Question.objects.create(quiz=quiz, question_text=text, order=quiz.questions.count()+1)
    for i, opt in enumerate(options_list):
        QuizOption.objects.create(question=q, option_text=opt, is_correct=(i==correct_idx))

# Match the region
quiz = Quiz.objects.filter(slug='match-region-demo').first()
if quiz:
    add_q(quiz, 'Which state is famous for the Backwaters?', ['Kerala', 'Goa', 'Tamil Nadu', 'Karnataka'], 0)
    add_q(quiz, 'Where is the Hawa Mahal located?', ['Delhi', 'Jaipur', 'Agra', 'Lucknow'], 1)
    add_q(quiz, 'Which region is known for the Chhau dance?', ['Eastern India', 'Western India', 'Southern India', 'Northern India'], 0)
    add_q(quiz, 'The Hornbill Festival is celebrated in which state?', ['Assam', 'Nagaland', 'Manipur', 'Mizoram'], 1)
    add_q(quiz, 'Which state is known as the Land of Five Rivers?', ['Punjab', 'Haryana', 'Uttar Pradesh', 'Gujarat'], 0)
    add_q(quiz, 'Where is the Sun Temple located?', ['Konark, Odisha', 'Modhera, Gujarat', 'Martand, Kashmir', 'All of the above'], 3)
    add_q(quiz, 'Which state is famous for Madhubani art?', ['Bihar', 'Jharkhand', 'West Bengal', 'Odisha'], 0)

# Guess the dance form
quiz = Quiz.objects.filter(slug='guess-dance-demo').first()
if quiz:
    add_q(quiz, 'Which dance is characterized by intricate footwork and spins, originating in Northern India?', ['Kathak', 'Bharatanatyam', 'Odissi', 'Manipuri'], 0)
    add_q(quiz, 'Which classical dance originates from Kerala and uses elaborate facial makeup?', ['Kathakali', 'Mohiniyattam', 'Kuchipudi', 'Sattriya'], 0)
    add_q(quiz, 'Which folk dance from Gujarat is performed in a circle using sticks?', ['Garba', 'Dandiya Raas', 'Bhavai', 'Tippani'], 1)
    add_q(quiz, 'Which dance form is synonymous with the Bihu festival of Assam?', ['Bihu Dance', 'Bhortal Dance', 'Sattriya', 'Ojapali'], 0)
    add_q(quiz, 'Which classical dance is associated with the temples of Tamil Nadu?', ['Bharatanatyam', 'Kuchipudi', 'Kathakali', 'Odissi'], 0)
    add_q(quiz, 'Which martial dance form originates from Odisha, Jharkhand, and West Bengal?', ['Chhau', 'Ghumura', 'Sambalpuri', 'Gotipua'], 0)
    add_q(quiz, 'Which dance form is dedicated to Lord Jagannath?', ['Odissi', 'Manipuri', 'Kathak', 'Bharatanatyam'], 0)

# Identify the instrument
quiz = Quiz.objects.filter(slug='sound-india-demo').first()
if quiz:
    add_q(quiz, 'Which stringed instrument is Ravi Shankar famously associated with?', ['Sitar', 'Sarod', 'Veena', 'Santoor'], 0)
    add_q(quiz, 'Which wind instrument is synonymous with classical artist Hariprasad Chaurasia?', ['Bansuri', 'Shehnai', 'Nadaswaram', 'Harmonium'], 0)
    add_q(quiz, 'Which double-headed drum is essential in Carnatic music?', ['Mridangam', 'Tabla', 'Pakhawaj', 'Dholak'], 0)
    add_q(quiz, 'Which instrument consists of a pair of hand drums (bayan and dayan)?', ['Tabla', 'Mridangam', 'Dhol', 'Duff'], 0)
    add_q(quiz, 'Which stringed instrument is played with a bow and is a staple in Hindustani classical music?', ['Sarangi', 'Esraj', 'Dilruba', 'Violin'], 0)
    add_q(quiz, 'Which instrument is known as the "hundred-stringed lute" from Kashmir?', ['Santoor', 'Rabab', 'Surbahar', 'Sitar'], 0)
    add_q(quiz, 'Which instrument is a small reed organ introduced by Europeans but adopted by Indian classical music?', ['Harmonium', 'Accordion', 'Shruti Box', 'Piano'], 0)

print("Quiz questions added successfully.")
