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
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Установка брата
RUN mkdir -p /var/www/brat
RUN curl http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz > /var/www/brat/brat-v1.3_Crunchy_Frog.tar.gz 
RUN cd /var/www/brat && tar -xvzf brat-v1.3_Crunchy_Frog.tar.gz

# Создание data & work директории и свяжем их сточками монтирования локальных томов (volumes)
RUN mkdir /bratdata && mkdir /bratcfg
RUN chown -R www-data:www-data /bratdata /bratcfg 
RUN chmod o-rwx /bratdata /bratcfg
RUN ln -s /bratdata /var/www/brat/brat-v1.3_Crunchy_Frog/data
RUN ln -s /bratcfg /var/www/brat/brat-v1.3_Crunchy_Frog/cfg 

VOLUME /bratdata
VOLUME /bratcfg

# Создание обертки для запуска с ключами
ADD brat_install_wrapper.sh /usr/bin/brat_install_wrapper.sh
RUN chmod +x /usr/bin/brat_install_wrapper.sh

# Допуск апачи
RUN chown -R www-data:www-data /var/www/brat/brat-v1.3_Crunchy_Frog/
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf

# CGI
RUN a2enmod cgi

EXPOSE 80

# Мы не можем использовать apachectl в качестве точки входа, 
# потому что она запускает apache, а затем завершает работу, беря с собой ваш контейнер.
# Вместо этого используйте supervisor для мониторинга процесса apache (https://riptutorial.com/ru/docker/example/14132/dockerfile-plus-supervisord-conf)

RUN mkdir -p /var/log/supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf 
CMD ["/usr/bin/supervisord"]





