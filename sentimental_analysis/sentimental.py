import json
import sys
sys.path.insert(0, './')

from pyspark.ml import Pipeline 
import pyspark.sql.functions as F
import sparknlp
from sparknlp.annotator import * 
from sparknlp.base import *
from pyspark.sql.types import StringType

from message_broker.consumers import MessageConsumers


started = False




class SentimentalAnalysis:

    @classmethod
    def main(cls, ch,method,properties,body):
        print("RECEIVING PAYLOAD . . . . . . . . . . . . . ")
        json_body = json.loads(body)
        text_list = []
        for text_ in json_body['video_comments']:
            text_list.append(text_['text'])

        cls.analyse_comments(text_list)
    
    @classmethod
    def analyse_comments(cls, text_list):
        spark = sparknlp.start()
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
        print(result)

        result.select(F.explode(F.arrays_zip(result.document.result, result.class_.result)).alias("cols")).select(F.expr("cols['0']").alias("chunk"), F.expr("cols['1']").alias('result')).show(truncate=False)
        # spark.stop()




MessageConsumers.consume_messages(queue_name='sentiment-queue', callback_function=SentimentalAnalysis.main)

