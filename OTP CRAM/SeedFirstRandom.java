package cram;
import java.util.Random;
public class SeedFirstRandom extends Challenge{
    // private String otp;
    // private String input;
    public SeedFirstRandom(){
        // this.otp = otp;
        // this.input = ip;
        this.name = "First random on setting OTP as seed";
    }
    public boolean verifyChallenge(){
        int user_input = Integer.parseInt(this.input);
        Random random = new Random();
        random.setSeed(Integer.parseInt(this.otp));
        int ans = random.nextInt();
        if(ans==user_input){
            return true;
        } else {
            return false;
        }
    }
}