from mbrs.cli.decode import CommonArguments
from simple_parsing import ArgumentParser, choice, field, flag
from simple_parsing.wrappers import dataclass_wrapper
from argparse import FileType, Namespace
from mbrs.metrics import Metric, get_metric
from mbrs.decoders import (
    DecoderBase,
    DecoderReferenceBased,
    DecoderReferenceless,
    get_decoder,
)

def parse_args() -> Namespace:

    common_arguments = CommonArguments(num_candidates = 1, hypotheses = 'test')
    
    meta_parser = ArgumentParser(add_help=False)
    meta_parser.add_arguments(common_arguments, "common")
    known_args, _ = meta_parser.parse_known_args()
    metric_type = get_metric(known_args.common.metric)
    decoder_type = get_decoder(known_args.common.decoder)
    print('aaaa')
    parser = ArgumentParser(add_help=True)
    parser.add_arguments(common_arguments, "common")
    parser.add_arguments(metric_type.Config, "metric", prefix="metric.")
    parser.add_arguments(decoder_type.Config, "decoder", prefix="decoder.")
    return parser.parse_args()


## CommonArgumentsクラスのフィールドを表示
#for field_name, field_info in CommonArguments.__dataclass_fields__.items():
#    print(f"Field: {field_name}, Type: {field_info.type}, Default: {field_info.default}")


#args = parse_args()
#print(args)

print(get_decoder)
