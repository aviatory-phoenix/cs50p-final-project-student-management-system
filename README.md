# Student Management System

#### Video Demo: https://youtu.be/6eGC0c-BdUw
#### Description:

## Overview

The Student Management System is a comprehensive Python application designed to handle academic data for educational institutions. This command-line interface system provides distinct functionality for three user types: administrators, teachers, and students, each with tailored access levels and capabilities. The system efficiently manages student records, test scores, academic averages, and ranking calculations while maintaining data integrity across multiple CSV files.

## System Architecture

### User Roles and Permissions

**Administrators** have full system access including the ability to view student overall averages with ranking information, accessing teacher performance metrics and creating new student accounts with automated enrollment in any of the 5 subjects available (math, phy, chem, bio, cs)

**Teachers** can access class-specific data, either for whole class or for an individual student. The former path allows display of all student test scores in tabular format, calculating the class average as well as student rankings, while the latter allows the teacher to access a particular student in their class via GRN and retrieve data such as their average score and rank in the subject.

**Students** have personalized access that allows them to view the courses they are enrolled in, access individual test scores across all subjects in a tabular format and check their averages and ranking position in each subject and overall.

## File Structure and Data Management

### Core Data Files

**`users.csv`** serves as the central user registry using the GRN (General Register Number) as a unique student identifier and discriminator between student and teacher accounts. Other fields include name and subject enrollment flags (1 for enrolled, 0 for not enrolled) for each of the subjects currently supported. GRN is used as the primary key across all files except passwords.csv.

**`passwords.csv`** maintains login credentials storing user names for display purposes, email addresses serving as usernames and encrypted passwords for system access.

**Subject-specific CSV files** (`math.csv`, `phy.csv`, `chem.csv`, `bio.csv`, `cs.csv`) each, using GRN as the only student identifier, store all available test scores for that student in the same line as their GRN in an "obtained_marks/max_marks" format (e.g. "17/20"). This allows for consistent test structures across all students and allows the teacher the flexibility to add data for new tests, as well as conduct tests of varying totals.

Each of the above files are loaded and stored as data structures that can later be accessed by any part of the program before main() is called in order to avoid repetitive File I/O.

CSV files were chosen as they provide human-readable data that teachers and admin members can manually edit if needed, require no external dependencies, and offer straightforward parsing logic. Moreover, they were found to be a useful model for databases and other information repositories which are used in real-world programs.

### Program Files

**`project.py`** contains the main application logic featuring:
- Object-oriented Student class with average calculation methods
- Modular pure functions for testability
- Comprehensive menu system with error handling
- CSV data parsing and percentage conversion routines

**`test_project.py`** provides unit test coverage for:
- Student average calculation algorithms
- Ranking and sorting functionality
- Data processing and transformation logic
- Edge case handling for empty or missing data

## Program Flow and User Journey

The user experience begins at the login interface where users enter their email credentials. The system cross-references the input against pre-loaded password data from passwords.csv, authenticating users and extracting their domain to determine access level. Varying domains based on the person's role have been deliberately set in order to maintain the role-specific functionality of the program. Upon successful login, users are seamlessly routed to role-specific menus that maintain continuous operation until explicit exit via Ctrl+D, eliminating repetitive authentication for multiple operations.

Administrators enter a comprehensive management dashboard where they can execute three core functions. Viewing student averages presents a ranked list of all students sorted by overall performance, calculated by aggregating subject averages while excluding unenrolled courses. Teacher performance metrics display subject-specific class averages for each educator, computed from their students' scores in their assigned subject. When creating new accounts, the system guides administrators through name collection, automatically generates sequential GRNs, processes subject enrollment preferences, and writes comprehensive records to users.csv, relevant subject files, and passwords.csv with default credentials—all while maintaining referential integrity across the database.

Teachers access a dual-path interface tailored to educational workflows. The whole-class management path enables display of all student test scores in professionally formatted tables using the tabulate library, with scores converted from raw "obtained_marks/max_marks" format to percentages for consistent analysis. Class average calculations aggregate individual student performance within the subject, while ranking functions sort students by achievement level. The individual student path allows targeted assistance through GRN-based lookup, retrieving specific averages and rank positions for personalized academic support.

Students navigate a personalized academic portal showcasing their individual progress. They can review enrolled courses filtered from their user profile, calculate both subject-specific and overall averages through the Student class methods that handle null scores gracefully, examine detailed test performance across all subjects in organized tabular displays, and determine their competitive standing through rank calculations that compare their performance against peers in each subject and overall. The system ensures accurate representation by filtering invalid scores and excluding unstarted subjects from overall calculations.

## Technical Implementation and Design Rationale

The backend architecture employs sophisticated data management with all CSV files pre-loaded into structured Python objects during program initialization. This strategy eliminates repetitive file I/O, significantly enhancing performance while ensuring data consistency throughout user sessions. The Student class serves as the computational core, encapsulating subject score lists and providing robust average calculation methods that gracefully handle edge cases like missing or null scores.

Pure functions separate business logic from I/O operations, enabling comprehensive unit testing and maintainable code architecture. Dynamic method dispatch using getattr() allows subject-agnostic code execution, while dictionary comprehensions and sorting algorithms efficiently process ranking calculations across datasets. Error handling permeates the system with EOFError exceptions enabling graceful exit from any input prompt and input validation ensuring data quality.

The percentage-based scoring normalization allows meaningful comparison across tests with varying maximum scores, while the tabular display system creates professional reports suitable for educational contexts. The continuous operation model mimics real-world application behavior, reducing login friction and enhancing user productivity during extended sessions.

