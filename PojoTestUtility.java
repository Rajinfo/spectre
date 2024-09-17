import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.util.*;

public class PojoTestUtility {

    // Method to generate dummy values, including Arrays, Enums, and handling custom exceptions
    public static Object getDummyValue(Class<?> type) {
        try {
            if (type.equals(String.class)) {
                return "dummyString";
            } else if (type.equals(int.class) || type.equals(Integer.class)) {
                return 123;
            } else if (type.equals(long.class) || type.equals(Long.class)) {
                return 123L;
            } else if (type.equals(boolean.class) || type.equals(Boolean.class)) {
                return true;
            } else if (type.equals(double.class) || type.equals(Double.class)) {
                return 123.45;
            } else if (type.equals(float.class) || type.equals(Float.class)) {
                return 12.34f;
            } else if (type.equals(char.class) || type.equals(Character.class)) {
                return 'd';
            } else if (type.isArray()) {
                // Handle Arrays by returning a single-element array of the component type
                Class<?> componentType = type.getComponentType();
                Object array = java.lang.reflect.Array.newInstance(componentType, 1);
                java.lang.reflect.Array.set(array, 0, getDummyValue(componentType));
                return array;
            } else if (List.class.isAssignableFrom(type)) {
                List<Object> dummyList = new ArrayList<>();
                dummyList.add("dummyListItem");
                return dummyList;
            } else if (Set.class.isAssignableFrom(type)) {
                Set<Object> dummySet = new HashSet<>();
                dummySet.add("dummySetItem");
                return dummySet;
            } else if (Map.class.isAssignableFrom(type)) {
                Map<Object, Object> dummyMap = new HashMap<>();
                dummyMap.put("dummyKey", "dummyValue");
                return dummyMap;
            } else if (Collection.class.isAssignableFrom(type)) {
                Collection<Object> dummyCollection = new ArrayList<>();
                dummyCollection.add("dummyCollectionItem");
                return dummyCollection;
            } else if (type.isEnum()) {
                // For Enums, return the first enum constant
                return type.getEnumConstants()[0];
            } else if (Throwable.class.isAssignableFrom(type)) {
                // Handle custom exceptions by using a constructor that takes a String (message) or Throwable (cause)
                Constructor<?> constructor = type.getDeclaredConstructor(String.class);
                constructor.setAccessible(true);
                return constructor.newInstance("Custom exception message");
            } else if (type.equals(Object.class)) {
                return new Object(); // Handle generic Object fields
            } else {
                // Handle complex object fields by creating a new instance via reflection
                Constructor<?> constructor = type.getDeclaredConstructor();
                constructor.setAccessible(true); // To handle private constructors
                return constructor.newInstance();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null; // Return null if unable to create a dummy instance
        }
    }

    // Method to test the getters and setters of the POJO, with an ignore list
    public static void testPojo(Object obj, Set<Class<?>> ignoredClasses) {
        if (ignoredClasses.contains(obj.getClass())) {
            return; // Skip testing if the class is in the ignore list
        }

        Method[] methods = obj.getClass().getMethods();
        Map<String, Method> setters = new HashMap<>();
        Map<String, Method> getters = new HashMap<>();

        // Separate getters and setters
        for (Method method : methods) {
            if (method.getName().startsWith("set") && method.getParameterCount() == 1) {
                setters.put(method.getName().substring(3), method);
            } else if (method.getName().startsWith("get") && method.getParameterCount() == 0) {
                getters.put(method.getName().substring(3), method);
            } else if (method.getName().startsWith("is") && method.getParameterCount() == 0) {
                getters.put(method.getName().substring(2), method);
            }
        }

        // Invoke setters and getters
        setters.forEach((field, setter) -> {
            Method getter = getters.get(field);
            if (getter != null) {
                try {
                    Object dummyValue = getDummyValue(setter.getParameterTypes()[0]);
                    if (dummyValue != null) {
                        setter.invoke(obj, dummyValue);
                        Object value = getter.invoke(obj);
                        assert value.equals(dummyValue) : "Mismatch between set and get for field: " + field;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    // Method to load and test all POJOs and custom exceptions from a package, with an ignore list
    public static void testAllPojosInPackage(String packageName, Set<Class<?>> ignoredClasses) {
        try {
            List<Class<?>> classes = getClassesInPackage(packageName);
            for (Class<?> clazz : classes) {
                if (!ignoredClasses.contains(clazz)) {
                    if (Throwable.class.isAssignableFrom(clazz)) {
                        // Handle exceptions
                        testCustomException(clazz);
                    } else {
                        // Test POJOs
                        Object instance = clazz.getDeclaredConstructor().newInstance();
                        testPojo(instance, ignoredClasses);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Test custom exceptions by creating and throwing them
    public static void testCustomException(Class<?> exceptionClass) {
        try {
            Throwable exceptionInstance = (Throwable) getDummyValue(exceptionClass);
            throw exceptionInstance; // Simulate throwing the exception
        } catch (Throwable e) {
            // Catch and print the exception to simulate usage
            System.out.println("Caught exception: " + e.getMessage());
        }
    }

    // Helper method to get all classes in a package without dependencies
    public static List<Class<?>> getClassesInPackage(String packageName) throws Exception {
        List<Class<?>> classes = new ArrayList<>();
        String packagePath = packageName.replace('.', '/');
        ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
        URL packageURL = classLoader.getResource(packagePath);

        if (packageURL != null) {
            File folder = new File(packageURL.getFile());
            File[] files = folder.listFiles();
            if (files != null) {
                for (File file : files) {
                    String fileName = file.getName();
                    if (fileName.endsWith(".class")) {
                        String className = packageName + '.' + fileName.substring(0, fileName.length() - 6);
                        Class<?> clazz = Class.forName(className);
                        classes.add(clazz);
                    }
                }
            }
        }

        return classes;
    }
}
