#uvicorn api:app --reload
#uvicorn ファイル名:FastAPI()の名前 --reload
from fastapi import FastAPI
from typing import Optional
import uvicorn
from starlette.middleware.cors import CORSMiddleware # 追加
from starlette.requests import Request
from fastapi import FastAPI, Form

from mbrs.decoders import get_decoder
from mbrs.metrics import get_metric


app = FastAPI(title="mbrs")

# Nikkeiの人から教えてもらったcorsのセッティング
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#mbrs-decode \
#  hypotheses.txt \
#  --num_candidates 1024 \
#  --nbest 1 \
#  --source sources.txt \
#  --references hypotheses.txt \
#  --output translations.txt \
#  --report report.txt --report_format rounded_outline \
#  --decoder mbr \
#  --metric comet \
#  --metric.model Unbabel/wmt22-comet-da \
#  --metric.batch_size 64 --metric.fp16 true

@app.get("/get")
async def mbrs_line(hypothesis: str,
                    source: str,
                    reference: Optional[List[str]] = None,
                    nbest: int = 1,
                    decoder: str = 'mbr',
                    metric: str = 'bleu',
                    decoder_config: dict = None,
                    metric_config: dict = None:
):
    # cliのdecode.pyからコピペ
    metric_type = get_metric(metric)
    metric: Metric = metric_type(metric)
    
    decoder_type = get_decoder(decoder)
    decoder: DecoderReferenceBased | DecoderReferenceless = decoder_type(
        decoder, metric
    )

    
    print(model,text)
    tgt = epi[model].transliterate(text)
    return {'result':tgt}


@app.get("/post")
async def mbrs_file(model: Optional[str] = 'jpn_Ktkn',text: Optional[str] = None):
    print(model,text)
    tgt = epi[model].transliterate(text)
    return {'result':tgt}


if __name__ == "__main__":
    #uvicorn.run(app, host="localhost", port=8091)
    pass
