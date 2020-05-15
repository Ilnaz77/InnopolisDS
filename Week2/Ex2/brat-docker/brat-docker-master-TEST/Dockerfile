# Базовый образ 
FROM ubuntu

# ЧТобы не ломалось тк спрашивает временной пояс
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Установка пакетов
RUN apt-get update
RUN apt-get install -y curl vim sudo wget rsync
RUN apt-get install -y apache2
RUN apt-get install -y python
RUN apt-get install -y supervisor


# Установка брата
RUN mkdir /var/www/ilnaz
RUN curl http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz > /var/www/ilnaz/brat-v1.3_Crunchy_Frog.tar.gz 
RUN cd /var/www/ilnaz && tar -xvzf brat-v1.3_Crunchy_Frog.tar.gz

# Создаем директорию data как описано на сайте и делаем его rwx для всех
RUN mkdir /var/www/ilnaz/brat-v1.3_Crunchy_Frog/data
RUN chmod 777 /var/www/ilnaz/brat-v1.3_Crunchy_Frog/data

# Создание обертки для запуска с ключами
ADD wrapper.sh /usr/bin/wrapper.sh
# Делаем файл исполняемым
RUN chmod +x /usr/bin/wrapper.sh 

# Допуск апачи
RUN chown -R www-data:www-data /var/www/ilnaz/brat-v1.3_Crunchy_Frog/
# Закинули конфиг в апачи файлы
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf

# CGI
RUN a2enmod cgi

# ПОРТ
EXPOSE 80

# https://riptutorial.com/ru/docker/example/14132/dockerfile-plus-supervisord-conf
RUN mkdir -p /var/log/supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf 
CMD ["/usr/bin/supervisord"]





