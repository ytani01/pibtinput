# pibt

Python library for bluetooth


##


## ペアリング

### 順序が重要: trust -> pair -> connect

``` bash
sudo bluetoothctl

scan on
# MAC_ADDR 確認
scan off
trust MAC_ADDR
pair MAC_ADDR
connect MAC_ADDR
```


### 動作確認

``` bash
ls /dev/input

sudo evtest
:
```


##
