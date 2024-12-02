*** Settings ***
Library    ../CitationLibrary.py
Library    ../UiLibrary.py

*** Keywords ***
Input Create Command
    Input    create

Input Export Command
    Input    export

Input Citation Information
    [Arguments]  ${ID}  ${author}
    Input  ${ID}
    Input  ${author}
    Input  title
    Input  journal
    Input  1999
    Input  volume
    Input  1--100
    
Input Print Command
    Input    print