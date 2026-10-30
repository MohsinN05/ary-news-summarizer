
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize_article(text, sentence_count=5):
    if not text or len(text.split()) < 30:
        return text

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LexRankSummarizer()

    summary_sentences = summarizer(
        parser.document,
        sentence_count
    )

    summary = " ".join(
        str(sentence)
        for sentence in summary_sentences
    )

    return summary if summary else text
