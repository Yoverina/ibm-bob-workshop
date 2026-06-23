package com.btn.ticketing.controller;

import com.btn.ticketing.model.Customer;
import com.btn.ticketing.model.Ticket;
import com.btn.ticketing.service.CustomerService;
import com.btn.ticketing.service.TicketService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.ui.Model;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

/**
 * Unit tests for DashboardController
 * Tests all endpoints with comprehensive coverage
 */
@ExtendWith(MockitoExtension.class)
class DashboardControllerTest {

    @Mock
    private TicketService ticketService;

    @Mock
    private CustomerService customerService;

    @Mock
    private Model model;

    @InjectMocks
    private DashboardController dashboardController;

    private List<Ticket> mockTickets;
    private List<Customer> mockCustomers;
    private List<Customer> mockActiveCustomers;

    @BeforeEach
    void setUp() {
        // Setup mock tickets
        Ticket ticket1 = new Ticket();
        ticket1.setId(1L);
        ticket1.setTicketNumber("TKT-001");
        ticket1.setStatus("OPEN");

        Ticket ticket2 = new Ticket();
        ticket2.setId(2L);
        ticket2.setTicketNumber("TKT-002");
        ticket2.setStatus("IN_PROGRESS");

        mockTickets = Arrays.asList(ticket1, ticket2);

        // Setup mock customers
        Customer customer1 = new Customer();
        customer1.setId(1L);
        customer1.setCustomerId("CUST-001");
        customer1.setActive(true);

        Customer customer2 = new Customer();
        customer2.setId(2L);
        customer2.setCustomerId("CUST-002");
        customer2.setActive(true);

        Customer customer3 = new Customer();
        customer3.setId(3L);
        customer3.setCustomerId("CUST-003");
        customer3.setActive(false);

        mockCustomers = Arrays.asList(customer1, customer2, customer3);
        mockActiveCustomers = Arrays.asList(customer1, customer2);
    }

    @Test
    void testDashboard_Success() {
        // Arrange
        when(ticketService.countTicketsByStatus("OPEN")).thenReturn(5L);
        when(ticketService.countTicketsByStatus("IN_PROGRESS")).thenReturn(3L);
        when(ticketService.countTicketsByStatus("RESOLVED")).thenReturn(10L);
        when(ticketService.countTicketsByStatus("CLOSED")).thenReturn(20L);
        when(ticketService.getActiveTickets()).thenReturn(mockTickets);
        when(customerService.getAllCustomers()).thenReturn(mockCustomers);
        when(customerService.getActiveCustomers()).thenReturn(mockActiveCustomers);

        // Act
        String viewName = dashboardController.dashboard(model);

        // Assert
        assertEquals("dashboard", viewName);
        verify(model).addAttribute("openTickets", 5L);
        verify(model).addAttribute("inProgressTickets", 3L);
        verify(model).addAttribute("resolvedTickets", 10L);
        verify(model).addAttribute("closedTickets", 20L);
        verify(model).addAttribute("totalTickets", 38L);
        verify(model).addAttribute("recentTickets", mockTickets);
        verify(model).addAttribute("totalCustomers", 3);
        verify(model).addAttribute("activeCustomers", 2);
        verify(ticketService).countTicketsByStatus("OPEN");
        verify(ticketService).countTicketsByStatus("IN_PROGRESS");
        verify(ticketService).countTicketsByStatus("RESOLVED");
        verify(ticketService).countTicketsByStatus("CLOSED");
        verify(ticketService).getActiveTickets();
        verify(customerService).getAllCustomers();
        verify(customerService).getActiveCustomers();
    }

    @Test
    void testDashboard_WithZeroTickets() {
        // Arrange
        when(ticketService.countTicketsByStatus(any())).thenReturn(0L);
        when(ticketService.getActiveTickets()).thenReturn(Collections.emptyList());
        when(customerService.getAllCustomers()).thenReturn(Collections.emptyList());
        when(customerService.getActiveCustomers()).thenReturn(Collections.emptyList());

        // Act
        String viewName = dashboardController.dashboard(model);

        // Assert
        assertEquals("dashboard", viewName);
        verify(model).addAttribute("openTickets", 0L);
        verify(model).addAttribute("inProgressTickets", 0L);
        verify(model).addAttribute("resolvedTickets", 0L);
        verify(model).addAttribute("closedTickets", 0L);
        verify(model).addAttribute("totalTickets", 0L);
        verify(model).addAttribute("recentTickets", Collections.emptyList());
        verify(model).addAttribute("totalCustomers", 0);
        verify(model).addAttribute("activeCustomers", 0);
    }

    @Test
    void testDashboard_WithException() {
        // Arrange
        when(ticketService.countTicketsByStatus("OPEN"))
                .thenThrow(new RuntimeException("Database connection error"));

        // Act
        String viewName = dashboardController.dashboard(model);

        // Assert
        assertEquals("error", viewName);
        verify(model).addAttribute(eq("error"), eq("Database connection error"));
        verify(ticketService).countTicketsByStatus("OPEN");
        verify(ticketService, never()).countTicketsByStatus("IN_PROGRESS");
    }

    @Test
    void testDashboard_ServiceThrowsNullPointerException() {
        // Arrange
        when(ticketService.countTicketsByStatus("OPEN")).thenReturn(5L);
        when(ticketService.countTicketsByStatus("IN_PROGRESS")).thenReturn(3L);
        when(ticketService.countTicketsByStatus("RESOLVED")).thenReturn(10L);
        when(ticketService.countTicketsByStatus("CLOSED")).thenReturn(20L);
        when(ticketService.getActiveTickets()).thenThrow(new NullPointerException("Null value encountered"));

        // Act
        String viewName = dashboardController.dashboard(model);

        // Assert
        assertEquals("error", viewName);
        verify(model).addAttribute(eq("error"), eq("Null value encountered"));
    }

    @Test
    void testTickets_Success() {
        // Arrange
        when(ticketService.getAllTickets()).thenReturn(mockTickets);

        // Act
        String viewName = dashboardController.tickets(model);

        // Assert
        assertEquals("tickets", viewName);
        verify(model).addAttribute("tickets", mockTickets);
        verify(ticketService).getAllTickets();
    }

    @Test
    void testTickets_EmptyList() {
        // Arrange
        when(ticketService.getAllTickets()).thenReturn(Collections.emptyList());

        // Act
        String viewName = dashboardController.tickets(model);

        // Assert
        assertEquals("tickets", viewName);
        verify(model).addAttribute("tickets", Collections.emptyList());
        verify(ticketService).getAllTickets();
    }

    @Test
    void testCustomers_Success() {
        // Arrange
        when(customerService.getAllCustomers()).thenReturn(mockCustomers);

        // Act
        String viewName = dashboardController.customers(model);

        // Assert
        assertEquals("customers", viewName);
        verify(model).addAttribute("customers", mockCustomers);
        verify(customerService).getAllCustomers();
    }

    @Test
    void testCustomers_EmptyList() {
        // Arrange
        when(customerService.getAllCustomers()).thenReturn(Collections.emptyList());

        // Act
        String viewName = dashboardController.customers(model);

        // Assert
        assertEquals("customers", viewName);
        verify(model).addAttribute("customers", Collections.emptyList());
        verify(customerService).getAllCustomers();
    }

    @Test
    void testDashboard_WithLargeNumbers() {
        // Arrange
        when(ticketService.countTicketsByStatus("OPEN")).thenReturn(1000L);
        when(ticketService.countTicketsByStatus("IN_PROGRESS")).thenReturn(500L);
        when(ticketService.countTicketsByStatus("RESOLVED")).thenReturn(2000L);
        when(ticketService.countTicketsByStatus("CLOSED")).thenReturn(5000L);
        when(ticketService.getActiveTickets()).thenReturn(mockTickets);
        when(customerService.getAllCustomers()).thenReturn(mockCustomers);
        when(customerService.getActiveCustomers()).thenReturn(mockActiveCustomers);

        // Act
        String viewName = dashboardController.dashboard(model);

        // Assert
        assertEquals("dashboard", viewName);
        verify(model).addAttribute("totalTickets", 8500L);
    }
}

// Made with Bob