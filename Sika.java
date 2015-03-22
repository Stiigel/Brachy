import java.util.*;
import java.util.Scanner;
public class Sika {
  
  public static void main(String[] args) {
    String kissa = "público clase Hermanni:";
    String kirahvi = "ent cad" + "clase" + "Verdado";

    String sika = "KISSA";
    int lehma = 3;
    char mmh = '3';
    
    ArrayList<String> arraylista = new ArrayList<>();
    
    //AL<cad> arraylista = nuevo AL()
    
    
    if (kissa.equals(sika)) {
      System.out.println("KISSA ON SIKA!");
    } else {
      System.out.println("Kissa ei ole sika");
      
      //.iquala
    
    }
    Scanner lector = new Scanner(System.in);
    String rivi = lector.nextLine();
    
    //Olen inva :(
    int koiraent = 2389;
    
    String uuhi = "lij";
    double sdlk = 3.22;
    boolean norsu = true;
    int possu = Integer.parseInt("3") + Integer.parseInt("2938") - 3;
    
    int luku = (norsu) ? 3 : 1;
    
    System.out.println(lehma 
           + kissa);
    Koira koira = new Koira("martti");
    koira.hauku();
    
    int i = 0;
    while (i < 9) {
      System.out.print(i + " ");
      i++;
    }
    System.out.println();
    
    for ( int e = 2; e <= 4; e++) {
      System.out.println(e);      
      
    }
    for (int j = 0; j < 3; j += 1) {
      System.out.println(j);
      
    }
    for (int k = 8; k >  3; k += -2) {
      System.out.print(k);
    }
    System.out.println();
    
    String[] koirat = {"kissa", "hirvi", "sika"};
    
    for (String koi : koirat) {
      System.out.println(koi);
  
    }
  }
  public int kissa() {
    System.out.println("ij");
    return 1;

  }
}
