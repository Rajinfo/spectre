import org.junit.Test;
import static org.junit.Assert.*;
import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.List;

public class CustomExceptionTestUtility {

    @Test
    public void testAllCustomExceptions() {
        List<Class<?>> exceptionClasses = findCustomExceptionClasses("com.yourpackage");

        for (Class<?> exceptionClass : exceptionClasses) {
            testExceptionConstructors(exceptionClass);
        }
    }

    private List<Class<?>> findCustomExceptionClasses(String packageName) {
        List<Class<?>> exceptionClasses = new ArrayList<>();
        // Initialize Reflections with the package to scan
        Reflections reflections = new Reflections(packageName, new SubTypesScanner(false));

        // Get all classes in the package
        Set<Class<?>> allClasses = reflections.getSubTypesOf(Object.class);

        // Filter classes that extend RuntimeException or Exception
        for (Class<?> clazz : allClasses) {
            if (RuntimeException.class.isAssignableFrom(clazz) Exception.class.isAssignableFrom(clazz)) {
                exceptionClasses.add(clazz);
            }
        }

        return exceptionClasses;
    }

    private void testExceptionConstructors(Class<?> exceptionClass) {
        Constructor<?>[] constructors = exceptionClass.getConstructors();

        for (Constructor<?> constructor : constructors) {
            Class<?>[] parameterTypes = constructor.getParameterTypes();

            try {
                Object exceptionInstance;
                if (parameterTypes.length == 0) {
                    exceptionInstance = constructor.newInstance();
                    assertNull(((Exception) exceptionInstance).getMessage());
                    assertNull(((Exception) exceptionInstance).getCause());
                } else if (parameterTypes.length == 1 && parameterTypes[0] == String.class) {
                    String message = "Test message";
                    exceptionInstance = constructor.newInstance(message);
                    assertEquals(message, ((Exception) exceptionInstance).getMessage());
                } else if (parameterTypes.length == 1 && parameterTypes[0] == Throwable.class) {
                    Throwable cause = new Throwable("Test cause");
                    exceptionInstance = constructor.newInstance(cause);
                    assertEquals(cause, ((Exception) exceptionInstance).getCause());
                } else if (parameterTypes.length == 2 && parameterTypes[0] == String.class && parameterTypes[1] == Throwable.class) {
                    String message = "Test message";
                    Throwable cause = new Throwable("Test cause");
                    exceptionInstance = constructor.newInstance(message, cause);
                    assertEquals(message, ((Exception) exceptionInstance).getMessage());
                    assertEquals(cause, ((Exception) exceptionInstance).getCause());
                }
            } catch (Exception e) {
                fail("Exception occurred while testing constructor: " + e.getMessage());
            }
        }
    }
}
