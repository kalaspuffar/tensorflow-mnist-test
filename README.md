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

Remove visual studio installations
https://github.com/Microsoft/VisualStudioUninstaller

### Download one of the below build tools
Download visual studio 2017
https://www.visualstudio.com/downloads/
MSBuild
https://www.microsoft.com/en-us/download/details.aspx?id=48159
Visual C++ Build Tools 2015
http://landinghub.visualstudio.com/visual-cpp-build-tools

### More required packages
Download python and install with the "Add python to environment variables" option.
https://www.python.org/

Download and install msys2.
http://www.msys2.org/

Download and install bazel distribution from the link below.
https://github.com/bazelbuild/bazel/releases

Download cuda and cudnn for GPU support.
https://developer.nvidia.com/cuda-downloads
https://developer.nvidia.com/cudnn

### Build bazel
Start by editing  \src\main\native\build_windows_jni.sh and adding
VSVARS="c:\tools\MVStudio2017\VC\Auxiliary\Build\vcvarsall.bat" or the path to
your installation.
```
cd [bazel-dist-dir]
pacman -Syuu gcc git curl zip unzip zlib-devel
export BAZEL_WRKDIR=c:/tempdir/shrtpath
export BAZEL_SH=c:/tools/msys64/usr/bin/bash.exe
export BAZEL_VS=c:/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio\ 14.0 Studio/2017/Community
export BAZEL_PYTHON=c:/tools/Python27/python.exe
./compile.sh
./compile.sh compile output/bazel.exe
```

### Build tensorflow
```
git clone https://github.com/tensorflow/tensorflow.git
cd [tensorflow]
pacman -Syuu patch protobuf
pip install six numpy wheel protobuf
export PYTHON_BIN_PATH=c:/tools/Python27/python.exe
export PYTHON_LIB_PATH=c:/tools/Python27/lib/site-packages
export BAZEL_WRKDIR=c:/tempdir/shrtpath
export BAZEL_SH=c:/tools/msys64/usr/bin/bash.exe
export BAZEL_VS=c:/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio\ 14.0
export BAZEL_PYTHON=c:/tools/Python27/python.exe
export CUDA_PATH=c:/cuda
export CUDA_PATH_V8_0=c:/cuda
export CUDNN_INSTALL_PATH=c:/cuda
export PATH=$PATH:/c/cuda/bin:/c/tools/Python27:/c/github/bazel-0.5.1-1/output/
```

#### Configure
```
$ ./configure
Do you wish to build TensorFlow with MKL support? [y/N] N
No MKL support will be enabled for TensorFlow
Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native]:
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] N
No XLA support will be enabled for TensorFlow
Do you wish to build TensorFlow with VERBS support? [y/N] N
No VERBS support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] y
CUDA support will be enabled for TensorFlow
Please specify the CUDA SDK version you want to use, e.g. 7.0. [Leave empty to default to CUDA 8.0]:
Please specify the location where CUDA  toolkit is installed. Refer to README.md for more details. [Default is C:/cuda]:
Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 6.0]:
Please specify the location where cuDNN  library is installed. Refer to README.md for more details. [Default is C:/cuda]:
Please specify a list of comma-separated Cuda compute capabilities you want to build with.
You can find the compute capability of your device at: https://developer.nvidia.com/cuda-gpus.
Please note that each additional compute capability significantly increases your build time and binary size.
[Default is: "3.5,5.2"]: 6.1
Do you wish to build TensorFlow with MPI support? [y/N] N
MPI support will not be enabled for TensorFlow
Configuration finished
```

#### Building tensorflow pip package
```
export BUILD_OPTS='--cpu=x64_windows_msvc --host_cpu=x64_windows_msvc --copt=/w --verbose_failures'
bazel build -c opt $BUILD_OPTS tensorflow/tools/pip_package:build_pip_package
```

Copy all files from
c:\tempdir\shrtpath\temp\_bazel_woden\incXe-uU\execroot\tensorflow\ to bazel-bin\tensorflow\tools\pip_package\build_pip_package.runfiles\
```
bazel-bin/tensorflow/tools/pip_package/build_pip_package c:/tmp/tensorflow_pkg
pip install c:\tmp\tensorflow_pkg\tensorflow-1.1.0rc1-cp35-cp35m-win_amd64.whl
```

#### Building tensorflow java dependencies.
```
bazel build -c opt $BUILD_OPTS //tensorflow/java:tensorflow //tensorflow/java:libtensorflow_jni
```

```
cd bazel-bin\tensorflow\java\
copy libtensorflow.jar to your build directory
copy libtensorflow_jni.so to tensorflow_jni.dll in your jni directory.
```
