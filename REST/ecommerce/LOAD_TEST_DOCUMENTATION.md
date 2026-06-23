# Load Testing Documentation

## Overview

This document provides comprehensive information about load testing the E-Commerce application using Locust, a modern load testing framework for Python.

## Table of Contents

1. [What is Load Testing?](#what-is-load-testing)
2. [Prerequisites](#prerequisites)
3. [Load Test Setup](#load-test-setup)
4. [Running Load Tests](#running-load-tests)
5. [Test Scenarios](#test-scenarios)
6. [Understanding Results](#understanding-results)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## What is Load Testing?

Load testing is a type of performance testing that simulates real-world load on a system to:
- Identify performance bottlenecks
- Determine maximum operating capacity
- Ensure system stability under expected load
- Measure response times and throughput
- Validate scalability

### Key Metrics

- **Response Time**: Time taken to complete a request
- **Throughput**: Number of requests processed per second (RPS)
- **Error Rate**: Percentage of failed requests
- **Concurrent Users**: Number of simultaneous users
- **95th Percentile**: 95% of requests complete within this time

---

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `locust==2.17.0` - Load testing framework
- All other required dependencies

### 2. Start the Application

Before running load tests, ensure the Flask application is running:

```bash
# Option 1: Using batch script
run.bat

# Option 2: Manual start
cd ecommerce
python app.py
```

The application should be accessible at `http://127.0.0.1:5000`

---

## Load Test Setup

### File Structure

```
ecommerce/
├── locustfile.py              # Load test scenarios
├── run_load_test.bat          # Batch script to run tests
├── LOAD_TEST_DOCUMENTATION.md # This file
└── load_test_report_*.html    # Generated test reports
```

### Test Configuration

The [`locustfile.py`](locustfile.py) contains three user classes:

1. **ECommerceUser** - Realistic user behavior with full workflow
2. **QuickTestUser** - Fast testing for basic functionality
3. **StressTestUser** - High-intensity stress testing

---

## Running Load Tests

### Method 1: Using Batch Script (Recommended)

```bash
run_load_test.bat
```

This provides 6 test options:

#### 1. Quick Test (Web UI)
- **Users**: 10
- **Spawn Rate**: 2 users/sec
- **Interface**: Web UI at http://localhost:8089
- **Use Case**: Quick validation, development testing

#### 2. Standard Test (Web UI)
- **Users**: 50
- **Spawn Rate**: 5 users/sec
- **Interface**: Web UI
- **Use Case**: Regular performance testing

#### 3. Stress Test (Web UI)
- **Users**: 100
- **Spawn Rate**: 10 users/sec
- **Interface**: Web UI
- **Use Case**: Stress testing, capacity planning

#### 4. Headless Quick Test (CLI)
- **Users**: 10
- **Duration**: 30 seconds
- **Output**: HTML report (`load_test_report_quick.html`)
- **Use Case**: Automated testing, CI/CD pipelines

#### 5. Headless Standard Test (CLI)
- **Users**: 50
- **Duration**: 60 seconds
- **Output**: HTML report (`load_test_report_standard.html`)
- **Use Case**: Performance benchmarking

#### 6. Custom Test (Web UI)
- **Parameters**: User-defined
- **Interface**: Web UI
- **Use Case**: Custom scenarios

### Method 2: Manual Locust Commands

#### Web UI Mode

```bash
# Basic command
locust -f locustfile.py --host=http://127.0.0.1:5000

# With specific parameters
locust -f locustfile.py --host=http://127.0.0.1:5000 --users=50 --spawn-rate=5
```

Then open http://localhost:8089 in your browser.

#### Headless Mode (CLI)

```bash
# Quick test
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=10 --spawn-rate=2 --run-time=30s --html=report.html

# Standard test
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=50 --spawn-rate=5 --run-time=60s --html=report.html

# Stress test
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=100 --spawn-rate=10 --run-time=120s --html=report.html
```

#### Advanced Options

```bash
# CSV output
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=50 --spawn-rate=5 --run-time=60s --csv=results

# Specific user class
locust -f locustfile.py --host=http://127.0.0.1:5000 QuickTestUser

# Multiple workers (distributed testing)
locust -f locustfile.py --host=http://127.0.0.1:5000 --master
locust -f locustfile.py --host=http://127.0.0.1:5000 --worker
```

---

## Test Scenarios

### ECommerceUser Behavior

Simulates realistic e-commerce user journey:

1. **Registration** (on_start)
   - Creates unique user account
   - Validates registration success

2. **Login** (on_start)
   - Authenticates user
   - Establishes session

3. **View Homepage** (Task weight: 1)
   - Loads main page
   - Views available products

4. **View Products** (Task weight: 3)
   - Most common action
   - Browses product catalog

5. **Add to Cart** (Task weight: 2)
   - Adds random products (ID 1-6)
   - Updates cart state

6. **View Cart** (Task weight: 2)
   - Reviews cart contents
   - Checks cart functionality

7. **Update Cart** (Task weight: 1)
   - Modifies item quantities
   - Tests cart updates

8. **Checkout** (Task weight: 1)
   - Completes purchase
   - Validates checkout flow

9. **Logout** (on_stop)
   - Ends user session
   - Cleanup

### Wait Times

- **ECommerceUser**: 1-5 seconds between tasks (realistic)
- **QuickTestUser**: 0.5-2 seconds (faster testing)
- **StressTestUser**: 0.1-0.5 seconds (maximum load)

---

## Understanding Results

### Web UI Dashboard

When using Web UI mode (http://localhost:8089), you'll see:

#### Statistics Tab
- **Type**: Request type (GET/POST)
- **Name**: Endpoint name
- **# Requests**: Total requests made
- **# Fails**: Failed requests
- **Median**: Median response time (ms)
- **95%ile**: 95th percentile response time
- **Average**: Average response time
- **Min/Max**: Minimum and maximum response times
- **RPS**: Requests per second
- **Failures/s**: Failures per second

#### Charts Tab
- **Total Requests per Second**: Throughput over time
- **Response Times**: Response time distribution
- **Number of Users**: Active users over time

#### Failures Tab
- Lists all failed requests with details
- Error messages and stack traces

#### Exceptions Tab
- Python exceptions encountered during testing

### HTML Reports

Generated HTML reports include:

1. **Summary Statistics**
   - Total requests, failures, RPS
   - Response time percentiles
   - Test duration and user count

2. **Request Statistics Table**
   - Detailed metrics per endpoint
   - Success/failure rates

3. **Response Time Charts**
   - Visual representation of performance
   - Distribution graphs

4. **Failure Details**
   - Error breakdown
   - Failure reasons

### Interpreting Results

#### Good Performance Indicators
- ✅ Response times < 200ms for most requests
- ✅ 95th percentile < 500ms
- ✅ Error rate < 1%
- ✅ Stable RPS throughout test
- ✅ No timeout errors

#### Warning Signs
- ⚠️ Response times > 500ms
- ⚠️ 95th percentile > 1000ms
- ⚠️ Error rate 1-5%
- ⚠️ Increasing response times over time
- ⚠️ Occasional timeouts

#### Critical Issues
- ❌ Response times > 2000ms
- ❌ Error rate > 5%
- ❌ Frequent timeouts
- ❌ Server crashes
- ❌ Database connection errors

---

## Best Practices

### 1. Test Environment

- **Isolate Testing**: Use dedicated test environment
- **Clean State**: Reset database between tests
- **Consistent Data**: Use same test data for comparisons
- **Monitor Resources**: Track CPU, memory, disk I/O

### 2. Test Design

- **Realistic Scenarios**: Model actual user behavior
- **Gradual Ramp-up**: Increase load gradually
- **Sustained Load**: Run tests for sufficient duration
- **Peak Load**: Test beyond expected capacity

### 3. Test Execution

```bash
# Start with baseline
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=10 --spawn-rate=1 --run-time=60s --html=baseline.html

# Increase load gradually
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=25 --spawn-rate=2 --run-time=60s --html=load_25.html
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=50 --spawn-rate=5 --run-time=60s --html=load_50.html
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=100 --spawn-rate=10 --run-time=60s --html=load_100.html

# Find breaking point
locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users=200 --spawn-rate=20 --run-time=120s --html=stress.html
```

### 4. Analysis

- Compare results across test runs
- Identify performance degradation patterns
- Correlate with system metrics
- Document findings and recommendations

### 5. Optimization Cycle

1. **Baseline**: Establish current performance
2. **Identify**: Find bottlenecks
3. **Optimize**: Implement improvements
4. **Verify**: Re-test to confirm gains
5. **Repeat**: Continue optimization

---

## Troubleshooting

### Common Issues

#### 1. "Connection Refused" Error

**Problem**: Cannot connect to Flask app

**Solution**:
```bash
# Verify app is running
netstat -ano | findstr :5000

# Start the app
run.bat
```

#### 2. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'locust'`

**Solution**:
```bash
pip install locust==2.17.0
```

#### 3. High Error Rates

**Problem**: Many failed requests during testing

**Possible Causes**:
- Database locks (SQLite limitation)
- Insufficient server resources
- Application bugs
- Network issues

**Solutions**:
- Reduce concurrent users
- Add database connection pooling
- Optimize database queries
- Fix application errors

#### 4. Slow Response Times

**Problem**: Response times > 1000ms

**Investigation**:
```python
# Add timing to app.py
import time
start = time.time()
# ... your code ...
print(f"Operation took {time.time() - start:.2f}s")
```

**Common Fixes**:
- Add database indexes
- Implement caching
- Optimize queries
- Use connection pooling

#### 5. Memory Issues

**Problem**: Application crashes under load

**Solution**:
- Monitor memory usage
- Fix memory leaks
- Increase available memory
- Implement pagination

### Debug Mode

Run Locust with verbose logging:

```bash
locust -f locustfile.py --host=http://127.0.0.1:5000 --loglevel DEBUG
```

---

## Performance Targets

### Recommended Targets for This Application

| Metric | Target | Acceptable | Poor |
|--------|--------|------------|------|
| Homepage Load | < 100ms | < 200ms | > 500ms |
| Product List | < 150ms | < 300ms | > 600ms |
| Add to Cart | < 200ms | < 400ms | > 800ms |
| Checkout | < 300ms | < 600ms | > 1000ms |
| Error Rate | < 0.1% | < 1% | > 5% |
| Concurrent Users | 50+ | 25+ | < 10 |

### Scaling Recommendations

- **10 users**: Development/Testing
- **25 users**: Small production deployment
- **50 users**: Medium production deployment
- **100+ users**: Requires optimization and scaling

---

## Additional Resources

### Locust Documentation
- Official Docs: https://docs.locust.io/
- GitHub: https://github.com/locustio/locust

### Performance Testing
- [Web Performance Best Practices](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [Load Testing Best Practices](https://www.blazemeter.com/blog/performance-testing-vs-load-testing-vs-stress-testing)

### Flask Optimization
- [Flask Performance Tips](https://flask.palletsprojects.com/en/latest/deploying/)
- [SQLite Performance](https://www.sqlite.org/performance.html)

---

## Changelog

### Version 1.0 (2026-06-23)
- Initial load testing setup
- Created locustfile.py with realistic scenarios
- Added run_load_test.bat for easy execution
- Comprehensive documentation

---

## Support

For issues or questions:
1. Check this documentation
2. Review Locust logs
3. Examine application logs
4. Check system resources

---

**Happy Load Testing! 🚀**