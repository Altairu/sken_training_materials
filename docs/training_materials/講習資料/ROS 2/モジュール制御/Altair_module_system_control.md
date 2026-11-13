# Altair_module_system_control

[https://github.com/Altairu/Altair_module_system_control](https://github.com/Altairu/Altair_module_system_control)

Altair Module System の各モジュールを Windows 11 上の軽量ネイティブアプリケーションとして制御するための統合制御システムです。
Node.js や npm、ROS2 環境を必要とせず、Rust と Tauri v2 によってコンパイルされた単一の実行ファイル `altair_module_system_control.exe` で最新の Ethernet-CAN 変換基板および USB-to-CAN アダプタによる 100Hz 制御や、Blockly / Python による自動制御プログラムの実行が可能です。

## 特徴

* Rust と Tauri v2 によるネイティブ構成のため、npm や Node.js が不要で、Windows 11 標準の WebView2 上で高精細かつ省メモリに動作します。
* `self_update` クレートによる GitHub Releases 連携を内蔵しており、アプリ起動時に新バージョンを自動確認し、ワンクリックで最新版の `.exe` へ自己更新できます。
* Ethernet-CAN 基板および USB-to-CAN の両方に対応し、GUI上でワンクリックで切り替えと接続ができます。Ethernet-CAN 利用時は、全体の送信チャンネルだけでなくモジュールごとに CAN1 / CAN2 / 両方 を個別に指定できます。
* MDD、サーボ、電磁弁に加えて、DJI RoboMaster モーターの M3508 P19 / M2006 P36 / GM6020 に対応しています。電流 / 電圧指令、速度 PID、位置 PID のカスケード制御、多回転角度の積算とゼロ点リセットを行えます。
* モジュール構成を JSON プロファイルとして保存や切り替え、インポート、エクスポートが可能です。
* Google Blockly を用いたビジュアルプログラミングから Python コードを自動生成し、足回り運動学ブロックやゲームパッド連動、RoboMaster モーター制御ブロックを含む動作プログラムをそのまま実行できます。

## システム構成

```mermaid
flowchart LR
    UI["Tauri v2 Window (WebView2)"] <-->|"HTTP REST / WebSocket"| Server["Rust Backend (axum + tokio)"]
    Behavior["Python Behavior Process"] <-->|"WebSocket"| Server
    Server <-->|"self_update"| GH["GitHub Releases"]
    Server -->|"100Hz Control Loop"| MM["Rust Module Manager"]
    MM <-->|"TCP 20B TX / 60B RX"| EthBridge["Rust Ethernet-CAN Bridge"]
    MM <-->|"Serial slcan"| UsbBridge["Rust USB-CAN Bridge"]
    EthBridge <-->|"192.168.2.123:5000"| Board["LANtoCAN Board"]
    UsbBridge <-->|"USB Serial"| Slcan["USB-to-CAN Adapter"]
```

## インストール方法

初めて利用する場合は、Windows 向けのインストーラーを利用することで、必要なファイル一式とデスクトップショートカットを簡単にセットアップできます。

* GitHub Releases の最新リリースから `altair_module_system_control_setup.exe` をダウンロードします。
* ダウンロードしたインストーラーを実行します。管理者権限は不要で、そのままウィザードに従って進めるだけでインストールが完了します。
* デスクトップまたはスタートメニューに作成された `Altair_module_system_control` のショートカットから起動できます。
* アプリの更新は起動時に自動確認され、画面上のボタンから最新バージョンへそのまま更新できます。


![alt text](image-24.png)

altair_module_system_control_setup.exeを起動します

![alt text](image-25.png)

![alt text](image-26.png)


## 起動とビルド方法

ビルド済みの実行ファイルを直接起動する場合は、プロジェクトルートにある実行ファイルを実行します。

```powershell
.\altair_module_system_control.exe
```

ウィンドウを開かずにバックグラウンドのWebサーバーとして起動する場合は `--server` オプションを付与します。

```powershell
.\altair_module_system_control.exe --server
```

ソースコードからリリースビルドを行う場合は以下のコマンドを実行します。

```powershell
cargo build --release
```


## GitHub Actions による自動ビルドと自動アップデート

* `main` ブランチへコードをプッシュするか、`v2.0.1` のようなタグをプッシュすると、`.github/workflows/release.yml` の GitHub Actions が自動的に起動します。
* GitHub Actions 上でバージョン番号の自動採番、`Cargo.toml` と `tauri.conf.json` のバージョン同期、`cargo build --release` による Windows 用 `.exe` のビルド、そして GitHub Releases への公開までがすべて自動で実行されます。
* アプリ起動時には `self_update` クレートが GitHub リポジトリ `Altairu/Altair_module_system_control` の Releases を自動確認します。新しいバージョンが公開されている場合は左メニュー下部に更新ボタンが表示され、クリックすると最新バイナリをダウンロードして実行ファイルを自己更新します。

## 使い方

### Ethernet-CAN 基板での接続

* PCの有線LANアダプタに固定IPアドレスとして `192.168.2.100`、サブネットマスクとして `255.255.255.0` を設定します。
* 画面左側の Connection パネルで Ethernet タブを選択します。
* IPアドレスに `192.168.2.123`、ポート番号に `5000` が入力されていることを確認し、Connect ボタンを押します。

以下は私の設定例
![alt text](image-27.png)

### USB-to-CAN での接続

* 画面左側の Connection パネルで USB タブを選択します。
* 自動探索にチェックを入れるか、COMポートを選択して Connect ボタンを押します。

### モジュールの追加と CAN チャンネル設定

* Dashboard 画面で Add Module を押すと、種別ごとに次の初期値が入力されます。
  * MDD: 名前 `MDD1` / Base CAN ID `0x200`
  * Servo: 名前 `Servo1` / Base CAN ID `0x100`
  * Solenoid Valve: 名前 `SV1` / Base CAN ID `0x300`
  * RoboMaster: 名前 `RM1` / モーター ID `1`
* Ethernet-CAN 接続時は、左パネルの全体 CAN チャンネル設定に加えて、各モジュール設定で `全体設定に従う` / `CAN1` / `CAN2` / `両方` を個別に選択できます。

### RoboMaster モーター制御

* M3508 P19 / M2006 P36 / GM6020 に対応しており、同じ送信 CAN ID に属する複数モーターの指令値は自動で 8 バイトフレームに集約されます。
  * M3508 / M2006: モーター ID 1〜4 は `0x200`、ID 5〜8 は `0x1FF` で電流指令を送信し、`0x201`〜`0x208` で受信します。
  * GM6020: モーター ID 1〜4 は `0x1FF`、ID 5〜7 は `0x2FF` で電圧指令を送信し、`0x205`〜`0x20B` で受信します。
* 制御モードは `current` / `voltage` / `speed_pid` / `position_pid` の 4 種類を選択できます。PID ゲインの初期値は P のみ有効で、I と D は `0.0` です (`vel_kp=20.0`, `pos_kp=3.0`)。
* Python や Blockly からは `RobomasClient` の `set_target` / `set_current` / `set_voltage` / `set_speed` / `set_position` / `reset_zero` / `stop` / `get_feedback` を利用できます。

### モジュールの制御開始

* Dashboard 画面で各モジュールの制御モードや PID ゲインを設定します。
* 左パネルの Send Params & Start ボタンを押すと、各モジュールへパラメータと制御モードが送信され、制御ループが開始されます。
* 各モジュールカード上部の UI操作送信 トグルをONにすると、スライダーやボタンの操作がリアルタイムにハードウェアへ送信されます。
