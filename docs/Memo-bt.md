# Bluetooth関係のMemo


## == Bluetoothイベントにより、コマンドの自動実行


### === edev

以下のコマンドで、イベント時のメッセージや情報を確認
``` bash
udevadm monitor --property

udevadm info -a -n /dev/input/event
```

ルールを設定

e.g. ``/etc/udev/rules.d/99-8BitDo.rules``
``` text
ACTION=="add", SUBSYSTEM=="input", ATTRS{name}=="8BitDo Micro gamepad Keyboard" SYMLINK+="input/8bitdo.kbd"
ACTION=="add", SUBSYSTEM=="input", ATTRS{name}=="8BitDo Micro gamepad" SYMLINK+="input/8bitdo.js"
```

ルールを反映

``` bash
sudo udevadm control --reload-rules
# sudo udevadm trigger
```

### === Triggerhappy

/etc/triggerhappy/triggers.d/foo.conf
``` text
KEY_ENTER 1  /.../command
```

``` bash
sudo systemctl restart triggerhappy
```
