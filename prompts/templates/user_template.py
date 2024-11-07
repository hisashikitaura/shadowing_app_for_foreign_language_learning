USER_TEMPLATE_GENERATE = '''
            I will make a shadowing practice app for {language_name} Language Learners.
            
            As for the {language_name} materials, generate {language_name} text for {language_name} Language Learners.
            The detailed requirements for the text to be created are as follows:
            -- Topic: {topic}
            -- Content: {content}
            -- Number of the sentences: Approx. {num_sentences}                
            -- Skill level: {level}, defined by the Common European Framework of Reference for Languages (CEFR)

            You can use words or phrases from the content, but you don't have to use the content all.
            If the content is None, it's no problem. You ignore it and generate text about the topic.
            '''

# BEFORE rails.generate()
USER_TEMPLATE_EXTRACT = '''
            Extract about 10-20 sentences on the {topic} related the topic.
            '''