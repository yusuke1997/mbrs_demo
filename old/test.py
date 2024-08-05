from mbrs.metrics import MetricChrF
from mbrs.decoders import DecoderMBR
print('aaaaa')
SOURCE = "ありがとう"
HYPOTHESES = ["Thanks", "Thank you", "Thank you so much", "Thank you.", "thank you"]


metric = MetricChrF(MetricChrF.Config())

# Setup MBR decoding.
decoder_cfg = DecoderMBR.Config()
decoder = DecoderMBR(decoder_cfg, metric)

print('aa')
# Decode by COMET-MBR.
# This example regards the hypotheses themselves as the pseudo-references.
# Args: (hypotheses, pseudo-references, source)
output = decoder.decode(HYPOTHESES, HYPOTHESES, source=SOURCE, nbest=1)

print(f"Selected index: {output.idx}")
print(f"Output sentence: {output.sentence}")
print(f"Expected score: {output.score}")
print(output)
