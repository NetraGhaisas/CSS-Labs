package cram;
public class Reverse extends Challenge{
    // private String otp;
    // private String input;
    public Reverse(){
        // this.otp = otp;
        // this.input = ip;
        this.name = "Reverse the OTP";
    }
    public boolean verifyChallenge(){
        String user_input = this.input;
        int i=0, j=user_input.length()-1;
        while(i<user_input.length() && j>=0){
            if(this.otp.charAt(i) == user_input.charAt(j)){
                i++;
                j--;
            } else{
                return false;
            }
        }
        return true;
    }
}