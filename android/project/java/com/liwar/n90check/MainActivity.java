package com.liwar.n90check;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private static final String HOME = "file:///android_asset/index.html";
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        SharedPreferences prefs = getSharedPreferences("n90_check", MODE_PRIVATE);

        web = new WebView(this);
        web.setBackgroundColor(Color.WHITE);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
        s.setDefaultTextEncodingName("UTF-8");

        web.setWebViewClient(new WebViewClient());
        web.addJavascriptInterface(new Store(prefs), "AndroidStore");
        setContentView(web);

        if (savedInstanceState != null) {
            web.restoreState(savedInstanceState);
        } else {
            web.loadUrl(HOME);
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        web.saveState(outState);
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            String url = web.getUrl();
            if (url != null && url.contains("index.html")) {
                finish();
                return true;
            }
            if (web.canGoBack()) {
                web.goBack();
                return true;
            }
        }
        return super.onKeyDown(keyCode, event);
    }

    /* 多车型版：按车型 KEY 独立存取勾选状态，额外记录上次使用的车型。
       注意不要重载同名方法，WebView 的 JS 桥对重载解析不稳定。 */
    private static final class Store {
        private static final String PREFIX = "state_";
        private static final String LAST = "last_model";
        private final SharedPreferences prefs;

        Store(SharedPreferences prefs) {
            this.prefs = prefs;
        }

        @JavascriptInterface
        public String load(String key) {
            if (key == null) return "";
            return prefs.getString(PREFIX + key, "");
        }

        @JavascriptInterface
        public void save(String key, String value) {
            if (key == null) return;
            prefs.edit().putString(PREFIX + key, value == null ? "" : value).apply();
        }

        @JavascriptInterface
        public String last() {
            return prefs.getString(LAST, "");
        }

        @JavascriptInterface
        public void setLast(String id) {
            prefs.edit().putString(LAST, id == null ? "" : id).apply();
        }
    }
}
