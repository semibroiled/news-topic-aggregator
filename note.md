Design choices

Used langchain because i wanted to potentially use something else instead of restricting myself to one service

used hugging face because more open source and community focused than lets say openai

went from huggingfacexx to endpoint which leveraged api calls to using a pipeline

api was accessing it alright, but some internal kwargs call screwed up my code

rather use a surefire way albeit long one that uses local resources than 

so not using prompt template as well

good thing is pipeline can handle keyword summarizer optimised for it

Kinda want to separate api calls to different utils fcns

Main script is a bit verbose, but getting it chunked to smaller units is also a chore

Add t