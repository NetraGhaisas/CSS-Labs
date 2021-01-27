package cram;
import java.net.*;
import java.io.*;
import java.util.*;
public class OTPClient {
  // BufferedReader br;
  ObjectInputStream inStream;
  ObjectOutputStream outStream;
  Socket socket;
  public OTPClient(){
    try{
      socket=new Socket("127.0.0.1",8888);
      outStream=new ObjectOutputStream(socket.getOutputStream());
      inStream=new ObjectInputStream(socket.getInputStream());
      String initMessage = (String)inStream.readObject();
      if(initMessage.equalsIgnoreCase("connected")){
      BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
      System.out.println("Connected!");
      String clientMessage="",serverMessage="";
      boolean sessionFlag = true;
      while(sessionFlag==true){
        System.out.println("OTP CRAM Client\n1. Sign up\n2. Login\n3. Exit");
        clientMessage=br.readLine();
        int op = Integer.parseInt(clientMessage);
        Map data;
        String[] creds;
        switch(op){
          case 1:
            creds = getCreds();
            data = new HashMap();
            data.put("option",0);
            outStream.writeObject(data);
            serverMessage=(String)inStream.readObject();
            System.out.println(serverMessage);
            System.out.println("Enter option: ");
            int option = Integer.parseInt(br.readLine());
            data = new HashMap();
            data.put("option",op);
            data.put("credentials",creds);
            data.put("challenge",option);
            outStream.writeObject(data);
            serverMessage=(String)inStream.readObject();
            System.out.println(serverMessage);
            break;
          case 2:
            creds = getCreds();
            data = new HashMap();
            data.put("option",op);
            data.put("credentials",creds);
            outStream.writeObject(data);
            Thread.sleep(1000);
            serverMessage = (String)inStream.readObject();
            if(serverMessage.equalsIgnoreCase("error")){
              System.out.println("User not found");
              break;
            }
            System.out.println("Challenge: "+serverMessage+"\nEnter response: ");
            String ans = br.readLine();
            data = new HashMap();
            data.put("option",3);
            data.put("response",ans);
            outStream.writeObject(data);
            serverMessage=(String)inStream.readObject();
            System.out.println(serverMessage);
            break;
          case 3:
            data = new HashMap();
            data.put("option",4);
            outStream.writeObject(data);
            sessionFlag = false;
            break;
        }
        // outStream.writeUTF(clientMessage);
        outStream.flush();
        // serverMessage=inStream.readUTF();
        // System.out.println(serverMessage);
      }
    } else {
      System.out.println(initMessage);
    }
      inStream.close();
      outStream.close();
      socket.close();
    }catch(Exception e){
      System.out.println(e);
    }
  }
  private String[] getCreds() throws IOException{
    Console console = System.console();
    System.out.println("Enter username: ");
    String username = console.readLine();
    // System.out.println("Enter password: ");
    String password = new String(console.readPassword("Enter password: "));
    return new String[]{username,password};
  }
  public static void main(String[] args) throws Exception {
    OTPClient client = new OTPClient();
  }
}
