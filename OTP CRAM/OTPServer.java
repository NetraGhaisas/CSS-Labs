package cram;
import java.net.*;
import java.io.*;
import java.util.*;
import java.security.SecureRandom;

public class OTPServer {
  ServerSocket server;
  static int counter = 0;
  ServerThread[] clients;
  final int LIMIT = 2;
  Challenge[] challengeList;
  Vector<User> userList;
  private Map<String,Long> otpList;
  private Vector<User> initUsers(){
    Vector<User> users = new Vector<User>();
    users.add(new User("netra","netra",new PlusOne()));
    users.add(new User("alice","alice",new SumOfDigits()));
    return users;
  }
  private Challenge[] initChallenges(){
    int numChallenges = 5;
    Challenge[] ch = new Challenge[numChallenges];
    ch[0] = new SumOfDigits();
    ch[1] = new PlusOne();
    ch[2] = new Reverse();
    ch[3] = new MaxDigit();
    ch[4] = new SeedFirstRandom();
    return ch;
  }
  public String getChallenges(){
    String res = "";
    for(int i=0;i<this.challengeList.length;i++){
      res += (i+1)+". "+this.challengeList[i].getName()+"\n";
    }
    System.out.println(res);
    return res;
  }

  public void purgeOTP(){
    long expiryMillis = 1000;
    long nowMillis = System.currentTimeMillis();
    Iterator<Map.Entry<String, Long>> itr = this.otpList.entrySet().iterator(); 
    while(itr.hasNext()) 
    { 
      Map.Entry<String, Long> entry = itr.next();
      if(nowMillis-(long)(entry.getValue())>=1000){
        itr.remove();
      }
    }
  }

  public String generateOTP(){
    purgeOTP();
    int lower = 10000000, upper = 99999999;
    int range = upper - lower;
    SecureRandom randomizer = new SecureRandom();
    String otp;
    while(true){
      otp = (lower + randomizer.nextInt(range)) + "";
      if(!this.otpList.containsKey(otp)){
        break;
      }
    }
    return otp;
  }
  public OTPServer(){
    try{
      int clientNo=0;
      if(server==null){
        this.userList = this.initUsers();
        this.challengeList = this.initChallenges();
        otpList = new HashMap<String,Long>();
        clients = new ServerThread[LIMIT];
        server=new ServerSocket(8888);
        System.out.println("Server Started ....");
      }
      while(true){
        Socket serverClient=server.accept();
        if(this.counter<LIMIT){
          this.counter++;
          clientNo++;
          System.out.println(" >> " + "Client No:" + clientNo + " started!\nTotal clients: "+counter);
          ServerThread sct = new ServerThread(this,serverClient,clientNo); //send  the request to a separate thread
          sct.start();
        } else{
          ObjectInputStream inStream = new ObjectInputStream(serverClient.getInputStream());
          ObjectOutputStream outStream=new ObjectOutputStream(serverClient.getOutputStream());
          outStream.writeObject("Connection refused: Server has reached maximum connection limit!"+this.counter);
          inStream.close();
          outStream.close();
          serverClient.close();
          System.out.println("A connection request was refused");
        }
      }
    }catch(Exception e){
      System.out.println(e);
    }
  }
  public static void main(String[] args) throws Exception {
    OTPServer otpServer = new OTPServer();
  }
}

class ServerThread extends Thread {
  OTPServer server;
  Socket serverClient;
  int clientNo;
  User sessionUser;
  ServerThread(OTPServer server, Socket inSocket,int counter){
    serverClient = inSocket;
    this.clientNo=counter;
    this.server = server;
  }
  
  public void run(){
    try{
      ObjectInputStream inStream = new ObjectInputStream(serverClient.getInputStream());
      ObjectOutputStream outStream = new ObjectOutputStream(serverClient.getOutputStream());
      outStream.writeObject("Connected");
      Map clientData;
      String serverMessage="";
      boolean sessionFlag = true;
      while(sessionFlag==true){
        clientData=(HashMap)inStream.readObject();
        System.out.println("From Client-" +clientNo+ ": Request is :"+clientData);
        int op = (int)clientData.get("option");
        switch(op){
          case 0:
            String challenges = this.server.getChallenges();
            outStream.writeObject(challenges);
            break;
          case 1:
            String u = ((String[])clientData.get("credentials"))[0];
            String p = ((String[])clientData.get("credentials"))[1];
            int idx = (int)clientData.get("challenge");
            Challenge c = this.server.challengeList[idx-1];
            this.server.userList.add(new User(u,p,c));
            outStream.writeObject("User added to database!\n");
            break;
          case 2:
            String un = ((String[])clientData.get("credentials"))[0];
            String pwd = ((String[])clientData.get("credentials"))[1];
            for(int i=0;i<this.server.userList.size();i++){
              if(this.server.userList.get(i).getUser().equals(un) && this.server.userList.get(i).getPwd().equals(pwd)){
                System.out.println("User "+un+" found in database!");
                this.sessionUser = this.server.userList.get(i);
                break;
              }
            }
            if(sessionUser==null){
              System.out.println("User "+un+" not found in database!");
              outStream.writeObject("error");
              break;
            }
            String otp = this.server.generateOTP();
            sessionUser.getCRAM().setOTP(otp);
            outStream.writeObject(otp);
            break;
          case 3:
            String ans = (String)clientData.get("response");
            sessionUser.getCRAM().setInput(ans);
            boolean status = sessionUser.getCRAM().verifyChallenge();
            if(status){
              outStream.writeObject("Correct! User authenticated\n");
            } else {
              outStream.writeObject("Incorrect!\n");
            }
            break;
          case 4:
            sessionFlag = false;
            break;
        }
        // serverMessage="From Server to Client-" + clientNo + " Square of " + clientData + " is " +square;
        // outStream.writeUTF(serverMessage);
        outStream.flush();
      }
      inStream.close();
      outStream.close();
      serverClient.close();
    }catch(Exception ex){
      System.out.println(ex);
      ex.printStackTrace();
    }finally{
      synchronized(this.server){
        this.server.counter--;
        System.out.println("Client " + clientNo + " exit! Total clients: "+this.server.counter);
      }
    }
  }
}
