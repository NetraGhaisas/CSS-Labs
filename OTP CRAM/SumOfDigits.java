package cram;
public class SumOfDigits extends Challenge{
    // private String otp;
    // private String input;
    public SumOfDigits(){
        // this.otp = otp;
        // this.input = ip;
        this.name = "Sum Of Digits";
    }
    public boolean verifyChallenge(){
        int user_input = Integer.parseInt(this.input);
        int ans = 0;
        for(char c : otp.toCharArray()){
            ans += (int)c - (int)('0');
        }
        if(ans==user_input){
            return true;
        } else {
            return false;
        }
    }
}