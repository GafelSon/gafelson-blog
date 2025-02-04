# views/utils/reading_time.py
import re

class ReadingTimeCalculator:
    """ Temporal estimation engine with HTML purification systems """
    
    _WORDS_PER_MIN = 200
    _HTML_TAG_REGEX = re.compile(r'<[^>]+>')
    
    @classmethod
    def calculate(cls, content: str) -> int:
        """ Compute reading duration with sanitization protocols"""
        clean_text = cls._HTML_TAG_REGEX.sub('', content)
        return max(1, round(len(clean_text.split()) / cls._WORDS_PER_MIN))
    
    @classmethod
    def words(cls, content: str) -> int:
        """ Compute words count in article """
        clean_text = cls._HTML_TAG_REGEX.sub('', content)
        return round(len(clean_text.split()))