package cram;
public class PlusOne extends Challenge{
    // private String otp;
    // private String input;
    public PlusOne(){
        // this.otp = otp;
        // this.input = ip;
        this.name = "Add 1";
    }
    public boolean verifyChallenge(){
        int user_input = Integer.parseInt(this.input);
        int ans = Integer.parseInt(this.otp) + 1;
        if(ans==user_input){
            return true;
        } else {
            return false;
        }
    }
}