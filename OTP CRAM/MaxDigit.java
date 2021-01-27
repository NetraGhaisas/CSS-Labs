package cram;

public class MaxDigit extends Challenge{
    // private String otp;
    // private String input;
    public MaxDigit(){
        // this.otp = otp;
        // this.input = ip;
        this.name = "Maximum digit in number";
    }
    public boolean verifyChallenge(){
        int user_input = Integer.parseInt(this.input);
        int ans = -1;
        for(char c : this.otp.toCharArray()){
            ans = Math.max(ans,((int)c-(int)('0')));
        }
        if(ans==user_input){
            return true;
        } else {
            return false;
        }
    }
}