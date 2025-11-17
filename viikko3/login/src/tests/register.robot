*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  veikko
    Set Password  veikko123
    Set Password confirmation  veikko123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  mi
    Set Password  mikko123
    Set Password confirmation  mikko123
    Click Button  Register
    Register Should Fail With Message  Invalid username or password

Register With Valid Username And Too Short Password
    Set Username  mikko
    Set Password  mikko
    Set Password confirmation  mikko
    Click Button  Register
    Register Should Fail With Message  Invalid username or password

Register With Valid Username And Invalid Password
    Set Username  mikko
    Set Password  mikkomikko
    Set Password confirmation  mikkomikko
    Click Button  Register
    Register Should Fail With Message  Invalid username or password

Register With Nonmatching Password And Password Confirmation
    Set Username  mikko
    Set Password  mikko123
    Set Password confirmation  mikkk123
    Click Button  Register
    Register Should Fail With Message  Passwords are nonmatching

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  Username is already in use

*** Keywords ***

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
