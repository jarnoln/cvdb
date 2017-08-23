Feature: Home page
    As a user
    I want to see home page titled "CVDB"
    and links to log in and sign up
    and if I click the links, I will see proper pages.

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
         And I will see link "Logout"

        When I click link "Logout"
        Then I will see title "Sign Out"

    Scenario: Login
        When I open root page
         And I click link "Login"
        Then I will see title "Sign In"
         And I will see element "login_form"
