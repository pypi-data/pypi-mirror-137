# audio-evaluator 
audio-evaluator is a simple, easy-to-use wrapper for performing Automatic Speech Recognition with PyTorch. 

It is being used as a supporting package for Earudite, a trivia game, to evaluate recording quality relative to a transcript.

### Installation:
As a package, you can install using [PyPI](https://pypi.org/project/audio-evaluator/):

`pip install audio-evaluator`

Alternatively, simply copy `setup.py` and install the packages (**with the correct versions**) in `requirements.txt`

### Example usage:
```py
from audioevaluator import evaluator as AUDIO_EVAL

FILENAME = 'frankenstein.wav' # path to file
TRANSCRIPT = 'frankenstein' # original transcript to compare to the ASR output

print(AUDIO_EVAL.evaluate_audio(FILENAME, TRANSCRIPT))
```