package cram;
public class User{
    private String username, password;
    private Challenge userChallenge;
    public User(String u, String p, Challenge c){
        username = u;
        password = p;
        userChallenge = c;
    }
    public String getUser(){
        return this.username;
    }
    public String getPwd(){
        return this.password;
    }
    public Challenge getCRAM(){
        return this.userChallenge;
    }
}