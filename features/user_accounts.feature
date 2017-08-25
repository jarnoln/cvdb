Feature: User account management
    As a user
    I want to see home page and links to log in and sign up
    and be able to create user account by signing up
    and be able to log in and out
    and be able to delete my account.

    Scenario: Open front page, check title and links
        When I open root page
        Then I will see title "CVDB"
         And I will see link "Login"
         And I will see link "Sign Up"

    Scenario: Sign Up
        When I open root page
         And I click link "Sign Up"
        Then I will see title "Sign Up"
         And I will see element "signup_form"

        When I fill signup form
        Then I will see title "Profile"
         And I will see element "navbar_logout"

        When I click element "navbar_logout"
        Then I will see title "CVDB"
         And I will see link "Login"

    Scenario: Login
        When I open root page
         And I click link "Login"
        Then I will see title "Sign In"
         And I will see element "login_form"

        When I fill login form
        Then I will see title "Profile"
         And I will see link "Delete account"

    Scenario: Delete account
        When I click link "Delete account"
        Then I will see title "Confirm delete user"
         And I will see element "button_delete"

        When I click element "button_delete"
        Then I will see title "CVDB"
         And I will see link "Login"
