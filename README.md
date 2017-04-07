# Tensorflow java MNIST demo

This project aims to give a tutorial training a MNIST model in python, reading it in java, verifying that you can use it in both languages with the same result.

## Prerequisites

To run this example you need the following.

* [Python](https://www.python.org/downloads)
* [Maven](https://maven.apache.org/install.html)
* Tensorflow >=1.0.1
* tensorflow_jni >=1.0.1
* libtensorflow.jar >=1.0.1

## Building tensorflow

As of me writing this the current version of tensorflow is 1.0.0-PREVIEW1, this version is missing the feature SavedModelBundle which makes the setup much easier. By running only one save you get a dir with a full model. So you could modify this demo to use the preview but building tensorflow in Linux or Mac are not that hard.


### Building tensorflow

Tensorflow uses the build system bazel, a install description could be found at [Building bazel](https://bazel.build/versions/master/docs/install.html) or following the steps below. (Tested on ubuntu trusty)

```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install bazel
sudo apt-get upgrade bazel
```

### Building tensorflow pip package

The easiest way to install tensorflow is with a pip package. To build your own package and install follow instructions at [Building tenserflow](https://www.tensorflow.org/install/install_sources) or the description below.

#### Fetch tensorflow source
```
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
```

#### Build tensorflow
```
sudo pip install six numpy wheel
bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
sudo pip install /tmp/tensorflow_pkg/tensorflow-1.0.1-py2-none-any.whl
```

### Building tensorflow java bindings (jni and jar)

Last but not least we need the java bindings, these can be built by following the description at [Building tenserflow jar](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/java) or the operations below.

#### Fetch tensorflow source
If you haven't done so already you need to fetch the source from github in order to build java bindings. Follow instructions below.
```
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
```

#### Build bindings
```
sudo apt-get install python swig python-numpy
./configure
bazel build --config opt //tensorflow/java:tensorflow //tensorflow/java:libtensorflow_jni
```
The JAR (libtensorflow.jar) and native library (libtensorflow_jni.so) will be in bazel-bin/tensorflow/java.

Copy the .so file to the jni directory in this project so ```./run.sh``` can find it. And install the jar in maven your repository by following the description below.


#### Install built jar in maven repo

After we built the bindings we can install them in our local maven repository with

```
mvn org.apache.maven.plugins:maven-install-plugin:2.5.2:install-file
  -Dfile=libtensorflow.jar
  -DgroupId=org.tensorflow
  -DartifactId=libtensorflow
  -Dversion=1.1.0-MINE
  -Dpackaging=jar
  -DgeneratePom=true
```

### Running this repo
Training can be done with ```python mnist_train.py``` in the project directory.

Verifying with java we can build the project with ```mvn package``` and run it with ```./run.sh``` in the project directory. This script will run the project jar with the jni binding library.

## (EXPERIMENTAL) Building tensorflow on Windows

We need to build Bazel because it has a bug in windows that requires the latest build.

```
Set-ExecutionPolicy Unrestricted
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install bazel
```

Start msys32
```
git clone https://github.com/google/protobuf.git
cd protobuf
git checkout v3.2.0
pacman -S unzip autoconf perl automake libtool gcc make
./autogen.sh
./configure
make
make check
sudo make install
```

```
git clone https://github.com/bazelbuild/bazel.git
```

Start msys32
```
export JAVA_HOME="$(ls -d C:/Program\ Files/Java/jdk* | sort | tail -n 1)"
export PATH=[Python Path]:[Bazel Path]:[VC Path]:$PATH
export BAZEL_SH=/usr/bin/bash.exe
export BAZEL_VS=[Visual Studio Path]
export BAZEL_PYTHON=[python.exe Path]
pacman -Syuu gcc git curl zip unzip zlib-devel
cd [Cloned bazel directory]
bazel build ///src:bazel
compile.sh
```

```
git clone https://github.com/tensorflow/tensorflow.git
git checkout r1.1
```

```
pip install numpy
export PYTHON_BIN_PATH=[python_exe_path]
export BAZEL_WRKDIR=c:/tempdir/shrtpath
export BAZEL_SH=c:/tools/msys64/usr/bin/bash.exe
export BAZEL_VS=[Visual Studio Path]
export BAZEL_PYTHON=[python.exe Path]
```

[Install uinst](http://www.nvidia.com/object/gpu-accelerated-applications-tensorflow-installation.html)
```
$ ./configure
Please specify the location of python. [Default is /usr/bin/python]: [enter]
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] n
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with GPU support? [y/N] y
GPU support will be enabled for TensorFlow
Please specify which gcc nvcc should use as the host compiler. [Default is /usr/bin/gcc]: [enter]
Please specify the Cuda SDK version you want to use, e.g. 7.0. [Leave empty to use system default]: 8.0
Please specify the location where CUDA 8.0 toolkit is installed. Refer to README.md for more details. [Default is /usr/local/cuda]: [enter]
Please specify the Cudnn version you want to use. [Leave empty to use system default]: 5
Please specify the location where cuDNN 5 library is installed. Refer to README.md for more details. [Default is /usr/local/cuda]: [enter]
[Default is: "3.5,5.2"]: 5.2,6.1
Setting up Cuda include
Setting up Cuda lib64
Setting up Cuda bin
Setting up Cuda nvvm
Setting up CUPTI include
Setting up CUPTI lib64
```

```
export BUILD_OPTS='--cpu=x64_windows_msvc --host_cpu=x64_windows_msvc --copt=/w --verbose_failures --experimental_ui'
bazel build -c opt $BUILD_OPTS tensorflow/tools/pip_package:build_pip_package
```

Copy all files from
c:\tempdir\shrtpath\temp\_bazel_woden\incXe-uU\execroot\tensorflow\ to bazel-bin\tensorflow\tools\pip_package\build_pip_package.runfiles\
```
bazel-bin/tensorflow/tools/pip_package/build_pip_package c:/tmp/tensorflow_pkg
pip install c:\tmp\tensorflow_pkg\tensorflow-1.1.0rc1-cp35-cp35m-win_amd64.whl
```

```
bazel build --config opt //tensorflow/java:tensorflow //tensorflow/java:libtensorflow_jni
```

copy libtensorflow_jni.so to tensorflow_jni.dll in your jni directory.

Windows 7 need Powershell 3.0
http://www.microsoft.com/en-us/download/details.aspx?id=34595
