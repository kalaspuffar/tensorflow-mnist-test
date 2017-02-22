# Tensorflow MNIST demo
Me testing our tensorflow and mnist in java

```
Set-ExecutionPolicy Unrestricted
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install bazel
```

```
git clone https://github.com/tensorflow/tensorflow.git
```

Start msys32
```
pip install numpy
export PYTHON_BIN_PATH=[python_exe_path]
export BAZEL_SH=/usr/bin/bash.exe
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
