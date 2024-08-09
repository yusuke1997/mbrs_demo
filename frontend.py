import streamlit as st
from mbrs import registry
from mbrs.decoders import get_decoder
from mbrs.metrics import get_metric
from dataclasses import dataclass, fields
from collections import defaultdict
from mbrs.metrics import Metric


def input_hyper_parameter(config_type):
    for field in fields(config_type.Config):
        field_name = field.name
        field_type = field.type
        if 'Optional' in field_type:
            field_type = field_type.replace('Optional[','')[:-1]

        if field_name in st.session_state.metric_configs[st.session_state.metric]:
            field_value = st.session_state.metric_configs[st.session_state.metric][field_name]
        else:
            field_value = getattr(config_type.Config, field_name, None)
        field_description = field.metadata.get("description", "")

        if field_type == 'bool':
            new_value = st.checkbox(field_name, value=field_value)
        elif field_type == 'int':
            new_value = st.number_input(field_name, value=field_value)
        elif field_type == 'float':
            new_value = st.number_input(field_name, value=float(field_value) if field_value is not None else 0.0)
        elif field_type == 'str':
            new_value = st.text_input(field_name, value=field_value)
        elif field_type == 'list[int]':
            list_str = st.text_input(field_name)
            try:
                new_value = [int(x.strip()) for x in list_str.split(",") if x.strip()]
            except ValueError:
                st.error(f"Invalid input for {field_name}. Please enter a comma-separated list of integers.")
                new_value = field_value
        else:
            st.write('missing value')
            st.write(field_type)
            new_value = None

        if issubclass(config_type, Metric):
            st.session_state.metric_configs[st.session_state.metric][field_name] = new_value
        else:
            st.session_state.decoder_configs[st.session_state.decoder][field_name] = new_value


def execute(SOURCE, HYPOTHESES):
    metric_type = get_metric(st.session_state.metric)
    metric_cfg = metric_type.Config(
        **st.session_state.metric_configs[st.session_state.metric]
    )
    metric = metric_type(metric_cfg)

    decoder_type = get_decoder(st.session_state.decoder)
    decoder_cfg = decoder_type.Config()
    decoder = decoder_type(decoder_cfg, metric)

    #SOURCE = "ありがとう"
    #HYPOTHESES = ["Thanks", "Thank you", "Thank you so much", "Thank you.", "thank you"]
    output = decoder.decode(HYPOTHESES, HYPOTHESES, source=SOURCE, nbest=len(HYPOTHESES))

    return output

def main():
    st.title('mbrs demo')
    a = registry.get_registry("decoder").keys()
    #st.write(a)


    # mbrの設定についての記載
    if "decoder" not in st.session_state:
        st.session_state.decoder = "mbr"
        st.session_state.decoder_configs = defaultdict(dict)
        #st.session_state.disabled = False
    if "metric" not in st.session_state:
        st.session_state.metric = "bleu"
        st.session_state.metric_configs = defaultdict(dict)

    st.divider()

    # ここはmetricsに関する記述箇所
    col1, col2 = st.columns(2)

    with col1:
        st.write('### Metric Name')
        option = st.selectbox(
            "Choose the metric",
            registry.get_registry("metric").keys(),
            key='metric'
        )
        #st.session_state.decoder = option
        
        #st.checkbox("Disable selectbox widget", key="disabled")
        
    with col2:
        st.write('### hyper parameter')
        metric_type = get_metric(st.session_state.metric)
        #st.write(decoder_type.Config)
        input_hyper_parameter(metric_type)

    st.divider()

    # ここから、decoderに関する情報
    col3, col4 = st.columns(2)

    with col3:
        st.write('### Decoder Name')
        option = st.selectbox(
            "Choose the mbr decoding method",
            registry.get_registry("decoder").keys(),
            key='decoder'
        )

    with col4:
        st.write('### hyper parameter')
        decoder_type = get_decoder(st.session_state.decoder)
        #st.write(decoder_type.Config)                                                                                                       
        input_hyper_parameter(decoder_type)

    st.divider()
    

    #use_file_upload = st.checkbox('Use file upload instead of text input')
    use_file_upload = False
    source = []
    hypothesis = []
    reference = []
    
    if use_file_upload:
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file1 = st.file_uploader("Upload File 1")
        with col2:
            uploaded_file2 = st.file_uploader("Upload File 2")
        if use_file_upload and st.checkbox('Add third file upload'):
            col3 = st.columns(1)
            with col3[0]:
                uploaded_file3 = st.file_uploader("Upload File 3")
    else:
        if 'comet' not in st.session_state.metric:
            col2 = st.columns(1)
            source = []
            with col2[0]:
                hypothesis = st.text_area("hypothesis").split('\n')
        else:
            col1, col2 = st.columns(2)
            with col1:
                source = st.text_area("source")
            with col2:
                hypothesis = st.text_area("hypothesis").split('\n')
                
        if st.session_state.metric != 'cometkiwi' and st.checkbox('Add reference'):
            col3 = st.columns(1)
            with col3[0]:
                reference = st.text_area("reference").split('\n')

    if st.button('Submit'):
        # ここでエラー定義。GPUは使わない
        if st.session_state.metric in ['bleurt', 'comet', 'cometkiwi', 'xcomet']:
            st.divider()
            st.warning('This demo site is not supprt embedding base metrics. Please install via `pip install mbrs`.', icon="⚠️")
        elif len(hypothesis) >32:
            st.divider()
            st.warning('This demo site is up to 32 hypotheses due to computational resources. Please install via `pip install mbrs`.', icon="⚠️")
        else:
            st.divider()
            #st.write('push')
            #st.write(st.session_state.metric_configs[st.session_state.metric])
            #st.write(st.session_state.metric_configs)
            #st.write(st.session_state.decoder_configs)
            a = execute(source, hypothesis)
            st.write(a)
            st.write('ID: ', str(a.idx[0]))
            st.write('Result: ', a.sentence[0])
            st.write('Score:', a.score[0])
            
if __name__ == "__main__":
    main()
