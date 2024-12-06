*** Settings ***
Library    ../CitationLibrary.py
Library    ../UiLibrary.py

*** Keywords ***
Input Create Command
    Input    create

Input Export Command
    Input    export

Input Citation Information
    [Arguments]  ${ID}  ${authors}
    Input  ${ID}
    Input  ${authors}
    Input  \
    Input  title
    Input  journal
    Input  1999
    Input  volume
    Input  1--100
    Input  keyword1
    Input  keyword2
    Input  \    # \ merkkaa robotissa tyhjää stringiä
    
Input Print Command
    Input    print