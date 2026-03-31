# unknownapp
This is an unknown application written in Java

---- For Submission (you must fill in the information below) ----
### Use Case Diagram

flowchart TD
    Start([Start]) --> initData[initData\nload JSON or seed defaults]
    initData --> LoginMenu[Login Menu\n1 Student  2 Admin  3 Exit]
    LoginMenu --> SaveExit([Save & Exit])

    LoginMenu -->|1 Student| StudentLogin[Student login\nenter ID or 'new']
    StudentLogin -->|new| CreateProfile[Create profile]
    CreateProfile --> StudentMenu
    StudentLogin --> StudentMenu[Student menu\n1-6 actions  7 Logout & Save]

    StudentMenu --> S1[1 View catalog]
    StudentMenu --> S2[2 Register for course\nchecks: dup, cap, prereq, time conflict]
    StudentMenu --> S3[3 Drop a course]
    StudentMenu --> S4[4 View schedule]
    StudentMenu --> S5[5 Billing summary]
    StudentMenu --> S6[6 Edit profile]
    StudentMenu --> S7[7 Save & logout]
    S7 -->|back to login| LoginMenu

    LoginMenu -->|2 Admin| AdminLogin[Admin login\npassword: admin123]
    AdminLogin --> AdminMenu[Admin menu\n1-9 actions  10 Logout & Save]

    AdminMenu --> A1[1 View catalog]
    AdminMenu --> A2[2 View class roster]
    AdminMenu --> A3[3 View all students]
    AdminMenu --> A4[4 Add student]
    AdminMenu --> A5[5 Edit student]
    AdminMenu --> A6[6 Add course]
    AdminMenu --> A7[7 Edit course]
    AdminMenu --> A8[8 View student schedule]
    AdminMenu --> A9[9 Billing summary]
    AdminMenu --> A10[10 Save & logout]
    A10 -->|back to login| LoginMenu
### Flowchart of the main workflow

### Prompts
