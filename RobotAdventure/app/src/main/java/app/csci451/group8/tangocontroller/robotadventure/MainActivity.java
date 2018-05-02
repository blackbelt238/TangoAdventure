package app.csci451.group8.tangocontroller.robotadventure;

import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Message;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

import app.csci451.group8.tangocontroller.R;
import edu.cmu.pocketsphinx.Assets;
import edu.cmu.pocketsphinx.Hypothesis;
import edu.cmu.pocketsphinx.RecognitionListener;
import edu.cmu.pocketsphinx.SpeechRecognizer;
import edu.cmu.pocketsphinx.SpeechRecognizerSetup;

import static android.widget.Toast.makeText;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, RecognitionListener {

    Button north, south, east, west, chest, station;
    HashMap<String, Button> buttons;
    ArrayList<String> actions;

    GameServer server;

    private String enemyName;

    TextView enemyNameText;

    Button attackButton;
    Button runButton;

    MediaPlayer mp;
    ImageButton enemyPortrait;

    TTS tts;

    /* Named searches allow to quickly reconfigure the decoder */
    private static final String KWS_SEARCH = "wakeup";
    private static final String MENU_SEARCH = "menu";
    private static final String SENDCOMMAND = "command";
    private static final String CONTINUE = "continue";
    private static final String START = "start";

    /* Keyword we are looking for to activate menu */
    private static final String KEYPHRASE = "tango";

    /* Used to handle permission request */
    private static final int PERMISSIONS_REQUEST_RECORD_AUDIO = 1;

    private SpeechRecognizer recognizer;
    private HashMap<String, Integer> captions;

    private String spokenString = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        server = new GameServer(this);
        //System.out.println(server.getIpAddress());

        tts = new TTS(this);
        tts.start();

        actions = new ArrayList<>();

        buttons = new HashMap<>();

        buttons.put("north", north = findViewById(R.id.northButton));
        buttons.put("south", south = findViewById(R.id.southButton));
        buttons.put("east", east = findViewById(R.id.eastbutton));
        buttons.put("west", west = findViewById(R.id.westButton));
        buttons.put("chest", chest = findViewById(R.id.chestButton));
        buttons.put("pool", station = findViewById(R.id.chargeButton));

        north.setOnClickListener(this);
        south.setOnClickListener(this);
        east.setOnClickListener(this);
        west.setOnClickListener(this);
        chest.setOnClickListener(this);
        station.setOnClickListener(this);

        disableAllActions();

        //enemyNameText = findViewById(R.id.enemyName);
        attackButton = findViewById(R.id.attack_button);
        runButton = findViewById(R.id.run_button);

        // Set listeners
        attackButton.setOnClickListener(this);
        runButton.setOnClickListener(this);

        toggleButtonState(false);

        buttons.put("attack", attackButton);
        buttons.put("run", runButton);

        // Prepare the data for UI
        captions = new HashMap<>();
        captions.put(KWS_SEARCH, R.string.kws_caption);
        captions.put(MENU_SEARCH, R.string.menu_caption);
        captions.put(SENDCOMMAND, R.string.command_caption);
        ((TextView) findViewById(R.id.caption_text))
                .setText("Preparing the recognizer");

        // Recognizer initialization is a time-consuming and it involves IO,
        // so we execute it in async task
        new SetupTask(this).execute();
    }

    @Override
    public void onClick(View view) {
        disableAllActions();
        String buttonText = ((Button) findViewById(view.getId())).getText().toString();
        if (buttonText.equals("pool")) {
            speak("Healed to full hit points");
        }
        server.uiCommand = buttonText;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        if (recognizer != null) {
            recognizer.cancel();
            recognizer.shutdown();
        }

        if (tts != null) {
            tts.destroy();
        }
    }

    private void speak(String message) {
        Message sendMsg = tts.handler.obtainMessage();
        Bundle b = new Bundle();
        b.putString("TT", message);
        sendMsg.setData(b);
        tts.handler.sendMessage(sendMsg);
    }

    private String createActionMessage() {
        StringBuilder sb = new StringBuilder();
        sb.append("My possible actions are ");
        for (String action : actions) {
            sb.append(action);
            sb.append(',');
        }
        sb.delete(sb.length() -1, sb.length() - 1);
        return sb.toString();
    }

    public void enablePossibleActions() {
        disableAllActions();
        speak(createActionMessage());
        for (String action : actions) {
            if (buttons.containsKey(action.toLowerCase())) {
                buttons.get(action.toLowerCase()).setEnabled(true);
            }
        }
    }

    private void disableAllActions() {
        north.setEnabled(false);
        south.setEnabled(false);
        east.setEnabled(false);
        west.setEnabled(false);
        chest.setEnabled(false);
        station.setEnabled(false);
    }

    public void startBattle(String enemyName) {
        toggleButtonState(true);
        disableAllActions();

        this.enemyName = enemyName;

        enemyPortrait = findViewById(R.id.imageButton);

        if (enemyName.equals("deer")) {
            enemyPortrait.setImageResource(R.drawable.bambi);
        } else {
            enemyPortrait.setImageResource(R.drawable.snake);
        }

        speak("Beginning combat on " + this.enemyName);

        server.uiCommand = "received hp";
    }

    public void win() {
        speak("You have won");
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        finish();
    }

    public void endCombat(String endCondition) {
        if (endCondition.contains("died")) {
            speak("You are dead.");
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            finish();
        } else {
            speak("You won! Gained " + endCondition + " experience");
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        server.uiCommand = "combat complete";
        enemyPortrait.setImageResource(android.R.color.black);
        toggleButtonState(false);
    }

    private void toggleButtonState(boolean state) {
        attackButton.setEnabled(state);
        runButton.setEnabled(state);
    }

    public void needKey() {
        speak("You need a key before you can open that chest");
        server.uiCommand = "need key";
    }

    public void damageDealt(String amount) {
        speak("Dealt " + amount + " damage to enemy");
        try {
            TimeUnit.SECONDS.sleep(2);
        } catch (Exception e) {
            e.printStackTrace();
        }
        server.uiCommand = "finished dealing damage";
        toggleButtonState(true);

    }

    public void damageRecv(String amount) {
        speak("Took " + amount + " damage from enemny");
        try {
            TimeUnit.SECONDS.sleep(2);
        } catch (Exception e) {
            e.printStackTrace();
        }
        server.uiCommand = "finished receiving damage";
        toggleButtonState(true);
    }

    public void runResult(boolean success) {
        if (success) {
            speak("Successfully ran away");
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            server.uiCommand = "finished running";
            endCombat("run");
        }

        speak("Could not escape");
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        server.uiCommand = "finished running";
        toggleButtonState(true);
    }

    private static class SetupTask extends AsyncTask<Void, Void, Exception> {
        WeakReference<MainActivity> activityReference;
        SetupTask(MainActivity activity) {
            this.activityReference = new WeakReference<>(activity);
        }
        @Override
        protected Exception doInBackground(Void... params) {
            try {
                Assets assets = new Assets(activityReference.get());
                File assetDir = assets.syncAssets();
                activityReference.get().setupRecognizer(assetDir);
            } catch (IOException e) {
                return e;
            }
            return null;
        }
        @Override
        protected void onPostExecute(Exception result) {
            if (result != null) {
                ((TextView) activityReference.get().findViewById(R.id.caption_text))
                        .setText("Failed to init recognizer " + result);
            } else {
                activityReference.get().switchSearch(KWS_SEARCH);
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String[] permissions, @NonNull  int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == PERMISSIONS_REQUEST_RECORD_AUDIO) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Recognizer initialization is a time-consuming and it involves IO,
                // so we execute it in async task
                new SetupTask(this).execute();
            } else {
                finish();
            }
        }
    }

    /**
     * In partial result we get quick updates about current hypothesis. In
     * keyword spotting mode we can react here, in other modes we need to wait
     * for final result in onResult.
     */
    @Override
    public void onPartialResult(Hypothesis hypothesis) {
        if (hypothesis == null)
            return;

        String text = hypothesis.getHypstr();
        if (text.equals(KEYPHRASE))
            switchSearch(MENU_SEARCH);
        else if (text.equals(SENDCOMMAND)) {
            switchSearch(SENDCOMMAND);
        }
    }

    /**
     * This callback is called when we stop the recognizer.
     */
    @Override
    public void onResult(Hypothesis hypothesis) {
        if (hypothesis != null) {
            String text = hypothesis.getHypstr();

            System.out.println(recognizer.getSearchName());

            String searchName = recognizer.getSearchName();
            System.out.println(searchName);

            if (searchName != null && (searchName.equals(KWS_SEARCH) || searchName.equals(START) || searchName.equals(CONTINUE))) {
                Client client = new Client("10.200.3.99", 5011, text);
                client.execute();
            }

            makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onBeginningOfSpeech() {
    }

    /**
     * We stop recognizer here to get a final result
     */
    @Override
    public void onEndOfSpeech() {
        if (!recognizer.getSearchName().equals(KWS_SEARCH)) {
            switchSearch(KWS_SEARCH);
        }
    }

    private void switchSearch(String searchName) {
        recognizer.stop();

        // If we are not spotting, start listening with timeout (10000 ms or 10 seconds).
        if (searchName.equals(KWS_SEARCH))
            recognizer.startListening(searchName);
        else
            recognizer.startListening(searchName, 10000);

        String caption = getResources().getString(captions.get(searchName));
        ((TextView) findViewById(R.id.caption_text)).setText(caption);
    }

    private void setupRecognizer(File assetsDir) throws IOException {
        // The recognizer can be configured to perform multiple searches
        // of different kind and switch between them

        recognizer = SpeechRecognizerSetup.defaultSetup()
                .setAcousticModel(new File(assetsDir, "en-us-ptm"))
                .setDictionary(new File(assetsDir, "cmudict-en-us.dict"))

                .setRawLogDir(assetsDir) // To disable logging of raw audio comment out this call (takes a lot of space on the device)

                .getRecognizer();
        recognizer.addListener(this);

        /* In your application you might not need to add all those searches.
          They are added here for demonstration. You can leave just one.
         */

        // Create keyword-activation search.
        recognizer.addKeyphraseSearch(KWS_SEARCH, KEYPHRASE);
        //recognizer.addKeyphraseSearch(KWS_SEARCH, EXIT);


        // Create grammar-based search for selection between demos
        File menuGrammar = new File(assetsDir, "menu.gram");
        recognizer.addGrammarSearch(MENU_SEARCH, menuGrammar);

        File commandGrammar = new File(assetsDir, "command.gram");
        recognizer.addGrammarSearch(SENDCOMMAND, commandGrammar);

//        // Create grammar-based search for digit recognition
//        File digitsGrammar = new File(assetsDir, "digits.gram");
//        recognizer.addGrammarSearch(DIGITS_SEARCH, digitsGrammar);
//
//        // Create language model search
//        File languageModel = new File(assetsDir, "weather.dmp");
//        recognizer.addNgramSearch(FORECAST_SEARCH, languageModel);
//
//        // Phonetic search
//        File phoneticModel = new File(assetsDir, "en-phone.dmp");
//        recognizer.addAllphoneSearch(PHONE_SEARCH, phoneticModel);
    }

    @Override
    public void onError(Exception error) {
        ((TextView) findViewById(R.id.caption_text)).setText(error.getMessage());
    }

    @Override
    public void onTimeout() {
        switchSearch(KWS_SEARCH);
    }
}
