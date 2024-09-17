import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.Set;

public class PojoTest {

    @Test
    public void testAllPojosInPackage() {
        String packageName = "com.example.myapp"; // Your package name
        Set<Class<?>> ignoredClasses = new HashSet<>();
        ignoredClasses.add(CustomException.class);  // Example of ignoring a specific exception
        PojoTestUtility.testAllPojosInPackage(packageName, ignoredClasses);
    }
}
