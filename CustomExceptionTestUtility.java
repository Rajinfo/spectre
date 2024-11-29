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

        // Logic to find classes in the package (e.g., using a library like Reflections)
        // For each class, check if it extends RuntimeException or Exception
        // Add it to exceptionClasses list if it does

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
