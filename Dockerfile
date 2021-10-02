# Credits 
FROM naytseyd/sedenbot:latest

# Maintainer
MAINTAINER 

# Zaman dilimini ayarla
ENV TZ=Europe/Istanbul

# Çalışma dizini
ENV PATH="/root/sedenuser/bin:$PATH"
WORKDIR /root/sedenuser

# Repoyu klonla
RUN 

# Oturum ve yapılandırmayı kopyala (varsa)
COPY 

# Botu çalıştır
CMD ["python3","Eage.py"]
