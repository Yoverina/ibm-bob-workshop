# Running Unit Tests for Java Ticketing Application

## Current Situation

This Spring Boot application requires **Java 17 or higher** due to:
- Spring Boot 3.2.3 (requires Java 17+)
- Jakarta EE 9+ packages (`jakarta.*` namespace)

Your system has **Java 11** installed, which is incompatible.

## Test File Overview

The [`TicketServiceTest.java`](src/test/java/com/btn/ticketing/service/TicketServiceTest.java) contains **13 comprehensive unit tests**:

### Test Coverage:
1. ✅ **shouldCreateTicketSuccessfully** - Validates ticket creation with auto-generated ticket number
2. ✅ **shouldGetAllTickets** - Tests retrieving all tickets from repository
3. ✅ **shouldGetTicketByIdWhenExists** - Tests finding ticket by ID (success case)
4. ✅ **shouldReturnEmptyWhenTicketNotFound** - Tests finding ticket by ID (not found case)
5. ✅ **shouldUpdateTicketSuccessfully** - Tests updating ticket details
6. ✅ **shouldThrowExceptionWhenUpdatingNonExistentTicket** - Tests error handling for invalid updates
7. ✅ **shouldDeleteTicketSuccessfully** - Tests ticket deletion
8. ✅ **shouldGetTicketsByStatus** - Tests filtering tickets by status
9. ✅ **shouldGetTicketsByCustomer** - Tests filtering tickets by customer
10. ✅ **shouldAssignTicketToAgent** - Tests assigning tickets to agents
11. ✅ **shouldResolveTicket** - Tests marking tickets as resolved
12. ✅ **shouldCloseTicket** - Tests closing resolved tickets
13. ✅ **shouldCountTicketsByStatus** - Tests counting tickets by status

### Testing Technologies Used:
- **JUnit 5** - Modern testing framework
- **Mockito** - Mocking framework for unit tests
- **AssertJ** - Fluent assertions for readable tests
- **Given-When-Then** pattern for clear test structure

## Solutions to Run Tests

### Option 1: Install Java 21 (Recommended)
```powershell
# Download from: https://www.oracle.com/java/technologies/downloads/#java21
# After installation, verify:
java -version

# Then run tests:
cd "Module-1-Java-Modernization/Module-Java Application"
./mvnw.cmd test
```

### Option 2: Use IDE (Easiest)
1. Open project in **IntelliJ IDEA** or **Eclipse**
2. IDE will automatically download Java 21 SDK
3. Right-click on `TicketServiceTest.java` → **Run Tests**
4. View results in IDE test runner

### Option 3: Use Docker (No Local Java Install)
```powershell
# Run tests in Java 21 container
docker run --rm -v "${PWD}:/app" -w /app maven:3.9-eclipse-temurin-21 mvn test
```

### Option 4: Downgrade Project (Not Recommended)
Requires extensive code changes:
- Downgrade Spring Boot 3.x → 2.7.x
- Change all `jakarta.*` → `javax.*` imports
- Update security configuration syntax
- Modify validation annotations

## Test Execution Output

When tests run successfully, you'll see output like:
```
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.btn.ticketing.service.TicketServiceTest
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] BUILD SUCCESS
```

## Maven Wrapper

The project now includes Maven wrapper (`mvnw.cmd`) which automatically downloads Maven when you run tests. No separate Maven installation needed!

## Next Steps

1. **Install Java 21** from Oracle or use OpenJDK
2. **Set JAVA_HOME** environment variable
3. **Run**: `./mvnw.cmd test`
4. **View** detailed test results in `target/surefire-reports/`

---

**Note**: The test file is well-structured and ready to run. Only the Java version compatibility prevents execution on your current system.