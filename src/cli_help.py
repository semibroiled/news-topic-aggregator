def help_command_output() -> str:
    return """
        - Language Settings\n\
            \t-- Use command '!setlang' on prompt to change query language\n\
            \t-- Type 'en' for English and 'de' for German\n\
        - Application Settings\n\
            \t-- Type in '!exit' or '!quit' to close application\n\
        - Advanced Queries\n\
            \t--Put your topic in quotation marks for exact match. (eg: \"elon musk\")\n\
            \t--Use Boolean Operators. (eg: (crypto AND bitcoin) NOT ethereum)\n"""
