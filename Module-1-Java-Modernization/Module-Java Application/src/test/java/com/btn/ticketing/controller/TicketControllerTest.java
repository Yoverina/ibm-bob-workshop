package com.btn.ticketing.controller;

import com.btn.ticketing.model.Customer;
import com.btn.ticketing.model.Ticket;
import com.btn.ticketing.service.TicketService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for TicketController
 * Tests all REST endpoints with comprehensive coverage
 */
@ExtendWith(MockitoExtension.class)
class TicketControllerTest {

    @Mock
    private TicketService ticketService;

    @InjectMocks
    private TicketController ticketController;

    private Ticket mockTicket;
    private Customer mockCustomer;
    private List<Ticket> mockTickets;

    @BeforeEach
    void setUp() {
        // Setup mock customer
        mockCustomer = new Customer();
        mockCustomer.setId(1L);
        mockCustomer.setCustomerId("CUST-001");
        mockCustomer.setName("John Doe");
        mockCustomer.setEmail("john@example.com");

        // Setup mock ticket
        mockTicket = new Ticket();
        mockTicket.setId(1L);
        mockTicket.setTicketNumber("TKT-12345678");
        mockTicket.setCustomer(mockCustomer);
        mockTicket.setSubject("Account Issue");
        mockTicket.setDescription("Cannot access my account");
        mockTicket.setCategory("ACCOUNT_ISSUE");
        mockTicket.setPriority("HIGH");
        mockTicket.setStatus("OPEN");
        mockTicket.setCreatedDate(LocalDateTime.now());

        // Setup mock ticket list
        Ticket ticket2 = new Ticket();
        ticket2.setId(2L);
        ticket2.setTicketNumber("TKT-87654321");
        ticket2.setStatus("IN_PROGRESS");

        mockTickets = Arrays.asList(mockTicket, ticket2);
    }

    @Test
    void testGetAllTickets_Success() {
        // Arrange
        when(ticketService.getAllTickets()).thenReturn(mockTickets);

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getAllTickets();

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().size());
        verify(ticketService).getAllTickets();
    }

    @Test
    void testGetAllTickets_EmptyList() {
        // Arrange
        when(ticketService.getAllTickets()).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getAllTickets();

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).getAllTickets();
    }

    @Test
    void testGetTicketById_Found() {
        // Arrange
        when(ticketService.getTicketById(1L)).thenReturn(Optional.of(mockTicket));

        // Act
        ResponseEntity<Ticket> response = ticketController.getTicketById(1L);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TKT-12345678", response.getBody().getTicketNumber());
        verify(ticketService).getTicketById(1L);
    }

    @Test
    void testGetTicketById_NotFound() {
        // Arrange
        when(ticketService.getTicketById(999L)).thenReturn(Optional.empty());

        // Act
        ResponseEntity<Ticket> response = ticketController.getTicketById(999L);

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).getTicketById(999L);
    }

    @Test
    void testGetTicketByNumber_Found() {
        // Arrange
        when(ticketService.getTicketByNumber("TKT-12345678")).thenReturn(Optional.of(mockTicket));

        // Act
        ResponseEntity<Ticket> response = ticketController.getTicketByNumber("TKT-12345678");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TKT-12345678", response.getBody().getTicketNumber());
        verify(ticketService).getTicketByNumber("TKT-12345678");
    }

    @Test
    void testGetTicketByNumber_NotFound() {
        // Arrange
        when(ticketService.getTicketByNumber("TKT-INVALID")).thenReturn(Optional.empty());

        // Act
        ResponseEntity<Ticket> response = ticketController.getTicketByNumber("TKT-INVALID");

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).getTicketByNumber("TKT-INVALID");
    }

    @Test
    void testCreateTicket_Success() {
        // Arrange
        Ticket newTicket = new Ticket();
        newTicket.setSubject("New Issue");
        newTicket.setDescription("Description");
        newTicket.setCategory("GENERAL");
        newTicket.setPriority("LOW");
        newTicket.setStatus("OPEN");

        when(ticketService.createTicket(any(Ticket.class))).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.createTicket(newTicket);

        // Assert
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TKT-12345678", response.getBody().getTicketNumber());
        verify(ticketService).createTicket(any(Ticket.class));
    }

    @Test
    void testUpdateTicket_Success() {
        // Arrange
        Ticket updatedTicket = new Ticket();
        updatedTicket.setSubject("Updated Subject");
        updatedTicket.setDescription("Updated Description");
        updatedTicket.setCategory("ACCOUNT_ISSUE");
        updatedTicket.setPriority("CRITICAL");
        updatedTicket.setStatus("IN_PROGRESS");

        when(ticketService.updateTicket(eq(1L), any(Ticket.class))).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.updateTicket(1L, updatedTicket);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        verify(ticketService).updateTicket(eq(1L), any(Ticket.class));
    }

    @Test
    void testUpdateTicket_NotFound() {
        // Arrange
        Ticket updatedTicket = new Ticket();
        when(ticketService.updateTicket(eq(999L), any(Ticket.class)))
                .thenThrow(new RuntimeException("Ticket not found"));

        // Act
        ResponseEntity<Ticket> response = ticketController.updateTicket(999L, updatedTicket);

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).updateTicket(eq(999L), any(Ticket.class));
    }

    @Test
    void testDeleteTicket_Success() {
        // Arrange
        doNothing().when(ticketService).deleteTicket(1L);

        // Act
        ResponseEntity<Void> response = ticketController.deleteTicket(1L);

        // Assert
        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).deleteTicket(1L);
    }

    @Test
    void testGetTicketsByStatus_Success() {
        // Arrange
        when(ticketService.getTicketsByStatus("OPEN")).thenReturn(mockTickets);

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getTicketsByStatus("OPEN");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().size());
        verify(ticketService).getTicketsByStatus("OPEN");
    }

    @Test
    void testGetTicketsByStatus_EmptyList() {
        // Arrange
        when(ticketService.getTicketsByStatus("CLOSED")).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getTicketsByStatus("CLOSED");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).getTicketsByStatus("CLOSED");
    }

    @Test
    void testGetTicketsByCustomer_Success() {
        // Arrange
        when(ticketService.getTicketsByCustomer(1L)).thenReturn(mockTickets);

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getTicketsByCustomer(1L);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().size());
        verify(ticketService).getTicketsByCustomer(1L);
    }

    @Test
    void testGetTicketsByCustomer_EmptyList() {
        // Arrange
        when(ticketService.getTicketsByCustomer(999L)).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getTicketsByCustomer(999L);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).getTicketsByCustomer(999L);
    }

    @Test
    void testGetActiveTickets_Success() {
        // Arrange
        when(ticketService.getActiveTickets()).thenReturn(mockTickets);

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getActiveTickets();

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().size());
        verify(ticketService).getActiveTickets();
    }

    @Test
    void testGetActiveTickets_EmptyList() {
        // Arrange
        when(ticketService.getActiveTickets()).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.getActiveTickets();

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).getActiveTickets();
    }

    @Test
    void testSearchTickets_Success() {
        // Arrange
        when(ticketService.searchTickets("account")).thenReturn(mockTickets);

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.searchTickets("account");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(2, response.getBody().size());
        verify(ticketService).searchTickets("account");
    }

    @Test
    void testSearchTickets_NoResults() {
        // Arrange
        when(ticketService.searchTickets("nonexistent")).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.searchTickets("nonexistent");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).searchTickets("nonexistent");
    }

    @Test
    void testAssignTicket_Success() {
        // Arrange
        mockTicket.setAssignedTo("agent1");
        mockTicket.setStatus("IN_PROGRESS");
        when(ticketService.assignTicket(1L, "agent1")).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.assignTicket(1L, "agent1");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("agent1", response.getBody().getAssignedTo());
        assertEquals("IN_PROGRESS", response.getBody().getStatus());
        verify(ticketService).assignTicket(1L, "agent1");
    }

    @Test
    void testAssignTicket_NotFound() {
        // Arrange
        when(ticketService.assignTicket(999L, "agent1"))
                .thenThrow(new RuntimeException("Ticket not found"));

        // Act
        ResponseEntity<Ticket> response = ticketController.assignTicket(999L, "agent1");

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).assignTicket(999L, "agent1");
    }

    @Test
    void testResolveTicket_Success() {
        // Arrange
        mockTicket.setStatus("RESOLVED");
        mockTicket.setResolution("Issue resolved successfully");
        mockTicket.setResolvedDate(LocalDateTime.now());
        when(ticketService.resolveTicket(1L, "Issue resolved successfully")).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.resolveTicket(1L, "Issue resolved successfully");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("RESOLVED", response.getBody().getStatus());
        assertEquals("Issue resolved successfully", response.getBody().getResolution());
        verify(ticketService).resolveTicket(1L, "Issue resolved successfully");
    }

    @Test
    void testResolveTicket_NotFound() {
        // Arrange
        when(ticketService.resolveTicket(999L, "Resolution"))
                .thenThrow(new RuntimeException("Ticket not found"));

        // Act
        ResponseEntity<Ticket> response = ticketController.resolveTicket(999L, "Resolution");

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).resolveTicket(999L, "Resolution");
    }

    @Test
    void testCloseTicket_Success() {
        // Arrange
        mockTicket.setStatus("CLOSED");
        mockTicket.setClosedDate(LocalDateTime.now());
        when(ticketService.closeTicket(1L)).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.closeTicket(1L);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("CLOSED", response.getBody().getStatus());
        assertNotNull(response.getBody().getClosedDate());
        verify(ticketService).closeTicket(1L);
    }

    @Test
    void testCloseTicket_NotFound() {
        // Arrange
        when(ticketService.closeTicket(999L))
                .thenThrow(new RuntimeException("Ticket not found"));

        // Act
        ResponseEntity<Ticket> response = ticketController.closeTicket(999L);

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(ticketService).closeTicket(999L);
    }

    @Test
    void testCreateTicket_WithAllFields() {
        // Arrange
        Ticket fullTicket = new Ticket();
        fullTicket.setSubject("Complete Ticket");
        fullTicket.setDescription("Full description");
        fullTicket.setCategory("TRANSACTION_DISPUTE");
        fullTicket.setPriority("CRITICAL");
        fullTicket.setStatus("OPEN");
        fullTicket.setCustomer(mockCustomer);

        when(ticketService.createTicket(any(Ticket.class))).thenReturn(fullTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.createTicket(fullTicket);

        // Assert
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        verify(ticketService).createTicket(any(Ticket.class));
    }

    @Test
    void testGetTicketsByStatus_MultipleStatuses() {
        // Arrange
        when(ticketService.getTicketsByStatus("OPEN")).thenReturn(mockTickets);
        when(ticketService.getTicketsByStatus("IN_PROGRESS")).thenReturn(Collections.singletonList(mockTicket));
        when(ticketService.getTicketsByStatus("RESOLVED")).thenReturn(Collections.emptyList());

        // Act & Assert
        ResponseEntity<List<Ticket>> openResponse = ticketController.getTicketsByStatus("OPEN");
        assertEquals(2, openResponse.getBody().size());

        ResponseEntity<List<Ticket>> inProgressResponse = ticketController.getTicketsByStatus("IN_PROGRESS");
        assertEquals(1, inProgressResponse.getBody().size());

        ResponseEntity<List<Ticket>> resolvedResponse = ticketController.getTicketsByStatus("RESOLVED");
        assertTrue(resolvedResponse.getBody().isEmpty());

        verify(ticketService).getTicketsByStatus("OPEN");
        verify(ticketService).getTicketsByStatus("IN_PROGRESS");
        verify(ticketService).getTicketsByStatus("RESOLVED");
    }

    @Test
    void testSearchTickets_WithSpecialCharacters() {
        // Arrange
        when(ticketService.searchTickets("account@#$")).thenReturn(Collections.emptyList());

        // Act
        ResponseEntity<List<Ticket>> response = ticketController.searchTickets("account@#$");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(response.getBody().isEmpty());
        verify(ticketService).searchTickets("account@#$");
    }

    @Test
    void testAssignTicket_WithEmptyUsername() {
        // Arrange
        when(ticketService.assignTicket(1L, "")).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.assignTicket(1L, "");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(ticketService).assignTicket(1L, "");
    }

    @Test
    void testResolveTicket_WithEmptyResolution() {
        // Arrange
        when(ticketService.resolveTicket(1L, "")).thenReturn(mockTicket);

        // Act
        ResponseEntity<Ticket> response = ticketController.resolveTicket(1L, "");

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(ticketService).resolveTicket(1L, "");
    }
}

// Made with Bob