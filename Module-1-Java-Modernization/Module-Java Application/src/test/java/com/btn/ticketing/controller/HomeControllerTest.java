package com.btn.ticketing.controller;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for HomeController
 * Tests all REST endpoints with comprehensive coverage
 */
@ExtendWith(MockitoExtension.class)
class HomeControllerTest {

    @InjectMocks
    private HomeController homeController;

    @BeforeEach
    void setUp() {
        // No setup needed as HomeController has no dependencies
    }

    @Test
    void testWelcome_ReturnsCorrectStructure() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertNotNull(response);
        assertEquals(8, response.size());
    }

    @Test
    void testWelcome_ApplicationName() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("application"));
        assertEquals("Bank Customer Service Ticketing System", response.get("application"));
    }

    @Test
    void testWelcome_Version() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("version"));
        assertEquals("1.0.0-LEGACY", response.get("version"));
    }

    @Test
    void testWelcome_Description() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("description"));
        assertEquals("Java Modernization Demo - Legacy Application", response.get("description"));
    }

    @Test
    void testWelcome_TechStack() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("techStack"));
        assertInstanceOf(Map.class, response.get("techStack"));
        
        @SuppressWarnings("unchecked")
        Map<String, String> techStack = (Map<String, String>) response.get("techStack");
        assertEquals("8", techStack.get("java"));
        assertEquals("2.7.18", techStack.get("springBoot"));
        assertEquals("javax (legacy)", techStack.get("namespace"));
    }

    @Test
    void testWelcome_Status() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("status"));
        assertEquals("✅ Running", response.get("status"));
    }

    @Test
    void testWelcome_AvailableEndpoints() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("availableEndpoints"));
        assertInstanceOf(Map.class, response.get("availableEndpoints"));
        
        @SuppressWarnings("unchecked")
        Map<String, String> endpoints = (Map<String, String>) response.get("availableEndpoints");
        assertEquals(4, endpoints.size());
        assertTrue(endpoints.containsKey("info"));
        assertTrue(endpoints.containsKey("tickets"));
        assertTrue(endpoints.containsKey("dashboard"));
        assertTrue(endpoints.containsKey("h2Console"));
    }

    @Test
    void testWelcome_Credentials() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("credentials"));
        assertInstanceOf(Map.class, response.get("credentials"));
        
        @SuppressWarnings("unchecked")
        Map<String, String> credentials = (Map<String, String>) response.get("credentials");
        assertEquals("admin", credentials.get("username"));
        assertEquals("admin123", credentials.get("password"));
    }

    @Test
    void testWelcome_Message() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        assertTrue(response.containsKey("message"));
        assertEquals("🏦 Welcome to Bank Ticketing System Demo", response.get("message"));
    }

    @Test
    void testInfo_ReturnsCorrectStructure() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertNotNull(response);
        assertEquals(6, response.size());
    }

    @Test
    void testInfo_ApplicationName() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("application"));
        assertEquals("Bank Customer Service Ticketing System", response.get("application"));
    }

    @Test
    void testInfo_Version() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("version"));
        assertEquals("1.0.0-LEGACY", response.get("version"));
    }

    @Test
    void testInfo_JavaVersion() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("java"));
        assertNotNull(response.get("java"));
        assertEquals(System.getProperty("java.version"), response.get("java"));
    }

    @Test
    void testInfo_SpringBootVersion() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("springBoot"));
        assertEquals("2.7.18", response.get("springBoot"));
    }

    @Test
    void testInfo_Status() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("status"));
        assertEquals("running", response.get("status"));
    }

    @Test
    void testInfo_Endpoints() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        assertTrue(response.containsKey("endpoints"));
        assertInstanceOf(String[].class, response.get("endpoints"));
        
        String[] endpoints = (String[]) response.get("endpoints");
        assertEquals(5, endpoints.length);
        assertEquals("GET / - Welcome page", endpoints[0]);
        assertEquals("GET /info - Application info", endpoints[1]);
        assertEquals("GET /dashboard - Dashboard view", endpoints[2]);
        assertEquals("GET /api/tickets - List all tickets", endpoints[3]);
        assertEquals("GET /h2-console - H2 Database console", endpoints[4]);
    }

    @Test
    void testWelcome_MultipleCallsReturnConsistentData() {
        // Act
        Map<String, Object> response1 = homeController.welcome();
        Map<String, Object> response2 = homeController.welcome();

        // Assert
        assertEquals(response1.get("application"), response2.get("application"));
        assertEquals(response1.get("version"), response2.get("version"));
        assertEquals(response1.get("status"), response2.get("status"));
    }

    @Test
    void testInfo_MultipleCallsReturnConsistentData() {
        // Act
        Map<String, Object> response1 = homeController.info();
        Map<String, Object> response2 = homeController.info();

        // Assert
        assertEquals(response1.get("application"), response2.get("application"));
        assertEquals(response1.get("version"), response2.get("version"));
        assertEquals(response1.get("status"), response2.get("status"));
        assertEquals(response1.get("springBoot"), response2.get("springBoot"));
    }

    @Test
    void testWelcome_AllKeysPresent() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        String[] expectedKeys = {
            "application", "version", "description", "techStack",
            "status", "availableEndpoints", "credentials", "message"
        };
        
        for (String key : expectedKeys) {
            assertTrue(response.containsKey(key), "Missing key: " + key);
        }
    }

    @Test
    void testInfo_AllKeysPresent() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        String[] expectedKeys = {
            "application", "version", "java", "springBoot", "status", "endpoints"
        };
        
        for (String key : expectedKeys) {
            assertTrue(response.containsKey(key), "Missing key: " + key);
        }
    }

    @Test
    void testWelcome_NoNullValues() {
        // Act
        Map<String, Object> response = homeController.welcome();

        // Assert
        response.values().forEach(value -> 
            assertNotNull(value, "Response should not contain null values")
        );
    }

    @Test
    void testInfo_NoNullValues() {
        // Act
        Map<String, Object> response = homeController.info();

        // Assert
        response.values().forEach(value -> 
            assertNotNull(value, "Response should not contain null values")
        );
    }
}

// Made with Bob