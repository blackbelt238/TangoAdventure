package app.csci451.group8.tangocontroller.robotadventure;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.Socket;

public class SocketServerReplyThread extends Thread {

    private Socket hostThreadSocket;
    private String message;

    SocketServerReplyThread(Socket socket, String message) {
        hostThreadSocket = socket;
        this.message = message;
    }

    @Override
    public void run() {
        OutputStream outputStream;

        try {
            outputStream = hostThreadSocket.getOutputStream();
            PrintStream printStream = new PrintStream(outputStream);
            printStream.println(message);
            printStream.close();

            //message += "replayed: " + msgReply + "\n";


        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
