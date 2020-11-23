# platformio_core_for_studio

>一个可发布的 platformio 最小包



## 1. 支持的平台：

+ win10 x64

## 2. 使用方法

1. 下载仓库到本地目录

2. （可选）添加仓库根目录到环境变量Path ，这样可以全局使用platformio 命令

   如果不执行此步骤，则需要使用据对路径调用

3. 根据 platformio core 的[文档](https://docs.platformio.org/en/latest/core/quickstart.html)使用 platformio

## 3. 发布步骤

1. 克隆仓库到本地
2. 删除piodebuggdb.py文件和platformio.py 文件
3. 将其他文件打包到 studio 安装包

## 4. 使用 Python 打包的步骤

1. 克隆仓库到本地
2. platformio 代码在platform_core/Lib 下，如果需要更新platformio，需要更新这里的库
3. 根据需要调整入口文件piodebuggdb.py文件和platformio.py
4. 执行 `pyinstaller -F  platformio.py` 打包生成 platformio.exe
5. 执行 `pyinstaller -F  piodebuggdb.py` 打包生成 piodebuggdb.exe

## 5. 使用 golang 打包的步骤

1. 克隆仓库到本地
2. platformio 代码在platform_core/Lib 下，如果需要更新platformio，需要更新这里的库
3. 根据需要调整入口文件 `golang_entrance\piodebuggdb\piodebuggdb.go` 文件和`golang_entrance\platformio\platformio.go`
4. 在 golang_entrance 目录下执行 `go build platformio\platformio.go` 打包生成 platformio.exe
5. 在 golang_entrance 目录下执行 `go build piodebuggdb\piodebuggdb.go` 打包生成 piodebuggdb.exe
6. 将生成的 exe 和 platformio_core 文件夹放在同级目录下运行

## 6. platformio 应用示例

​	参考[文档](https://git.rt-thread.com/realthread/ide_bug_report/uploads/5494f65d2f8358a480bd856890137006/%E5%88%9D%E6%AD%A5%E6%96%B9%E6%A1%881110.pdf)
