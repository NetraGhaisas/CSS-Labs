import cram.SumOfDigits;
import java.util.*;
public class Test{
    public static void main(String[] args){
        // SumOfDigits t = new SumOfDigits("12345","15");
        // boolean ans = t.verifyChallenge();
        // System.out.println(ans);
        // Map data = new HashMap();
        // int op = 1;
        // String[] creds = {"asdf","12345"};
        // String option = "1";
        // data.put("option",op);
        // data.put("credentials",creds);
        // data.put("challenge",option);
        // System.out.println(data.toString());
        Scanner s = new Scanner(System.in);
        System.out.println("Enter seed: ");
        Random r = new Random();
        r.setSeed(s.nextInt());
        System.out.println(r.nextInt());
    }
}