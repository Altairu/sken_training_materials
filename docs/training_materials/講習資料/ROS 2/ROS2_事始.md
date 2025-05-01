# Ubuntu 22.04 LTSでのROS2 Humble Hawksbillのインストール手順
Ubuntu 22.04 LTS（Jammy Jellyfish）にROS2 Humble 機会があったのでメモしてたのを記事にしました。
一応説明すると、ROS2（Robot Operating System 2）は、ロボット開発のためのオープンソースフレームワーク

以下を持ってきました

[Ubuntu 22.04 LTSでのROS2 Humble Hawksbillのインストール手順](https://qiita.com/_Altair_/items/4b2fdae96dd8a94f55a4)

## 前提条件

まず、以下の前提条件を確認しといてや：

- Ubuntu 22.04 LTSがインストールされていること
- 管理者権限（sudo）があること

## インストール手順

### 1. パッケージの更新

まずは、システムのパッケージを最新の状態に更新に。

```bash
sudo apt update
sudo apt upgrade
```

### 2. ソースリストの追加

ROS2のパッケージをダウンロードするために、ソースリストを追加する必要がある。

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
```

### 3. ロケールの設定

ロケール（言語と地域設定）を適切に設定しとく。

```bash
sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### 4. aptリポジトリの追加

ROS2のaptリポジトリを追加する。

```bash
sudo apt install curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
```

### 5. ROS2 Humbleのインストール

ROS2 Humble Hawksbillをインストール。

```bash
sudo apt install ros-humble-desktop
```

### 6. 環境変数の設定

ROS2の環境変数を設定するために、`.bashrc`に追記。

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 7. colconのインストール

ビルドツールであるcolconをインストールする。

```bash
sudo apt install python3-colcon-common-extensions
```

### 8. 動作確認

最後に、ROS2が正しくインストールされているか確認するために、デモノードを実行

```bash
ros2 run demo_nodes_cpp talker
```

別のターミナルを開いて、リスナーを実行

```bash
ros2 run demo_nodes_cpp listener
```

### おわりに

これで、Ubuntu 22.04 LTSにROS2 Humble Hawksbillのインストールが完了したはず。
初めてUbuntu触ったときは色々戸惑ったけど慣れればいける。気がする…

??? Note
    著者:Shion Noguchi