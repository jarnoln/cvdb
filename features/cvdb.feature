Feature: CVDB
    As a user
    I want to see default Django page

    Scenario: Open front page and check title

        When I open root page
        Then I will see title "Welcome to Django"
