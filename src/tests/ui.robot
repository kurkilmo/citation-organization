*** Settings ***
Resource    resource.robot
Test Setup    Start Ui
Test Teardown    Empty File

*** Keywords ***
Input Create and Create Citation
    [Arguments]  ${ID}  ${author}
    Input Create Command
    Input Citation Information    ${ID}    ${author}

*** Test Cases ***
Create New Citation
    Input Create and Create Citation  ID  authori
    Start Ui
    Output Should Contain    Publication ID added.

Print Citations
    Input Create and Create Citation    ID1    author1
    Input Create and Create Citation    ID2    author2
    Input Print Command
    Start Ui
    Output Should Contain Bib    ID1    author1
    Output Should Contain Bib    ID2    author2