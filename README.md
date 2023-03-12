# news_predict
  
**step1 :** git clone https://github.com/phawitb/news_predict.git  
  
**step2 : install library**  
  pip3 install gdown  
  pip3 install transformers  
  pip install torchvision  
  pip3 install emoji  
  
gdown  4.6.0  
transformers  4.26.0  
torchvision  0.14.1  
emoji  2.2.0  
mysql-connector  2.2.9  
mysql-connector-python   8.0.29  
  
**step3 : loadmodels**  
python3 load_models.py  
  
**step4 : edit path,batch_size in config.py**  
  
**step5 : set cron job**  
which python3 >> /usr/bin/python3   
  
crontab -e  
#ทำงานเวลา 22.00น. ในทุกๆวัน  
MAILTO="phawit.boo@gmail.com"  
0 22 * * * /usr/bin/python3 /home/agentai/phawit/news_predict/predict_sever.py >> /home/agentai/phawit/log/news_predict.log 2>&1  
  
crontab -l  
  
/etc/init.d/cron start  
#sudo service cron reload
  
  
**model** >> https://drive.google.com/drive/folders/1rsmgf633meVZNNip_PJwFJRECPu0whMz  
  
-------------------------------------------------------------  

**login sever**  
ssh [username sever]@[ip sever]  
  
**sever**  
sudo su  
nc -nlvp 443  
nc -nlvp 80  
nc -nlvp 8080  

nc -nlvp 8080 > 1.zip  

**local**  
nc -nv [ip sever] 8080  
nc -nv [ip sever] 8080 < wisesight_sentiment_wangchanberta_useful-20230119T042521Z-001.zip  


