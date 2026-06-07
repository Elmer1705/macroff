name: Build APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libtool libtool-bin autoconf automake pkg-config python3-pip zip unzip openjdk-17-jdk

      - name: Install buildozer
        run: |
          pip install buildozer cython

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: macroff-apk
          path: bin/*.apk
