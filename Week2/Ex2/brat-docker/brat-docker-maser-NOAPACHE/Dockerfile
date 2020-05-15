from ubuntu
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN apt-get install -y curl vim sudo wget rsync
RUN apt-get update
RUN apt-get install -y python

RUN mkdir -p /var/www/ilnaz
#RUN curl http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz > /var/www/ilnaz/brat-v1.3_Crunchy_Frog.tar.gz 
#RUN cd /var/www/ilnaz && tar -xvzf brat-v1.3_Crunchy_Frog.tar.gz
COPY ./brat-v1.3_Crunchy_Frog /var/www/ilnaz/brat-v1.3_Crunchy_Frog

#RUN mkdir /var/www/ilnaz/brat-v1.3_Crunchy_Frog/data
#RUN chmod 777 /var/www/ilnaz/brat-v1.3_Crunchy_Frog/data

EXPOSE 80
WORKDIR /var/www/ilnaz/brat-v1.3_Crunchy_Frog

cmd ["python", "standalone.py"]
