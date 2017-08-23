Feature: Home page
    As a user
    I want to see home page titled "CVDB"
    and links to log in and sign up
    and if I click the links, I will see proper page.

    Scenario: Open front page, check title and links
        When I open root page
        Then I will see title "CVDB"
         And I will see link "Login"
         And I will see link "Sign Up"

    Scenario: Sign Up
        When I open root page
         And I will click link "Sign Up"
        Then I will see title "Sign Up"

    Scenario: Login
        When I open root page
         And I will click link "Login"
        Then I will see title "Sign In"

