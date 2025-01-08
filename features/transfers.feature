Feature: Transfers

  Scenario: Perform an outgoing transfer
    Given I create an account using name: "John", last name: "Doe", pesel: "12345678901", and saldo: "1000"
    And I create an account using name: "Jane", last name: "Smith", pesel: "98765432109", and saldo: "0"
    When I transfer 500 zł from pesel: "12345678901" to pesel: "98765432109" as "outgoing"
    Then Account with pesel "12345678901" has saldo equal to "500"
    And Account with pesel "98765432109" has saldo equal to "500"

  Scenario: Perform an express transfer
    Given I create an account using name: "Anna", last name: "Taylor", pesel: "56789012345", and saldo: "302"
    And I create an account using name: "Mike", last name: "Johnson", pesel: "09876543210", and saldo: "0"
    When I transfer 300 zł from pesel: "56789012345" to pesel: "09876543210" as "express"
    Then Account with pesel "56789012345" has saldo equal to "1"
    And Account with pesel "09876543210" has saldo equal to "300"

  Scenario: Perform an incoming transfer
    Given I create an account using name: "Sarah", last name: "Connor", pesel: "45678901234", and saldo: "0"
    When I transfer 700 zł to pesel: "45678901234" as "incoming"
    Then Account with pesel "45678901234" has saldo equal to "700"
