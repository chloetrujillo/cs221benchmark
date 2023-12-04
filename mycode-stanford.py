from explorecourses import *
from explorecourses import filters
import nltk
import string
from nltk.corpus import stopwords  # Add this line to import stopwords
nltk.download('stopwords')  # This line downloads the 'stopwords' resource
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
from collections import Counter
print(1)
connect = CourseConnection()

import csv

header = ['Department', 'Title', 'Subtitle', 'Description', 'ID']

years = []
x = 2001
while x < 2024:
    value = str(x) + "-" + str(x+1)
    x = x+2
    years.append(value)
print(years)

def remove_parentheses(s):
    result = ""
    skip = 0
    for i in range(len(s)):
        if s[i] == "(":
            skip = 1
        elif s[i] == ")":
            skip = 0
        elif skip == 0:
            result += s[i]
    return result

# Use NLTK stopwords
stopwords = set(stopwords.words('english'))

recentmajors = [
    'Athletics and Club Sports (ATHLETIC)',
    'Kinesiology (KIN)',
    'Outdoor Education (OUTDOOR)',
    'Physical Wellness (PHYSWELL)',
    'Earth Systems (EARTHSYS)',
    'Energy Science and Engineering (ENERGY)',
    'Environment and Resources (ENVRES)',
    'Earth and Planetary Sciences (EPS)',
    'Earth System Science (ESS)',
    'Oceans (OCEANS)',
    'Geophysics (GEOPHYS)',
    'Sustainability (SUSTAIN)',
    'Sustainability Science and Practice (SUST)',
    'Accounting (ACCT)',
    'Action Learning Programs (ALP)',
    'Business General Pathways (BUSGEN)',
    'Economic Analysis & Policy (MGTECON)',
    'Finance (FINANCE)',
    'GSB General & Interdisciplinary (GSBGEN)',
    'GSB Interdisciplinary (GSBGID)',
    'Human Resource Management (HRMGT)',
    'Marketing (MKTG)',
    'Operations Information & Technology (OIT)',
    'Organizational Behavior (OB)',
    'Political Economics (POLECON)',
    'Strategic Management (STRAMGT)',
    'Education (EDUC)',
    'Aeronautics & Astronautics (AA)',
    'Bioengineering (BIOE)',
    'Chemical Engineering (CHEMENG)',
    'Civil & Environmental Engineering (CEE)',
    'Computational & Mathematical Engineering (CME)',
    'Computer Science (CS)',
    'Design (DESIGN)',
    'Design Institute (DESINST)',
    'Electrical Engineering (EE)',
    'Engineering (ENGR)',
    'Management Science & Engineering (MS&E)',
    'Materials Science & Engineer (MATSCI)',
    'Mechanical Engineering (ME)',
    'Scientific Computing & Comput\'l Math (SCCM)',
    'African & African American Studies (AFRICAAM)',
    'African & Middle Eastern Languages (AMELANG)',
    'African Studies (AFRICAST)',
    'American Studies (AMSTUD)',
    'Anthropology (ANTHRO)',
    'Applied Physics (APPPHYS)',
    'Arabic Language (ARABLANG)',
    'Archaeology (ARCHLGY)',
    'Art History (ARTHIST)',
    'Arts Institute (ARTSINST)',
    'Art Studio (ARTSTUDI)',
    'Asian American Studies (ASNAMST)',
    'Asian Languages (ASNLANG)',
    'Biology (BIO)',
    'Biology/Hopkins Marine (BIOHOPK)',
    'Biophysics (BIOPHYS)',
    'Catalan Language Courses (CATLANG)',
    'Chemistry (CHEM)',
    'Chicana/o-Latina/o Studies (CHILATST)',
    'Chinese (CHINA)',
    'Chinese Language (CHINLANG)',
    'Classics (CLASSICS)',
    'Communication (COMM)',
    'Comparative Literature (COMPLIT)',
    'Comparative Studies in Race & Ethnicity (CSRE)',
    'Dance (DANCE)',
    'Data Science (DATASCI)',
    'Division of Literatures, Cultures, & Languages (DLCL)',
    'Drama (TAPS)',
    'East Asian Languages & Cultures (EALC)',
    'East Asian Studies (EASTASN)',
    'Economics (ECON)',
    'English (ENGLISH)',
    'English for Foreign Students (EFSLANG)',
    'Ethics in Society (ETHICSOC)',
    'Feminist, Gender and Sexuality Studies (FEMGEN)',
    'Film Production (FILMPROD)',
    'Film and Media Studies (FILMEDIA)',
    'French Language (FRENLANG)',
    'French Studies (FRENCH)',
    'German Language (GERLANG)',
    'German Studies (GERMAN)',
    'Global Studies (GLOBAL)',
    'History (HISTORY)',
    'History & Philosophy of Science (HPS)',
    'Human Biology (HUMBIO)',
    'Human Rights (HUMRTS)',
    'Humanities Core (HUMCORE)',
    'Humanities & Sciences (HUMSCI)',
    'Iberian & Latin American Cultures (ILAC)',
    'Institute for International Studies (FSI) (IIS)',
    'International Policy (INTLPOL)',
    'International Relations (INTNLREL)',
    'Italian Language (ITALLANG)',
    'Italian Studies (ITALIAN)',
    'Japanese (JAPAN)',
    'Japanese Language (JAPANLNG)',
    'Jewish Studies (JEWISHST)',
    'Korean (KOREA)',
    'Korean Language (KORLANG)',
    'Latin American Studies (LATINAM)',
    'Linguistics (LINGUIST)',
    'Master of Liberal Arts (MLA)',
    'Mathematical & Computational Science (MCS)',
    'Mathematics (MATH)',
    'Medieval Studies (MEDVLST)',
    'Modern Thought & Literature (MTL)',
    'Music (MUSIC)',
    'Native American Studies (NATIVEAM)',
    'Philosophy (PHIL)',
    'Physics (PHYSICS)',
    'Political Science (POLISCI)',
    'Portuguese Language (PORTLANG)',
    'Psychology (PSYCH)',
    'Public Policy (PUBLPOL)',
    'Religious Studies (RELIGST)',
    'Russian, East European, & Eurasian Studies (REES)',
    'Science, Technology, & Society (STS)',
    'Slavic Language (SLAVLANG)',
    'Slavic Studies (SLAVIC)',
    'Sociology (SOC)',
    'Spanish Language (SPANLANG)',
    'Spanish, Portuguese, & Catalan Literature (ILAC)',
    'Special Language Program (SPECLANG)',
    'Stanford in Washington (SIW)',
    'Statistics (STATS)',
    'Symbolic Systems (SYMSYS)',
    'Theater and Performance Studies (TAPS)',
    'Tibetan Language (TIBETLNG)',
    'Urban Studies (URBANST)',
    'Law (LAW)',
    'Law, Nonprofessional (LAWGEN)',
    'Anesthesia (ANES)',
    'Biochemistry (BIOC)',
    'Biomedical Data Science (BIODS)',
    'Biomedical Informatics (BIOMEDIN)',
    'Biomedical Physics (BMP)',
    'Biosciences Interdisciplinary (BIOS)',
    'Cancer Biology (CBIO)',
    'Cardiothoracic Surgery (CTS)',
    'Chemical & Systems Biology (CSB)',
    'Community Health and Prevention Research (CHPR)',
    'Comparative Medicine (COMPMED)',
    'Dermatology (DERM)',
    'Developmental Biology (DBIO)',
    'Emergency Medicine (EMED)',
    'Epidemiology (EPI)',
    'Family and Community Medicine (FAMMED)',
    'Genetics (GENE)',
    'Health Research & Policy (HRP)',
    'Immunology (IMMUNOL)',
    'Leadership Innovations (LEAD)',
    'Lifeworks (LIFE)',
    'Medicine (MED)',
    'Medicine Interdisciplinary (INDE)',
    'Microbiology & Immunology (MI)',
    'Molecular & Cellular Physiology (MCP)',
    'Neurobiology (NBIO)',
    'Neurology & Neurological Sciences (NENS)',
    'Neurosciences Program (NEPR)',
    'Neurosurgery (NSUR)',
    'Obstetrics & Gynecology (OBGYN)',
    'Ophthalmology (OPHT)',
    'Orthopedic Surgery (ORTHO)',
    'Otolaryngology (OTOHNS)',
    'Pathology (PATH)',
    'Pediatrics (PEDS)',
    'Physician Assistant Studies (PAS)',
    'Psychiatry (PSYC)',
    'Radiation Oncology (RADO)',
    'Radiology (RAD)',
    'School of Medicine General (SOMGEN)',
    'Stem Cell Biology and Regenerative Medicine (STEMREM)',
    'Structural Biology (SBIO)',
    'Surgery (SURG)',
    'Urology (UROL)',
    'Wellness Education (WELLNESS)',
    'Center for Teaching and Learning (CTL)',
    'Civic, Liberal, and Global Education (COLLEGE)',
    'Education as Self-Fashioning (ESF)',
    'Immersion in the Arts (ITALIC)',
    'Online Bridge Course (SOAR)',
    'Oral Communications (ORALCOMM)',
    'Overseas Studies General (OSPGEN)',
    'Overseas Studies in Australia (OSPAUSTL)',
    'Overseas Studies in Barcelona (CASB) (OSPBARCL)',
    'Overseas Studies in Beijing (OSPBEIJ)',
    'Overseas Studies in Berlin (OSPBER)',
    'Overseas Studies in Cape Town (OSPCPTWN)',
    'Overseas Studies in Florence (OSPFLOR)',
    'Overseas Studies in Hong Kong (OSPHONGK)',
    'Overseas Studies in Istanbul (OSPISTAN)',
    'Overseas Studies in Kyoto (OSPKYOTO)',
    'Overseas Studies in Kyoto (KCJS) (OSPKYOCT)',
    'Overseas Studies in Madrid (OSPMADRD)',
    'Overseas Studies in Oxford (OSPOXFRD)',
    'Overseas Studies in Paris (OSPPARIS)',
    'Overseas Studies in Santiago (OSPSANTG)',
    'Residential Programs (RESPROG)',
    'ROTC Air Force (ROTCAF)',
    'ROTC Army (ROTCARMY)',
    'ROTC Navy (ROTCNAVY)',
    'Stanford in New York (SINY)',
    'Structured Liberal Education (SLE)',
    'Thinking Matters (THINK)',
    'Undergraduate Advising and Research (UAR)',
    'Writing & Rhetoric, Program in (PWR)',
    'Teaching and Learning (VPTL)'
]

recentmajors = set(recentmajors)

with open('majorkeywords.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for year in years:
        print(year)
        for school in connect.get_schools(year):
            for dept in school.departments:
                if str(dept) in recentmajors:
                    try:
                        # Create a Counter to count words for each department-year combination
                        word_count = Counter()

                        courses = connect.get_courses_by_department(dept.code, year=year)
                        for course in courses:
                            if course.description != "":
                                try:
                                    # Remove parentheses from course description
                                    description = remove_parentheses(course.description)
                                    # Tokenize the description into words
                                    words = nltk.word_tokenize(description)
                                    # Lemmatize the words
                                    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stopwords and word not in string.punctuation]
                                    # Update the word count for the department-year combination
                                    word_count.update(words)
                                except Exception as e:
                                    print(f"Error processing course description: {e}")

                        # Write the top 10 words and their counts for each department-year combination
                        top_words_counts = [(word, count) for word, count in word_count.most_common(100)]
                        writer.writerow([school, dept.code, year] + [word for word, count in top_words_counts])

                    except Exception as e:
                        print(f"Error processing {dept.code} - {year}: {e}")



#with open('coursedescriptions2003.csv', 'w', encoding='UTF8', newline='') as f:
 #   writer = csv.writer(f)
#    writer.writerow(header)
#    year = years[1]
 #   for school in connect.get_schools(year):
 #       for dept in school.departments:
#            if str(dept) in recentmajors:
#                try:
#                   courses = connect.get_courses_by_department(dept.code, year=year)
 #                   for course in courses:
 #                       if course.description != "":
                            # Remove parentheses from course description
 #                           description = remove_parentheses(course.description)
                            # Tokenize the description into words
 #                           words = nltk.word_tokenize(description)
                            # Remove stopwords
  #                          words = [word.lower() for word in words if word.lower() not in stopwords and word not in string.punctuation]
  #                          writer.writerow([school, dept.code, year] + words)

 #               except Exception as e:
 #                   print(f"Error processing {dept.code} - {year}: {e}")