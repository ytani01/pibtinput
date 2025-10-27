# Bluetooth関係のMemo


## == Bluetoothイベントにより、コマンドの自動実行


### === edev

以下のコマンドで、イベント時の
``` bash
udevadm monitor --property
```

``/etc/udev/rules.d/99-foo.rules``にルールを設定
``` text
ACTION=="bind", SUBSYSTEM=="input", ATTRS{name}=="Bluetooth Keyboard", RUN+="/usr/local/bin/on_btkeyboard_connected.sh"
```

ルールを反映

``` bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### === Triggerhappy

/etc/triggerhappy/triggers.d/foo.conf
``` text
KEY_ENTER 1  /.../command
```

``` bash
sudo systemctl restart triggerhappy
```
