"""
starter_preprocess.py
Starter code for text preprocessing - focus on the statistics, not the regex!

This is the same code you'll use in the main Shannon assignment next week.
"""

import re
import json
import requests
from typing import List, Dict, Tuple
from collections import Counter
import string


class TextPreprocessor:
    """Handles all the annoying text cleaning so you can focus on the fun stuff"""

    def __init__(self):
        # Gutenberg markers (these are common, add more if needed)
        self.gutenberg_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** END OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
            "<<THIS ELECTRONIC VERSION"
        ]

    def clean_gutenberg_text(self, raw_text: str) -> str:
        """Remove Project Gutenberg headers/footers"""
        lines = raw_text.split('\n')

        # Find start and end markers
        start_idx = 0
        end_idx = len(lines)

        for i, line in enumerate(lines):
            if any(marker in line for marker in self.gutenberg_markers[:4]):
                if "START" in line:
                    start_idx = i + 1
                elif "END" in line:
                    end_idx = i
                    break

        # Join the cleaned lines
        cleaned = '\n'.join(lines[start_idx:end_idx])

        # Remove excessive whitespace
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = re.sub(r' {2,}', ' ', cleaned)

        return cleaned.strip()

    def normalize_text(self, text: str, preserve_sentences: bool = True) -> str:
        """
        Normalize text while preserving sentence boundaries

        Args:
            text: Input text
            preserve_sentences: If True, keeps . ! ? for sentence detection
        """
        # Convert to lowercase
        text = text.lower()

        # Standardize quotes and dashes
        text = re.sub(r'[""]', '"', text)
        text = re.sub(r"['’]", "'", text)
        text = re.sub(r'—|–', '-', text)

        if preserve_sentences:
            # Keep sentence endings but remove other punctuation
            text = re.sub(r'[^\w\s.!?\'-]', ' ', text)
        else:
            # Remove all punctuation except apostrophes in contractions
            text = re.sub(r"(?<!\w)'(?!\w)|[^\w\s]", ' ', text)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def tokenize_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def tokenize_words(self, text: str) -> List[str]:
        """Split text into words"""
        text_for_words = re.sub(r'[.!?]', '', text)
        words = text_for_words.split()
        words = [w for w in words if w]
        return words

    def tokenize_chars(self, text: str, include_space: bool = True) -> List[str]:
        """Split text into characters"""
        if include_space:
            text = re.sub(r'\s+', ' ', text)
            return list(text)
        else:
            return [c for c in text if c != ' ']

    def get_sentence_lengths(self, sentences: List[str]) -> List[int]:
        """Get word count for each sentence"""
        return [len(self.tokenize_words(sent)) for sent in sentences]

    def fetch_from_url(self, url: str) -> str:
        """
        Fetch text content from a URL (especially Project Gutenberg)
        """
        if not url.lower().endswith(".txt"):
            raise ValueError("URL must point to a .txt file")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL: {e}")

    def get_text_statistics(self, text: str) -> Dict:
        """
        Calculate basic statistics about the text.
        Includes counts, averages, and top words.
        """
        words = self.tokenize_words(text)
        sentences = self.tokenize_sentences(text)

        if not words or not sentences:
            raise ValueError("Text must contain both words and sentences.")

        total_characters = len(text)
        total_words = len(words)
        total_sentences = len(sentences)
        avg_word_length = sum(len(w) for w in words) / total_words
        avg_sentence_length = total_words / total_sentences

        # Use Counter for most common words
        word_counts = Counter([w.lower() for w in words])
        most_common_words = word_counts.most_common(10)

        return {
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "most_common_words": most_common_words
        }

    def create_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        Create a simple extractive summary by returning the first N sentences
        """
        sentences = self.tokenize_sentences(text)
        if not sentences:
            return ""
        summary = " ".join(sentences[:num_sentences])
        return summary.strip()


class FrequencyAnalyzer:
    """Calculate n-gram frequencies from tokenized text"""

    def calculate_ngrams(self, tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
        """
        Calculate n-gram frequencies
        """
        if n == 1:
            return dict(Counter(tokens))

        ngrams = [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
        return dict(Counter(ngrams))

    def calculate_probabilities(self, ngram_counts: Dict, smoothing: float = 0.0) -> Dict:
        """
        Convert counts to probabilities
        """
        total = sum(ngram_counts.values()) + smoothing * len(ngram_counts)
        return {ngram: (count + smoothing) / total for ngram, count in ngram_counts.items()}

    def save_frequencies(self, frequencies: Dict, filename: str):
        """Save frequency dictionary to JSON file"""
        json_friendly = {}
        for key, value in frequencies.items():
            if isinstance(key, tuple):
                json_friendly['||'.join(key)] = value
            else:
                json_friendly[key] = value

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_friendly, f, indent=2, ensure_ascii=False)

    def load_frequencies(self, filename: str) -> Dict:
        """Load frequency dictionary from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        frequencies = {}
        for key, value in json_data.items():
            if '||' in key:
                frequencies[tuple(key.split('||'))] = value
            else:
                frequencies[key] = value

        return frequencies


# Example usage to test your setup
if __name__ == "__main__":
    sample_text = """
    This is a test. This is only a test!
    If this were a real emergency, you would be informed.
    """

    preprocessor = TextPreprocessor()
    analyzer = FrequencyAnalyzer()

    clean_text = preprocessor.normalize_text(sample_text)
    print(f"Cleaned text: {clean_text}\n")

    sentences = preprocessor.tokenize_sentences(clean_text)
    print(f"Sentences: {sentences}\n")

    words = preprocessor.tokenize_words(clean_text)
    print(f"Words: {words}\n")

    bigrams = analyzer.calculate_ngrams(words, 2)
    print(f"Word bigrams: {bigrams}\n")

    chars = preprocessor.tokenize_chars(clean_text)
    char_trigrams = analyzer.calculate_ngrams(chars, 3)
    print(
        f"Character trigrams (first 5): {dict(list(char_trigrams.items())[:5])}\n")

    stats = preprocessor.get_text_statistics(clean_text)
    print(f"Text statistics:\n{json.dumps(stats, indent=2)}\n")

    print("✅ All functions implemented and working!")
