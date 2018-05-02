package app.csci451.group8.tangocontroller;

import android.os.Bundle;
import android.speech.RecognitionListener;
import android.util.Log;

/**
 * Created by Ryan Brand on 4/2/2018.
 */

public class SpeechListener implements RecognitionListener {
    @Override
    public void onReadyForSpeech(Bundle bundle) {
        System.out.println("Ready for speech");
    }

    @Override
    public void onBeginningOfSpeech() {
        System.out.println("Beginning speech");
    }

    @Override
    public void onRmsChanged(float v) {

    }

    @Override
    public void onBufferReceived(byte[] bytes) {

    }

    @Override
    public void onEndOfSpeech() {
        System.out.println("Speech Ended");
    }

    @Override
    public void onError(int i) {

    }

    @Override
    public void onResults(Bundle bundle) {
        String str = new String();
        Log.d("MYAPP","onResults " + bundle);
    }

    @Override
    public void onPartialResults(Bundle bundle) {

    }

    @Override
    public void onEvent(int i, Bundle bundle) {

    }
}
