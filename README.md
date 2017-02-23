# Tensorflow MNIST demo
Me testing our tensorflow and mnist in java

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
```

Start msys32
```
pip install numpy
export PYTHON_BIN_PATH=[python_exe_path]
export BAZEL_SH=/usr/bin/bash.exe
export BAZEL_VS=[Visual Studio Path]
export BAZEL_PYTHON=[python.exe Path]
./configure
bazel build --config opt //tensorflow/java:tensorflow //tensorflow/java:libtensorflow_jni
```

Windows 7 need Powershell 3.0
http://www.microsoft.com/en-us/download/details.aspx?id=34595

```
mvn archetype:generate
  -DgroupId=org.ea.tensorflow
  -DartifactId=tensorflow-mnist
  -Dversion=0.0.1
  -DinteractiveMode=false
```


```
mvn org.apache.maven.plugins:maven-install-plugin:2.5.2:install-file
  -Dfile=libtensorflow-1.0.0-PREVIEW1.jar
  -DgroupId=org.tensorflow
  -DartifactId=libtensorflow
  -Dversion=1.0.0-PREVIEW1
  -Dpackaging=jar
  -DgeneratePom=true
```
