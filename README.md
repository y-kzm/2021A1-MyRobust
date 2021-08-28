# SecCamp2021[A-8] ロバチャン.

---
## My Robust Protocol.
Yokoo Kazuma  
2021_08_27  

---
## Ready. 
~~~
### Taro. ###
$ ./ready.sh
~~~

---
## Usage. 
~~~
### Hanako. ###
$ ./yokoo/robust/hanako.py

### Taro. ###
$ timeout 120 ./yokoo/robust/taro.py
~~~

---
## Check. 
~~~
### Hanako. ###
./cmp.py
~~~

---
## Memo.
* server.py と client.py は、ただファイルデータをフラグメントしてUDP上で送信するだけのプログラム  
* hanako.py と taro.py は上記にACKを加えたプログラム  
  > フラグメントしたパケットを１つ１つ、相手が受け取ったことを確認してから次のパケットを送っているのでめちゃめちゃ効率悪い...  

