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
    Output Should Contain    Article ID added.

Print Citations
    Input Create and Create Citation    ID1    author1
    Input Create and Create Citation    ID2    author2
    Input Print Command
    Start Ui
    Output Should Contain Bib    ID1    author1
    Output Should Contain Bib    ID2    author2

Export Citations
    Input Create and Create Citation    ID1    author1
    Input Create and Create Citation    ID2    author2
    Input Export Command
    Input    src/tests/test_export.bib
    Start Ui
    File Should Containt    src/tests/test_export.bib    ID1    author1
    File Should Containt    src/tests/test_export.bib    ID2    author2
    Delete File    src/tests/test_export.bib