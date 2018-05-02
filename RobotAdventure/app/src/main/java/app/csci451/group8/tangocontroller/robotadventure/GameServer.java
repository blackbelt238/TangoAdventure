package app.csci451.group8.tangocontroller.robotadventure;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;

import app.csci451.group8.tangocontroller.robotadventure.utils.ResponseParser;

public class GameServer {
    MainActivity activity;
    ServerSocket serverSocket;
    String receivedMessage;
    String uiCommand;
    Socket socket;
    boolean cont = true;
    static final int socketServerPORT = 5011;

    public GameServer(MainActivity activity) {
        this.activity = activity;
        Thread socketServerThread = new Thread(new SocketServerThread());
        socketServerThread.start();
    }

    public void sendResponse(String response, Socket socket) {
        SocketServerReplyThread socketServerReplyThread =
                new SocketServerReplyThread(socket, response);
        socketServerReplyThread.run();
    }

    public int getPort() {
        return socketServerPORT;
    }

    public void onDestroy() {
        if (serverSocket != null) {
            try {
                System.out.println("Destroying");
                serverSocket.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }


    private class SocketServerThread extends Thread {


        private String processMessage(String message) {
            if (message.equals("class")) {
                sendResponse("wizard", socket);
                return "wizard";
            }

            if (message.contains("action")) {
                message = message.replace("action:", "");
                message = ResponseParser.parseGarbage(message);
                ArrayList<String> actions = new ArrayList<String>(Arrays.asList(message.split(", ")));
                ( activity).actions = actions;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        ( activity).enablePossibleActions();
                    }
                });
            } else if (message.contains("combat")) {
                System.out.println("Inside combat");
                message = message.replace("combat:", "");
                message = ResponseParser.parseGarbage(message);
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.startBattle(finalMessage);
                    }
                });
            } else if (message.contains("dealt")) {
                message = message.replace("dealt:", "");
                message = ResponseParser.parseGarbage(message);
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.damageDealt(finalMessage);
                    }
                });
            } else if (message.contains("recv")) {
                message = message.replace("recv:", "");
                message = ResponseParser.parseGarbage(message);
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.damageRecv(finalMessage);
                    }
                });
            } else if (message.contains("run")) {
                message = message.replace("run:", "");
                message = ResponseParser.parseGarbage(message);
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.runResult(Boolean.parseBoolean(finalMessage));
                    }
                });
            } else if (message.contains("gained")) {
                message = message.replace("gained:", "");
                message = ResponseParser.parseGarbage(message);
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.endCombat(finalMessage);
                    }
                });
            } else if (message.equals("need key")) {
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.needKey();
                    }
                });
            } else if (message.equals("died")) {
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.endCombat(finalMessage);
                    }
                });
            } else if (message.equals("win")) {
                final String finalMessage = message;
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        activity.win();
                    }
                });
            }

            return null;
        }

        @Override
        public void run() {
            try {
                // create ServerSocket using specified port
                serverSocket = new ServerSocket(socketServerPORT);

                while (cont) {
                    // block the call until connection is created and return
                    // Socket object
                    socket = serverSocket.accept();
                    System.out.println(socket.getInetAddress() + ":" + socket.getPort());
                    BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    receivedMessage = input.readLine();
                    String response = processMessage(receivedMessage);
                    while(uiCommand == null && response == null);
                    if (response == null) {
                        response = uiCommand;
                    }
                    uiCommand = null;
                    sendResponse(response.toLowerCase(), socket);
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }


    public static String getIpAddress() {
        String ipAddress = "Unable to Fetch IP..";
        try {
            Enumeration en;
            en = NetworkInterface.getNetworkInterfaces();
            while ( en.hasMoreElements()) {
                NetworkInterface intf = (NetworkInterface)en.nextElement();
                for (Enumeration enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = (InetAddress)enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()&&inetAddress instanceof Inet4Address) {
                        ipAddress=inetAddress.getHostAddress().toString();
                        return ipAddress;
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return ipAddress;
    }
}
