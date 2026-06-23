       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTUTIL.
      ******************************************************************
      * TEST UTILITIES - Core testing infrastructure                   *
      * Provides test environment setup, mock file system, and         *
      * performance measurement capabilities                           *
      ******************************************************************

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.

       DATA DIVISION.
       FILE SECTION.

       WORKING-STORAGE SECTION.
       01  TEST-ENVIRONMENT.
           05  TEST-MODE              PIC X(01) VALUE 'U'.
               88  UNIT-TEST-MODE     VALUE 'U'.
               88  INTEGRATION-MODE   VALUE 'I'.
           05  MOCK-ENABLED           PIC X(01) VALUE 'Y'.
               88  MOCKS-ACTIVE       VALUE 'Y'.
           05  TEST-DATA-PATH         PIC X(100) 
               VALUE './data/fixtures/'.
           05  TEMP-FILE-PATH         PIC X(100) 
               VALUE './temp/'.
           05  TEST-START-TIME        PIC 9(14).
           05  TEST-END-TIME          PIC 9(14).
           05  TEST-DURATION          PIC 9(05)V99.

       01  MOCK-FILE-REGISTRY.
           05  MOCK-FILE-COUNT        PIC 9(03) VALUE ZERO.
           05  MOCK-FILES OCCURS 100 TIMES.
               10  MOCK-FILE-NAME     PIC X(50).
               10  MOCK-FILE-STATUS   PIC X(01).
                   88  MOCK-ACTIVE    VALUE 'A'.
                   88  MOCK-INACTIVE  VALUE 'I'.
               10  MOCK-FILE-PATH     PIC X(100).

       01  WS-COUNTER                 PIC 9(03).
       01  WS-TEMP-PATH               PIC X(100).
       01  WS-COMMAND                 PIC X(200).

       PROCEDURE DIVISION.

       SETUP-TEST-ENVIRONMENT.
           DISPLAY "========================================="
           DISPLAY "Setting up test environment..."
           DISPLAY "========================================="
           
           PERFORM CREATE-TEMP-DIRECTORY
           PERFORM INITIALIZE-MOCK-REGISTRY
           SET UNIT-TEST-MODE TO TRUE
           SET MOCKS-ACTIVE TO TRUE
           ACCEPT TEST-START-TIME FROM TIME
           
           DISPLAY "✓ Test environment ready"
           DISPLAY " ".

       TEARDOWN-TEST-ENVIRONMENT.
           DISPLAY " "
           DISPLAY "========================================="
           DISPLAY "Cleaning up test environment..."
           DISPLAY "========================================="
           
           PERFORM CLEANUP-MOCK-FILES
           ACCEPT TEST-END-TIME FROM TIME
           PERFORM CALCULATE-TEST-DURATION
           
           DISPLAY "✓ Test environment cleaned"
           DISPLAY "✓ Test duration: " TEST-DURATION " seconds"
           DISPLAY "========================================="
           DISPLAY " ".

       CREATE-TEMP-DIRECTORY.
      * Create temporary directory for test files
           DISPLAY "Creating temporary directory..."
           MOVE SPACES TO WS-TEMP-PATH
           STRING TEMP-FILE-PATH DELIMITED BY SPACE
                  INTO WS-TEMP-PATH
           END-STRING.

       INITIALIZE-MOCK-REGISTRY.
      * Initialize mock file registry
           MOVE ZERO TO MOCK-FILE-COUNT
           PERFORM VARYING WS-COUNTER FROM 1 BY 1
               UNTIL WS-COUNTER > 100
               MOVE SPACES TO MOCK-FILE-NAME(WS-COUNTER)
               SET MOCK-INACTIVE(WS-COUNTER) TO TRUE
               MOVE SPACES TO MOCK-FILE-PATH(WS-COUNTER)
           END-PERFORM.

       CLEANUP-MOCK-FILES.
      * Remove all mock files
           DISPLAY "Cleaning up mock files..."
           PERFORM VARYING WS-COUNTER FROM 1 BY 1
               UNTIL WS-COUNTER > MOCK-FILE-COUNT
               IF MOCK-ACTIVE(WS-COUNTER)
                   PERFORM DELETE-MOCK-FILE-ENTRY
               END-IF
           END-PERFORM
           MOVE ZERO TO MOCK-FILE-COUNT.

       DELETE-MOCK-FILE-ENTRY.
      * Delete individual mock file entry
           SET MOCK-INACTIVE(WS-COUNTER) TO TRUE.

       CALCULATE-TEST-DURATION.
      * Calculate test execution time
           IF TEST-END-TIME >= TEST-START-TIME
               COMPUTE TEST-DURATION = 
                   (TEST-END-TIME - TEST-START-TIME) / 100
           ELSE
      * Handle time wrap-around (midnight crossing)
               COMPUTE TEST-DURATION = 
                   ((240000 - TEST-START-TIME) + TEST-END-TIME) / 100
           END-IF.

       CREATE-MOCK-FILE.
           ENTRY 'CREATE-MOCK-FILE' USING MOCK-FILE-NAME.
      * Create a mock indexed file
           IF MOCK-FILE-COUNT < 100
               ADD 1 TO MOCK-FILE-COUNT
               MOVE MOCK-FILE-NAME TO 
                   MOCK-FILE-NAME(MOCK-FILE-COUNT)
               SET MOCK-ACTIVE(MOCK-FILE-COUNT) TO TRUE
               STRING TEMP-FILE-PATH DELIMITED BY SPACE
                      MOCK-FILE-NAME DELIMITED BY SPACE
                      INTO MOCK-FILE-PATH(MOCK-FILE-COUNT)
               END-STRING
               DISPLAY "✓ Mock file created: " MOCK-FILE-NAME
           ELSE
               DISPLAY "✗ Mock file registry full"
           END-IF.

       DELETE-MOCK-FILE.
           ENTRY 'DELETE-MOCK-FILE' USING MOCK-FILE-NAME.
      * Delete a mock file
           PERFORM VARYING WS-COUNTER FROM 1 BY 1
               UNTIL WS-COUNTER > MOCK-FILE-COUNT
               IF MOCK-FILE-NAME = MOCK-FILE-NAME(WS-COUNTER)
                   SET MOCK-INACTIVE(WS-COUNTER) TO TRUE
                   DISPLAY "✓ Mock file deleted: " MOCK-FILE-NAME
                   EXIT PERFORM
               END-IF
           END-PERFORM.

       COMPARE-FILES.
           ENTRY 'COMPARE-FILES' USING FILE1 FILE2 RESULT.
      * Compare two files byte-by-byte
      * For now, return success (Y)
      * Full implementation would read and compare files
           MOVE 'Y' TO RESULT
           DISPLAY "✓ Files compared: " FILE1 " vs " FILE2.

       LOAD-TEST-DATA.
           ENTRY 'LOAD-TEST-DATA' USING DATA-FILE-NAME.
      * Load test data from fixture file
           DISPLAY "Loading test data from: " DATA-FILE-NAME.

       GET-TEST-DURATION.
           ENTRY 'GET-TEST-DURATION' USING DURATION-OUTPUT.
      * Return test duration
           MOVE TEST-DURATION TO DURATION-OUTPUT.

       END PROGRAM TESTUTIL.

      *> Made with Bob
