package app.csci451.group8.tangocontroller;

import android.content.Context;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.util.Locale;

/**
 * Created by Ryan Brand on 3/19/2018.
 */

public class TTS extends Thread implements TextToSpeech.OnInitListener {

    private TextToSpeech tts;
    private Context con;
    public Handler handler;
    private String last;

    public TTS(Context con) {
        this.con = con;
        tts = new TextToSpeech(con, this, "com.google.android.tts");
        last = "c";
    }

    public void onInit(int i) {
        int result = -1;
        if (i == TextToSpeech.SUCCESS) {
            result = tts.setLanguage(Locale.US);
            tts.setPitch(-20);
            tts.setSpeechRate(0);
        }

        if (result == TextToSpeech.ERROR || result == TextToSpeech.LANG_MISSING_DATA) {
            Toast.makeText(con, "Language of data not working", Toast.LENGTH_SHORT).show();
        }
    }

    public void destroy() {
        tts.shutdown();
    }

    public void run() {
        Looper.prepare();
            handler = new Handler() {
                public void handleMessage(Message msg) {
                    String response = msg.getData().getString("TT");
                    tts.speak(response, TextToSpeech.QUEUE_FLUSH, null);
                }
            };
        Looper.loop();
    }
}
