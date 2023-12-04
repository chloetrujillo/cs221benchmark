import csv
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('stopwords')


## Used to tokenize the course descriptions
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

stopwords = set(stopwords.words('english'))
def tokenize_description(description):
    # Remove parentheses from course description
    description = remove_parentheses(description)
    # Tokenize the description into words
    words = nltk.word_tokenize(description)
    # Remove stopwords
    words = [word.lower() for word in words if word.lower() not in stopwords and word not in string.punctuation]
    return words


## Used to calculate the similarity between two sets of words
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union if union != 0 else 0
    return similarity

def compute_similarity(row1, row2):
    # Assuming columns after the first three contain the words
    set1 = set(row1[3:])
    set2 = set(row2[3:])
    similarity = jaccard_similarity(set1, set2)
    return similarity


## Used to narrow down the years and departments we sampled from. These list all the departments/majors that still exist in 2023, and the sampled years span every other year since 2001.
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
majorcodes = ['ATHLETIC', 'KIN', 'OUTDOOR', 'PHYSWELL', 'EARTHSYS', 'ENERGY', 'ENVRES', 'EPS', 'ESS', 'OCEANS', 'GEOPHYS', 'SUSTAIN', 'SUST', 'ACCT', 'ALP', 'BUSGEN', 'MGTECON', 'FINANCE', 'GSBGEN', 'GSBGID', 'HRMGT', 'MKTG', 'OIT', 'OB', 'POLECON', 'STRAMGT', 'EDUC', 'AA', 'BIOE', 'CHEMENG', 'CEE', 'CME', 'CS', 'DESIGN', 'DESINST', 'EE', 'ENGR', 'MS&E', 'MATSCI', 'ME', 'SCCM', 'AFRICAAM', 'AMELANG', 'AFRICAST', 'AMSTUD', 'ANTHRO', 'APPPHYS', 'ARABLANG', 'ARCHLGY', 'ARTHIST', 'ARTSINST', 'ARTSTUDI', 'ASNAMST', 'ASNLANG', 'BIO', 'BIOHOPK', 'BIOPHYS', 'CATLANG', 'CHEM', 'CHILATST', 'CHINA', 'CHINLANG', 'CLASSICS', 'COMM', 'COMPLIT', 'CSRE', 'DANCE', 'DATASCI', 'DLCL', 'TAPS', 'EALC', 'EASTASN', 'ECON', 'ENGLISH', 'EFSLANG', 'ETHICSOC', 'FEMGEN', 'FILMPROD', 'FILMEDIA', 'FRENLANG', 'FRENCH', 'GERLANG', 'GERMAN', 'GLOBAL', 'HISTORY', 'HPS', 'HUMBIO', 'HUMRTS', 'HUMCORE', 'HUMSCI', 'ILAC', 'IIS', 'INTLPOL', 'INTNLREL', 'ITALLANG', 'ITALIAN', 'JAPAN', 'JAPANLNG', 'JEWISHST', 'KOREA', 'KORLANG', 'LATINAM', 'LINGUIST', 'MLA', 'MCS', 'MATH', 'MEDVLST', 'MTL', 'MUSIC', 'NATIVEAM', 'PHIL', 'PHYSICS', 'POLISCI', 'PORTLANG', 'PSYCH', 'PUBLPOL', 'RELIGST', 'REES', 'STS', 'SLAVLANG', 'SLAVIC', 'SOC', 'SPANLANG', 'ILAC', 'SPECLANG', 'SIW', 'STATS', 'SYMSYS', 'TAPS', 'TIBETLNG', 'URBANST', 'LAW', 'LAWGEN', 'ANES', 'BIOC', 'BIODS', 'BIOMEDIN', 'BMP', 'BIOS', 'CBIO', 'CTS', 'CSB', 'CHPR', 'COMPMED', 'DERM', 'DBIO', 'EMED', 'EPI', 'FAMMED', 'GENE', 'HRP', 'IMMUNOL', 'LEAD', 'LIFE', 'MED', 'INDE', 'MI', 'MCP', 'NBIO', 'NENS', 'NEPR', 'NSUR', 'OBGYN', 'OPHT', 'ORTHO', 'OTOHNS', 'PATH', 'PEDS', 'PAS', 'PSYC', 'RADO', 'RAD', 'SOMGEN', 'STEMREM', 'SBIO', 'SURG', 'UROL', 'WELLNESS', 'CTL', 'COLLEGE', 'ESF', 'ITALIC', 'SOAR', 'ORALCOMM', 'OSPGEN', 'OSPAUSTL', 'CASB', 'OSPBARCL', 'OSPBEIJ', 'OSPBER', 'OSPCPTWN', 'OSPFLOR', 'OSPHONGK', 'OSPISTAN', 'OSPKYOTO', 'OSPKYOCT', 'OSPMADRD', 'OSPOXFRD', 'OSPPARIS', 'OSPSANTG', 'RESPROG', 'ROTCAF', 'ROTCARMY', 'ROTCNAVY', 'SINY', 'SLE', 'THINK', 'UAR', 'PWR', 'VPTL']
year_options = ['2001-2002', '2003-2004', '2005-2006', '2007-2008', '2009-2010', '2011-2012', '2013-2014', '2015-2016', '2017-2018', '2019-2020', '2021-2022', '2023-2024']


## This funciton is the user inerface for our benchmark -- 
## In mode 1, users can provide a description and the program will classify the description based on the overlap in keywords between the user input and a dept/year's most common words (from the CSV)
## In mode 2, you acn enter two year,dept pairs and it will return the similarity between the most frequent words (specified in the CSV) for that tuple.
def main():
    # Read the CSV file
    with open('majorkeywords.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read the header

        # Create a dictionary to store word similarities and matched words for each row
        word_similarity_dict = {}

        mode = input("Type 1 to predict what department a given course description belongs to. Press 2 to compare the similarity of two given year-department combinations.")

        if mode == "1":
            # Ask the user to choose a year from the list
            user_year = input(f"Choose a year from the list {year_options}: ")

            # Ensure the user input is a valid year
            while user_year not in year_options:
                print("Invalid year. Please choose from the provided list.")
                user_year = input(f"Choose a year from the list {year_options}: ")

            try:
                # Tokenize the user's description into words
                user_words = nltk.word_tokenize(user_description)
                # Lemmatize the words
                user_words = [lemmatizer.lemmatize(word.lower()) for word in user_words if word.lower() not in stopwords and word not in string.punctuation]
                # Check if there are at least 2 words
                if len(user_words) < 2:
                    raise ValueError("Please enter a course description with at least 2 words.")
            except Exception as e:
                print(f"Error processing user description: {e}")
            # Iterate through the rows in the CSV
            for row in reader:
                # Check if the row's year matches the user's input
                if row[2] == user_year:
                    # Assuming that columns from 3 onwards contain the tokenized words
                    row_words = row[3:14]

                    # Calculate word similarity by finding common words
                    common_words = set(user_words).intersection(row_words)
                    similarity = len(common_words)

                    # Store the similarity and matched words in the dictionary
                    key = row[0] + ", " + row[1]  # school (column 1) + ", " + dept (column 2)
                    word_similarity_dict[key] = {"similarity": similarity, "common_words": common_words}

            # Find the top 3 matches
            top_matches = sorted(word_similarity_dict.items(), key=lambda x: x[1]["similarity"], reverse=True)[:3]

            # Display the results
            if top_matches:
                print(f"\nTop 3 Matches for {user_year}:\n")
                for match in top_matches:
                    print(f"{match[0]} - Word Similarity: {match[1]['similarity']}")
                    print("Common Words:", ', '.join(match[1]['common_words']))
                    print("\n")
            else:
                print(f"\nNo matches found for {user_year}.")

        if mode == "2":

            print(f"\n \n You will be asked to choose two year-department combinations to compare.  \n \n \n These are the years you can choose from: \n\n {year_options}.  \n \n \n These are the departments you can choose from: \n\n  {recentmajors} \n \n")
            # Ask the user to choose a year from the list
            user_year1 = input("What is the year of your comparison? ")
            while user_year1 not in year_options:
                print("Invalid year. Please choose from the provided list.")
                user_year1 = input("What is the year of your comparison? ")

            user_dept1 = input("What is the code of the first department in your comparison? If the department is Symbolic Systems (SYMSYS), just type SYMSYS: ")
            while user_dept1 not in majorcodes:
                print("Invalid code. Please choose from the provided list.")
                user_dept1 = input("What is the code of the first department in your comparison? If the department is Symbolic Systems (SYMSYS), just type SYMSYS: ")

            user_dept2 = input("What is the code of the second department in your comparison? If the department is Symbolic Systems (SYMSYS), just type SYMSYS: ")
            while user_dept2 not in majorcodes:
                print("What is the code of the second department in your comparison? If the department is Symbolic Systems (SYMSYS), just type SYMSYS: ")
                user_dept2 = input("What is the code of the second department in your comparison? ")


                    # Find the rows corresponding to user's choices
            rows = []
            f.seek(0)  # Reset file pointer to the beginning
            next(reader)  # Skip header
            for row in reader:
                if (row[2] == user_year1 and row[1] == user_dept1) or (row[2] == user_year1 and row[1] == user_dept2):
                    rows.append(row)

            # Compute similarity
            similarity = compute_similarity(rows[0], rows[1])

            print(f"The similarity between {user_dept1} in {user_year1} and {user_dept2} in {user_year1} is: {similarity}")





if __name__ == "__main__":
    main()
