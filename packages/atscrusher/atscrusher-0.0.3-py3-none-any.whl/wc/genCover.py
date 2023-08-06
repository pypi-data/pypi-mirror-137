targetCompanyStatement = 'At Schwab, what unites our employees is a shared belief that the work we do can make a direct impact on the client. We know it takes a broad set of skills to ensure that our clients feel the full impact and power of investing. That\'s why we work hard to develop a workforce full of unique perspectives, work experiences, and backgrounds.'
usersBeliefs = 'My name is Pablo Acosta and high quality APIs are what I live for. There is just something so magical about creating APIs that the entire world can benefit from. When I create an API, I take into account multiple key questions. These questions being, how useful is the API, can it scale to suit the needs of devs, and can I make it. Again this is what I live for and I love answering these questions'

exCompanyStatement = 'ServiceMax\'s mission is to help customers keep the world running with asset-centric field service management software. As the recognized leader in this space, ServiceMax\'s mobile apps and cloud-based software provide a complete view of assets to field service teams. By optimizing field service operations, customers across all industries can better manage the complexities of service, support faster growth, and run more profitable, outcome-centric businesses.'
exampleUserBeliefs = 'My name is Anthony Cavuoti. I like to spend my time building applications that take advantage of the latest technology breakthroughs in a way that is meant to help people out. I like to build the kind of tools that help users organize their data so they can make better decisions about the future. What I like about this kind of work is that it helps people better take advantage of the dizzying amount of tools available to them in this day and age. When you\'re all organized, you free the mental capacity to learn a new tool to make you more effective.'
exampleResponse = 'Hello ServiceMax team. I see you\'re in the industry of assisting others in managing client data so that they can be more profitable. This is exactly the kind of thing I believe in because management software is a lot like organization software. The goal is to external align reality with your internal perceptions in order to improve the future state of your project. Believe me, I am interested in this kind of worldly improvement.'

import openai

def generate(company, personal, key): 
    openai.api_key = key
    start_sequence = "```"
    
    response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt="Company\n" + exCompanyStatement + "\nApplicant\n" + exampleUserBeliefs + "\n```\nCoverletter\n" + exampleResponse + "\n```\nCompany\n" + company + "\nApplicant\n" + personal + "\n```\nCoverletter\n",
            temperature=0.22,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        ).choices[0].text

    return response
