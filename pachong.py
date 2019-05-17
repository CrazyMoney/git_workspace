import  requests
import  pymysql
import pickle
def getOnepage():
    header = {"User-Agent" : " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    global r
    r  = requests.get("https://maoyan.com/board")

    print(r)
    print(r.text)
getOnepage()
output = open ("movie.pkl","wb")
pickle.dump(r,output)
output.close()



