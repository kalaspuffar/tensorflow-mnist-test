#!/bin/bash

TF_TYPE="cpu"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
mkdir -p ./jni
curl -L \
  "https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow_jni-${TF_TYPE}-${OS}-x86_64-1.0.0-PREVIEW1.tar.gz" |
tar -xz -C ./jni
