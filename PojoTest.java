import org.junit.jupiter.api.Test;

public class PojoTest {

    @Test
    public void testAllPojosInPackage() {
        String packageName = "com.example.myapp.pojos"; // Your package name
        
        PojoTestUtility.testAllPojosInPackage(packageName);
    }
}
