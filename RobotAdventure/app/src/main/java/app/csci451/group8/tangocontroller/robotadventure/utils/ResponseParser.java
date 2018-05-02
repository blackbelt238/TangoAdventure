package app.csci451.group8.tangocontroller.robotadventure.utils;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Ryan Brand on 4/17/2018.
 */

public class ResponseParser {
    public static List<String> parseAttackResponse(String input) {
        ArrayList<String> hpVals = new ArrayList();
        return hpVals;
    }

    public static String parseGarbage(String input) {
        input = input.replace("[", "");
        input = input.replace("]", "");
        return input.replace("'", "");
    }
}
