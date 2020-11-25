# PlatformIO CLI

- 自动拉取 Platformio-core；
- 自动检查 Plafomio-core 是否更新；
- 自动更新 platformio-core；
- 自动测试 platformio 功能， 进行工程的创建，编译测试；
- 自动打包。

## boards list：

```shell
platformio boards --json-output
```

- --json-output: 以 json 格式输出

  ```shell
      {
          "id": "nucleo_f072rb",
          "name": "ST Nucleo F072RB",
          "platform": "ststm32",
          "mcu": "STM32F072RBT6",
          "fcpu": 48000000,
          "ram": 16384,
          "rom": 131072,
          "frameworks": [
              "arduino",
              "cmsis",
              "mbed",
              "stm32cube",
              "libopencm3"
          ],
          "vendor": "ST",
          "url": "https://developer.mbed.org/platforms/ST-Nucleo-F072RB/",
          "connectivity": [
              "can"
          ],
          "debug": {
              "tools": {
                  "blackmagic": {},
                  "jlink": {},
                  "stlink": {
                      "onboard": true,
                      "default": true
                  }
              }
          }
      },
  ```

## Init Project：

```shell
platformio init --board nucleo_h743zi --ide=eclipse --project-option framework=cmsis --project-dir test
```

- **-b, --board** : board ID
- **--ide** ：IDE
- **-O, --project-option** ： custom `platformio.ini` file
- **-d, --project-dir** ：project path

## Build  Project

```shell
platformio -f -c eclipse run
```

## Clean  Project

```shell
platformio -f -c eclipse run --target clean
```

## Upload  Project

```shell
platformio -f -c eclipse run --target upload
```

## Debug Project

```shell
platformio -f -c eclipse debug --interface=gdb -x .pioinit
```

- **--interface=gdb** : start GDB 