from typing import Dict
import torch
import torchaudio
import jiwer


class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, ignore):
        super().__init__()
        self.labels = labels
        self.ignore = ignore

    def forward(self, emission: torch.Tensor) -> str:
        """
        Given a sequence emission over labels, get the best path string
        :param emission: Logit tensors. Shape `[num_seq, num_label]`.
        :return: the resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i not in self.ignore]
        return ''.join([self.labels[i] for i in indices])


class ASREngine:
    def __init__(self):
        torch.random.manual_seed(0)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # print(torch.__version__) # MAKE SURE 1.10.0
        # print(torchaudio.__version__) # MAKE SURE 0.10.0
        # print(device)

        self.bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
        self.model = self.bundle.get_model().to(self.device)

    def transcribe(self, SPEECH_FILE: str):
        """
        Performs ASR on SPEECH_FILE and returns the transcript
        :param SPEECH_FILE: path to the audio file to perform ASR on
        :return: string result of ASR
        """

        waveform, sample_rate = torchaudio.load(SPEECH_FILE)
        waveform = waveform.to(self.device)

        if sample_rate != self.bundle.sample_rate:
            waveform = torchaudio.functional.resample(
                waveform, sample_rate, self.bundle.sample_rate
            )

        with torch.inference_mode():
            features, _ = self.model.extract_features(waveform)

        with torch.inference_mode():
            emission, _ = self.model(waveform)

        decoder = GreedyCTCDecoder(
            labels=self.bundle.get_labels(), ignore=(0, 1, 2, 3),
        )
        transcript = decoder(emission[0])
        return transcript

ASREngine_instance = ASREngine()
def evaluate_audio(SPEECH_FILE: str, TRANSCRIPT: str) -> Dict[str,float]:
    """
    Evaluates the recording quality of an audio by comparing the ASR result to the original transcript
    :param SPEECH_FILE: string file path of the audio file
    :param TRANSCRIPT: original transcript
    :return: dictionary containing 3 fields: word error rate, match error rate, and word information lost
    """
    asr_transcript = ASREngine_instance.transcribe(SPEECH_FILE)
    asr_transcript = asr_transcript.replace('|', ' ')

    transformation = jiwer.Compose([
        jiwer.Strip(),
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.ReduceToListOfListOfWords(),
    ])

    wer = jiwer.wer(TRANSCRIPT, asr_transcript, truth_transform=transformation, hypothesis_transform=transformation)
    mer = jiwer.mer(TRANSCRIPT, asr_transcript, truth_transform=transformation, hypothesis_transform=transformation)
    wil = jiwer.wil(TRANSCRIPT, asr_transcript, truth_transform=transformation, hypothesis_transform=transformation)

    return {'wer': wer, 'mer': mer, 'wil': wil}