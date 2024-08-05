from mbrs import registry, timer
from mbrs.decoders import get_decoder
from mbrs.metrics import get_metric


print(registry.get_registry("decoder").keys())
print(registry.get_registry("metric").keys())
