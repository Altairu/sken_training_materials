# [**AltairMD_V7**](https://github.com/Altairu/AltairMD_V7)


![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

https://github.com/Altairu/AltairMD_V7

---
### **仕様**

* 30V~10V(フォトカプラを変更すると10V以下も可)
* 最大40A 

|SDs|Ps1|Ps2|出力|
|:----:|:----:|:----:|:----:|
|HIGH|LOW	|LOW	|停止|
|HIGH|LOW	|HIGH	|逆転|
|HIGH|HIGH	|LOW	|正転|
|HIGH|HIGH	|HIGH	|`ブレーキ`（非推奨）|
|LOW|X	|X	|0|

### **降圧**

![alt text](image-3.png)

![alt text](image-4.png)

### **三端子レギュレーター** 
### **[NJM7812SDL1]()**

* **12Vに降圧**
* **端子が3つ(入力・グラウンド・出力）**
* **三端子レギュレータは落とした分の電圧をすべて`熱`として消費**
* **ダイオード**
レギュレータに逆電流が流れるのを防止
* **コンデンサ**
コンデンサは入力側と出力側に0.1～10[uF]程度入れるのが一般的


## **フォトカプラ**

![alt text](image-5.png)

### [TLP152](https://akizukidenshi.com/catalog/g/g110824/)

* 取り付け様式:	SMD/SMT	
* パッケージ/ケース:SOIC-6
* 電源電圧min.：10V
* 電源電圧max.：30V
* 出力電流：2A
* 入力電流max.：20mA
* 上昇応答時間：95ns
* 下降応答時間：110ns


## **MOSFET**
[**RSJ400N10**](https://www.rohm.co.jp/products/mosfets/small-signal/single-nch/rsj400n10-product)
Nch 100V 40A Power MOSFET

![alt text](image-6.png)

* 4V駆動タイプ
* Nチャンネル　パワーMOSFET
* 高速スイッチング
* 駆動回路が簡単
* 並列使用が容易

ゲート抵抗は10[Ω]で設定している

### **ハーフブリッジゲートドライバ**
### [**IR2302STRPBF**](https://akizukidenshi.com/catalog/g/g115656/)

![alt text](image-7.png)

![alt text](image-8.png)

* IN端子
ハイサイドMOSFETをONにするか、ローサイドMOSFETをONにするかの切り替えを行う
Hが入力されるとハイサイド、Lが入力されるとローサイドがONとなる
**ハイサイドにNchMOSFETを使うためにブーストラップ回路を使用**
* ブートストラップコンデンサの容量は[10uF]
* ブートストラップダイオード
(ファストリカバリダイオード)
* `100％出力は不可`
ブートストラップ回路の制約で
コンデンサのチャージ時間が必要.

# Ｈブリッジ回路

![alt text](image-9.png)


| Ps1 | Ps2 | Q1  | Q2  | Q3  | Q4  | 1    | 2    | 
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | 
| L   | L   | H   | L   | H   | L   | open | open | 
| L   | H   | H   | H   | L   | L   | L    | H    | 
| H   | L   | L   | L   | H   | H   | H    | L    | 
| H   | H   | H   | H   | H   | H   | L    | L    | 

