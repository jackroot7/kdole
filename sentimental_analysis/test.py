import pandas as pd
import numpy as np
import json

from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import sparknlp
from sparknlp.annotator import * 
from sparknlp.base import *
from sparknlp.pretrained import PretrainedPipeline
from pyspark.sql.types import StringType, IntegerType


spark = sparknlp.start()
print ("Spark NLP Version :", sparknlp.version())
spark

text_list=[
    """Tukio bora katika sinema ilikuwa wakati Gerardo anajaribu kupata wimbo ambao unaendelea kupitia kichwa chake.""",
    """Ni dharau kwa akili ya mtu na upotezaji mkubwa wa pesa""",
    """Kris Kristoffersen ni mzuri kwenye sinema hii na kweli hufanya tofauti.""",
    """Hadithi yenyewe ni ya kutabirika tu na ya uvivu.""",
    """Ninapendekeza hizi kwa kuwa zinaonekana nzuri sana, kifahari na nzuri""",
    """Safaricom si muache kucheza na mkopo wa nambari yangu tafadhali. mnanifilisisha😓😓😯""",
    """Bidhaa ilikuwa bora na inafanya kazi vizuri kuliko ya verizon na bei ilikuwa rahisi """,
    """Siwezi kuona jinsi sinema hii inavyoweza kuwa msukumo kwa mtu yeyote kushinda woga na kukataliwa.""",
    """Asante sana kwa mapokezi mazuri � Mungu awabariki awalinde awajalie afya njema watu wote wa Tanzania. Watu wengi nchini Poland hawapendi kinachoendela nchini  yetu, ndiyo maana hatutaki vita dhidi Urusi. Ni muhimu kutenganisha serikali na raia wa kawaida.""",
    "KAZI IENDELEE"
]

# Define the paths where your models are saved
model_path = "path/to/your/models"

document_assembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
normalizer = Normalizer().setInputCols(["token"]).setOutputCol("normalized")
stopwords_cleaner = StopWordsCleaner.load("/home/jackroot7/Videos/OpenSourced/kdole/sentimental_analysis/stopwords").setInputCols(["normalized"]).setOutputCol("cleanTokens").setCaseSensitive(False)
embeddings = XlmRoBertaEmbeddings.load("/home/jackroot7/Videos/OpenSourced/kdole/sentimental_analysis/xlm_roberta_base_finetuned_swahili_sw").setInputCols(["document", "cleanTokens"]).setOutputCol("embeddings")
embeddingsSentence = SentenceEmbeddings().setInputCols(["document", "embeddings"]).setOutputCol("sentence_embeddings").setPoolingStrategy("AVERAGE")
sentimentClassifier = ClassifierDLModel.load("/home/jackroot7/Videos/OpenSourced/kdole/sentimental_analysis/classifierdl_xlm_roberta_sentiment_sw").setInputCols(["sentence_embeddings"]).setOutputCol("class_")

sw_pipeline = Pipeline(stages=[document_assembler, tokenizer, normalizer, stopwords_cleaner, embeddings, embeddingsSentence, sentimentClassifier])

df = spark.createDataFrame(text_list, StringType()).toDF("text")
result = sw_pipeline.fit(df).transform(df)

result.select(F.explode(F.arrays_zip(result.document.result, result.class_.result)).alias("cols")).select(F.expr("cols['0']").alias("chunk"), F.expr("cols['1']").alias('result')).show(truncate=False)
