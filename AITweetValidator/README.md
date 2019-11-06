# AITweetValidator

AITweetValidator is an AI tool that detects tweets that did not originate from the tweet owners. The tool is an adaptation of AI-Tweet-Validator (github.com/JoshuaGRubin/AI-Tweet-Validator) for distributed processing.  

The tool generates a model for each user based on the user's ~ 1000 tweets.

Separate of concerns is key for scaling this project. The goal is to modularize each process for re-usability and for tracking bottle-neck areas. 


### Modifications to the Tool

Some processes from that project have been changed to keep processing modular, but the general logic reamains intact.

- Interdependence of tweets based on other users in a group of hard coded users (negative tweet cases) is removed. Instead, a chosen set of tweet users' tweets now represent the constant negative cases. The user ids for these negative cases can be found in build/data/negative_processed

- Fetching tweet texts from tweet objects are separate from AI processing, this is now done at the beginning of the distributed system pipeline

- For the purpose of demonstrating scaling, the tool now produces one AI model (using random forest classification), rather than three for algorithm performance comparison as originally intended. Comparison amongst various algorithms can now be done at scale by running them as a separate process and output them to a store. Output can then be fetched for comparison or further analysis or processing

