#!/bin/bash
# 构建「小米澎程提车速查卡_全车型.apk」
#
# 依赖：JDK 17、Android SDK platform 34、build-tools 34.0.0
#   - 已装好工具链时用 JAVA_HOME / ANDROID_SDK_DIR 指定即可
#   - 未指定时回退到本目录下的便携目录 android/jdk、android/sdk（不入库）
#
# 注意：keystore 为本地自签名演示证书，不入库；正式分发请使用自己的密钥。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
PROJ="$HERE/project"

SDK="${ANDROID_SDK_DIR:-$HERE/sdk}"
ANDROID_JAR="$SDK/platforms/android-34/android.jar"
BT="$SDK/build-tools/34.0.0"

if [ -n "${JAVA_HOME:-}" ]; then
  J="$JAVA_HOME"
else
  J="$(find "$HERE/jdk" -maxdepth 4 -type d -name Home -print -quit 2>/dev/null || true)"
fi

if [ -z "${J:-}" ] || [ ! -x "$J/bin/javac" ]; then
  echo "未找到 JDK 17，请设置 JAVA_HOME 或把便携 JDK 放到 android/jdk/" >&2
  exit 1
fi
if [ ! -f "$ANDROID_JAR" ] || [ ! -x "$BT/aapt2" ]; then
  echo "未找到 Android SDK 34 / build-tools 34.0.0，请设置 ANDROID_SDK_DIR" >&2
  exit 1
fi

export JAVA_HOME="$J"
export PATH="$J/bin:$PATH"

# 本地自签名演示口令（私钥不入库，此口令不是凭据）；正式分发请用 KS_PASS 覆盖
KS_PASS="${KS_PASS:-n90check}"
# 默认覆盖仓库根目录的成品 APK；测试构建可用 APK_OUT 指向临时路径
OUT="${APK_OUT:-$REPO/小米澎程提车速查卡_全车型.apk}"

cd "$PROJ"

echo "[1/8] 编译 MainActivity.java"
rm -rf classes && mkdir -p classes
"$J/bin/javac" --release 8 -classpath "$ANDROID_JAR" -d classes \
  java/com/liwar/n90check/MainActivity.java

echo "[2/8] d8 生成 classes.dex"
rm -f classes.dex
"$BT/d8" --lib "$ANDROID_JAR" --min-api 23 --output . $(find classes -name '*.class')

echo "[3/8] aapt2 编译资源"
rm -f res.zip base.apk unsigned.apk aligned.apk
"$BT/aapt2" compile --dir res -o res.zip

echo "[4/8] aapt2 链接基础 APK（含 assets/）"
"$BT/aapt2" link -o base.apk -I "$ANDROID_JAR" \
  --manifest AndroidManifest.xml -A assets \
  --min-sdk-version 23 --target-sdk-version 34 res.zip

echo "[5/8] 合入 classes.dex"
cp base.apk unsigned.apk
zip -q unsigned.apk classes.dex

echo "[6/8] zipalign"
"$BT/zipalign" -f -p 4 unsigned.apk aligned.apk

echo "[7/8] 生成自签名证书并签名"
if [ ! -f n90.keystore ]; then
  "$J/bin/keytool" -genkeypair -keystore n90.keystore -alias n90 \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" \
    -dname "CN=PengchengCheck, OU=Personal, O=Personal, L=Beijing, ST=Beijing, C=CN" \
    >/dev/null 2>&1
fi
"$BT/apksigner" sign --ks n90.keystore \
  --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
  --out "$OUT" aligned.apk

echo "[8/8] 验证签名"
"$BT/apksigner" verify --verbose "$OUT" | head -8
echo "成品：$OUT"
