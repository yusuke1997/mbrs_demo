import streamlit as st
import epitran
import json
import pandas as pd
import Levenshtein
import pykakasi
import os
import httpx

@st.cache(allow_output_mutation=True)
def load_epitran(model: str):
    epi = epitran.Epitran(model)
    return epi


def calc_score(ipa, gold):
    score = []
    for i,j, in zip(ipa,gold):
        if j is not None:
            score.append(Levenshtein.distance(i, j))
        else:
            score.append(None)
    return score

def convert(kks,text):
    result = kks.convert(text)
    return ''.join([item['kana'] for item in result])

class Epitran:

    def __init__(self, local = False):

        self.local = local
        if local:
            self.epi = {}
            self.epi['jpn_Ktkn'] = load_epitran('jpn_Ktkn')
            self.epi['jpn-Ktkn-red'] = load_epitran('jpn-Ktkn-red')
            self.epi['jpn_Ktkn_without_post'] = load_epitran('jpn_Ktkn_without_post')
            self.epi['jpn-Ktkn-red_without_post'] = load_epitran('jpn-Ktkn-red_without_post')
            
    def transliterate(self,s,text):
        
        if self.local:
            return epi[s].transliterate(text)
        else:
            response = httpx.get('http://localhost:8091/get?model={}&text={}'.format(s,text))
            try:
                return json.loads(response.content)['result']
            except:
                return ''

def Abracadabra():
    st.set_page_config(
        page_title="Japanese G2P",
        page_icon="random",
        #layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        f'''
        <style>
        .sidebar .sidebar-content {{
        width: 375px;
        }}
        </style>
        ''',
        unsafe_allow_html=True
    )

    hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    
def main():

    Abracadabra()
    
    st.title('カタカナからIPAへの変換ツール')
    texts = st.text_area('カタカナを入力してください。IPAに変換した結果を出力します。\nもし評価用データセットに含まれているカタカナならスコアも出力します。\nカタカナ以外にも対応していますがpykakasiで変換しているだけなので了承ください。ローマ字などは対象外。改行で複数変換可能。',height = 300)

    
    #epi = {}
    #epi['jpn_Ktkn'] = load_epitran('jpn_Ktkn')
    #epi['jpn-Ktkn-red'] = load_epitran('jpn-Ktkn-red')
    #epi['jpn_Ktkn_without_post'] = load_epitran('jpn_Ktkn_without_post')
    #epi['jpn-Ktkn-red_without_post'] = load_epitran('jpn-Ktkn-red_without_post')

    epi = Epitran()
    
    kks = pykakasi.kakasi()
    
    select = st.multiselect("デモとして出力したい変換ツールを選択してください",['jpn_Ktkn','jpn-Ktkn-red','jpn_Ktkn_without_post','jpn-Ktkn-red_without_post'],['jpn_Ktkn'])
    is_calc_score = st.checkbox('スコアを表示する')

    
    with open('./rule_kana_to_ipa/scripts/proc_jpn_kana_narrow.json') as f:
        data = json.load(f)

    st.sidebar.write('# 評価用データセット一覧')

    if os.path.exists('index_data.pickle'):
        all_data = pd.read_pickle('index_data.pickle')
        search_index_list = st.sidebar.multiselect('絞り込み用', all_data.columns[1:])
    else:
        with open('./rule_kana_to_ipa/scripts/analyzed_wordlist.json') as f:
            wrong_data = json.load(f)
    
        #st.sidebar.dataframe(pd.DataFrame(data.keys()))
        df_wrong_data = pd.DataFrame(wrong_data).T
        df_correct_data = pd.DataFrame([True]*len(set(data) - set(df_wrong_data.index)),list(set(data) - set(df_wrong_data.index)),['correct'])
        #df_correct_data = df_correct_data.set_index(
        #st.sidebar.write(df_correct_data)
        all_data = pd.concat([df_correct_data,df_wrong_data]).fillna(False)
        search_index_list = st.sidebar.multiselect('絞り込み用', all_data.columns)
        all_data['Levenshtein'] = all_data.index.map(lambda name: Levenshtein.distance(epi['jpn_Ktkn'].transliterate(name), data[name]))
        all_data = all_data.reindex(columns=['Levenshtein','correct']+list(df_wrong_data.columns))
        pd.to_pickle(all_data, 'index_data.pickle')
    
    disp_data = all_data
    for index in search_index_list:
        disp_data = disp_data[(disp_data[index] == True)]
    st.sidebar.dataframe(disp_data.sort_index(),height = 500)
    
    if not select:
        st.error("少なくとも１つは変換ツールを選択してください")

    else:
        text_list = texts.split('\n')
        st.write('## 出力結果')
        epi_ipa_list = {'original':text_list}
        text_list = [convert(kks,text) for text in text_list]
        if is_calc_score:
            gold_list = []
            for text in text_list:
                if text in data:
                    gold_list.append(data[text])
                else:
                    gold_list.append(None)
            epi_ipa_list['gold'] = gold_list
        for s in select:
            ipa_list = []
            for text in text_list:
                ipa_list.append(epi.transliterate(s,text))
            epi_ipa_list[s] = ipa_list
            if is_calc_score:
                score = calc_score(ipa_list, epi_ipa_list['gold'])
                epi_ipa_list['{}-score'.format(s)] = score

        df = pd.DataFrame(epi_ipa_list)
        st.table(df.fillna(''))


        
if __name__ == "__main__":
    main()
