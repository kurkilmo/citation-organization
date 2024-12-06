*** Settings ***
Library  ../CitationLibrary.py
Test Teardown    Empty File

*** Test Cases ***
Add New Citation
    Add New Citation  Joku Ukko  Random Sitaatti
    ${citations}=  Get All Citations
    Should Contain  ${citations}  Joku Ukko: Random Sitaatti

Add Multiple Citations
    Add New Citation  Toinen Kaveri  Hullu Teos
    Add New Citation  Kolmas Jaba  Makia Tutkimus
    ${citations}=  Get All Citations
    Should Contain  ${citations}  Toinen Kaveri: Hullu Teos
    Should Contain  ${citations}  Kolmas Jaba: Makia Tutkimus

Retrieve Empty List
    ${citations}=  Get All Citations
    Should Be Empty  ${citations}

Remove All Citations
    Add New Citation  Jaska  Facebook-päivitys
    ${citations}=  Get All Citations
    Should Contain  ${citations}  Jaska: Facebook-päivitys
    Empty File
    ${citations}=  Get All Citations
    Should Be Empty  ${citations}