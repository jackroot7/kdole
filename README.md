RABITMQ
* Install erlang
* Install rabbitmq-server
* Enable rabbitmq-server as system program
* Start rabbitmq-server at backend
* Enable rabbitmq management plugin

[Source]: https://medium.com/analytics-vidhya/how-to-use-rabbitmq-with-python-e0ccfe7fa959#:~:text=Setting%20up%20rabbitmq%2Dserver&text=But%20first%20we%20need%20to,a%20system%20program%20at%20backend.&text=sudo%20rabbitmqctl%20set_permissions%20%2Dp%20%2F%20user,client%20called%20pika%20in%20python.



<!-- Script to start my servers  -->

1. Run Streamlit Dashboard. It give interface to submit channel ID `[ streamlit run app.py ]`
2. Run channel servic that will receive ID from dashboard and find list of videos `[ python extractors/channels.py ]`
3. Run videos main file to receive video informations `[ python extractors/main.py ]`
4. Run sentimental analysis service that will receive data from video service and perfom sentiment analysis `[ python sentimental_analysis/sentimental.py ]`
5. Run database service that receive will just receive data from multiple videos and save them.
