USER_TEMPLATE_CREATE = '''
            I will make a shadowing practice app for {language_name} Language Learners.
            
            As for the {language_name} materials, create {language_name} text for {language_name} Language Learners.
            The detailed requirements for the text to be created are as follows:
            -- Topic: {topic}
            -- Relevant Chunks: {relevant_chunks}
            -- Number of the sentences: Approx. {num_sentences}                
            -- Skill level: {level}, defined by the Common European Framework of Reference for Languages (CEFR)

            The text you create should contain words or phrases from the "Relevant Chunks" above, but you don't have to use them all.
            If the "Relevant Chunks" are None, it's no problem. You ignore it and create text about the topic.
            '''

USER_TEMPLATE_EXTRACT = '''
            Extract 10 random sentences directly that describes {topic}. That sentences necessarily have subjects and verbs.
            No numbering and No line break code.
            '''