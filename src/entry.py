from data import PhoneticData

class PronDictEntry:
    """
    Contains information on a pronunciation dict entry and methods to manipulate it
    The initialisation of a PronDictEntry object takes a word string and its transcription as parameters, as well
    as a reference transcript, e.g. containing syllabified or stress labeled transcript of "word".
    """

    def __init__(self, word="", transcription="", reference=""):
        """

        :param word: a dictionary entry (ex: "dag")
        :param transcription: transcription of "word", with the phones space separated (ex: "t a: G")
        :param reference: a reference transcript, can also be a syllabified or stress labeled string

        """
        self.word = word
        self.transcript = transcription.strip()
        self.transcription_arr = self.transcript.split()
        self.transcript_variants = set()
        self.transcript_variants.add(self.transcript)
        self.gpos = "nil"  # guessed part-of-speech
        # transcript, syllabification or stress labeled reference string for testing
        self.reference_transcr = reference
        self.syllables = []
        self.compound_elements = []
        self.entailing_compounds = [] # compounds where this word is one part
        self.frequency = 0

    def __str__(self):
        return self.word + "\t" + self.gpos + "\t" + self.transcript + "\t" + str(self.syllables)

    def __repr__(self):
        return self.__str__()

    def simplify_compound_variants(self):
        tmp_variants = self.transcript_variants
        self.transcript_variants = set()
        orig_transcript = self.transcript
        no_postaspir = orig_transcript.replace("_h", "")
        self.transcript_variants.add(orig_transcript)
        for t in tmp_variants:
            if t.replace(":", "") == orig_transcript or orig_transcript.replace(":", "") == t:
                continue
            elif t == no_postaspir:
                continue
            elif t.replace(":", "") == no_postaspir or no_postaspir.replace(":", "") == t:
                continue
            else:
                self.transcript_variants.add(t)

    def update_syllables(self, ind, prev_syll, syll):
        self.syllables[ind - 1] = prev_syll
        self.syllables[ind] = syll

    def cmu_format_syllables(self):
        formatted_string = "("
        for syll in self.syllables:
            formatted_string += "((" + syll.content + ") " + str(syll.stress) + ") "

        return formatted_string.strip() + ")"

    def cmu_format(self):
        return "("" + self.word + "" " + self.gpos + " " + self.cmu_format_syllables() + ")"

    def dot_format_syllables(self):
        sylls = ""
        for syll in self.syllables:
            sylls += syll.content.strip() + "."
        sylls = sylls[0:-1]
        return sylls

    def syllable_format(self):
        return self.word + " - " + self.dot_format_syllables()

    def stress_format(self):
        sylls = ""
        for syll in self.syllables:
            stressed_phones = []
            phones = syll.content.strip().split()
            for p in phones:
                if p in PhonDict.get_alphabet().vowels:
                    p = p + str(syll.stress)
                stressed_phones.append(p)

            sylls += " ".join(stressed_phones) + " "

        return sylls.strip()

    def simple_stress_format(self):
        return self.stress_format()


class PhonDict:

    alphabet = None

    @staticmethod
    def get_alphabet():
        if None == PhonDict.alphabet:
            PhonDict.alphabet = PhoneticData()
        return PhonDict.alphabet
