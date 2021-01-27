package cram;
public abstract class Challenge{
    protected String otp;
    protected String input;
    protected String name;
    public abstract boolean verifyChallenge();
    public String getName(){
        return this.name;
    }
    public void setOTP(String otp){
        this.otp = otp;
    }
    public void setInput(String ip){
        this.input = ip;
    }
}